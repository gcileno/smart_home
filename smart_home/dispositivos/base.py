from abc import ABC, abstractmethod

class Dispositivo(ABC):
    def __init__(self, nome, estado):
        self.nome = nome
        self.estado = estado