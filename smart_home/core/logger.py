from dataclasses import asdict, dataclass

@dataclass
class Logger():
    timestamp: str
    dispositivo: str
    evento: str
    estado_origem: str
    estado_destino: str
    id_dispositivo: str
    total_wh: str
    inicio_periodo: str
    fim_periodo: str

    def to_dict(self):
        return asdict(self)