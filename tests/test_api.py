# Testar as rotas da API
from app.models.produto import Produto
from app.models.categoria import Categoria
from app.models.cliente import Cliente


# Testar abror a tela de produtos 
def test_tela_produtos_retorna_200(usuario_fake):

    # Requisição na rota de produtos
    resposta = usuario_fake.get("/produtos/")

    # 200 = "ok", a página caregou sem erro
    assert resposta.status_code == 200

# Teste etrar na tela de produtos sem o login
def test_tela_produtos_sem_login():
    from fastapi.testclient import TestClient
    from app.main import app

    usuario_sem_login = TestClient(app)

    # Requisição na rota de produtos
    resposta = usuario_sem_login.get("/produtos/")

    assert resposta.status_code == 401

def test_pagina_de_produtos_lista_produto_criado(usuario_fake, db_session):
    #Criar algo real no banco de dados
    categoria = Categoria(nome="Camisas")
    db_session.add(categoria)
    db_session.commit()

    # Criar um produto
    produto= Produto(nome="Camisa Polo", preco=100.0, estoque_atual=85, categoria_id=categoria.id)
    db_session.add(produto)
    db_session.commit()

    # Requisicão para a tela de produtos
    resposta = usuario_fake.get("/produtos/")

    # reposta.text = HTML completo
    assert "Camisa Polo" in resposta.text



#Exercicio = Criar um cliente e verificar se eçe aparece na tela de clientes 
def test_cliente_aparece_na_tela(usuario_fake, db_session):
    cliente = Cliente(nome="Raul Bissoli")
    db_session.add(cliente)
    db_session.commit()

    resposta = usuario_fake.get("/clientes/")
    assert "Raul Bissoli" in resposta.text

def test_criar_produto_no_formulario_web(usuario_fake):

    resposta = usuario_fake.post("/produtos/novo", data={
        "nome": "Boné","preco": "49.90", "estoque_atual": "15"},

    )

    assert resposta.status_code == 302
    assert resposta.headers["location"] == "/produtos?criado=ok"

    resposta_lista = usuario_fake.get("/produtos/")
    assert "Boné" in resposta_lista.text

