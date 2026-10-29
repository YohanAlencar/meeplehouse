from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os

app = FastAPI(title="MeepleHouse API", version="1.0.0")

# Permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ARQUIVO_DADOS = "jogos.json"

class Jogo(BaseModel):
    titulo: str
    editora: str
    tempo: int
    jogadores: str
    estado: str

def ler_dados():
    if not os.path.exists(ARQUIVO_DADOS):
        return []
    with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def salvar_dados(dados):
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

@app.get("/jogos")
def listar_jogos():
    return ler_dados()

@app.post("/jogos")
def criar_jogo(jogo: Jogo):
    jogos = ler_dados()
    novo_id = max([j.get("id", 0) for j in jogos], default=0) + 1
    novo_jogo = {"id": novo_id, **jogo.dict()}
    jogos.append(novo_jogo)
    salvar_dados(jogos)
    return {"mensagem": "Jogo cadastrado com sucesso!", "jogo": novo_jogo}

@app.put("/jogos/{jogo_id}")
def atualizar_jogo(jogo_id: int, jogo: Jogo):
    jogos = ler_dados()
    for index, j in enumerate(jogos):
        if j.get("id") == jogo_id:
            jogos[index] = {"id": jogo_id, **jogo.dict()}
            salvar_dados(jogos)
            return {"mensagem": "Jogo atualizado com sucesso!", "jogo": jogos[index]}
    raise HTTPException(status_code=404, detail="Jogo não encontrado.")

@app.delete("/jogos/{jogo_id}")
def excluir_jogo(jogo_id: int):
    jogos = ler_dados()
    novos_jogos = [j for j in jogos if j.get("id") != jogo_id]
    if len(novos_jogos) == len(jogos):
        raise HTTPException(status_code=404, detail="Jogo não encontrado.")
    salvar_dados(novos_jogos)
    return {"mensagem": "Jogo excluído com sucesso!"}