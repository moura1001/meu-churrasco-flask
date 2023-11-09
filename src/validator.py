import re

from wtforms.validators import ValidationError

def validate_cpf(form, field):
    cpf = field.data
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

