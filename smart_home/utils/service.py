import csv
from pathlib import Path

def criar_log_eventos(path: str) -> None:
    """
    Cria um arquivo de log CSV com o cabeçalho especificado, caso não exista.
    
    Args:
        path (str): Caminho do arquivo de log.
    """
    log_file = Path(path)

    if not log_file.exists():
        with open(log_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["timestamp", "dispositivo", "evento", "estado_origem", "estado_destino"])


def criar_log_relatorio(path: str) -> None:
    """
    Cria um arquivo de log CSV com o cabeçalho especificado, caso não exista.

    Args:
        path (str): Caminho do arquivo de log.
    """
    log_file = Path(path)

    if not log_file.exists():
        with open(log_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["id_dispositivo", "total_wh", "inicio_periodo", "fim_periodo"])