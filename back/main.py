from fastapi import FastAPI
from typing import List, Union
from pydantic import BaseModel
from utils import runSimulation
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class VectorEstado(BaseModel):
    id: float
    evento: str
    llegada_aparato: float
    fin_reparacion_1: float
    fin_reparacion_2: float
    fin_reparacion_3: float
    monto_cobro: float
    reparador_1: str
    reparador_2: str
    reparador_3: str
    cola: int
    aparatos: List[List[Union[str, float]]]


@app.get("/simulacion", response_model=List[VectorEstado])
def read_vector_estado(offset: int = 0, limit: int = 10, horas: float = 1):
    return runSimulation(horasASimular=horas)[offset : offset + limit]
