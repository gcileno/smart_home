from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Optional

from smart_home.core.logger import Logger

class Dispositivo(ABC):
    def __init__(self, nome, estado, tipo=None):
        self.nome = nome
        self.estado = estado
        self.tipo = tipo
        self.machine = None
        self.logger = None
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

    def atualizar_log(self, event: Optional[object] = None):

        self.logger = Logger (
            timestamp = datetime.now().isoformat(),
            dispositivo= self.nome,
            id_dispositivo = self.nome,
            evento = event.event.name if event else None,
            estado_origem = event.transition.source if event else None,
            estado_destino = event.transition.dest if event else None,
            inicio_periodo = datetime.today(),
            fim_periodo = datetime.combine(datetime.today(), datetime.min.time()) + timedelta(days=1),
            total_wh = None
        )

    # --- Observer ---
    def adicionar_observador(self, *observador):
        self._observadores.extend(observador)

    def notificar_observadores(self, **data):
        for obs in self._observadores:
            if hasattr(obs, "update"): 
                obs.update(**data)  # se for objeto