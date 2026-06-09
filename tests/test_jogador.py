from jogador import Jogador, JogadorCautelosoStategy, JogadorImpulsivoStategy, JogadorExigenteStategy
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


def test_jogador_exigente_deve_comprar_quando_aluguel_maior_que_50():
    stategy = JogadorExigenteStategy()
    jogador = Jogador(stategy)
    propriedade = Propriedade(1000, 250)

    assert jogador.deve_comprar(propriedade) is True


def test_jogador_exigente_nao_deve_comprar_quando_aluguel_menor_que_50():
    stategy = JogadorExigenteStategy()
    jogador = Jogador(stategy)
    propriedade = Propriedade(300, 30)

    
    assert jogador.deve_comprar(propriedade) is False