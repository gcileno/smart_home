class ConfigHub():

    def __init__(self):
        pass

    def atualizar(self):
        print('Atualizar arquivo log')
    
    def inicializar_hub(self):
        print('Leitura do arquivo config.json para inicializar o hub')

class LogEventosHub():
    def __init__(self):
        pass

    def atualizar_log(self, **kawrgs):

        with open('data/log.csv', 'a') as log:
            log.write(kawrgs)

class LogRelatoriosHub():
    def __init__(self):
        pass

    def atualizar_log(self, **kawrgs):

        with open('data/relatorio.csv', 'a') as log:
            log.write(kawrgs)