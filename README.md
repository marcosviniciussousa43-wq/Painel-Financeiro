# Painel-Financeiro
Dashboard financeiro feito com Python (FastAPI) para analisar metas de longo prazo com dados reais da Selic e IPCA.
# 📊 Dashboard de Metas Financeiras

**Status do Projeto: Em Desenvolvimento (Work in Progress)**

## 🎯 Visão Geral

O **Dashboard de Metas Financeiras** é uma aplicação web pessoal projetada para rastrear, analisar e projetar o crescimento de patrimônio focado em metas de longo prazo, como a independência financeira ou atingir o primeiro milhão em investimentos.

Este projeto vai além de uma simples calculadora de juros compostos. O objetivo é criar um painel de controle que busca dados reais do mercado (como a taxa Selic e o IPCA) para fornecer uma visão clara do progresso e da rentabilidade real dos investimentos.

## 🚀 O Problema Resolvido

A maioria das ferramentas de investimento foca no curto prazo ou em cálculos isolados. Este dashboard resolve um problema pessoal e comum: "Com meus aportes atuais e o cenário econômico (juros vs. inflação), quando eu realmente atingirei minha meta financeira?"

Ele foi criado para ser um "mapa da jornada" para objetivos de longo prazo.

## 🛠️ Tecnologias Planejadas

Este projeto será construído utilizando um conjunto de tecnologias modernas para garantir uma base robusta e escalável:

* **Backend:** Python
    * **Framework API:** FastAPI (preferencial) ou Flask (para criar a lógica de negócios e os endpoints de dados).
* **Frontend:** HTML5, CSS3 e JavaScript (para criar a interface do usuário e os gráficos interativos).
* **Integrações (APIs):** API de Valores do Banco Central do Brasil (BCB) para buscar dados atualizados da Selic e do IPCA.
* **Banco de Dados (Planejado):** SQLite ou PostgreSQL (para armazenar o histórico de aportes e o cadastro de metas).

## 🗺️ Roadmap (Próximos Passos)

O desenvolvimento do projeto seguirá estes passos:

* [ ] **Fase 1: Core (Backend)**
    * [ ] Estruturar o projeto com FastAPI/Flask.
    * [ ] Criar os *endpoints* lógicos para o cálculo de juros compostos.
    * [ ] Integrar com a API do BCB para buscar a taxa Selic e o IPCA.
* [ ] **Fase 2: Interface (Frontend)**
    * [ ] Criar a tela inicial para cadastro de metas (Valor inicial, aportes, meta final).
    * [ ] Desenvolver os gráficos de projeção (Patrimônio vs. Tempo).
* [ ] **Fase 3: Funcionalidades Avançadas**
    * [ ] Implementar banco de dados para salvar o progresso.
    * [ ] Adicionar cálculo de "Rentabilidade Real" (descontando o IPCA).
