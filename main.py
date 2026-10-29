from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import redis
import json

app = FastAPI(title="MeepleHouse API - Redis", version="1.0.0")

# Configurar CORS para permitir a comunicação com o frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conexão com o Redis (protocol=2 garante compatibilidade com o Redis 5 instalado localmente)
db = redis.Redis(host="localhost", port=6379, decode_responses=True, protocol=2)

class Jogo(BaseModel):
    titulo: str
    editora: str
    tempo: int
    jogadores: str
    estado: str

REDIS_KEY = "meeplehouse:dados"

def ler_redis():
    dados = db.get(REDIS_KEY)
    if not dados:
        return []
    try:
        return json.loads(dados)
    except:
        return []

def salvar_redis(jogos):
    db.set(REDIS_KEY, json.dumps(jogos, ensure_ascii=False))

@app.get("/jogos")
def listar_jogos():
    return ler_redis()

@app.post("/jogos")
def criar_jogo(jogo: Jogo):
    jogos = ler_redis()
    novo_id = max([j.get("id", 0) for j in jogos], default=0) + 1
    novo_jogo = {"id": novo_id, **jogo.dict()}
    jogos.append(novo_jogo)
    salvar_redis(jogos)
    return {"mensagem": "Jogo cadastrado com sucesso!", "jogo": novo_jogo}

@app.put("/jogos/{jogo_id}")
def atualizar_jogo(jogo_id: int, jogo: Jogo):
    jogos = ler_redis()
    encontrado = False
    for index, j in enumerate(jogos):
        if j.get("id") == jogo_id:
            jogos[index] = {"id": jogo_id, **jogo.dict()}
            encontrado = True
            break
    
    if not encontrado:
        raise HTTPException(status_code=404, detail="Jogo não encontrado.")
    
    salvar_redis(jogos)
    return {"mensagem": "Jogo atualizado com sucesso!"}

@app.delete("/jogos/{jogo_id}")
def excluir_jogo(jogo_id: int):
    jogos = ler_redis()
    novos_jogos = [j for j in jogos if j.get("id") != jogo_id]
    
    if len(novos_jogos) == len(jogos):
        raise HTTPException(status_code=404, detail="Jogo não encontrado.")
    
    salvar_redis(novos_jogos)
    return {"mensagem": "Jogo excluído com sucesso!"}