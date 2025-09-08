from abc import ABC, abstractmethod

class Dispositivo(ABC):
    def __init__(self, nome, estado):
        self.nome = nome
        self.estado = estado  

    # --- nome ---
    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        if isinstance(valor, str) and valor:
            self._nome = valor
        else:
            raise ValueError("Nome deve ser uma string não vazia.")

    # --- estado deve ser instanciado pelas novas classes
    @property
    @abstractmethod
    def estado(self):
        """Estado atual do dispositivo (Enum ou valor específico da subclasse)."""
        pass

    @estado.setter
    @abstractmethod
    def estado(self, valor):
        """Define o estado do dispositivo (validado na subclasse)."""
        pass