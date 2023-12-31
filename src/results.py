from src.model import Result, Info
from src import config

def calculate(cep=None, cpf=None, qtd_convidados=None):
    return Result(
        Info(label="Quantidade de carne", value="1 kg por convidado"),
        Info(label="Quantidade de bebida", value="1 l por convidado"),
        config.CEP_ORIGEM
    )
