import copy
import random
import math
from classes import Reparador, Aparato

# estados aparato: SR (siendo reparado), ER (esperando reparacion)
# estados reaparador: libre, ocupado
# {Hora,Evento,(RND,Llegada Aparato),(RND,Fin Reparacion),(RND,Monto Cobro),[Reparadores],{Aparatos}}
VECTOR_ESTADO = dict()


# Formatear resultados
def formatResult(vector_estado: dict, result: list) -> None:
    formatted = {
        "hora": float("{:.3f}".format(vector_estado["hora"])),
        "evento": vector_estado["evento"],
        "llegada_aparato": float(
            "{:.3f}".format(vector_estado["eventos"]["llegada aparato"])
        ),
        "fin_reparacion_1": float(
            "{:.3f}".format(vector_estado["eventos"]["fin reparacion 1"])
        ),
        "fin_reparacion_2": float(
            "{:.3f}".format(vector_estado["eventos"]["fin reparacion 2"])
        ),
        "fin_reparacion_3": float(
            "{:.3f}".format(vector_estado["eventos"]["fin reparacion 3"])
        ),
        "monto_cobro": float("{:.3f}".format(vector_estado["monto cobro"])),
        "reparador_1": vector_estado["reparadores"]["r1"].estado,
        "reparador_2": vector_estado["reparadores"]["r2"].estado,
        "reparador_3": vector_estado["reparadores"]["r3"].estado,
        "cola": vector_estado["cola"],
        # "aparatos": [
        #     [val.estado, val.tiempo_llegada]
        #     for key, val in vector_estado["aparatos"].items()
        # ],
        # "estado_aparato": [
        #     val.estado for key, val in vector_estado["aparatos"].items()
        # ],
        # "tiempo_llegada_aparato": [
        #     float("{:.3f}".format(val.tiempo_llegada))
        #     for key, val in vector_estado["aparatos"].items()
        # ],
    }

    for i, aparato in enumerate(vector_estado["aparatos"].values()):
        formatted[f"a{i}_estado"] = aparato.estado
        formatted[f"a{i}_tiempo llegada"] = float(
            "{:.3f}".format(aparato.tiempo_llegada)
        )

    result.append(formatted)


############################
# Inicializacion


def init_simulation(result: list) -> None:
    # init objetos permanentes
    reparador1 = Reparador("libre")
    reparador2 = Reparador("libre")
    reparador3 = Reparador("libre")

    # calcular tiempo de llegada de primer aparato
    tiempo_llegada = calcularNuevoTiempo(evento="llegada aparato")
    tiempos_eventos = {
        "llegada aparato": tiempo_llegada,
        "fin reparacion 1": 999,
        "fin reparacion 2": 999,
        "fin reparacion 3": 999,
    }

    valores_iniciales = {
        "hora": 0,
        "evento": "inicio",
        "eventos": tiempos_eventos,
        "monto cobro": 0,
        "reparadores": {
            "r1": reparador1,
            "r2": reparador2,
            "r3": reparador3,
        },
        "cola": 0,
        "aparatos": {},
    }
    VECTOR_ESTADO = copy.deepcopy(valores_iniciales)
    formatResult(vector_estado=VECTOR_ESTADO, result=result)
    return VECTOR_ESTADO


###############################


# Convertir minutos/horas
def min_to_hours(minutes: float) -> float:
    return minutes / 60


def hours_to_min(hours: float) -> float:
    return


# Manejar paso de eventos
def setNewTime(tiempos_eventos: dict, current_event: str, new_time: float) -> None:
    tiempos_eventos[current_event] = new_time


def getNextEvent(tiempos_eventos: dict) -> str:
    return min(
        (event for event in tiempos_eventos if tiempos_eventos[event] is not None),
        key=tiempos_eventos.get,
    )


# calcular nuevo tiempo de evento
def calcularNuevoTiempo(evento: str) -> float:
    if evento == "llegada aparato":
        return Aparato.llegadaAparato()
    else:
        return Reparador.finReparacion()


