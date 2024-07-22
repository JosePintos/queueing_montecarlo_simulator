import copy
from fastapi import FastAPI, Query, HTTPException
from typing import List, Union, Dict, Optional, Any
from pydantic import BaseModel
from utils import init_simulation, actualizarEstado
from fastapi.middleware.cors import CORSMiddleware
import uuid
import json


app = FastAPI()

# allow cors
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for simulation states
simulation_states = {}


# Function to generate a unique token
def generate_token():
    return str(uuid.uuid4())


# Model for the response
class SimulationResponse(BaseModel):
    total: int
    vectors: List[Dict[str, Any]]
    next_token: Optional[str] = None


@app.get("/simulacion", response_model=SimulationResponse)
def read_vector_estado(
    token: Optional[str] = Query(None),
    limit: int = Query(10),
    horas: float = Query(1.0),
) -> SimulationResponse:
    chunk_result = []
    if token:
        # Fetch the state using the token
        state = simulation_states.get(token)
        if not state:
            raise HTTPException(status_code=404, detail="Invalid token")
    else:
        # Initialize a new simulation state
        state = {
            "vector_estado": init_simulation(chunk_result),
            "result": [],
            "hora": 0,
            "total": 0,
        }
    # Generate the next chunk of results

    while state["hora"] < horas and len(chunk_result) < limit:
        actualizarEstado(VECTOR_ESTADO=state["vector_estado"], result=chunk_result)
        state["hora"] = state["vector_estado"]["hora"]
        state["total"] += 1

    # Generate a new token for the next request
    next_token = generate_token()
    simulation_states[next_token] = state

    # Return the current set of results and the next token
    return SimulationResponse(
        total=state["total"], vectors=chunk_result, next_token=next_token
    )
