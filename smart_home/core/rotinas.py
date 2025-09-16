from dataclasses import dataclass
from typing import Type
from smart_home.dispositivos.base import Dispositivo

@dataclass
class Rotina:
    nome: str
    regras: dict[Type[Dispositivo], list[str]]
    # exemplo:
    # {
    #   Luz: ["desligar"],
    #   Persiana: ["fechar"],
    #   Porta: ["trancar"]
    # }

    def executar(self, dispositivos: list[Dispositivo]):
        for disp in dispositivos:
            for tipo, acoes in self.regras.items():
                if isinstance(disp, tipo):
                    for acao in acoes:
                        metodo = getattr(disp, acao, None)
                        if callable(metodo):
                            metodo()
                        else:
                            print(f"Ação '{acao}' não encontrada no dispositivo '{disp.nome}'.")
