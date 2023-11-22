import re
import requests
from concurrent import futures
from datetime import date

from src.logger import mylogger
from src import config
import src.model as model

def getOpcoesEntrega(cep_entrega=None):
    opcoesEntrega = {opcao.name: opcao.value for opcao in model.OpcoesEntrega}
    opcoesResultsKeys = {opcao.value[2]: opcao.name for opcao in model.OpcoesEntrega}
    
    results = _calculateDeliveryFee(model.OpcoesEntrega.C_04510.value[0], cep_entrega) 
    for result in results:
        opKey = opcoesResultsKeys[result]
        opcao = opcoesEntrega[opKey]
        opcoesEntrega[opKey] = {
            'delivery_option': opcao[1],
            'delivery_fee': results[result].replace("$", "$ ")
        }
        
    return opcoesEntrega

def _calculateDeliveryFee(codigoServico=None, cepDestino=None):
    #url = "http://ws.correios.com.br/calculador/CalcPrecoPrazo.aspx"
    url = "https://www2.correios.com.br/sistemas/precosPrazos/prazos.cfm"

    # dados para o cálculo do frete
    data = date.today().strftime("%d/%m/%Y")
    codServico = codigoServico
    compararServico = True
    cepOrigem = config.CEP_ORIGEM
    cepDest = cepDestino
    peso = 8
    selecao = model.FormatoEncomenda.F_1.value[1]
    formato = model.FormatoEncomenda.F_1.value[0]
    comprimento = 16
    altura = 16
    largura = 16
    diametro = 0
    maoPropria = False
    ckValorDeclarado = False
    valorDeclarado = ""
    avisoRecebimento = False

    # parâmetros da url de cálculo
    params = {
        'data': data,
        'dataAtual': data,
        'servico': codServico,
        'compararServico': "on" if compararServico else "N", 
        'cepOrigem': cepOrigem,
        'cepDestino': cepDest,
        'Selecao': selecao,
        'Formato': formato,
        'embalagem1': "outraEmbalagem1",
        'embalagem2': "",
        'nomeEmbalagemCaixa': "",
        'nomeEmbalagemEnvelope': "",
        'peso': peso,
        'Comprimento': comprimento,
        'Altura': altura,
        'Largura': largura,
        'Diametro': diametro,
        'Selecao1': 1,
        'proCod_in_1': "",
        'TipoEmbalagem1': "",
        #'MaoPropria': "S" if maoPropria else "N",
        #'ckValorDeclarado': "S" if ckValorDeclarado else "N",
        'valorDeclarado': valorDeclarado,
        #'avisoRecebimento': "S" if avisoRecebimento else "N",
        'Calcular': "Calcular"
    }
    for i in range(2, 31):
        params[f'Selecao{i}'] = ""
        params[f'proCod_in_{i}'] = ""
        params[f'TipoEmbalagem{i}'] = ""

    headers = {
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        'Accept-Encoding': "gzip, deflate, br",
        'Content-Type': "application/x-www-form-urlencoded"
    }

    try:
        r = requests.post(url, data=params, headers=headers, timeout=32)
        r.raise_for_status()
        resultContent = re.sub(r"\s+", "", r.content.decode('ISO-8859-1'))
        
        deliveryFees = {}

        servicosRegex = re.search(r"<trclass=\"dragDropSection\">(.+)<th>Prazodeentrega<small>", resultContent, re.DOTALL)
        valorTotalRegex = re.search(r"<tfoot>(.+)</tfoot>", resultContent, re.DOTALL)
        
        if servicosRegex and valorTotalRegex:
            servicos = servicosRegex.group(1)
            valoresTotal = valorTotalRegex.group(1)
            
            servicos = re.findall(r"<td>([\w\d]+)</td>", servicos)
            valoresTotal = re.findall(r"<td>([-,R$\d]+)</td>", valoresTotal)
            
            if servicos and valoresTotal:
               deliveryFees = dict(zip(servicos, valoresTotal)) 
        else:
            servicoRegex = re.search(r"PZN\-008: Serviço indisponível para o trecho informado", resultContent, re.DOTALL)
            if not servicoRegex:
                mylogger.info("Info", "input", f"{{{codigoServico}, {cepDestino}}}", "content", resultContent)

        return deliveryFees
    except requests.exceptions.HTTPError as errh:
        mylogger.error("calculateDeliveryFee", "Http Error:", errh)
        raise errh
    except requests.exceptions.ConnectionError as errc:
        mylogger.error("calculateDeliveryFee", "Error Connecting:", errc)
        raise errc
    except requests.exceptions.Timeout as errt:
        mylogger.error("calculateDeliveryFee", "Timeout Error:", errt)
        raise errt
    except requests.exceptions.RequestException as err:
        mylogger.error("calculateDeliveryFee", "OOps: Something Else", err)
        raise err

