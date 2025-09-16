from asyncio import sleep
from datetime import datetime, timedelta
from enum import Enum, auto
from transitions import Machine
from smart_home.core.observers import LogEventosHub, LogRelatoriosHub
from smart_home.core.logger import Logger
from smart_home.dispositivos.base import Dispositivo
from smart_home.dispositivos.luz import CorLuz

class EstadoTomada(Enum):
    ON = auto()
    OFF = auto()

TRANSICOES_TOMADA = [
    {"trigger": "ligar", "source": EstadoTomada.OFF.name, "dest": EstadoTomada.ON.name},
    {"trigger": "desligar", "source": EstadoTomada.ON.name, "dest": EstadoTomada.OFF.name},
]

class Tomada(Dispositivo):

    def __init__(self, nome, estado=EstadoTomada.OFF, potencia_w: int = 0):
        super().__init__(nome, estado)

        # validar potência
        if not isinstance(potencia_w, int) or potencia_w < 0:
            raise ValueError("Potência deve ser um inteiro maior ou igual a 0.")
        self._potencia_w = potencia_w

        # métricas
        self._consumo_wh = 0.0
        self._momento_ligou: datetime | None = None

        #Inicializar logger
        self.logger = Logger(
            dispositivo=self.nome,
            id_dispositivo=self.nome,
            evento=None,
            estado_origem=None,
            estado_destino=None,
            inicio_periodo=None,
            fim_periodo=None,
            total_wh=None
        )
        # inicializar máquina de estados
        self.machine = Machine(
            model=self,
            states=[estado.name for estado in EstadoTomada],
            transitions=TRANSICOES_TOMADA,
            initial=EstadoTomada.OFF.name,
            auto_transitions=False,
            send_event=True,
            after_state_change="atualizar_log"
        )

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
    
    def on_enter_ON(self, event):
        """Ao ligar, registra o momento."""
        self._momento_ligou = datetime.now()
        
        #atualizar o self.logger diretamente aqui
        self.logger.timestamp = datetime.now()
        self.logger.id_dispositivo = self.nome
        self.logger.evento = 'LIGAR'
        self.logger.estado_origem = EstadoTomada[event.transition.source]
        self.logger.total_wh = self.consumo_wh
        self.logger.inicio_periodo = datetime.today()

        self.notificar_observadores(**self.logger.to_dict())
    
    def on_exit_ON(self, event):
        """Ao desligar, acumula o consumo até aqui."""
        if self._momento_ligou:
            tempo_h = (datetime.now() - self._momento_ligou).total_seconds() / 3600
            self._consumo_wh += self._potencia_w * tempo_h
            self._momento_ligou = None
        
        #atualizar o self.logger diretamente aqui
        self.logger.id_dispositivo = self.nome
        self.logger.estado_origem = EstadoTomada[event.transition.source]
        self.logger.estado_destino = EstadoTomada[event.transition.dest]
        self.logger.timestamp = datetime.now()
        self.logger.total_wh = self.consumo_wh
        self.logger.fim_periodo = datetime.today()
        self.notificar_observadores(**self.logger.to_dict())
    

    # --- estado ---
    def estado(self, valor):
        if not isinstance(valor, EstadoTomada):
            raise ValueError("Estado inválido: deve ser uma instância de EstadoTomada")
        self.estado = valor

    def atualizar_log(self, event=None):
        self.logger.dispositivo = self.nome
        self.logger.evento = event.event.name if event else None
        self.logger.estado_origem = EstadoTomada[event.transition.source] if event else None
        self.logger.estado_destino = EstadoTomada[event.transition.dest] if event else None
        self.logger.inicio_periodo = datetime.today()
        self.logger.fim_periodo = datetime.combine(datetime.today(), datetime.min.time()) + timedelta(days=1)
        self.logger.total_wh = None


if __name__ == "__main__":
    tom = Tomada(nome='Tomada de tv sala', estado=EstadoTomada.OFF, potencia_w=40)
    eve = LogEventosHub()
    rel = LogRelatoriosHub()
    tom.adicionar_observador(eve, rel)
    tom.potencia_w = 80
    tom.ligar()
    sleep(10)  # Simula 10 segundos ligado
    tom.desligar()

