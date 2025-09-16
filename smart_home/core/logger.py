from dataclasses import asdict, dataclass

@dataclass
class Logger():
    timestamp: str = None
    dispositivo: str = None
    evento: str = None
    estado_origem: str = None
    estado_destino: str = None
    id_dispositivo: str = None
    total_wh: str = None
    inicio_periodo: str = None
    fim_periodo: str = None

    def to_dict(self):
        return asdict(self)