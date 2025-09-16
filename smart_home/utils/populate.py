from smart_home.core.hub import Hub
from smart_home.core.rotinas import Rotina
from smart_home.dispositivos.porta import Porta
from smart_home.dispositivos.luz import Luz
from smart_home.dispositivos.tomada import Tomada
from smart_home.dispositivos.aspirador import Aspirador
from smart_home.dispositivos.irrigador import Irrigador
from smart_home.dispositivos.persiana import Persiana

def popular_dispositivos(hub: Hub):
    '''
    Popula o Hub com dispositivos de exemplo.
    '''
    dispo = [
        Porta(nome="Porta da Entrada"),
        Porta(nome="Porta dos Fundos"),
        Porta(nome="Porta do Escritório"),
        Luz(nome="Luz da Sala"),
        Luz(nome="Luz da Cozinha"),
        Luz(nome="Luz do Quarto das Crianças"),
        Luz(nome="Luz do Banheiro"),
        Luz(nome="Luz do Quarto do Casal"),
        Tomada(nome="Tomada da TV", potencia_w=200),
        Tomada(nome="Tomada do Computador", potencia_w=150),
        Tomada(nome="Tomada do Carregador", potencia_w=50),
        Tomada(nome="Tomada do Abajur", potencia_w=30),
        Tomada(nome="Tomada do Ar Condicionado", potencia_w=1000),
        Tomada(nome="Tomada do Ventilador", potencia_w=75),
        Tomada(nome="Tomada do Microondas", potencia_w=1200),
        Tomada(nome="Tomada da Geladeira", potencia_w=800),
        Tomada(nome="Aspirador", potencia_w=300),
        Aspirador(nome="Aspirador Dory"),
        Irrigador(nome="Irrigador do Jardim"),
        Persiana(nome="Persiana da Sala"),
        Persiana(nome="Persiana do Quarto do Casal"),
        Persiana(nome="Persiana do Quarto das Crianças"),
    ]
    
    for dispositivo in dispo:
        hub.adicionar_dispositivo(dispositivo)

def popular_rotinas(hub: Hub):
    '''
    Popula o Hub com rotinas de exemplo.
    '''
    rotinas = [
        Rotina(
            'Bom dia raio de sol', {
            Luz: ['ligar'],
            Persiana: ['abrir'],
            Porta: ['destrancar'],
            Aspirador: ['ligar', 'limpar_casa', 'desligar'],
            Tomada: ['ligar'],
            Irrigador: ['ligar', 'iniciar_irrigacao', 'parar_irrigacao', 'desligar']
        }),
        Rotina(
            'Hora do soninho', {
            Luz: ['desligar'],
            Persiana: ['fechar'],
            Porta: ['trancar']
        })
    ]

    for rotina in rotinas:
        hub.adicionar_rotina(rotina)
