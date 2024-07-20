import random
import math


class Aparato:
    _last_id = 0

    def __init__(self, estado: str, tiempo_llegada: float) -> None:
        Aparato._last_id += 1
        self._id = Aparato._last_id
        self._estado = estado
        self._tiempo_llegada = tiempo_llegada

    @property
    def id(self) -> int:
        return self._id

    @property
    def estado(self) -> str:
        return self._estado

    @estado.setter
    def estado(self, value: str) -> None:
        self._estado = value

    @property
    def tiempo_llegada(self) -> float:
        return self._tiempo_llegada

    @tiempo_llegada.setter
    def tiempo_llegada(self, value: str) -> None:
        self._tiempo_llegada = value

    # Calcular tiempo que espero el cliente
    def calcularTiempoDeEspera(self, tiempo_fin: float) -> float:
        return tiempo_fin - self._tiempo_llegada

    # Chequear precio
    def esGratis(self, tiempo_fin: float) -> bool:
        demora = self.calcularTiempoDeEspera(tiempo_fin)
        return True if demora > 30 else False

    # Calcular proxima llegada
    @staticmethod
    def llegadaAparato(media: float = 1 / 7) -> float:
        rnd = random.random()
        return -media * (math.log(1 - rnd))


class Reparador:
    _lastId = 0
    _cola = 0

    def __init__(self, estado: str) -> None:
        Reparador._lastId += 1
        self._id = Reparador._lastId
        self._estado = estado

    @property
    def estado(self) -> str:
        return self._estado

    @estado.setter
    def estado(self, value: str) -> None:
        self._estado = value

    @staticmethod
    def getCola():
        return Reparador._cola

    @staticmethod
    def incrementCola():
        Reparador._cola += 1

    @staticmethod
    def decrementCola():
        Reparador._cola -= 1

    # Calcular cobro
    @staticmethod
    def montoACobrar(precio_min: float = 100, precio_max: float = 400) -> float:
        rnd = random.random()
        return (precio_min + (rnd * (precio_max - precio_min))) * 0.75

    # Calcular fin servicio
    @staticmethod
    def finReparacion(
        tiempo_min: float = 13 / 60, tiempo_max: float = 17 / 60
    ) -> float:
        rnd = random.random()
        return tiempo_min + (rnd * (tiempo_max - tiempo_min))
