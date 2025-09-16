from smart_home.core.hub import Hub
from smart_home.dispositivos.base import Dispositivo
from rich.console import Console
from rich.panel import Panel


console = Console()

def remover_dispositivo(hub: Hub):
    console.clear()
    if not hub.dispositivos:
        console.print("[bold red]Nenhum dispositivo disponível para remoção.[/bold red]")
        input("\nPressione Enter para continuar...")
        return

    conteudo = "\n".join(f"[bold cyan]{idx + 1}.[/bold cyan] {dispositivo.nome}" for idx, dispositivo in enumerate(hub.dispositivos))
    console.print(Panel(conteudo, title="[bold magenta]Dispositivos Disponíveis[/bold magenta]", expand=False))

    _input = input("Digite o número do dispositivo que deseja remover: ")

    try:
        idx = int(_input) - 1
        if idx < 0 or idx >= len(hub.dispositivos):
            raise ValueError("Índice fora do intervalo.")
        
        dispositivo_removido = hub.dispositivos[idx]
        hub.remover_dispositivo(dispositivo_removido.nome)
        console.print(f"[bold green]✔ Dispositivo '{dispositivo_removido.nome}' removido com sucesso![/bold green]")
        
    except ValueError as ve:
        console.print(f"[bold red]Erro:[/bold red] {ve}")

    console.input("\n[bold cyan] Pressione Enter para continuar... [/bold cyan]")
