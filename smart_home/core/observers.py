import csv

class LogEventosHub:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, caminho = "smart_home/data/log.csv"):
        self.log_caminho = caminho

    def update(self, **kwargs):
        """
        Recebe dados de notificação e grava no log CSV.
        kwargs esperados: timestamp, dispositivo, evento, estado_origem, estado_destino
        """
        with open(self.log_caminho, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                kwargs.get("timestamp"),
                kwargs.get("dispositivo"),
                kwargs.get("evento"),
                kwargs.get("estado_origem"),
                kwargs.get("estado_destino")
            ])

class LogRelatoriosHub():
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, caminho = "smart_home/data/relatorio.csv"):
        self.log_caminho = caminho

    def update(self, **kwargs):
        """
        Recebe dados de notificação e grava no log CSV.
        kwargs esperados: id_dispositivo, total_wh, inicio_periodo, fim_periodo
        """
        with open(self.log_caminho, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                kwargs.get("id_dispositivo"),
                kwargs.get("total_wh"),
                kwargs.get("inicio_periodo"),
                kwargs.get("fim_periodo"),
            ])