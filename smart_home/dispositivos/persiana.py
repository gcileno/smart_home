from datetime import datetime
from enum import Enum, auto
from typing import Optional
from transitions import Machine
from smart_home.core.logger import Logger
from smart_home.core.observers import LogEventosHub, LogRelatoriosHub
from smart_home.dispositivos.base import Dispositivo

class LuminosidadePersiana(Enum):
    CLARO = auto()
    MEDIA = auto()
    ESCURA = auto()

class EstadoPersiana(Enum):
    ABERTA = auto()
    FECHADA = auto()

# Máquina de estados para a persiana
TRANSITIONS = [
    {'trigger': 'abrir', 'source': 'FECHADA', 'dest': 'ABERTA'},
    {'trigger': 'fechar', 'source': 'ABERTA', 'dest': 'FECHADA'}
]

class Persiana(Dispositivo):

    def __init__(self, nome, estado=EstadoPersiana.FECHADA, luminosidade=LuminosidadePersiana.ESCURA):
        super().__init__(nome, estado)
        self.luminosidade = luminosidade

        # Máquina de estados
        self.machine = Machine(
            model=self,
            states= [estado.name for estado in EstadoPersiana],
            transitions=TRANSITIONS,
            initial=estado.name,
            send_event=True,
            after_state_change='atualizar_log'
        )
        self.atualizar_log()

    def on_enter_ABERTA(self, event):
        print(f"A Persiana {self.nome} está agora ABERTA.")
        self.atualizar_log(event)
        self.notificar_observadores(**self.logger.to_dict())
    
    def on_enter_FECHADA(self, event):
        print(f"A Persianas {self.nome} está agora FECHADA.")
        self.atualizar_log(event)
        self.notificar_observadores(**self.logger.to_dict())

    # Método para alterar luminosidade
    def set_luminosidade(self, valor: LuminosidadePersiana):

        if not isinstance(valor, LuminosidadePersiana):
            raise ValueError("Valor deve ser da classe LuminosidadePersiana.")
        
        self.logger.estado_destino = valor.name
        self.logger.estado_origem = self.luminosidade
        self.logger.fim_periodo = datetime.today()

        self.luminosidade = valor
        self.notificar_observadores(**self.logger.to_dict())


        # --- Logger de eventos ---
    def atualizar_log(self, event: Optional[object] = None):

        self.logger = Logger(

            timestamp= datetime.today(),
            dispositivo= self.nome,
            evento= event.event.name if event else None,
            estado_origem= event.transition.source if event else None,
            estado_destino= event.transition.dest if event else None,
            id_dispositivo= self.nome,
            total_wh= 12,
            inicio_periodo=datetime.today(),
            fim_periodo=datetime.today(),
        )
    
    def estado(self, valor):
        if not isinstance(valor, EstadoPersiana):
            raise ValueError("Estado deve ser da classe EstadoPersiana.")
        self.to_estado(valor.name)
        self.notificar_observadores(event=None)

if __name__ == "__main__":
    # Criar persiana iniciando fechada e com luminosidade escura
    p = Persiana(nome="Sala", estado=EstadoPersiana.FECHADA)
    eve = LogEventosHub()
    rel = LogRelatoriosHub()

    p.adicionar_observador(eve,rel)
    # Testar abrir/fechar
    p.abrir()
    p.fechar()

    # Testar luminosidade
    p.abrir()
    p.set_luminosidade(LuminosidadePersiana.CLARO)
    p.set_luminosidade(LuminosidadePersiana.ESCURA)
