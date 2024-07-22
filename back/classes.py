import random
import math


class Aparato:
    _last_id = 0

    def __init__(
        self,
        estado: str,
        tiempo_llegada: float,
        idReparador: int = None,
        posicionEnCola: int = None,
    ) -> None:
        Aparato._last_id += 1
        self._id = Aparato._last_id
        self._estado = estado
        self._tiempo_llegada = tiempo_llegada
        self._idReparador = idReparador
        self._posicionEnCola = posicionEnCola

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

    @property
    def idReparador(self) -> int:
        return self._idReparador

    @idReparador.setter
    def idReparador(self, value: int) -> None:
        self._idReparador = value

    @property
    def posicionEnCola(self) -> int:
        return self._posicionEnCola

    @posicionEnCola.setter
    def idReparador(self, value: int) -> None:
        self._posicionEnCola = value

    # Calcular tiempo que espero el cliente
    def calcularTiempoDeEspera(self, tiempo_fin: float) -> float:
        return tiempo_fin - self._tiempo_llegada

    # Chequear precio
    def esGratis(self, tiempo_fin: float) -> bool:
        demora = self.calcularTiempoDeEspera(tiempo_fin)
        return True if demora > 0.5 else False

    # Calcular proxima llegada
    @staticmethod
    def llegadaAparato(media: float, rnd: float) -> float:
        media = 1 / 7 if not media else media
        return -media * (math.log(1 - rnd))


class Reparador:
    _lastId = 0
    _cola = []

    def __init__(self, estado: str, idAparato: int = None) -> None:
        Reparador._lastId += 1
        self._id = Reparador._lastId
        self._estado = estado
        self._idAparato = idAparato

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
    def idAparato(self) -> int:
        return self._idAparato

    @idAparato.setter
    def idAparato(self, value: int) -> None:
        self._idAparato = value

    @classmethod
    def getCola(cls):
        return cls._cola

    @classmethod
    def incrementCola(cls, aparato):
        cls._cola.append(aparato)

    @classmethod
    def decrementCola(cls):
        if cls._cola:
            cls._cola.pop(0)

    # Calcular cobro
    @staticmethod
    def montoACobrar(precio_min: float, precio_max: float, rnd: float) -> float:
        precio_min = 100 if not precio_min else precio_min
        precio_max = 400 if not precio_max else precio_max
        return (precio_min + (rnd * (precio_max - precio_min))) * 0.75

    # Calcular fin servicio
    @staticmethod
    def finReparacion(tiempo_min: float, tiempo_max: float, rnd: float) -> float:
        tiempo_min = 13 if not tiempo_min else tiempo_min
        tiempo_max = 17 if not tiempo_max else tiempo_max
        return (tiempo_min / 60) + (rnd * ((tiempo_max / 60) - (tiempo_min / 60)))
