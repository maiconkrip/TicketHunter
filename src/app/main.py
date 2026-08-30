def calcular_idade(ano_nascimento: int, ano_atual: int = 2026) -> int:
    """Calcula a idade com base no ano de nascimento."""
    return ano_atual - ano_nascimento


def run() -> None:
    try:
        ano = int(input("Digite o ano do seu nascimento: "))
        idade = calcular_idade(ano)
        print(f"Sua idade é: {idade} anos.")
    except ValueError:
        print("Por favor, digite um ano válido.")


if __name__ == "__main__":
    run()