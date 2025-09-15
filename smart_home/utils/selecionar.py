'''
    Tela para selecionar um dispoisito dentro da lista de disponeis no Hub
'''
from smart_home.dispositivos.base import Dispositivo
from smart_home.utils.listar import listar_dispositivos
from smart_home.core.hub import Hub

def detalhes_dispositivos(dispositivo: Dispositivo):
    pass

def selecionar_dipositivo(hub: Hub):
    
    listar_dispositivos(hub.dispositivos)

    _input = input("Digite o numero do dispositivo que deseja ver: ")

