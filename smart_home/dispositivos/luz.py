from datetime import datetime
from enum import Enum, auto
from typing import Optional
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
        super().__init__(nome, estado, tipo = 'LUZ')
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
        self.atualizar_log()

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
    def definir_cor(self, valor: CorLuz):
        if not isinstance(valor, CorLuz):
            raise ValueError("Estado inválido: deve ser uma instância de EstadoTomada")
        
        self.logger.dispositivo = self.nome
        self.logger.evento = 'COR ALTERADA'
        self.logger.estado_origem = self._cor
        self.logger.estado_destino = valor.name
        self.logger.inicio_periodo = datetime.today()
        self.logger.fim_periodo = datetime.today()
        self.logger.total_wh = None
        self.notificar_observadores(**self.logger.to_dict())
    
        self._cor = valor

    @property
    def brilho(self):
        return self._brilho
    
    @brilho.setter
    def definir_brilho(self,valor):

        if valor is None or valor.isalpha():
            raise ValueError('Digite um valor válido')
        
        elif 0 < int(valor) < 100:
            self.logger.dispositivo = self.nome
            self.logger.evento = 'BRILHO ALTERADO'
            self.logger.estado_origem = self._brilho
            self.logger.estado_destino = valor
            self.logger.inicio_periodo = datetime.today()
            self.logger.fim_periodo = datetime.today()
            self.logger.total_wh = None
            self._brilho = valor
            print(f'Brilho definido para {self._brilho}%')
            self.notificar_observadores(**self.logger.to_dict())

        else:
            raise ValueError('Digite um valor entre 0 e 100.')
    
    def luz_ligada(self) ->bool:
        if self.estado == EstadoLuz.ON:
            return True

        return False

    def atualizar_log(self, event: Optional[object] = None):

        self.logger = Logger(

            timestamp= datetime.today(),
            dispositivo= self.nome,
            evento= event.event.name if event else None,
            estado_origem= EstadoLuz[event.transition.source] if event else None,
            estado_destino= EstadoLuz[event.transition.dest] if event else None,
            id_dispositivo= self.nome,
            total_wh= 12,
            inicio_periodo=datetime.today(),
            fim_periodo=datetime.today(),
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
    luz.definir_brilho = '80'
    luz.definir_cor = CorLuz.NEUTRA
    luz.definir_brilho = '75'
    luz.definir_cor = CorLuz.QUENTE
    luz.desligar()