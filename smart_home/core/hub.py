from smart_home.core.observers import LogEventosHub, LogRelatoriosHub
from smart_home.dispositivos.base import Dispositivo

class Hub:
   
    def __init__(self):
        super().__init__()
        self.dispositivos : list[Dispositivo] = []
        self.eventos = LogEventosHub()
        self.relatorios = LogRelatoriosHub()
    
    def adicionar_dispositivo(self, dispositivo: Dispositivo):
        #Incluindo os observadores
        dispositivo.adicionar_observador(self.eventos, self.relatorios)

        #Inserir na lista de dispositos do hub
        self.dispositivos.append(dispositivo)

    def remover_dispositivo(self, dispositivo_id: Dispositivo):
        self.dispositivos = [d for d in self.dispositivos if d.nome != dispositivo_id]
    
