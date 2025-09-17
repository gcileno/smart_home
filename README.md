# Smart Home
Atividade avaliativa realizada por Gabriel Cileno de Medeiros Costa como parte da disciplina Orientação a Objetos em Python.

### Apresentação

<div align="left">

[![Assista no YouTube](https://img.youtube.com/vi/J9W6YQoZdmU/0.jpg)](https://youtu.be/J9W6YQoZdmU)
</div>

- [Ver vídeo no YouTube](https://youtu.be/J9W6YQoZdmU)
- [Ver vídeo no Google Drive](https://drive.google.com/file/d/1YBqUM7A1m_RmB4LrC4N6wcFuilNHIjDQ/view?usp=sharing)

## Instalação de Dependências

Antes de instalar as dependências, recomenda-se criar e ativar um ambiente virtual (venv):

No Windows:
```
python -m venv venv
venv\Scripts\activate
```

No Linux/Mac:
```
python3 -m venv venv
source venv/bin/activate
```

Depois, instale as dependências necessárias utilizando o arquivo `requirements.txt`:

```
pip install -r requirements.txt
```

Isso irá instalar todas as bibliotecas Python necessárias para o funcionamento do projeto.

## Descrição do main.py

O arquivo `main.py` é o ponto de entrada do projeto. Ele inicializa e executa a aplicação principal de automação residencial, controlando os dispositivos e gerenciando os estados do sistema.

## Como usar

Para executar o projeto, certifique-se de que as dependências estejam instaladas e o ambiente virtual ativado. Em seguida, execute o comando abaixo no terminal:

```
python main.py
```

O sistema será iniciado e você poderá acompanhar as operações conforme implementado no código.

<details>
<summary><strong>Utils <code>utils</code></strong></summary>

A pasta `utils` contém funções auxiliares e módulos de apoio utilizados em diferentes partes do projeto. Cada arquivo dentro dessa pasta tem uma responsabilidade específica, como manipulação de dados, validações ou utilidades gerais para facilitar o desenvolvimento e manutenção do sistema.

- **criar.py**: Tela e funções para cadastro de novos dispositivos e seleção de estados iniciais.
- **interface.py**: Implementa menus, opções e interação principal com o usuário via terminal.
- **listar.py**: Função para listar dispositivos do sistema em formato de tabela usando Rich.
- **populate.py**: Popula o sistema com dispositivos e rotinas de exemplo para testes e demonstração.
- **selecionar.py**: Tela para selecionar um dispositivo da lista disponível no Hub.
- **service.py**: Serviços para geração de arquivos de configuração e logs (JSON e CSV).

- `__init__.py`: Torna a pasta um pacote Python.

</details>

<details>
<summary><strong>Core <code>core</code></strong></summary>

A pasta `core` reúne os componentes centrais da lógica do sistema, responsáveis pela orquestração dos dispositivos, rotinas e registro de eventos.

- **hub.py**: Define a classe principal `Hub`, responsável por gerenciar os dispositivos, rotinas e observadores do sistema. Permite adicionar/remover dispositivos, executar rotinas e integra os logs de eventos e relatórios.
- **logger.py**: Estrutura de dados para registro de eventos e relatórios, facilitando a serialização e manipulação das informações de log.
- **observers.py**: Implementa os observadores do padrão Observer, responsáveis por registrar eventos e relatórios em arquivos CSV de forma centralizada e singleton.
- **rotinas.py**: Define a classe `Rotina`, que representa um conjunto de ações automatizadas a serem executadas em dispositivos do sistema, permitindo a criação de cenários e automações personalizadas.

</details>

<details>
<summary><strong>Dispositivos <code>dispositivos</code></strong></summary>

A pasta `dispositivos` contém todas as classes que representam os dispositivos físicos ou virtuais controlados pelo sistema. Cada dispositivo implementa comportamentos e estados próprios, além de integrar-se ao padrão Observer para registro de eventos.

- **base.py**: Classe abstrata base para todos os dispositivos. Define propriedades comuns, interface para estados, integração com logs e observadores.
- **aspirador.py**: Implementa o dispositivo Aspirador, com máquina de estados para ligar, iniciar limpeza, retornar à base e carregar. Gerencia bateria e localização.
- **irrigador.py**: Representa o dispositivo Irrigador, com estados para ligar, desligar e irrigar. Integração com logs e notificações de eventos.
- **luz.py**: Dispositivo de iluminação, com controle de estado (ligado/desligado), cor e brilho. Permite alteração dinâmica e registro detalhado de eventos.
- **persiana.py**: Controla persianas automáticas, com estados de aberta/fechada e ajuste de luminosidade. Notifica eventos de alteração de estado.
- **porta.py**: Dispositivo de porta inteligente, com estados trancada, destrancada e aberta. Inclui lógica para tentativas inválidas de trancamento.
- **tomada.py**: Representa tomadas inteligentes, com controle de estado, potência e cálculo de consumo energético. Registra eventos de uso e consumo.

Cada classe de dispositivo herda de `base.py`, garantindo interface padronizada, integração com logs e suporte ao padrão Observer para monitoramento e automação.

</details>