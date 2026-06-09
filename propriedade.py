class Propriedade:
    def __init__(self, custo, aluguel, proprietario=None) -> None:
        self._custo = custo
        self._aluguel = aluguel
        self._proprietario = proprietario

    @property
    def custo(self):
        return self._custo