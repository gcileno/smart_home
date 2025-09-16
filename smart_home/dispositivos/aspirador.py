from datetime import datetime
from enum import Enum, auto
from typing import Optional
from transitions import Machine
from smart_home.core.logger import Logger
from smart_home.core.observers import LogEventosHub, LogRelatoriosHub
from smart_home.dispositivos.base import Dispositivo

class COMODO(Enum):
    SALA = auto()
    COZINHA = auto()
    QUARTO = auto()
    BANHEIRO = auto()
    ESCRITORIO = auto()
    BASE = auto()

class EstadoAspirador(Enum):
    DESLIGADO = auto()
    LIGADO = auto()
    LIMPEZA = auto()
    RETORNANDO_BASE = auto()
    CARREGANDO = auto()

TRANSITIONS = [
    {'trigger': 'ligar', 'source': 'DESLIGADO', 'dest': 'LIGADO'},
    {'trigger': 'desligar', 'source': ['LIGADO','RETORNANDO_BASE', 'CARREGANDO'], 'dest': 'DESLIGADO'},
    {'trigger': 'iniciar_limpeza', 'source': 'LIGADO', 'dest': 'LIMPEZA'},
    {'trigger': 'voltar_base', 'source': 'LIMPEZA', 'dest': 'RETORNANDO_BASE'},
    {'trigger': 'iniciar_carregamento', 'source': 'RETORNANDO_BASE', 'dest': 'CARREGANDO'},
    {'trigger': 'carga_completa', 'source': 'CARREGANDO', 'dest': 'LIGADO'}
]

class Aspirador(Dispositivo):

    def __init__(self, nome: str):
        super().__init__(nome, estado=EstadoAspirador.DESLIGADO)
        self.bateria = 100 
        self.localizacao = "Base"

        #Atualizando a máquina de estados
        self.machine = Machine(
            model=self, 
            states=[estado.name for estado in EstadoAspirador], 
            initial=EstadoAspirador.DESLIGADO.name,
            transitions=TRANSITIONS,
            auto_transitions=False,
            send_event=True,
            after_state_change=['atualizar_log', 'sincronizar_estado']
        )

        self.atualizar_log()

    def sincronizar_estado(self, event):
        self.estado = EstadoAspirador[self.state]

    def estado(self, valor):

        if isinstance(valor, EstadoAspirador):
            self.estado = valor
            print(self.estado)
        else:
            raise ValueError("Estado inválido para o aspirador.")
    
    def on_exit_LIGADO(self, event):
        self.bateria -= 3  # Consumo de bateria ao ligar
        self.localizacao = "BASE"
        print(f"{self.nome} está ligado. Bateria: {self.bateria}%")
        self.atualizar_log(event)
        self.notificar_observadores(**self.logger.to_dict())
    
    def on_enter_LIMPEZA(self, event):
        print(f"{self.nome} está limpando...")
        self.atualizar_log(event)
        self.notificar_observadores(**self.logger.to_dict())
    
    def on_enter_RETORNANDO_BASE(self, event):
        self.localizacao = "[ LOG ] Indo para a base"
        print(f"[LOG{self.nome} está retornando para a base.")
        self.iniciar_carregamento()
        self.atualizar_log(event)
        self.notificar_observadores(logger=self.logger.to_dict())
    
    def on_enter_CARREGANDO(self, event):
        self.localizacao = "BASE"
        print(f"{self.nome} está carregando...")
        self.bateria = 100  # Simula o carregamento completo
        self.atualizar_log(event)
        self.notificar_observadores(**self.logger.to_dict())
        self.carga_completa()

    def on_exit_CARREGANDO(self, event):
        print(f"{self.nome} terminou de carregar. Bateria: {self.bateria}%")
        self.atualizar_log(event)
        self.notificar_observadores(**self.logger.to_dict())

    def on_exit_DESLIGADO(self, event):
        print(f"{self.nome} foi desligado.")
        self.atualizar_log(event)
        self.notificar_observadores(**self.logger.to_dict())
    
    def limpar_casa(self):
        self.iniciar_limpeza()
        for comodo in COMODO:
            print(f"{self.nome} está limpando o {comodo.name}.")
            self.bateria -= 15  # Consumo de bateria por cômodo

            self.logger.timestamp = datetime.now().isoformat()
            self.logger.dispositivo = self.nome
            self.logger.evento = f'LIMPANDO {comodo.name}'
            self.logger.estado_origem = f'{self.estado.name} - {self.localizacao}'
            self.logger.estado_destino = f'{self.estado.name} - {comodo.name}'

            self.notificar_observadores(**self.logger.to_dict())

            if self.bateria <= 20:
                print(f"{self.nome} está com bateria baixa ({self.bateria}%). Retornando para a base.")
                self.voltar_base()
                break

if __name__ == "__main__":
    aspirador = Aspirador("Aspirador Dory")
    eve = LogEventosHub()
    rel = LogRelatoriosHub()
    aspirador.adicionar_observador(eve, rel)
    aspirador.ligar()
    aspirador.limpar_casa()
