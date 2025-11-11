# 1. Importa o FastAPI
from fastapi import FastAPI

# 2. Cria uma "instância" da aplicação
app = FastAPI()

# 3. Define o primeiro "endpoint" (a primeira URL)
@app.get("/")
def raiz():
    """
    Este é o endpoint raiz da API.
    Retorna uma mensagem de boas-vindas.
    """
    return {"mensagem": "Bem-vindo ao Painel Financeiro!"}

# 4. (Bônus) Endpoint para testar o roadmap
@app.get("/fase1")
def fase1():
    """
    Endpoint que confirma a Fase 1 do roadmap.
    """
    return {"status": "Fase 1 (Core Backend) iniciada com sucesso!"}