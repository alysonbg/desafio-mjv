from unittest.mock import patch
from jogador import Jogador, JogadorCautelosoStategy, JogadorImpulsivoStategy, JogadorExigenteStategy, JogadorAleatorioStategy
from propriedade import Propriedade


def test_jogador_cauteloso_deve_comprar():
    stategy = JogadorCautelosoStategy()
    jogador = Jogador("Teste", stategy)
    propriedade = Propriedade(200, 50)

    assert jogador.deve_comprar(propriedade) is True
    

def test_jogador_cauteloso_nao_deve_comprar():
    stategy = JogadorCautelosoStategy()
    jogador = Jogador("Teste", stategy)
    propriedade = Propriedade(1000, 250)

    assert jogador.deve_comprar(propriedade) is False


def test_jogador_impulsivo_deve_comprar_com_saldo():
    stategy = JogadorImpulsivoStategy()
    jogador = Jogador("Teste", stategy)
    propriedade = Propriedade(200, 50)

    assert jogador.deve_comprar(propriedade) is True


def test_jogador_impulsivo_nao_compra_sem_saldo():
    stategy = JogadorImpulsivoStategy()
    jogador = Jogador("Teste", stategy)
    propriedade = Propriedade(1000, 250)

    assert jogador.deve_comprar(propriedade) is False


def test_jogador_exigente_deve_comprar_quando_aluguel_maior_que_50():
    stategy = JogadorExigenteStategy()
    jogador = Jogador("Teste", stategy)
    propriedade = Propriedade(200, 60)

    assert jogador.deve_comprar(propriedade) is True


def test_jogador_exigente_nao_deve_comprar_quando_aluguel_menor_que_50():
    stategy = JogadorExigenteStategy()
    jogador = Jogador("Teste", stategy)
    propriedade = Propriedade(300, 30)

    
    assert jogador.deve_comprar(propriedade) is False


@patch('jogador.random.choice')
def test_jogador_aleatorio_com_saldo_retorna_true(mock_choice):
    mock_choice.return_value = True
    stategy = JogadorAleatorioStategy()
    jogador = Jogador("Teste", stategy)
    propriedade = Propriedade(200, 50)

    assert jogador.deve_comprar(propriedade) is True
    mock_choice.assert_called_once_with([True, False])


@patch('jogador.random.choice')
def test_jogador_aleatorio_com_saldo_retorna_false(mock_choice):
    mock_choice.return_value = False
    stategy = JogadorAleatorioStategy()
    jogador = Jogador("Teste", stategy)
    propriedade = Propriedade(200, 50)

    assert jogador.deve_comprar(propriedade) is False
    mock_choice.assert_called_once_with([True, False])


@patch('jogador.random.choice')
def test_jogador_aleatorio_sem_saldo_falha(mock_choice):
    stategy = JogadorAleatorioStategy()
    jogador = Jogador("Teste", stategy)
    propriedade = Propriedade(1000, 250)

    assert jogador.deve_comprar(propriedade) is False
    mock_choice.assert_not_called()


def test_aumenta_saldo_do_jogador():
    stategy = JogadorCautelosoStategy()
    jogador = Jogador("Teste", stategy)
    jogador.incrementa_saldo(100)

    assert jogador.saldo == 400


def test_decrementa_saldo_do_jogador():
    stategy = JogadorCautelosoStategy()
    jogador = Jogador("Teste", stategy)
    jogador.decrementa_saldo(100)

    assert jogador.saldo == 200