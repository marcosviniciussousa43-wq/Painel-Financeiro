# schemas.py
# Este arquivo define os "moldes" (schemas) de dados
# que nossa API vai receber (requests) ou enviar (responses).

from pydantic import BaseModel, Field

class ProjecaoRequest(BaseModel):
    """
    Define o molde de dados que o usuário DEVE enviar
    para o endpoint de projeção.
    """
    valor_inicial: float = Field(
        ..., # ... significa que é obrigatório
        gt=0, # "greater than" (maior que) 0
        description="O valor inicial do investimento."
    )
    aporte_mensal: float = Field(
        ...,
        ge=0, # "greater than or equal" (maior ou igual) a 0
        description="O valor do aporte mensal regular."
    )
    meses_por_ano_sem_aporte: int = Field(
        default=0, # Se não for enviado, o padrão é 0
        ge=0, # Mínimo 0
        le=11, # Máximo 11 (não pode pular os 12 meses)
        description="Quantos meses por ano o usuário planeja NÃO depositar (ex: férias)."
    )
    meta_financeira: float = Field(
        ...,
        gt=0,
        description="O valor final da meta a ser atingida."
    )

    # O Pydantic nos dá um validador de exemplo automático!
    class Config:
        json_schema_extra = {
            "example": {
                "valor_inicial": 6000,
                "aporte_mensal": 1000,
                "meses_por_ano_sem_aporte": 2, # Ex: Pula 2 meses (só aporta 10x)
                "meta_financeira": 1000000
            }
        }