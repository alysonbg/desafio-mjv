from fastapi import FastAPI
import random

from jogo import Jogo
from jogador import (
    Jogador, 
    JogadorCautelosoStategy, 
    JogadorImpulsivoStategy, 
    JogadorExigenteStategy, 
    JogadorAleatorioStategy
)
from propriedade import Propriedade

app = FastAPI()

@app.get("/jogo/simular")
def simular_jogo():
    jogo = Jogo()
    
    # Adiciona os 4 jogadores com as respectivas estratégias
    jogo.add_jogador(Jogador("impulsivo", JogadorImpulsivoStategy()))
    jogo.add_jogador(Jogador("exigente", JogadorExigenteStategy()))
    jogo.add_jogador(Jogador("cauteloso", JogadorCautelosoStategy()))
    jogo.add_jogador(Jogador("aleatorio", JogadorAleatorioStategy()))
    
    # Adiciona 20 propriedades com custos e aluguéis definidos (simulados)
    for _ in range(20):
        custo = random.randint(50, 200)
        aluguel = random.randint(10, int(custo / 2))
        jogo.add_propriedade(Propriedade(custo, aluguel))
        
    vencedores = jogo.simular()
    
    response = {
        "vencedor": vencedores[0].nome if vencedores else "",
        "jogadores": [j.nome for j in vencedores]
    }
    
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
