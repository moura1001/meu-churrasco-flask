import pytest
from wtforms.validators import ValidationError

from src import application, CalculateForm, validator

@pytest.fixture(scope='module')
def flask_context():
    app = application
    #app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False

    with app.app_context():
        yield app

@pytest.fixture(scope='module')
def client(flask_context): 
    return flask_context.test_client()

def test_validate_cpf(client):
    with client:
        invalid_cpf = "invalid"
        form_data = {'cpf':invalid_cpf, 'cep': 'cep', 'qtd_convidados': 32}
        response = client.post('/', data=form_data)

        assert response.status_code == 400
        
        valid_cpf = "532.617.840-08"
        form_data = {'cpf':valid_cpf, 'cep': 'cep', 'qtd_convidados': 32}
        response = client.post('/', data=form_data)

        assert response.status_code == 200
        
        valid_cpf2 = "53261784008"
        form_data = {'cpf':valid_cpf2, 'cep': 'cep', 'qtd_convidados': 32}
        response = client.post('/', data=form_data)

        assert response.status_code == 200
        
