from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from src.app.main import app

client = TestClient(app)

def test_buscar_voos_sem_chave_api(monkeypatch):
    monkeypatch.delenv("SERPAPI_KEY", raising=False)
    monkeypatch.setenv("SERPAPI_KEY", "")
    
    response = client.get("/api/voos?origem=POA&destino=GRU&data_ida=2026-10-15")
    assert response.status_code == 500
    assert "SERPAPI_KEY não configurada" in response.json()["detail"]

@patch("src.app.main.GoogleSearch")
def test_buscar_voos_com_sucesso(mock_google_search, monkeypatch):
    monkeypatch.setenv("SERPAPI_KEY", "chave_de_teste_fake")
    
    # Configura o mock da instância retornada por GoogleSearch(params)
    mock_instance = MagicMock()
    mock_instance.get_dict.return_value = {
        "best_flights": [
            {
                "price": 450,
                "total_duration": 100,
                "flights": [
                    {"airline": "LATAM", "flight_number": "LA3000"}
                ]
            }
        ]
    }
    mock_google_search.return_value = mock_instance

    response = client.get("/api/voos?origem=POA&destino=GRU&data_ida=2026-10-15")
    
    assert response.status_code == 200
    data = response.json()
    assert data["origem"] == "POA"
    assert data["destino"] == "GRU"
    assert len(data["voos"]) == 1
    assert data["voos"][0]["companhia"] == "LATAM"
    assert data["voos"][0]["preco"] == 450