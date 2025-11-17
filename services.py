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
# ADICIONE ESTA FUNÇÃO NO services.py

# Em services.py
# (O resto do arquivo continua igual, só mude esta função)

def get_dados_economicos_reais():
    """
    Busca Selic, IPCA e já calcula as rentabilidades reais (Bruta e Líquida).
    Retorna uma tupla (selic, ipca, rentabilidade_real_bruta, rentabilidade_real_liquida)
    Retorna (None, None, None, None) em caso de falha.
    """
    # Esta é a alíquota de Imposto de Renda para investimentos de longo prazo
    ALIQUOTA_IR_LONGO_PRAZO = 0.15 # 15%
    
    taxa_selic_percent = buscar_taxa_selic_bcb()
    taxa_ipca_percent = buscar_taxa_ipca_bcb()

    if taxa_selic_percent is None or taxa_ipca_percent is None:
        return None, None, None, None # <-- MUDANÇA AQUI

    # 1. Converter para decimais
    taxa_selic_decimal = taxa_selic_percent / 100
    taxa_ipca_decimal = taxa_ipca_percent / 100

    # 2. Calcular a rentabilidade real BRUTA (como era antes)
    rentabilidade_real_bruta = calcular_rentabilidade_real(
        taxa_selic_decimal, taxa_ipca_decimal
    )
    
    # 3. Calcular a rentabilidade LÍQUIDA (A GRANDE MUDANÇA)
    
    # Primeiro, aplicamos o imposto sobre o ganho nominal (Selic)
    ganho_nominal_liquido_decimal = taxa_selic_decimal * (1 - ALIQUOTA_IR_LONGO_PRAZO) # Ex: 10.5% * (1 - 0.15) = 8.925%
    
    # Segundo, calculamos a rentabilidade real em cima desse ganho líquido
    rentabilidade_real_liquida = calcular_rentabilidade_real(
        ganho_nominal_liquido_decimal, taxa_ipca_decimal # ( (1 + 0.08925) / (1 + 0.0468) ) - 1
    )
    
    # 4. Retorna os 4 valores
    return (
        taxa_selic_percent, 
        taxa_ipca_percent, 
        rentabilidade_real_bruta, 
        rentabilidade_real_liquida
    )

def calcular_projecao_meta(
    valor_inicial: float,
    aporte_mensal: float,
    meses_sem_aporte_por_ano: int,
    meta_financeira: float,
    taxa_real_anual: float
):
    """
    Calcula a projeção de juros compostos mês a mês até atingir a meta,
    com base na rentabilidade real.
    """

    # 1. Converter a taxa real ANUAL para MENSAL
    # Esta é a fórmula correta de juros compostos
    taxa_real_mensal = (1 + taxa_real_anual) ** (1/12) - 1

    # 2. Inicializar variáveis
    valor_atual = valor_inicial
    meses_totais = 0
    resumo_anual = [] # Lista para guardar os resumos de cada ano

    # Variáveis para o resumo do ano
    juros_ganhos_no_ano = 0
    aportes_feitos_no_ano = 0
    valor_no_inicio_do_ano = valor_inicial

    # Quantos meses por ano ela DE FATO aporta
    meses_de_aporte_por_ano = 12 - meses_sem_aporte_por_ano

    # 3. O Loop Principal (o motor da calculadora)
    while valor_atual < meta_financeira:

        # Para o limite de segurança, caso a meta seja impossível
        if meses_totais > (12 * 100): # Limite de 100 anos
            raise ValueError("A meta não foi atingida em 100 anos. Verifique os valores.")

        meses_totais += 1

        # 1. Calcula os juros do mês (sobre o que já tinha)
        juros_do_mes = valor_atual * taxa_real_mensal
        valor_atual += juros_do_mes
        juros_ganhos_no_ano += juros_do_mes

        # 2. Adiciona o aporte?
        # (meses_totais % 12) nos dá o mês atual do ano (de 1 a 11, e 0 para o 12º)
        # Se o mês atual for MENOR que o número de meses que ela aporta, ela aporta.
        mes_do_ano_atual = meses_totais % 12 
        if mes_do_ano_atual != 0 and mes_do_ano_atual <= meses_de_aporte_por_ano:
             valor_atual += aporte_mensal
             aportes_feitos_no_ano += aporte_mensal
        # Caso especial para o 12º mês (mês % 12 == 0)
        elif mes_do_ano_atual == 0 and 12 <= meses_de_aporte_por_ano:
             valor_atual += aporte_mensal
             aportes_feitos_no_ano += aporte_mensal


        # 3. Fechamento do Ano?
        if meses_totais % 12 == 0:
            ano = meses_totais // 12
            resumo_anual.append({
                "ano": ano,
                "valor_inicio_ano": round(valor_no_inicio_do_ano, 2),
                "aportes_no_ano": round(aportes_feitos_no_ano, 2),
                "juros_ganhos_no_ano": round(juros_ganhos_no_ano, 2),
                "valor_final_ano": round(valor_atual, 2)
            })

            # Reseta os contadores para o próximo ano
            juros_ganhos_no_ano = 0
            aportes_feitos_no_ano = 0
            valor_no_inicio_do_ano = valor_atual

    # 4. Retorna o resultado final
    return {
        "meses_para_atingir_meta": meses_totais,
        "anos_para_atingir_meta": round(meses_totais / 12, 1),
        "valor_final_atingido": round(valor_atual, 2),
        "resumo_anual": resumo_anual
    }