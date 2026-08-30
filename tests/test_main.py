from src.app.main import calcular_idade


def test_calcular_idade():
    assert calcular_idade(2000, 2026) == 26