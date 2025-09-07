from enum import Enum, auto
from base import Dispositivo

class EstadoPorta(Enum):
    TRANCADA = auto()
    DESTRANCADA = auto()
    ABERTA = auto()

TRANSICOES = [
    {"trigger": "trancar", "source": EstadoPorta.DESTRANCADA, "dest": EstadoPorta.TRANCADA},
    {"trigger": "trancar", "source": EstadoPorta.ABERTA, "dest": EstadoPorta.ABERTA, "after": "aviso_trancar_aberta"},
    {"trigger": "destrancar", "source": EstadoPorta.TRANCADA, "dest": EstadoPorta.DESTRANCADA},
    {"trigger": "abrir", "source": EstadoPorta.DESTRANCADA, "dest": EstadoPorta.ABERTA},
    {"trigger": "fechar", "source": EstadoPorta.ABERTA, "dest": EstadoPorta.DESTRANCADA},
]

class Porta(Dispositivo):

    def __init__(self, nome, estado = EstadoPorta.TRANCADA):
        super().__init__(nome, estado)
        self.__tentativas_invalidas = 0
    
    def aviso_trancar_aberta(self):
        self.__tentativas_invalidas += 1
        print("Não é possível trancar pois a porta está aberta!")