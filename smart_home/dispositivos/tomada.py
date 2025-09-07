from datetime import datetime
from enum import Enum, auto
from base import Dispositivo

class EstadoTomada(Enum):
    ON = auto()
    OFF = auto()

TRANSICOES = [
    #{"trigger": "trancar", "source": EstadoPorta.DESTRANCADA, "dest": EstadoPorta.TRANCADA},
]

class Tomada(Dispositivo):
    def __init__(self, nome, potencia_w: int, estado=EstadoTomada.OFF):
        super().__init__(nome, estado)

        # valida potência
        if not isinstance(potencia_w, int) or potencia_w < 0:
            raise ValueError("Potência deve ser um inteiro maior ou igual a 0.")
        self._potencia_w = potencia_w

        # métricas
        self._consumo_wh = 0.0
        self._momento_ligou: datetime | None = None

    # --- potencia_w ---
    @property
    def potencia_w(self) -> int:
        return self._potencia_w

    @potencia_w.setter
    def potencia_w(self, valor: int):
        if not isinstance(valor, int) or valor < 0:
            raise ValueError("Potência deve ser um inteiro maior ou igual a 0.")
        self._potencia_w = valor

    # --- consumo_wh ---
    @property
    def consumo_wh(self) -> float:
        """Retorna o consumo acumulado (Wh)."""
        # se estiver ligado, contabiliza até o momento atual
        if self.estado == EstadoTomada.ON and self._momento_ligou:
            tempo_h = (datetime.now() - self._momento_ligou).total_seconds() / 3600
            return self._consumo_wh + (self._potencia_w * tempo_h)
        return self._consumo_wh

    # --- estado ---
    @Dispositivo.estado.setter
    def estado(self, valor):
        if not isinstance(valor, EstadoTomada):
            raise ValueError("Estado inválido: deve ser uma instância de EstadoTomada")

        # se desligar, acumula o consumo até aqui
        if self._estado == EstadoTomada.ON and valor == EstadoTomada.OFF:
            if self._momento_ligou:
                tempo_h = (datetime.now() - self._momento_ligou).total_seconds() / 3600
                self._consumo_wh += self._potencia_w * tempo_h
                self._momento_ligou = None

        # se ligar, registra o momento
        if self._estado == EstadoTomada.OFF and valor == EstadoTomada.ON:
            self._momento_ligou = datetime.now()

        self._estado = valor