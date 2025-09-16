from datetime import datetime
from enum import Enum, auto
from typing import Optional
from transitions import Machine
from smart_home.core.logger import Logger
from smart_home.dispositivos.base import Dispositivo

class EstadoPorta(Enum):
    TRANCADA = auto()
    DESTRANCADA = auto()
    ABERTA = auto()

TRANSICOES = [
    {"trigger": "trancar", "source": EstadoPorta.DESTRANCADA.name, "dest": EstadoPorta.TRANCADA.name},
    {"trigger": "trancar", "source": EstadoPorta.ABERTA.name, "dest": EstadoPorta.ABERTA.name, "after": "aviso_trancar_aberta"},
    {"trigger": "destrancar", "source": EstadoPorta.TRANCADA.name, "dest": EstadoPorta.DESTRANCADA.name},
    {"trigger": "abrir", "source": EstadoPorta.DESTRANCADA.name, "dest": EstadoPorta.ABERTA.name},
    {"trigger": "fechar", "source": EstadoPorta.ABERTA.name, "dest": EstadoPorta.DESTRANCADA.name},
]

class Porta(Dispositivo):

    def __init__(self, nome, estado = EstadoPorta.TRANCADA):
        super().__init__(nome, estado, tipo = 'Porta')
        self.__tentativas_invalidas = 0

        self.machine = Machine(
            model=self,
            states=[estado.name for estado in EstadoPorta],
            transitions=TRANSICOES,
            initial=estado.name,
            send_event=True,
            after_state_change="atualizar_log"
        )

        self.atualizar_log()

    def on_enter_TRANCADA(self, event):
        print(f"A porta {self.nome} foi trancada.")
        self.atualizar_log(event)
        self.notificar_observadores(**self.logger.to_dict())
    
    def on_enter_DESTRANCADA(self, event):
        print(f"A porta {self.nome} foi destrancada.")
        self.atualizar_log(event)
        self.notificar_observadores(**self.logger.to_dict())
    
    def on_enter_ABERTA(self, event):
        print(f"A porta {self.nome} foi aberta.")
        self.atualizar_log(event)
        self.notificar_observadores(**self.logger.to_dict())

    def estado(self,valor):
        if not isinstance(valor, EstadoPorta):
            raise ValueError('Estado inválido para a porta, verifique suas opções.')
        
    def aviso_trancar_aberta(self, event):
        self.__tentativas_invalidas += 1
        print("Não é possível trancar pois a porta está aberta!")
    
    def atualizar_log(self, event: Optional[object] = None):

        self.logger = Logger(

            timestamp= datetime.today(),
            dispositivo= self.nome,
            evento= event.event.name if event else None,
            estado_origem= EstadoPorta[event.transition.source] if event else None,
            estado_destino= EstadoPorta[event.transition.dest] if event else None,
            id_dispositivo= self.nome,
            total_wh= 12,
            inicio_periodo=datetime.today(),
            fim_periodo=datetime.today(),
        )

if __name__ == "__main__":
    from smart_home.core.observers import LogEventosHub, LogRelatoriosHub

    eve = LogEventosHub()
    rel = LogRelatoriosHub()

    porta = Porta("Porta da Frente", EstadoPorta.TRANCADA)
    porta.adicionar_observador(eve, rel)
    porta.destrancar()
    porta.abrir()
    porta.trancar()  # Tentativa inválida, pois a porta está aberta
    porta.fechar()
    porta.trancar()  # Agora é válido, pois a porta está fechada