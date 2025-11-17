# main.py
# Versão 3.0 (Líquida) - CORRIGIDA

from fastapi import FastAPI, HTTPException
# 1. IMPORTAÇÕES NOVAS para servir arquivos
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse 
import uvicorn # Importamos o uvicorn para rodar o app

import services
import schemas

# --- Configuração da Aplicação ---
app = FastAPI()

# 2. "MONTAR" A PASTA ESTÁTICA
app.mount("/static", StaticFiles(directory="static"), name="static")


# --- Endpoints (As URLs da sua API) ---

# 3. ENDPOINT RAIZ ("/")
@app.get("/")
def raiz():
    """
    Serve o arquivo HTML principal da aplicação.
    """
    return FileResponse("static/index.html")


# 4. ENDPOINTS ANTIGOS (Selic e IPCA)
@app.get("/taxa-selic")
def get_taxa_selic():
    """
    Endpoint para buscar a taxa Selic atualizada do BCB.
    """
    print("Recebida requisição para /taxa-selic")
    taxa = services.buscar_taxa_selic_bcb()
    if taxa is None:
        raise HTTPException(status_code=500, detail="Não foi possível buscar a taxa Selic no Banco Central.")
    return {"taxa_selic_anual": taxa}


@app.get("/taxa-ipca")
def get_taxa_ipca():
    """
    Endpoint para buscar o IPCA atualizado (acumulado 12 meses) do BCB.
    """
    print("Recebida requisição para /taxa-ipca")
    taxa = services.buscar_taxa_ipca_bcb()
    if taxa is None:
        raise HTTPException(status_code=500, detail="Não foi possível buscar a taxa IPCA no Banco Central.")
    return {"ipca_acumulado_12m": taxa}


# 5. ENDPOINT ATUALIZADO (Rentabilidade Real - Bruta e Líquida)
@app.get("/rentabilidade-real")
def get_rentabilidade_real():
    """
    Endpoint que busca Selic, IPCA e calcula ambas rentabilidades (bruta e líquida).
    """
    print("Recebida requisição para /rentabilidade-real")
    
    # Agora pegamos os 4 valores
    selic, ipca, rentabilidade_bruta, rentabilidade_liquida = services.get_dados_economicos_reais()
    
    if rentabilidade_bruta is None: # Se um falhar, todos falham
        raise HTTPException(status_code=500, detail="Não foi possível buscar os dados do BCB (Selic ou IPCA).")

    # Retornamos tudo no JSON
    return {
        "taxa_selic_anual": selic,
        "ipca_acumulado_12m": ipca,
        "rentabilidade_real_bruta_anual": round(rentabilidade_bruta * 100, 2),
        "rentabilidade_real_liquida_anual": round(rentabilidade_liquida * 100, 2)
    }


# 6. ENDPOINT ATUALIZADO (Projeção Líquida)
@app.post("/projetar-meta")
def projetar_meta(request: schemas.ProjecaoRequest):
    """
    Recebe os dados do usuário e calcula a projeção para atingir a meta
    usando a rentabilidade real LÍQUIDA (já com imposto).
    """
    print(f"Recebida requisição para /projetar-meta com dados: {request}")
    
    # Pegamos os 4 valores
    # Usamos "_" para ignorar os valores que não vamos usar aqui
    _, _, _, rentabilidade_real_liquida_decimal = services.get_dados_economicos_reais()
    
    if rentabilidade_real_liquida_decimal is None:
        raise HTTPException(status_code=500, detail="Não foi possível buscar os dados do BCB para o cálculo.")

    try:
        # PASSAMOS A TAXA LÍQUIDA PARA A CALCULADORA
        projecao = services.calcular_projecao_meta(
            valor_inicial=request.valor_inicial,
            aporte_mensal=request.aporte_mensal,
            meses_sem_aporte_por_ano=request.meses_por_ano_sem_aporte,
            meta_financeira=request.meta_financeira,
            taxa_real_anual=rentabilidade_real_liquida_decimal
        )
        return projecao
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno no cálculo: {e}")


# --- Ponto de Entrada para Rodar a Aplicação ---
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)