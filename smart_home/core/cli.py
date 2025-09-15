from smart_home.utils import interface
from smart_home.utils.service import criar_log_eventos, criar_log_relatorio
from smart_home.core.hub import Hub

def main():
    '''
    Ponto de entrada para a aplicação de automação residencial.
    Inicializa o sistema, cria arquivos de log se necessário e inicia a interface CLI.
    '''
    criar_log_eventos('smart_home/data/log.csv')
    criar_log_relatorio('smart_home/data/relatorio.csv')
    hub = Hub()
    
    interface.home(hub)

if __name__ == "__main__":
    main()
