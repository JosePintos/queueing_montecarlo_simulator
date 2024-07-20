import copy
import random
import math
from classes import Reparador, Aparato

# estados aparato: SR (siendo reparado), ER (esperando reparacion)
# estados reaparador: libre, ocupado


# Convertir minutos/horas
def min_to_hours(minutes: float) -> float:
    return minutes / 60


def hours_to_min(hours: float) -> float:
    return


# Manejar next event y tiempos
tiempos_eventos = {
    "llegada aparato": 0,
    "fin reparacion 1": 999,
    "fin reparacion 2": 999,
    "fin reparacion 3": 999,
}


def setNewTime(current_event: str, new_time: float) -> None:
    tiempos_eventos[current_event] = new_time


def getNextEvent() -> str:
    return min(tiempos_eventos, key=tiempos_eventos.get)


# calcular nuevo tiempo de evento
def calcularNuevoTiempo(evento: str) -> float:
    if evento == "llegada aparato":
        return Aparato.llegadaAparato()
    else:
        return Reparador.finReparacion()


# funcion responsable de actualizar el vector estado
def actualizarEstado(result: list) -> None:
    """
    1. actualizar evento
        a. get min time
        b. setear el tiempo siguiente del evento que acaba de suceder (param) y mostrar en tabla
        c. actualizar current min
    2. crear objeto cliente si es necesario
        a. contar tiempo de espera
    3. cambiar estados de objetos temp y perm si correpsonde
    4. actualizar cola si es necesario
    5. calcular cobro y acumularlo
    """
    current_minimo = getNextEvent()
    VECTOR_ESTADO["hora"] += tiempos_eventos[current_minimo]

    evento = current_minimo
    VECTOR_ESTADO["evento"] = evento
    setNewTime(current_event=evento, new_time=calcularNuevoTiempo(evento=evento))
    current_minimo = getNextEvent()

    cola = VECTOR_ESTADO["cola"]
    reparadores = VECTOR_ESTADO["reparadores"]
    aparatos = VECTOR_ESTADO["aparatos"]
    if evento == "llegada aparato":
        if reparadores["r1"] == "libre":
            estado_aparato = "SR 1"
            reparadores["r1"] = "ocupado"
        elif reparadores["r2"] == "libre":
            estado_aparato = "SR 2"
            reparadores["r2"] = "ocupado"
        elif reparadores["r3"] == "libre":
            estado_aparato = "SR 3"
            reparadores["r3"] = "ocupado"
        else:
            estado_aparato = "ER"
            Reparador.incrementCola()
        nuevo_aparato = Aparato(
            estado=estado_aparato, tiempo_llegada=VECTOR_ESTADO["hora"]
        )
        aparatos[nuevo_aparato.id] = [
            nuevo_aparato.estado,
            nuevo_aparato.tiempo_llegada,
        ]

    if evento.startswith("fin reparacion"):
        aparato_reparado_key = [
            list(aparatos.values()).index(f"SR {evento[len(evento)]}")
        ]
        VECTOR_ESTADO["monto cobro"] = 0
        if not aparatos[aparato_reparado_key].esGratis(
            tiempo_fin=VECTOR_ESTADO["hora"]
        ):
            VECTOR_ESTADO["monto cobro"] = Reparador.montoACobrar()
        del aparatos[aparato_reparado_key]

        if cola > 0:
            Reparador.decrementCola()
            next_aparato_in_line = min(
                aparatos.values(), key=lambda p: p.tiempo_llegada, default=None
            )
            aparatos[next_aparato_in_line] = f"SR {evento[len(evento)]}"
        else:
            reparadores[f"r{evento[len(evento)]}"] = "libre"

    result.append(copy.deepcopy(VECTOR_ESTADO))


############################

# init objetos permanentes
reparador1 = Reparador("libre")
reparador2 = Reparador("libre")
reparador3 = Reparador("libre")

# primer cliente que entra al sistema
media = 1 / 7  # reemplazar media por el input
aparato_1 = Aparato("SR", (-media * (math.log(1 - random.random()))))

# Inicializacion
# {Hora,Evento,(RND,Llegada Aparato),(RND,Fin Reparacion),(RND,Monto Cobro),[Reparadores],{Aparatos}}
VECTOR_ESTADO = {
    "hora": 0,
    "evento": "inicio",
    "llegada aparato": aparato_1.tiempo_llegada,
    "eventos": tiempos_eventos,
    "monto cobro": 0,
    "reparadores": {
        "r1": reparador1.estado,
        "r2": reparador2.estado,
        "r3": reparador3.estado,
    },
    "cola": Reparador.getCola(),
    "aparatos": {aparato_1.id: [aparato_1.estado, aparato_1.tiempo_llegada]},
}


def runSimulation(
    horasASimular: float,
    media: float = None,
    minPrecio: float = None,
    maxPrecio: float = None,
    minTiempo: float = None,
    maxTiempo: float = None,
):
    result = []
    while VECTOR_ESTADO["hora"] < horasASimular:
        actualizarEstado(result=result)
    return result
