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
        "id": vector_estado["hora"],
        "evento": vector_estado["evento"],
        "llegada_aparato": vector_estado["eventos"]["llegada aparato"],
        "fin_reparacion_1": vector_estado["eventos"]["fin reparacion 1"],
        "fin_reparacion_2": vector_estado["eventos"]["fin reparacion 2"],
        "fin_reparacion_3": vector_estado["eventos"]["fin reparacion 3"],
        "monto_cobro": vector_estado["monto cobro"],
        "reparador_1": vector_estado["reparadores"]["r1"].estado,
        "reparador_2": vector_estado["reparadores"]["r2"].estado,
        "reparador_3": vector_estado["reparadores"]["r3"].estado,
        "cola": vector_estado["cola"],
        "aparatos": [
            [val.estado, val.tiempo_llegada]
            for key, val in vector_estado["aparatos"].items()
        ],
    }

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
    setNewTime(current_event="llegada aparato", new_time=tiempo_llegada)
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
    VECTOR_ESTADO.update(valores_iniciales)

    formatResult(vector_estado=copy.deepcopy(VECTOR_ESTADO), result=result)


###############################


# Convertir minutos/horas
def min_to_hours(minutes: float) -> float:
    return minutes / 60


def hours_to_min(hours: float) -> float:
    return


# Manejar next event y tiempos
tiempos_eventos = {
    "llegada aparato": 999,
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


#########################################
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
    #    breakpoint()
    VECTOR_ESTADO["hora"] = tiempos_eventos[getNextEvent()]
    evento = getNextEvent()
    VECTOR_ESTADO["evento"] = evento

    cola = len(Reparador.getCola())
    reparadores = VECTOR_ESTADO["reparadores"]
    aparatos = VECTOR_ESTADO["aparatos"]

    if evento == "llegada aparato":
        setNewTime(
            current_event=evento,
            new_time=calcularNuevoTiempo(evento=evento) + VECTOR_ESTADO["hora"],
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
                current_event="fin reparacion 1",
                new_time=calcularNuevoTiempo(evento="fin reparacion 1")
                + VECTOR_ESTADO["hora"],
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
                current_event="fin reparacion 2",
                new_time=calcularNuevoTiempo(evento="fin reparacion 2")
                + VECTOR_ESTADO["hora"],
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
                current_event="fin reparacion 3",
                new_time=calcularNuevoTiempo(evento="fin reparacion 3")
                + VECTOR_ESTADO["hora"],
            )
        else:
            nuevo_aparato = Aparato(
                estado="ER",
                tiempo_llegada=VECTOR_ESTADO["hora"],
                posicionEnCola=Reparador.getCola(),
            )
            Reparador.incrementCola(nuevo_aparato)

        aparatos[nuevo_aparato.id] = nuevo_aparato

    else:  # el evento es de fin reparacion
        # breakpoint()
        setNewTime(
            current_event=evento,
            new_time=999,
        )
        VECTOR_ESTADO["monto cobro"] = 0
        aparato_reparado_key = reparadores[f"r{evento[len(evento)-1]}"].idAparato

        if not aparatos[aparato_reparado_key].esGratis(
            tiempo_fin=VECTOR_ESTADO["hora"]
        ):
            VECTOR_ESTADO["monto cobro"] += Reparador.montoACobrar()
        # del aparatos[aparato_reparado_key]
        aparatos[aparato_reparado_key].estado = "FIN"
        if cola > 0:
            Reparador.decrementCola()
            next_aparato_in_line = min(
                aparatos.values(), key=lambda p: p.tiempo_llegada
            )

            setNewTime(
                current_event=f"fin reparacion {evento[len(evento)-1]}",
                new_time=calcularNuevoTiempo(
                    evento=f"fin reparacion {evento[len(evento)-1]}"
                )
                + VECTOR_ESTADO["hora"],
            )
            aparatos[next_aparato_in_line.id].estado = f"SR {evento[len(evento)-1]}"
        else:
            reparadores[f"r{evento[len(evento)-1]}"].estado = "libre"
            reparadores[f"r{evento[len(evento)-1]}"].idAparato = None

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
    init_simulation(result=result)
    while VECTOR_ESTADO["hora"] < horasASimular:
        actualizarEstado(result=result)
    return result


if __name__ == "__main__":
    print(runSimulation(horasASimular=2))
