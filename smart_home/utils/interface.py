from enum import Enum, auto
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from smart_home.core.hub import Hub
from smart_home.utils.criar import criar_dispositivo, menu_criar_dispositivo

console = Console()

class OpcoesMenuInicial(Enum):
    LISTAR = auto()
    MOSTRAR = auto()
    EXECUTAR_COMANDO = auto()
    ALTERAR_ATRIBUTO = auto()
    EXECUTAR_ROTINA = auto()
    GERAR_RELATORIO = auto()
    SALVAR_CONFIG = auto()
    ADICIONAR = auto()
    REMOVER = auto()
    SAIR = auto()


# Mapeamento de ícones + textos para cada opção
MENU_OPCOES = {
    OpcoesMenuInicial.LISTAR: ("💡", "Listar dispositivos"),
    OpcoesMenuInicial.MOSTRAR: ("🔎", "Mostrar dispositivo"),
    OpcoesMenuInicial.EXECUTAR_COMANDO: ("⚙️", "Executar comando em dispositivo"),
    OpcoesMenuInicial.ALTERAR_ATRIBUTO: ("🛠️", "Alterar atributo de dispositivo"),
    OpcoesMenuInicial.EXECUTAR_ROTINA: ("🤖", "Executar rotina"),
    OpcoesMenuInicial.GERAR_RELATORIO: ("📊", "Gerar relatório"),
    OpcoesMenuInicial.SALVAR_CONFIG: ("💾", "Salvar configuração"),
    OpcoesMenuInicial.ADICIONAR: ("➕", "Adicionar dispositivo"),
    OpcoesMenuInicial.REMOVER: ("🗑️", "Remover dispositivo"),
    OpcoesMenuInicial.SAIR: ("🚪", "Sair"),
}


def menu():
    tabela = Table(show_header=False, show_edge=False, padding=(0,1))

    for idx, opcao in enumerate(OpcoesMenuInicial, start=1):
        icone, texto = MENU_OPCOES[opcao]
        tabela.add_row(str(idx), f"{icone} {texto}")

    painel = Panel(
        tabela,
        title="[bold cyan]=== SMART HOME HUB ===[/bold cyan]",
        border_style="bright_magenta",
        padding=(1, 2),
    )

    console.print(painel)


def pegar_opcao() -> OpcoesMenuInicial:
    escolha = console.input("[bold yellow]👉 Escolha uma opção:[/bold yellow] ")

    try:
        escolha_int = int(escolha)
        return list(OpcoesMenuInicial)[escolha_int - 1]
    except (ValueError, IndexError):
        #console.print("[bold red]⚠ Opção inválida![/bold red]")
        return None

def home(hub: Hub):
    esc = None

    while esc != OpcoesMenuInicial.SAIR:
        menu()
        esc = pegar_opcao()
                
        match esc:
            case OpcoesMenuInicial.LISTAR:
                print('Chamando função para listar os objetos')
            case OpcoesMenuInicial.ADICIONAR:
                d = menu_criar_dispositivo()
                hub.adicionar_dispositivo(d)
            case _:
                console.print("[bold red]⚠ Opção inválida![/bold red]")


    console.print("[bold cyan]👋 Encerrando o Smart Home Hub...[/bold cyan]")

