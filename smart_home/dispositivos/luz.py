from enum import Enum, auto
from base import Dispositivo

class CorLuz(Enum):
    QUENTE = auto()
    FRIA = auto()
    NEUTRA = auto()

class EstadoLuz(Enum):
    ON = auto()
    OFF = auto()

TRANSICOES_LUZ= [
    { 'trigger': 'ligar', 'source': EstadoLuz.OFF, 'dest' : EstadoLuz.ON },
    { 'trigger': 'desligar', 'source': EstadoLuz.ON, 'dest' : EstadoLuz.OFF },
    { 
        'trigger': 'novo_brilho', 
        'source': EstadoLuz.ON, 
        'dest' : EstadoLuz.ON, 
        'conditions' : ['luz_ligada'], 
        'after' : 'definir_brilho'
    },
]

class Luz(Dispositivo):

    def __init__(self, nome, estado = EstadoLuz.OFF, cor = CorLuz.QUENTE, brilho: int = 60):
        super().__init__(nome, estado)
        self._brilho = brilho
        self._cor = cor

        #implementr classe NotNull ou ValueError?

    @Dispositivo.estado.setter
    def estado(self, valor):

        if not isinstance(valor, EstadoLuz):
            raise ValueError("Estado inválido: deve ser uma instância de EstadoTomada")

        self.estado = valor
    
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
        
