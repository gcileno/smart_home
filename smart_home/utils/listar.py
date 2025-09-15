from smart_home.dispositivos.base import Dispositivo

def listar_dispositivos(dispositivos: list[Dispositivo]):
    """
    Lista os dispositivos disponíveis no sistema.

    Args:
        dispositivos (list): Lista de dispositivos a serem listados.
    """
    if not dispositivos:
        print("Nenhum dispositivo encontrado.")
        return

    print("Dispositivos disponíveis:")
    for idx, dispositivo in enumerate(dispositivos, start=1):
        print(f"{idx}. {dispositivo.nome} - Estado: {dispositivo['estado']}")