#########################################
# funcion responsable de actualizar el vector estado
def actualizarEstado(VECTOR_ESTADO: dict, result: list) -> None:
    current_event = getNextEvent(VECTOR_ESTADO["eventos"])
    VECTOR_ESTADO["hora"] = VECTOR_ESTADO["eventos"][current_event]
    VECTOR_ESTADO["evento"] = current_event

    cola = len(Reparador.getCola())
    reparadores = VECTOR_ESTADO["reparadores"]
    aparatos = VECTOR_ESTADO["aparatos"]

    if current_event == "llegada aparato":
        setNewTime(
            VECTOR_ESTADO["eventos"],
            current_event,
            calcularNuevoTiempo(evento=current_event) + VECTOR_ESTADO["hora"],
        )
        if reparadores["r1"].estado == "libre":
            reparadores["r1"].estado = "ocupado"
            nuevo_aparato = Aparato(
                estado="SR 1",
                tiempo_llegada=VECTOR_ESTADO["hora"],
                idReparador=reparadores["r1"].id,
            )
            reparadores["r1"].idAparato = nuevo_aparato.id
            setNewTime(
                VECTOR_ESTADO["eventos"],
                "fin reparacion 1",
                calcularNuevoTiempo(evento="fin reparacion 1") + VECTOR_ESTADO["hora"],
            )
        elif reparadores["r2"].estado == "libre":
            reparadores["r2"].estado = "ocupado"
            nuevo_aparato = Aparato(
                estado="SR 2",
                tiempo_llegada=VECTOR_ESTADO["hora"],
                idReparador=reparadores["r2"].id,
            )
            reparadores["r2"].idAparato = nuevo_aparato.id
            setNewTime(
                VECTOR_ESTADO["eventos"],
                "fin reparacion 2",
                calcularNuevoTiempo(evento="fin reparacion 2") + VECTOR_ESTADO["hora"],
            )
        elif reparadores["r3"].estado == "libre":
            reparadores["r3"].estado = "ocupado"
            nuevo_aparato = Aparato(
                estado="SR 3",
                tiempo_llegada=VECTOR_ESTADO["hora"],
                idReparador=reparadores["r3"].id,
            )
            reparadores["r3"].idAparato = nuevo_aparato.id
            setNewTime(
                VECTOR_ESTADO["eventos"],
                "fin reparacion 3",
                calcularNuevoTiempo(evento="fin reparacion 3") + VECTOR_ESTADO["hora"],
            )
        else:
            nuevo_aparato = Aparato(
                estado="ER",
                tiempo_llegada=VECTOR_ESTADO["hora"],
                posicionEnCola=Reparador.getCola(),
            )
            Reparador.incrementCola(nuevo_aparato)

        aparatos[nuevo_aparato.id] = nuevo_aparato
    else:
        setNewTime(VECTOR_ESTADO["eventos"], current_event, 999)
        reparador_id = current_event[-1]
        aparato_reparado_key = reparadores[f"r{reparador_id}"].idAparato

        if not aparatos[aparato_reparado_key].esGratis(
            tiempo_fin=VECTOR_ESTADO["hora"]
        ):
            VECTOR_ESTADO["monto cobro"] += Reparador.montoACobrar()
        aparatos[aparato_reparado_key].estado = "FIN"

        if cola > 0:
            Reparador.decrementCola()
            next_aparato_in_line = min(
                (aparato for aparato in aparatos.values() if aparato.estado == "ER"),
                key=lambda p: p.tiempo_llegada,
            )
            reparadores[f"r{reparador_id}"].idAparato = next_aparato_in_line.id
            aparatos[next_aparato_in_line.id].estado = f"SR {reparador_id}"
            setNewTime(
                VECTOR_ESTADO["eventos"],
                f"fin reparacion {reparador_id}",
                calcularNuevoTiempo(evento=f"fin reparacion {reparador_id}")
                + VECTOR_ESTADO["hora"],
            )
        else:
            reparadores[f"r{reparador_id}"].estado = "libre"
            reparadores[f"r{reparador_id}"].idAparato = None

    VECTOR_ESTADO["cola"] = len(Reparador.getCola())
    formatResult(vector_estado=copy.deepcopy(VECTOR_ESTADO), result=result)


def runSimulation(
    horasASimular: float,
    media: float = None,
    minPrecio: float = None,
    maxPrecio: float = None,
    minTiempo: float = None,
    maxTiempo: float = None,
):
    result = []
    VECTOR_ESTADO = init_simulation(result=result)
    while VECTOR_ESTADO["hora"] < horasASimular:
        actualizarEstado(VECTOR_ESTADO=VECTOR_ESTADO, result=result)
    return result


if __name__ == "__main__":
    print(runSimulation(horasASimular=2)[0:25])
