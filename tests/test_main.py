import pytest
from src.app.main import calcular_idade


def test_calcular_idade_valida():
    assert calcular_idade(2000, 2026) == 26


def test_calcular_idade_futura_lanca_excecao():
    with pytest.raises(ValueError, match="futuro"):
        calcular_idade(2030, 2025)