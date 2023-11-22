from enum import Enum
import src.calculator as calc

class OpcoesEntrega(Enum):
    C_04014 = "04014", "SEDEX à vista", "SEDEX",
    C_04510 = "04510", "PAC à vista", "PAC"
    C_04782 = "04782", "SEDEX 12 (à vista)", "SEDEX12"
    C_04790 = "04790", "SEDEX 10 (à vista)", "SEDEX10"
    C_04804 = "04804", "SEDEX Hoje à vista", "SEDEXHoje"

class FormatoEncomenda(Enum):
    F_1 = 1, "caixa selected", "Formato caixa/pacote"
    F_2 = 2, "rolo selected", "Formato rolo/prisma"
    F_3 = 3, "envelope selected", "Envelope"

def fieldMessageError(classType, fieldName, expectedType, gotValue):
    return f"{fieldName}, campo da classe {classType} deve ser {expectedType}, porém foi fornecido o valor {gotValue}"

### Info
class Info():
    def __init__(self, label=None, value=None):
        if (not (isinstance(label, str))) or (not label.strip()):
            raise ValueError(fieldMessageError(self.getType(), "label", "uma string não vazia", label))
        self._label_ = label

        if (not (isinstance(value, str))) or (not value.strip()):
            raise ValueError(fieldMessageError(self.getType(), "value", "uma string não vazia", value))
        self._value_ = value

    @staticmethod
    def getType():
        return "Info{label:string, value:string}"

    @property
    def label(self):
        return self._label_

    @property
    def value(self):
        return self._value_



### Churrasco results
class Result():
    def __init__(self, qtd_carne=None, qtd_bebida=None, cep_entrega=None):
        if (not (isinstance(cep_entrega, str))) or (not cep_entrega.strip()):
            raise ValueError(fieldMessageError(self.getType(), "cep_entrega", "uma string não vazia", cep_entrega))
        
        if not (isinstance(qtd_carne, Info)):
            raise ValueError(fieldMessageError(self.getType(), "qtd_carne", f"uma instância da classe {Info.getType()}", qtd_carne))
        self._qtd_carne_ = qtd_carne

        if not (isinstance(qtd_bebida, Info)):
            raise ValueError(fieldMessageError(self.getType(), "qtd_bebida", f"uma instância da classe {Info.getType()}", qtd_bebida))
        self._qtd_bebida_ = qtd_bebida
        
        self._opcoes_entrega_ = calc.getOpcoesEntrega(cep_entrega)

    @staticmethod
    def getType():
        return "Result{qtd_carne:Info, qtd_bebida:Info, opcoes_entrega:{key:string, value:string}}"

    @property
    def qtd_carne(self):
        return self._qtd_carne_

    @property
    def qtd_bebida(self):
        return self._qtd_bebida_

    @property
    def opcoes_entrega(self):
        return self._opcoes_entrega_
