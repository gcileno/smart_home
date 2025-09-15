from abc import ABC, abstractmethod

class Dispositivo(ABC):
    def __init__(self, nome, estado):
        self.nome = nome
        self.estado = estado  
        self._observadores = []

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

    # --- Observer ---
    def adicionar_observador(self, *observador):
        self._observadores.extend(observador)

    def remover_observador(self, observador):
        """Remove um observador registrado."""
        if observador in self._observadores:
            self._observadores.remove(observador)

    def notificar_observadores(self, evento: str, valor_antigo=None, valor_novo=None):
        """Notifica todos os observadores sobre uma mudança."""
        for obs in self._observadores:
            if hasattr(obs, "update"):  
                obs.update(self, evento, valor_antigo, valor_novo)  # se for objeto