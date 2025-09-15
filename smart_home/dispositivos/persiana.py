from enum import Enum, auto
from smart_home.dispositivos.base import Dispositivo

class LuminosidadePersiana(Enum):
    CLARO = auto()
    MEDIA = auto()
    ESCURA = auto()

class EstadoPersiana(Enum):
    ABERTA = auto()
    FECHADA = auto()

TRANSICOES_PERSIANA = [
    {'trigger': 'abrir', 'source': EstadoPersiana.FECHADA, 'dest': EstadoPersiana.ABERTA},
    {'trigger': 'fechar', 'source': EstadoPersiana.ABERTA, 'dest': EstadoPersiana.FECHADA},
]

class Persiana(Dispositivo):

    def __init__(self, nome, estado, luminosidade = LuminosidadePersiana.MEDIA):
        super().__init__(nome, estado)

        self._luminosidade = luminosidade
    
    @property
    def estado(self):
        return self._nome
    
    @estado.setter
    def estado(self, valor):
        if not isinstance(valor, EstadoPersiana):
            raise ValueError('Estado não encontrado para a perciana, reveja suas opções.')
    
    @property
    def luminosidade(self):
        return self._luminosidade
    
    @luminosidade.setter
    def luminosidade(self, valor):

        if not isinstance(valor, LuminosidadePersiana):
            raise ValueError('Estado não encontrado para a perciana, reveja suas opções.')
        
        if self.estado == EstadoPersiana.FECHADA:
            self._luminosidade = valor
        else:
            raise ValueError('Não é possivel alterar as paletas com a persina abert.')
