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
<summary><strong>Pasta <code>utils</code></strong></summary>

A pasta `utils` contém funções auxiliares e módulos de apoio utilizados em diferentes partes do projeto. Cada arquivo dentro dessa pasta tem uma responsabilidade específica, como manipulação de dados, validações ou utilidades gerais para facilitar o desenvolvimento e manutenção do sistema.

- **criar.py**: Tela e funções para cadastro de novos dispositivos e seleção de estados iniciais.
- **interface.py**: Implementa menus, opções e interação principal com o usuário via terminal.
- **listar.py**: Função para listar dispositivos do sistema em formato de tabela usando Rich.
- **populate.py**: Popula o sistema com dispositivos e rotinas de exemplo para testes e demonstração.
- **selecionar.py**: Tela para selecionar um dispositivo da lista disponível no Hub.
- **service.py**: Serviços para geração de arquivos de configuração e logs (JSON e CSV).

- `__init__.py`: Torna a pasta um pacote Python.

</details>