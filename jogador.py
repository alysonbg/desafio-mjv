from abc import ABC, abstractmethod
from typing import Protocol
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

        if novo_saldo >= 80:
            resultado = True
            
        return resultado


class JogadorImpulsivoStategy(JogadorStategy):
    def run(self, propriedade: Propriedade, jogador: Avaliavel) -> bool:
        return True



class Jogador:
    def __init__(self, estrategia: JogadorStategy) -> None:
        self._saldo = 300
        self.posicao = 0
        self.estrategia = estrategia

    @property
    def saldo(self):
        return self._saldo

    def deve_comprar(self, propriedade: Propriedade) -> bool:
        return self.estrategia.run(propriedade, self)
        
