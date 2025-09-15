"""
    Tela com cadastro de dispositos e novas machinas
"""

from smart_home.dispositivos.luz import Luz, EstadoLuz
from smart_home.dispositivos.tomada import Tomada, EstadoTomada
from smart_home.dispositivos.persiana import Persiana, EstadoPersiana
from smart_home.dispositivos.porta import Porta, EstadoPorta
from smart_home.dispositivos.base import Dispositivo


def menu_criar_dispositivo():
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

def criar_dispositivo(tipo: str, nome: str, estado: str) -> Dispositivo:
    """
    Cria uma instância de dispositivo com base no tipo, nome e estado fornecidos.
    
    Args:
        tipo (str): Tipo do dispositivo ('luz', 'tomada', 'persiana', 'porta').
        nome (str): Nome do dispositivo.
        estado (str): Estado inicial do dispositivo (deve ser um valor válido do Enum correspondente).
    
    Returns:
        Dispositivo: Instância do dispositivo criado.
    
    Raises:
        ValueError: Se o tipo ou estado for inválido.
    """
    tipo = tipo.lower()
    
    if tipo == 'luz':
        try:
            estado_enum = EstadoLuz[estado.upper()]
            return Luz(nome, estado_enum)
        except KeyError:
            raise ValueError(f"Estado inválido para Luz: {estado}. Opções válidas: {[e.name for e in EstadoLuz]}")
    
    elif tipo == 'tomada':
        try:
            estado_enum = EstadoTomada[estado.upper()]
            return Tomada(nome, estado_enum)
        except KeyError:
            raise ValueError(f"Estado inválido para Tomada: {estado}. Opções válidas: {[e.name for e in EstadoTomada]}")
    
    elif tipo == 'persiana':
        try:
            estado_enum = EstadoPersiana[estado.upper()]
            return Persiana(nome, estado_enum)
        except KeyError:
            raise ValueError(f"Estado inválido para Persiana: {estado}. Opções válidas: {[e.name for e in EstadoPersiana]}")
    
    elif tipo == 'porta':
        try:
            estado_enum = EstadoPorta[estado.upper()]
            return Porta(nome, estado_enum)
        except KeyError:
            raise ValueError(f"Estado inválido para Porta: {estado}. Opções válidas: {[e.name for e in EstadoPorta]}")
    
    else:
        raise ValueError(f"Tipo de dispositivo inválido: {tipo}. Opções válidas: ['luz', 'tomada', 'persiana', 'porta']")
