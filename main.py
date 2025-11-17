import requests  # <-- Importamos a nova biblioteca
from fastapi import FastAPI, HTTPException  # <-- Importamos o HTTPException para erros

# --- Configuração da Aplicação ---
app = FastAPI()

# --- Funções de Lógica (Serviços) ---

def buscar_taxa_selic_bcb():
    """
    Busca o último valor da Meta Selic (% a.a.) na API do Banco Central.
    Retorna o valor como um float (número) ou None se falhar.
    """
    # Este é o URL da API que encontramos
    url_api = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/1?formato=json"

    try:
        # 1. Tenta fazer a requisição para a API
        response = requests.get(url_api)
        
        # 2. Verifica se a requisição falhou (ex: erro 404, 500)
        response.raise_for_status()  # Se falhar, levanta um erro

        # 3. Pega os dados em formato JSON
        dados = response.json()

        # 4. Extrai o valor (O JSON é uma lista [0] com um objeto {'valor': ...})
        valor_selic_str = dados[0]['valor']
        
        # 5. Converte o valor de texto (ex: "10.50") para um número
        return float(valor_selic_str)

    except requests.RequestException as e:
        # 6. Captura erros de rede (ex: sem internet, API fora do ar)
        print(f"Erro de rede ao buscar Selic: {e}")
        return None
    except (IndexError, KeyError, TypeError) as e:
        # 7. Captura erros se o formato do JSON mudar
        print(f"Erro ao processar o JSON da Selic: {e}")
        return None

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
    
    # Chama nossa função de lógica
    taxa = buscar_taxa_selic_bcb()

    # Verifica se a função conseguiu buscar o dado
    if taxa is None:
        # Se deu erro (None), retorna um erro 500 para o usuário
        raise HTTPException(status_code=500, detail="Não foi possível buscar a taxa Selic no Banco Central.")
    
    # Se deu tudo certo, retorna o valor
    return {"taxa_selic_anual": taxa}
# --- ADICIONE ESTE NOVO CÓDIGO NO FINAL DO SEU main.py ---

def buscar_taxa_ipca_bcb():
    """
    Busca o último valor do IPCA (acumulado 12 meses) na API do Banco Central.
    Retorna o valor como um float (número) ou None se falhar.
    """
    # Código 13522 = IPCA Acumulado 12 meses
    url_api = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.13522/dados/ultimos/1?formato=json"

    try:
        # 1. Tenta fazer a requisição para a API
        response = requests.get(url_api)
        response.raise_for_status()  # Se falhar, levanta um erro

        # 2. Pega os dados em formato JSON
        dados = response.json()

        # 3. Extrai e converte o valor
        valor_ipca_str = dados[0]['valor']
        return float(valor_ipca_str)

    except requests.RequestException as e:
        print(f"Erro de rede ao buscar IPCA: {e}")
        return None
    except (IndexError, KeyError, TypeError) as e:
        print(f"Erro ao processar o JSON do IPCA: {e}")
        return None

@app.get("/taxa-ipca")
def get_taxa_ipca():
    """
    Endpoint para buscar o IPCA atualizado (acumulado 12 meses) do BCB.
    """
    print("Recebida requisição para /taxa-ipca")
    
    # Chama nossa nova função de lógica
    taxa = buscar_taxa_ipca_bcb()

    if taxa is None:
        # Se deu erro, retorna um erro 500
        raise HTTPException(status_code=500, detail="Não foi possível buscar a taxa IPCA no Banco Central.")
    
    # Se deu tudo certo, retorna o valor
    return {"ipca_acumulado_12m": taxa}
# --- ADICIONE ESTE NOVO CÓDIGO NO FINAL DO SEU main.py ---

def calcular_rentabilidade_real(taxa_nominal_anual, taxa_inflacao_anual):
    """
    Calcula a rentabilidade real com base na taxa nominal e na inflação.
    As taxas devem ser decimais (ex: 10.5% = 0.105)
    """
    # Fórmula: Rentabilidade Real = [(1 + Rentabilidade Nominal) / (1 + Inflação)] - 1
    rentabilidade_real = ((1 + taxa_nominal_anual) / (1 + taxa_inflacao_anual)) - 1
    return rentabilidade_real

@app.get("/rentabilidade-real")
def get_rentabilidade_real():
    """
    Endpoint que busca Selic, IPCA e calcula a rentabilidade real.
    """
    print("Recebida requisição para /rentabilidade-real")
    
    # 1. Busca os dados (reutilizando nossas funções!)
    taxa_selic_percent = buscar_taxa_selic_bcb()
    taxa_ipca_percent = buscar_taxa_ipca_bcb()

    # 2. Checa se algum dos dados falhou
    if taxa_selic_percent is None or taxa_ipca_percent is None:
        raise HTTPException(status_code=500, detail="Não foi possível buscar os dados do BCB (Selic ou IPCA).")

    # 3. Converte os percentuais (ex: 10.5) para decimais (ex: 0.105)
    taxa_selic_decimal = taxa_selic_percent / 100
    taxa_ipca_decimal = taxa_ipca_percent / 100

    # 4. Calcula a rentabilidade real
    rentabilidade_real_decimal = calcular_rentabilidade_real(taxa_selic_decimal, taxa_ipca_decimal)
    
    # 5. Converte o resultado de volta para percentual para exibição
    rentabilidade_real_percent = rentabilidade_real_decimal * 100

    # 6. Retorna tudo em um JSON completo!
    return {
        "taxa_selic_anual": taxa_selic_percent,
        "ipca_acumulado_12m": taxa_ipca_percent,
        "rentabilidade_real_anual": round(rentabilidade_real_percent, 2) # Arredonda para 2 casas decimais
    }