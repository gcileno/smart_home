'''
    Tela para selecionar um dispoisito dentro da lista de disponeis no Hub
'''
from smart_home.dispositivos.base import Dispositivo
from smart_home.utils.listar import listar_dispositivos
from smart_home.core.hub import Hub

from rich.console import Console
from rich.panel import Panel

console = Console()


def detalhes_dispositivos(dispositivo: Dispositivo):
    conteudo = (
        f"[bold cyan]Nome:[/bold cyan] {dispositivo.nome}\n"
        f"[bold green]Tipo:[/bold green] {dispositivo.tipo}\n"
        f"[bold yellow]Estado:[/bold yellow] {dispositivo.estado}"
    )
    console.print(Panel(conteudo, title="[bold magenta]Dispositivo[/bold magenta]", expand=False))
    input("\nPressione Enter para continuar...")



def selecionar_dipositivo(hub: Hub):
    
    console.clear()
    listar_dispositivos(hub.dispositivos)

    _input = input("Digite o numero do dispositivo que deseja ver: ")

    try:
        idx = int(_input) - 1
        if idx < 0 or idx >= len(hub.dispositivos):
            raise ValueError("Índice fora do intervalo.")
        dispositivo = hub.dispositivos[idx]
        detalhes_dispositivos(dispositivo)
        
    except ValueError as ve:
        console.print(f"[bold red]Erro:[/bold red] {ve}")
        input("\nPressione Enter para continuar...")

