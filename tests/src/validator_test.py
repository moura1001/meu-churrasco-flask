import pytest
from src.app import application

@pytest.fixture(scope='module')
def flask_context():
    app = application
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False

    with app.app_context():
        yield app

@pytest.fixture(scope='module')
def client(flask_context): 
    return flask_context.test_client()

def test_validate_cpf(client):
    with client:
        invalid_cpf = "invalid"
        ignored_cep = "06194-010"
        form_data = {'cpf':invalid_cpf, 'cep': ignored_cep, 'qtd_convidados': 32}
        response = client.post("/", data=form_data)

        assert response.status_code == 400
        
        valid_cpf = "532.617.840-08"
        form_data = {'cpf':valid_cpf, 'cep': ignored_cep, 'qtd_convidados': 32}
        response = client.post("/", data=form_data)
        
        assert response.status_code == 200
        
        valid_cpf2 = "53261784008"
        form_data = {'cpf':valid_cpf2, 'cep': ignored_cep, 'qtd_convidados': 32}
        response = client.post('/', data=form_data)
        
        assert response.status_code == 200

def test_validate_cep(client):
    with client:
        invalid_cep = "invalid"
        valid_cpf = "532.617.840-08"
        form_data = {'cpf':valid_cpf, 'cep': invalid_cep, 'qtd_convidados': 32}
        response = client.post("/", data=form_data)

        assert response.status_code == 400
        
        valid_cep = "06194-010"
        form_data = {'cpf':valid_cpf, 'cep': valid_cep, 'qtd_convidados': 32}
        response = client.post("/", data=form_data)

        assert response.status_code == 200
        
        valid_cep2 = "06194010"
        form_data = {'cpf':valid_cpf, 'cep': valid_cep2, 'qtd_convidados': 32}
        response = client.post('/', data=form_data)

        assert response.status_code == 200
        
        
