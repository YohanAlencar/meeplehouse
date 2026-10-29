import json
import os
import uuid
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="MeepleHouse API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_FILE = "jogos.json"

def ler_dados():
    if not os.path.exists(DB_FILE):
        return []
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def escrever_dados(dados):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

class JogoSchema(BaseModel):
    id: Optional[str] = None
    titulo: str
    editora: str
    tempo_partida: int
    numero_jogadores: str
    estado_conservacao: str
    status: Optional[str] = "Na prateleira"

@app.get("/jogos", response_model=List[JogoSchema])
def listar_jogos():
    return ler_dados()

@app.post("/jogos", response_model=JogoSchema)
def criar_jogo(jogo: JogoSchema):
    jogos = ler_dados()
    if not jogo.id:
        jogo.id = str(uuid.uuid4())
    
    jogos.append(jogo.dict())
    escrever_dados(jogos)
    return jogo

@app.delete("/jogos/{jogo_id}")
def deletar_jogo(jogo_id: str):
    jogos = ler_dados()
    novos_jogos = [j for j in jogos if j.get("id") != jogo_id]
    
    if len(novos_jogos) == len(jogos):
        raise HTTPException(status_code=404, detail="Jogo não encontrado")
    
    escrever_dados(novos_jogos)
    return {"message": "Jogo removido com sucesso"}