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