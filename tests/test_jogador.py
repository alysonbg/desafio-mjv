from jogador import Jogador, JogadorCautelosoStategy, JogadorImpulsivoStategy
from propriedade import Propriedade


def test_jogador_cauteloso_deve_comprar():
    stategy = JogadorCautelosoStategy()
    jogador = Jogador(stategy)
    propriedade = Propriedade(200, 50)

    assert jogador.deve_comprar(propriedade) is True
    

def test_jogador_cauteloso_nao_deve_comprar():
    stategy = JogadorCautelosoStategy()
    jogador = Jogador(stategy)
    propriedade = Propriedade(1000, 250)

    assert jogador.deve_comprar(propriedade) is False


def test_jogador_impulsivo_deve_comprar_com_saldo():
    stategy = JogadorImpulsivoStategy()
    jogador = Jogador(stategy)
    propriedade = Propriedade(200, 50)

    assert jogador.deve_comprar(propriedade) is True


def test_jogador_impulsivo_deve_comprar_sem_saldo():
    stategy = JogadorImpulsivoStategy()
    jogador = Jogador(stategy)
    propriedade = Propriedade(1000, 250)

    assert jogador.deve_comprar(propriedade) is True




