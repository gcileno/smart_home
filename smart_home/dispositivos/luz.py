from enum import Enum, auto
from base import Dispositivo


class Luz(Dispositivo):

    def __init__(self, nome, estado = 'ON', cor = 'QUENTE', brilho: int = 60):
        super().__init__(nome, estado)
        self.__brilho = brilho
        self.__cor = cor
    
    def ligar_luz(self):

        if self.estado == self.EstadoLuz.OFF:
            self.estado = self.EstadoLuz.ON

        print(f'Ligando a {self.nome}')
    
    def desligar_luz(self):
        print(f'Desligando a {self.nome}.')
    
    def definir_brilho(self, novo_brilho: int):
        self._brilho = novo_brilho
        print(f'Novo brilho aplicado')
    
    def definir_cor(self, novo_brilho):
        self.__brilho = novo_brilho
        print('Novo brilho definico')

    class Cor(Enum):
        QUENTE = auto()
        FRIA = auto()
        NEUTRA = auto()

    class EstadoLuz(Enum):
        ON = auto()
        OFF = auto()
        