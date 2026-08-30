import os
from dotenv import load_dotenv

load_dotenv()

ENVIRONMENT = os.getenv("ENVIRONMENT", "DEV")


def calcular_idade(ano_nascimento: int, ano_atual: int = 2026) -> int:
    """Calcula a idade com base no ano de nascimento."""
    if ano_nascimento > ano_atual:
        raise ValueError("O ano de nascimento não pode ser no futuro.")
    return ano_atual - ano_nascimento

def calcular_idade2(ano_nascimento: int, ano_atual: int = 2026) -> int:
    """Calcula a idade com base no ano de nascimento."""
    if ano_nascimento >= ano_atual:
        raise ValueError("O ano de nascimento não pode ser no futuro.")
    return ano_atual - ano_nascimento


def run() -> None:
    print(f"--- Iniciando TicketHunter [Ambiente: {ENVIRONMENT}] ---")
    try:
        ano = int(input("Digite o ano do seu nascimento: "))
        idade = calcular_idade(ano)
        print(f"Sua idade é: {idade} anos.")
    except ValueError as e:
        print(f"Erro desconhecido: {e}")

def converter_ano_para_texto(ano: int) -> str:
    """Converte o ano de nascimento para representação textual."""
    if not isinstance(ano, int):
        raise TypeError("O ano deve ser um número inteiro.")
    return f"Ano de nascimento registrado: {ano}"

if __name__ == "__main__":
    run()