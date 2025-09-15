"""
    Tela com cadastro de dispositos e novas machinas
"""

from smart_home.dispositivos.luz import Luz, EstadoLuz
from smart_home.dispositivos.tomada import Tomada, EstadoTomada
from smart_home.dispositivos.persiana import Persiana, EstadoPersiana
from smart_home.dispositivos.porta import Porta, EstadoPorta
from smart_home.dispositivos.base import Dispositivo


def menu_criar_dispositivo() -> Dispositivo:
    dispositivos_opcoes = {
        "1": ("Luz", Luz, EstadoLuz),
        "2": ("Tomada", Tomada, EstadoTomada),
        "3": ("Persiana", Persiana, EstadoPersiana),
        "4": ("Porta", Porta, EstadoPorta),
    }

    print("\n=== Criar Dispositivo ===")
    for key, (nome, _, _) in dispositivos_opcoes.items():
        print(f"{key} - {nome}")

    escolha = input("Escolha o tipo de dispositivo: ").strip()
    if escolha not in dispositivos_opcoes:
        print("❌ Opção inválida!")
        return None

    nome, classe_dispositivo, enum_estado = dispositivos_opcoes[escolha]

    dispositivo_nome = input(f"Digite o nome da {nome}: ").strip()

    print("\nEstados possíveis:")
    for i, estado in enumerate(enum_estado, start=1):
        print(f"{i} - {estado.name}")

    escolha_estado = input("Escolha o estado inicial: ").strip()

    try:
        estado_inicial = list(enum_estado)[int(escolha_estado) - 1]
    except (IndexError, ValueError):
        print("❌ Estado inválido!")
        return None

    # cria a instância corretamente
    dispositivo = classe_dispositivo(dispositivo_nome, estado_inicial)
    print(f"\n✅ Dispositivo criado: {dispositivo_nome} ({nome}, {estado_inicial.name})")

    return dispositivo