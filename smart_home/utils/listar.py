from rich.console import Console
from rich.table import Table

from smart_home.dispositivos.base import Dispositivo

console = Console()

def listar_dispositivos(dispositivos: list[Dispositivo]):
    """
    Lista os dispositivos disponíveis no sistema em formato de tabela bonita (Rich).

    Args:
        dispositivos (list): Lista de dispositivos a serem listados.
    """
    if not dispositivos:
        console.print("[bold red]Nenhum dispositivo encontrado.[/bold red]")
        return
    console.clear()
    table = Table(title="📡 Dispositivos disponíveis")

    table.add_column("ID", justify="center", style="cyan", no_wrap=True)
    table.add_column("Nome", style="green")
    table.add_column("Estado", style="magenta")

    for idx, dispositivo in enumerate(dispositivos, start=1):
        table.add_row(
            str(idx),
            dispositivo.nome,
            str(dispositivo.estado.name if hasattr(dispositivo.estado, "name") else dispositivo.estado)
        )

    console.print(table)
    console.input("\n[bold cyan] Pressione Enter para continuar... [/bold cyan]")