# main.py
# Este arquivo é o "Roteador" (Router).
# Ele APENAS lida com as URLs e chama os serviços.

from fastapi import FastAPI, HTTPException

# 1. IMPORTA as funções do nosso novo arquivo "services"
import services

# --- Configuração da Aplicação ---
app = FastAPI()

# --- Endpoints (As URLs da sua API) ---

@app.get("/")
def raiz():
    """Endpoint raiz com mensagem de boas-vindas."""
    return {"mensagem": "Bem-vindo ao Painel Financeiro!"}


@app.get("/taxa-selic")
def get_taxa_selic():
    """
    Endpoint para buscar a taxa Selic atualizada do BCB.
    """
    print("Recebida requisição para /taxa-selic")
    
    # 2. CHAMA o serviço
    taxa = services.buscar_taxa_selic_bcb() # <-- Mudou!

    if taxa is None:
        raise HTTPException(status_code=500, detail="Não foi possível buscar a taxa Selic no Banco Central.")
    
    return {"taxa_selic_anual": taxa}


@app.get("/taxa-ipca")
def get_taxa_ipca():
    """
    Endpoint para buscar o IPCA atualizado (acumulado 12 meses) do BCB.
    """
    print("Recebida requisição para /taxa-ipca")
    
    # 3. CHAMA o serviço
    taxa = services.buscar_taxa_ipca_bcb() # <-- Mudou!

    if taxa is None:
        raise HTTPException(status_code=500, detail="Não foi possível buscar a taxa IPCA no Banco Central.")
    
    return {"ipca_acumulado_12m": taxa}


@app.get("/rentabilidade-real")
def get_rentabilidade_real():
    """
    Endpoint que busca Selic, IPCA e calcula a rentabilidade real.
    """
    print("Recebida requisição para /rentabilidade-real")
    
    # 4. CHAMA os serviços
    taxa_selic_percent = services.buscar_taxa_selic_bcb() # <-- Mudou!
    taxa_ipca_percent = services.buscar_taxa_ipca_bcb() # <-- Mudou!

    if taxa_selic_percent is None or taxa_ipca_percent is None:
        raise HTTPException(status_code=500, detail="Não foi possível buscar os dados do BCB (Selic ou IPCA).")

    taxa_selic_decimal = taxa_selic_percent / 100
    taxa_ipca_decimal = taxa_ipca_percent / 100

    # 5. CHAMA o serviço
    rentabilidade_real_decimal = services.calcular_rentabilidade_real(taxa_selic_decimal, taxa_ipca_decimal) # <-- Mudou!
    
    rentabilidade_real_percent = rentabilidade_real_decimal * 100

    return {
        "taxa_selic_anual": taxa_selic_percent,
        "ipca_acumulado_12m": taxa_ipca_percent,
        "rentabilidade_real_anual": round(rentabilidade_real_percent, 2)
    }