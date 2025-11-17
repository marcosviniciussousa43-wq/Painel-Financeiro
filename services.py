# services.py
# Este arquivo contém TODA a lógica de negócio e acesso a APIs.

import requests  # <-- A importação saiu do main.py e veio para cá

# --- Funções de Lógica (Serviços) ---

def buscar_taxa_selic_bcb():
    """
    Busca o último valor da Meta Selic (% a.a.) na API do Banco Central.
    Retorna o valor como um float (número) ou None se falhar.
    """
    url_api = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/1?formato=json"
    try:
        response = requests.get(url_api)
        response.raise_for_status()
        dados = response.json()
        valor_selic_str = dados[0]['valor']
        return float(valor_selic_str)
    except requests.RequestException as e:
        print(f"Erro de rede ao buscar Selic: {e}")
        return None
    except (IndexError, KeyError, TypeError) as e:
        print(f"Erro ao processar o JSON da Selic: {e}")
        return None

def buscar_taxa_ipca_bcb():
    """
    Busca o último valor do IPCA (acumulado 12 meses) na API do Banco Central.
    Retorna o valor como um float (número) ou None se falhar.
    """
    url_api = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.13522/dados/ultimos/1?formato=json"
    try:
        response = requests.get(url_api)
        response.raise_for_status()
        dados = response.json()
        valor_ipca_str = dados[0]['valor']
        return float(valor_ipca_str)
    except requests.RequestException as e:
        print(f"Erro de rede ao buscar IPCA: {e}")
        return None
    except (IndexError, KeyError, TypeError) as e:
        print(f"Erro ao processar o JSON do IPCA: {e}")
        return None

def calcular_rentabilidade_real(taxa_nominal_anual, taxa_inflacao_anual):
    """
    Calcula a rentabilidade real com base na taxa nominal e na inflação.
    As taxas devem ser decimais (ex: 10.5% = 0.105)
    """
    rentabilidade_real = ((1 + taxa_nominal_anual) / (1 + taxa_inflacao_anual)) - 1
    return rentabilidade_real