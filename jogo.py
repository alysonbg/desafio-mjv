import random

class Jogo:
    def __init__(self):
        self.propriedades = []
        self.jogadores = []
        self.rodada_atual = 0

    def add_jogador(self, jogador):
        self.jogadores.append(jogador)

    def add_propriedade(self, propriedade):
        self.propriedades.append(propriedade)

    def inicializar_jogo(self):
        # Embaralha jogadores no começo da partida
        random.shuffle(self.jogadores)
        self.rodada_atual = 0

    def rolar_dado(self):
        return random.randint(1, 6)

    def remover_jogador(self, jogador):
        # Libera as propriedades do jogador caso ele perca o jogo
        for prop in self.propriedades:
            if prop.proprietario == jogador:
                prop.proprietario = None
        self.jogadores.remove(jogador)

    def simular(self):
        self.inicializar_jogo()

        while self.rodada_atual < 1000 and len(self.jogadores) > 1:
            self.rodada_atual += 1
            
            jogadores_para_remover = []
            
            for jogador in self.jogadores:
                if jogador in jogadores_para_remover:
                    continue
                
                # Joga o dado
                dado = self.rolar_dado()
                jogador.posicao += dado
                
                # Verifica se completou uma volta
                if jogador.posicao >= 20:
                    jogador.incrementa_saldo(100)
                    jogador.posicao = jogador.posicao % 20
                
                propriedade = self.propriedades[jogador.posicao]
                
                if propriedade.proprietario is None:
                    # Verifica se pode e quer comprar
                    if jogador.saldo >= propriedade.custo and jogador.deve_comprar(propriedade):
                        jogador.decrementa_saldo(propriedade.custo)
                        propriedade.proprietario = jogador
                elif propriedade.proprietario != jogador:
                    # Paga aluguel ao proprietário
                    jogador.decrementa_saldo(propriedade.aluguel)
                    propriedade.proprietario.incrementa_saldo(propriedade.aluguel)
                    
                # Verifica falência
                if jogador.saldo < 0:
                    jogadores_para_remover.append(jogador)
                    
            for jogador_removido in jogadores_para_remover:
                self.remover_jogador(jogador_removido)

        # Retorna a lista de jogadores ordenada por saldo.
        # Caso o jogo termine no timeout (rodada 1000) ou apenas com um vencedor.
        # A ordem inicial da lista `self.jogadores` após o shuffle dita o desempate
        # naturalmente com o sorted (stable sort do Python) para jogadores com o mesmo saldo.
        vencedores = sorted(self.jogadores, key=lambda j: j.saldo, reverse=True)
        return vencedores