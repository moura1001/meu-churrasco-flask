import pytest

from contextlib import contextmanager
from requests.exceptions import RequestException
from src.calculator import getOpcoesEntrega
from src import config

@contextmanager
def not_raises(expectedException):
    try:
        yield
    except expectedException as errExpected:
        pytest.fail(reason=f"Did raise exception {errExpected} when it should not!")
    except Exception as errNotExpected:
        pytest.fail(reason=f"An unexpected exception {errNotExpected} raised.")

def test_calculate_delivery_fee():
    cepOrigem = "09010100"
    cepDestino = "24310430"
    config.CEP_ORIGEM = cepOrigem

    with not_raises(RequestException):
        opcoesEntrega = getOpcoesEntrega(cepDestino)

