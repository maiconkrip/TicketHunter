import os
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from serpapi import GoogleSearch
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="TicketHunter - Buscador de Voos")

# Permite requisições do front-end
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/voos")
def buscar_voos(
    origem: str = Query(..., description="Código IATA de origem, ex: POA"),
    destino: str = Query(..., description="Código IATA de destino, ex: GRU"),
    data_ida: str = Query(..., description="Data de ida no formato YYYY-MM-DD")
):
    """
    Busca opções de voos utilizando a SerpApi (Google Flights Engine).
    """
    # Consulta a chave no momento da requisição
    serpapi_key = os.getenv("SERPAPI_KEY")

    if not serpapi_key:
        raise HTTPException(
            status_code=500, 
            detail="SERPAPI_KEY não configurada no ambiente."
        )

    params = {
        "engine": "google_flights",
        "departure_id": origem.upper(),
        "arrival_id": destino.upper(),
        "outbound_date": data_ida,
        "currency": "BRL",
        "hl": "pt",
        "api_key": serpapi_key
    }

    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        
        # Filtra e extrai apenas os dados mais relevantes dos voos
        best_flights = results.get("best_flights", [])
        other_flights = results.get("other_flights", [])
        
        todos_voos = best_flights + other_flights
        
        voos_formatados = []
        for flight in todos_voos:
            first_segment = flight.get("flights", [])[0] if flight.get("flights") else {}
            voos_formatados.append({
                "companhia": first_segment.get("airline"),
                "numero_voo": first_segment.get("flight_number"),
                "preco": flight.get("price"),
                "duracao_total_minutos": flight.get("total_duration"),
                "escalas": len(flight.get("flights", [])) - 1
            })

        return {
            "origem": origem.upper(),
            "destino": destino.upper(),
            "data_ida": data_ida,
            "total_resultados": len(voos_formatados),
            "voos": voos_formatados
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar voos: {str(e)}")