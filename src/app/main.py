import os
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import serpapi
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="TicketHunter - Buscador de Voos")

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
    serpapi_key = os.getenv("SERPAPI_KEY")

    if not serpapi_key:
        raise HTTPException(
            status_code=500, 
            detail="SERPAPI_KEY não configurada no ambiente."
        )

    try:
        # Inicializa o cliente oficial da SerpApi
        client = serpapi.Client(api_key=serpapi_key)

        results = client.search({
            "engine": "google_flights",
            "departure_id": origem.upper(),
            "arrival_id": destino.upper(),
            "outbound_date": data_ida,
            "currency": "BRL",
            "hl": "pt",
            "gl": "br",
            "type": "2"  # 2 para voos só de ida (One-way)
        })

        if "error" in results:
            raise HTTPException(status_code=400, detail=f"Erro SerpApi: {results['error']}")

        # Coleta das chaves retornadas pelo client.search()
        best_flights = results.get("best_flights", [])
        other_flights = results.get("other_flights", [])
        
        todos_voos = best_flights + other_flights

        voos_formatados = []
        for flight in todos_voos:
            flights_list = flight.get("flights", [])
            first_segment = flights_list[0] if flights_list else {}
            
            voos_formatados.append({
                "companhia": first_segment.get("airline", "N/A"),
                "numero_voo": first_segment.get("flight_number", "N/A"),
                "preco": flight.get("price"),
                "duracao_total_minutos": flight.get("total_duration"),
                "escalas": max(0, len(flights_list) - 1)
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