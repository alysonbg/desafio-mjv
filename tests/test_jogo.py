import pytest
from unittest.mock import patch

from jogo import Jogo
from jogador import Jogador, JogadorImpulsivoStategy
from propriedade import Propriedade


def test_jogo_inicializacao():
    jogo = Jogo()
    assert len(jogo.propriedades) == 0
    assert len(jogo.jogadores) == 0
    assert jogo.rodada_atual == 0


def test_add_jogador():
    jogo = Jogo()
    jogador = Jogador("Impulsivo", JogadorImpulsivoStategy())
    jogo.add_jogador(jogador)
    assert len(jogo.jogadores) == 1
    assert jogo.jogadores[0] == jogador


def test_add_propriedade():
    jogo = Jogo()
    prop = Propriedade(100, 50)
    jogo.add_propriedade(prop)
    assert len(jogo.propriedades) == 1
    assert jogo.propriedades[0] == prop


@patch('jogo.random.shuffle')
def test_inicializar_jogo(mock_shuffle):
    jogo = Jogo()
    jogador1 = Jogador("J1", JogadorImpulsivoStategy())
    jogador2 = Jogador("J2", JogadorImpulsivoStategy())
    jogo.add_jogador(jogador1)
    jogo.add_jogador(jogador2)
    
    jogo.rodada_atual = 10
    jogo.inicializar_jogo()
    
    mock_shuffle.assert_called_once_with(jogo.jogadores)
    assert jogo.rodada_atual == 0


@patch('jogo.random.randint')
def test_rolar_dado(mock_randint):
    mock_randint.return_value = 4
    jogo = Jogo()
    resultado = jogo.rolar_dado()
    assert resultado == 4
    mock_randint.assert_called_once_with(1, 6)


def test_remover_jogador_libera_propriedades():
    jogo = Jogo()
    jogador1 = Jogador("J1", JogadorImpulsivoStategy())
    jogador2 = Jogador("J2", JogadorImpulsivoStategy())
    
    prop1 = Propriedade(100, 50, proprietario=jogador1)
    prop2 = Propriedade(100, 50, proprietario=jogador2)
    prop3 = Propriedade(100, 50, proprietario=jogador1)
    
    jogo.add_jogador(jogador1)
    jogo.add_jogador(jogador2)
    
    jogo.add_propriedade(prop1)
    jogo.add_propriedade(prop2)
    jogo.add_propriedade(prop3)
    
    jogo.remover_jogador(jogador1)
    
    assert len(jogo.jogadores) == 1
    assert jogador1 not in jogo.jogadores
    assert prop1.proprietario is None
    assert prop3.proprietario is None
    assert prop2.proprietario == jogador2  # Propriedade do J2 continua com ele


@patch('jogo.Jogo.rolar_dado')
@patch('jogo.random.shuffle')
def test_simular_jogador_vai_a_falencia(mock_shuffle, mock_rolar_dado):
    jogo = Jogo()
    
    jogador1 = Jogador("J1", JogadorImpulsivoStategy())
    jogador2 = Jogador("J2", JogadorImpulsivoStategy())
    # Definindo um saldo que causará falência ao pagar o primeiro aluguel
    jogador2._saldo = 10
    
    jogo.add_jogador(jogador1)
    jogo.add_jogador(jogador2)
    
    # Criamos o tabuleiro com 2 propriedades
    prop_inicial = Propriedade(100, 50)
    prop_j1 = Propriedade(100, 50, proprietario=jogador1)
    
    jogo.add_propriedade(prop_inicial)
    jogo.add_propriedade(prop_j1)
    
    # Garantimos que a ordem dos jogadores não seja alterada no shuffle
    mock_shuffle.side_effect = lambda x: x
    
    # Na rodada 1:
    # J1 rola 1, cai na prop_j1 (que já é dele, nada acontece)
    # J2 rola 1, cai na prop_j1, paga aluguel (50), fica com -40 e é removido.
    mock_rolar_dado.side_effect = [1, 1]
    
    vencedores = jogo.simular()
    
    assert len(vencedores) == 1
    assert vencedores[0] == jogador1
    assert len(jogo.jogadores) == 1
    assert jogador1 in jogo.jogadores
    assert jogador2 not in jogo.jogadores


@patch('jogo.Jogo.rolar_dado')
@patch('jogo.random.shuffle')
def test_simular_jogador_ganha_bonus_volta(mock_shuffle, mock_rolar_dado):
    jogo = Jogo()
    
    jogador = Jogador("J1", JogadorImpulsivoStategy())
    jogador.posicao = 18
    # Configurando saldo alto para não comprar e ir à falência, ou caso compre que não importe
    jogador._saldo = 300
    
    jogo.add_jogador(jogador)
    
    # Necessitamos de um adversário para o jogo rodar
    jogador_fake = Jogador("Fake", JogadorImpulsivoStategy())
    jogador_fake._saldo = 0
    jogo.add_jogador(jogador_fake)
    
    for _ in range(20):
        # Propriedades caras demais para comprar
        jogo.add_propriedade(Propriedade(1000, 100))
        
    mock_shuffle.side_effect = lambda x: x
    
    # Turno 1: 
    # J1 (posicao 18) rola 3, vai para 21 -> posição 1, ganha 100
    # J2 (posicao 0) rola 1, cai na prop[1], não tem dinheiro pra comprar, fim do turno
    # Turno 2:
    # J1 rola 1...
    # Para forçar o fim do jogo, o J2 vai cair em uma propriedade de J1 e falir, ou forçaremos falência manual
    # Vamos setar J2 para cair numa prop com aluguel onde proprietario seja J1, mas não há nenhuma.
    
    mock_rolar_dado.side_effect = [3, 1]
    
    # Modificaremos o jogo manualmente para encerrar no loop, 
    # já que não queremos esperar 1000 turnos. E faremos a falência de J2.
    jogo.propriedades[1].proprietario = jogador
    
    jogo.simular()
    
    # Ao final, J1 deve ter saldo 400 (300 inicial + 100 da volta), além do aluguel recebido (100) = 500
    assert jogador.saldo == 500
    assert jogador.posicao == 1


@patch('jogo.Jogo.rolar_dado')
@patch('jogo.random.shuffle')
def test_simular_termino_timeout_rodadas(mock_shuffle, mock_rolar_dado):
    jogo = Jogo()
    
    jogador1 = Jogador("J1", JogadorImpulsivoStategy())
    jogador2 = Jogador("J2", JogadorImpulsivoStategy())
    
    jogo.add_jogador(jogador1)
    jogo.add_jogador(jogador2)
    
    for _ in range(20):
        # Propriedades gratuitas para evitar problemas de saldo e aluguel zero
        jogo.add_propriedade(Propriedade(10000, 0))
        
    mock_shuffle.side_effect = lambda x: x
    
    # Fornece rolagem de dados infinita (sempre 1)
    mock_rolar_dado.return_value = 1
    
    vencedores = jogo.simular()
    
    assert jogo.rodada_atual == 1000
    assert len(vencedores) == 2
