import pytest
from app import app

# Cria um cliente de teste falso para não precisarmos subir o servidor real
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_status_code(client):
    resposta = client.get('/')
    assert resposta.status_code == 200

def test_home_mensagem(client):
    resposta = client.get('/')
    dados = resposta.get_json()
    assert dados['mensagem'] == "Bem-vindo à API integracao!"

# TODO: Missão 6.1 - Criar um teste para a sua rota /api/soma
# Dica: chame client.get('/api/soma?a=10&b=5')
# Verifique se o status code é 200 e se o JSON retornado é 15
def test_soma(client):
    resposta = client.get('/api/soma?a=10&b=5')
    assert resposta.status_code == 200
    dados = resposta.get_json()
    assert dados['resultado'] == 15