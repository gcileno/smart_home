from datetime import datetime
from enum import Enum, auto
from transitions import Machine

from smart_home.dispositivos.base import Dispositivo
from smart_home.core.logger import Logger
from smart_home.core.observers import LogEventosHub, LogRelatoriosHub

class CorLuz(Enum):
    QUENTE = auto()
    FRIA = auto()
    NEUTRA = auto()

class EstadoLuz(Enum):
    ON = auto()
    OFF = auto()

TRANSICOES_LUZ= [
        { 
            'trigger': 'ligar', 
            'source': EstadoLuz.OFF.name, 
            'dest' : EstadoLuz.ON.name,
        },
        {
            'trigger': 'desligar', 
            'source': EstadoLuz.ON.name, 
            'dest' : EstadoLuz.OFF.name,
            #'conditions' : ['luz_ligada'] 
        }
    ]

class Luz(Dispositivo):

    def __init__(self, nome, estado = EstadoLuz.OFF, cor = CorLuz.QUENTE, brilho: int = 60):
        super().__init__(nome, estado)
        self._brilho = brilho
        self._cor = cor

        self.machine = Machine(
            model= self,
            states= [estado.name for estado in EstadoLuz],
            transitions= TRANSICOES_LUZ,
            initial= self.estado.name,
            send_event=True,
            after_state_change = "atualizar_log"
        )

    @property
    def estado(self):
        return self._estado
    
    @estado.setter
    def estado(self, valor):
        if not isinstance(valor, EstadoLuz):
            raise ValueError("Estado inválido: deve ser uma instância de EstadoLuz")

        self._estado = valor
    
    @property
    def cor(self):
        return self._cor

    @cor.setter
    def definir_cor(self, valor):
        if not isinstance(valor, CorLuz):
            raise ValueError("Estado inválido: deve ser uma instância de EstadoTomada")
        self._cor = valor

    @property
    def brilho(self):
        return self._brilho
    
    @brilho.setter
    def definir_brilho(self,valor):

        if valor is None or valor.is_alpha:
            raise ValueError('Digite um valor válido')
        
        elif 0 < valor < 100:
            self._brilho = valor
        else:
            raise ValueError('Digite um valor entre 0 e 100.')
    
    def luz_ligada(self) ->bool:
        if self.estado == EstadoLuz.ON:
            return True

        return False

    def atualizar_log(self, event):

        self.logger = Logger(

            timestamp= datetime.today(),
            dispositivo= self.nome,
            evento= event.event.name,
            estado_origem= EstadoLuz[event.transition.source],
            estado_destino= EstadoLuz[event.transition.dest],
            id_dispositivo= self.nome,
            total_wh= None,
            inicio_periodo=None,
            fim_periodo=None
        )
    
    def on_enter_ON(self, event):
        self.atualizar_log(event)
        self.notificar_observadores(**self.logger.to_dict())
    
    def on_enter_OFF(self, event):
        self.atualizar_log(event)
        self.notificar_observadores(**self.logger.to_dict())

if __name__ == "__main__":
    luz = Luz('Luz da sala', EstadoLuz.OFF, CorLuz.FRIA, brilho=40)
    eve = LogEventosHub()
    rel = LogRelatoriosHub()
    luz.adicionar_observador(eve, rel)
    luz.ligar()
    luz.desligar()