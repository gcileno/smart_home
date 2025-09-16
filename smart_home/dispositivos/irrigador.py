from asyncio import sleep
from datetime import datetime, timedelta
from enum import Enum, auto
from transitions import Machine
from smart_home.core.observers import LogEventosHub, LogRelatoriosHub
from smart_home.core.logger import Logger
from smart_home.dispositivos.base import Dispositivo

class EstadoIrrigador(Enum):
    ON = auto()
    OFF = auto()
    IRRIGANDO = auto()

TRANSICOES_IRRIGADOR = [
        {"trigger": "ligar", "source": EstadoIrrigador.OFF.name, "dest": EstadoIrrigador.ON.name},
        {"trigger": "desligar", "source": EstadoIrrigador.ON.name, "dest": EstadoIrrigador.OFF.name},
        {"trigger": "iniciar_irrigacao", "source": EstadoIrrigador.ON.name, "dest": EstadoIrrigador.IRRIGANDO.name},
        {"trigger": "parar_irrigacao", "source": EstadoIrrigador.IRRIGANDO.name, "dest": EstadoIrrigador.ON.name}
    ]

class Irrigador(Dispositivo):
    def __init__(self, nome, estado = EstadoIrrigador.OFF):
        super().__init__(nome, estado, tipo = "Irrigador")

        self.machine = Machine(
            model=self,
            states=[estado.name for estado in EstadoIrrigador],
            transitions=TRANSICOES_IRRIGADOR,
            initial=self.estado.name,
            send_event=True,
            after_state_change="atualizar_log"
        )
    
    def estado(self, valor):
        if not isinstance(valor, EstadoIrrigador):
            raise ValueError("Estado inválido: deve ser uma instância de EstadoIrrigador")

        self._estado = valor
    
    def on_enter_IRRIGANDO(self, event):
        print(f"{self.nome} iniciou a irrigação.")
        self.atualizar_log(event)
        self.notificar_observadores(**self.logger.to_dict())
    
    def on_exit_IRRIGANDO(self, event):
        print(f"{self.nome} parou a irrigação.")
        self.atualizar_log(event)
        self.notificar_observadores(**self.logger.to_dict())
    
    def on_enter_ON(self, event):
        print(f"{self.nome} está ligado.")
        self.atualizar_log(event)
        self.notificar_observadores(**self.logger.to_dict())

    def on_enter_OFF(self, event):
        print(f"{self.nome} está desligado.")
        self.atualizar_log(event)
        self.notificar_observadores(**self.logger.to_dict())

if __name__ == "__main__":
    irrigador = Irrigador("Irrigador Jardim", EstadoIrrigador.OFF)
    irrigador.adicionar_observador(LogEventosHub(), LogRelatoriosHub())

    irrigador.ligar()
    sleep(1)
    irrigador.iniciar_irrigacao()
    sleep(1)
    irrigador.parar_irrigacao()
    sleep(1)
    irrigador.desligar()
