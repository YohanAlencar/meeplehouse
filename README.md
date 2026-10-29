# 🏰 MeepleHouse - Gestão de Jogos de Tabuleiro

O **MeepleHouse** é uma aplicação web completa para gestão e catalogação de jogos de tabuleiro, desenvolvida com backend em **FastAPI** e persistência de dados em memória de alta performance utilizando o **Redis**.

---

## 🛠️ Tecnologias Utilizadas

- **Backend:** Python / FastAPI
- **Base de Dados:** Redis (utilizando `redis-py` com protocolo v2)
- **Frontend:** HTML5, CSS3, JavaScript (Fetch API) e Bootstrap 5
- **Servidor Web / ASGI:** Uvicorn

---

## 📋 Pré-requisitos

1. **Python 3.10+** instalado.
2. **Servidor Redis** em execução na máquina (`localhost:6379`).

---

## 🚀 Como Executar o Projeto

### 1. Iniciar o Servidor Redis
Certifica-te de que o serviço do Redis está ativo na tua máquina local na porta padrão (`6379`).

### 2. Instalar as Dependências
No terminal, na pasta do projeto, instala os pacotes necessários:

```bash
pip install -r requirements.txt