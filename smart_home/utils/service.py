import csv
import json
from pathlib import Path
from smart_home.core.hub import Hub

def gerar_arquivo_confi(hub: Hub, path: str):
    '''
    'Cria ou sobrescreve um arquivo de configuração JSON os dispositovos do Hub passado por parâmetro
    no caminho especificado.
    '''
    dispositivos_data = [hub.dispositivos.__dict__ for dispositivo in hub.dispositivos]
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(dispositivos_data, file, indent=4, ensure_ascii=False)


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