# main.py
# Este arquivo é o "Roteador" (Router).
# Ele APENAS lida com as URLs e chama os serviços.

from fastapi import FastAPI, HTTPException

# 1. IMPORTA as funções do nosso novo arquivo "services"
import services
import schemas
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


# SUBSTITUA O ENDPOINT ANTIGO POR ESTE
@app.get("/rentabilidade-real")
def get_rentabilidade_real():
    """
    Endpoint que busca Selic, IPCA e calcula a rentabilidade real.
    """
    print("Recebida requisição para /rentabilidade-real")

    selic, ipca, rentabilidade_real = services.get_dados_economicos_reais()

    if rentabilidade_real is None:
        raise HTTPException(status_code=500, detail="Não foi possível buscar os dados do BCB (Selic ou IPCA).")

    return {
        "taxa_selic_anual": selic,
        "ipca_acumulado_12m": ipca,
        "rentabilidade_real_anual": round(rentabilidade_real * 100, 2)
    }
# ADICIONE ESTE NOVO ENDPOINT NO FINAL DO main.py

@app.post("/projetar-meta")
def projetar_meta(request: schemas.ProjecaoRequest):
    """
    Recebe os dados do usuário e calcula a projeção para atingir a meta
    usando a rentabilidade real atual.
    """
    print(f"Recebida requisição para /projetar-meta com dados: {request}")

    # 1. Pega os dados econômicos atuais
    _, _, rentabilidade_real_decimal = services.get_dados_economicos_reais()

    if rentabilidade_real_decimal is None:
        raise HTTPException(status_code=500, detail="Não foi possível buscar os dados do BCB para o cálculo.")

    try:
        # 2. Chama a super calculadora
        projecao = services.calcular_projecao_meta(
            valor_inicial=request.valor_inicial,
            aporte_mensal=request.aporte_mensal,
            meses_sem_aporte_por_ano=request.meses_por_ano_sem_aporte,
            meta_financeira=request.meta_financeira,
            taxa_real_anual=rentabilidade_real_decimal
        )
        return projecao

    except ValueError as e:
        # Captura o erro (ex: 100 anos)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Captura qualquer outro erro inesperado
        raise HTTPException(status_code=500, detail=f"Erro interno no cálculo: {e}")