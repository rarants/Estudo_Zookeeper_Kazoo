# Estudo Zookeeper usando Kazoo
Desenvolvido para o estudar o funcionamento do Zookeeper por meio da biblioteca [Kazoo](https://kazoo.readthedocs.io/en/latest/) do Python. :sparkles:
## :clipboard: Requerimentos
Ter o [Zookeeper](https://zookeeper.apache.org/) baixado e instalados o [Python 3](https://www.python.org/), o gerenciador de pacotes pip e a biblioteca Kazoo.
### :wrench: Instalando
1. **Python 3:** `$ sudo apt-get install python3`
2. **Pip 3:**: `$ sudo apt install python-pip3`
3. **Kazoo:** `$ pip3 install kazoo`
### :wrench: Verificando se foram instalados corretamente
1. **Python 3:** `$ python3 --version`
2. **Pip 3:**: `$ pip3 --version`
3. **Kazoo:** `$ pip3 install kazoo`
## :heavy_check_mark: Preparando o ambiente
No **terminal**, inicie o servidor Zookeeper:
- Entre no diretório onde se encontra o download (por padrão): `$ cd Downloads` 
- Extraia o arquivo baixado usando: `$ tar -xvzf zookeeper-3.4.5.tar.gz`
- Entre no diretório onde se encontra a pasta extraída: `$ cd zookeeper-3.4.5.tar.gz`
- Na pasta **conf** faça uma cópia do arquivo **zoo_sample.cfg** e renomeie para **zoo.cfg**
- Edite este novo arquivo para que fique [assim](./zookeeper-3.4.5/conf/zoo.cfg):
`tickTime=2000
 initLimit=10
 syncLimit=5
 dataDir=/tmp/zookeeper
 clientPort=2181`
- Execute o servidor zookeeper: `bin/zkServer.sh start` ou `bin/zkServer.sh start-foreground`
- Abra o diretório onde o arquivo **.py** se encontra e use o comando: `$ python3 nome_arquivo.py`.
## :pencil: Composição
Este repositório é composto pelos seguintes arquivos:
| Arquivo | Descrição |
| :--- | :--- |
| [Cliente.py](./examples/Cliente.py) | Arquivo principal que inicia a Client CLI e assiste eventos de conexão |

## :mag_right: Funcionamento do Código
