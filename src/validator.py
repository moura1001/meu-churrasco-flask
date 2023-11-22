import time
import re
from brazilcep import get_address_from_cep, exceptions, WebService

from wtforms.validators import ValidationError
from src.logger import mylogger

def validate_cpf(form, field):
    cpf = field.data
    if len(cpf) > 14 or not cpf or cpf.isspace():
        raise ValidationError("CPF mal formatado")
    
    numeros = [int(digito) for digito in cpf if digito.isdigit()]

    formatacao = False
    quant_digitos = False
    validacao1 = False
    validacao2 = False
    
    # Verifica a estrutura do CPF (111.222.333-44). Pontuação não é obrigatória
    if re.match(r"\d{3}\.?\d{3}\.?\d{3}-?\d{2}", cpf):
        formatacao = True
    
    if len(numeros) == 11 and (len(cpf) == 11 or len(cpf) == 14):
        quant_digitos = True
    
    if not formatacao or not quant_digitos:
        raise ValidationError("CPF mal formatado")

    soma_produtos1 = sum(a*b for a, b in zip(numeros[0:9], range(10, 1, -1)))
    digito_esperado1 = (soma_produtos1 * 10 % 11) % 10
    if numeros[9] == digito_esperado1:
        validacao1 = True

    soma_produtos2 = sum(a*b for a, b in zip(numeros[0:10], range(11, 1, -1)))
    digito_esperado2 = (soma_produtos2 * 10 % 11) % 10
    if numeros[10] == digito_esperado2:
        validacao2 = True

    if not validacao1 or not validacao2:
        raise ValidationError("CPF inválido")

def validate_cep(form, field):
    cep = field.data
    if len(cep) > 9 or not cep or cep.isspace():
        raise ValidationError("CEP mal formatado")
    
    numeros = [int(digito) for digito in cep if digito.isdigit()]

    formatacao = False
    quant_digitos = False
    
    # Verifica a estrutura do CEP (11222-333)
    if re.match(r"\d{5}-?\d{3}", cep):
        formatacao = True
    
    if len(numeros) == 8 and len(cep) == 8:
        quant_digitos = True
    
    # Pontuação não permitida para reaproveitar a entrada no WebService dos Correios
    if not formatacao or not quant_digitos:
        raise ValidationError("CEP mal formatado. Utilize apenas os números")
    
    try:
        get_address_from_cep(cep, timeout=2, webservice=WebService.VIACEP)
    except exceptions.InvalidCEP as eic:
        mylogger.error(eic)
        raise ValidationError("CEP inválido")
    except exceptions.CEPNotFound as ecnf:
        mylogger.error(ecnf)
        raise ValidationError("CEP não encontrado")
    except exceptions.BlockedByFlood as ebbf:
        mylogger.error(ebbf)
        raise ValidationError("Foram identificadas muitas requisições do seu endereço. Por favor, aguarde alguns minutos antes de tentar novamente.")
    except exceptions.BrazilCEPException as e:
        mylogger.error(e)
        raise ValidationError("Erro ao acessar API para consulta do CEP. Por favor, aguarde alguns minutos antes de tentar novamente.")

