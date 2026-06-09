from abc import ABC, abstractmethod
from typing import Protocol
import random
from propriedade import Propriedade


class Avaliavel(Protocol):
    @property
    def saldo(self) -> int:
        pass


class JogadorStategy(ABC):
    @abstractmethod
    def run(self, propriedade: Propriedade, jogador) -> bool:
        pass


class JogadorCautelosoStategy(JogadorStategy):
    def run(self, propriedade: Propriedade, jogador: Avaliavel) -> bool:
        resultado = False

        novo_saldo = jogador.saldo - propriedade.custo

        if novo_saldo >= 80 and novo_saldo > 0:
            resultado = True
            
        return resultado


class JogadorImpulsivoStategy(JogadorStategy):
    def run(self, propriedade: Propriedade, jogador: Avaliavel) -> bool:
        resultado = False
        novo_saldo = jogador.saldo - propriedade.custo

        if novo_saldo > 0:
            resultado = True

        return resultado


class JogadorExigenteStategy(JogadorStategy):
    def run(self, propriedade: Propriedade, jogador: Avaliavel) -> bool:
        resultado = False

        novo_saldo = jogador.saldo - propriedade.custo

        if propriedade.aluguel > 50 and novo_saldo > 0:
            resultado = True

        return resultado


class JogadorAleatorioStategy(JogadorStategy):
    def run(self, propriedade: Propriedade, jogador: Avaliavel) -> bool:
        novo_saldo = jogador.saldo - propriedade.custo

        if novo_saldo > 0:
            return random.choice([True, False])

        return False


class Jogador:
    def __init__(self, nome: str, estrategia: JogadorStategy) -> None:
        self.nome = nome
        self._saldo = 300
        self.posicao = 0
        self.estrategia = estrategia

    @property
    def saldo(self):
        return self._saldo

    def incrementa_saldo(self, valor: int):
        self._saldo += valor

    def decrementa_saldo(self, valor: int):
        self._saldo -= valor
        
    def deve_comprar(self, propriedade: Propriedade) -> bool:
        return self.estrategia.run(propriedade, self)
        
