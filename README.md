# Estudo Zookeeper usando Kazoo
Desenvolvido para o estudar o funcionamento do Zookeeper por meio da biblioteca [Kazoo](https://kazoo.readthedocs.io/en/latest/) do Python. :sparkles:
## :clipboard: Requerimentos
Ter o [Zookeeper](https://zookeeper.apache.org/) baixado (e, consequentemente, o Java) e o [Python 3](https://www.python.org/), o gerenciador de pacotes pip e a biblioteca Kazoo instalados.
### :wrench: Instalando
1. **Python 3:** `$ sudo apt-get install python3`
2. **Pip 3:** `$ sudo apt install python-pip3`
3. **Kazoo:** `$ pip3 install kazoo`
### :wrench: Verificando se foram instalados corretamente (ou qual a versão, se já instalados)
1. **Python 3:** `$ python3 --version`
2. **Pip 3:** `$ pip3 --version`
## :heavy_check_mark: Preparando o ambiente
No **terminal**, inicie o servidor Zookeeper:
- Entre no diretório onde se encontra o download (por padrão): `$ cd Downloads` 
- Extraia o arquivo baixado usando: `$ tar -xvzf zookeeper-3.4.5.tar.gz`
- Entre no diretório onde se encontra a pasta extraída: `$ cd zookeeper-3.4.5.tar.gz`
- Na pasta **conf** faça uma cópia do arquivo **zoo_sample.cfg** e renomeie para **zoo.cfg**
- Edite este novo arquivo para que fique assim:
```
 tickTime=2000
 initLimit=10
 syncLimit=5
 dataDir=/tmp/zookeeper
 clientPort=2181
 ```
- Execute o servidor zookeeper no terminal: `$ bin/zkServer.sh start` ou `$ bin/zkServer.sh start-foreground`
- Abra o diretório onde o arquivo **.py** se encontra e use o comando: `$ python3 nome_arquivo.py`.

## :pencil: Composição
Este repositório é composto pelos seguintes arquivos:
| Arquivo | Descrição |
| :--- | :--- |
| [Listener.py](./examples/Listener.py) | Arquivo principal que inicia a Client CLI e assiste eventos de conexão |
| [CreatingAZNode.py](./examples/CreatingAZnode.py) | Arquivo que testa a criação de nodes e verifica se eles existem |
| [ReadingData.py](./examples/ReadingData.py) | Arquivo que testa a leitura de dados dos nodes |
| [UpdatingData.py](./examples/UpdatingData.py) | Arquivo que testa a alteração dos dados dos nodes |
| [DefaultWatcher.py](./examples/DefaultWatcher.py) | Arquivo para testar um watcher padrão do Zookeeper |
| [Watcher.py](./examples/Watcher.py) | Arquivo para testar um watcher da API do Kazoo |

## :mag_right: Funcionamento do Código
### :paperclip: [Listener.py](./examples/Listener.py)
```python
from kazoo.client import KazooClient
from kazoo.client import KazooState
import time

def my_listener(state):
    if state == KazooState.LOST:
        print("State = lost")
    elif state == KazooState.SUSPENDED:
        print("State = suspended")
    elif state == KazooState.CONNECTED:
        print("State = connected")
    else:
        print("other")
        
zk = KazooClient(hosts='127.0.0.1:2181')    # Salva na var **zk** o host onde será feita a conexão (e onde se encontra o zkServer rodando)
zk.add_listener(my_listener)                # Adiciona um listener do estado da conexão, passando a função my_listener
zk.start()                                  # Inicia-se uma conexão KazooCLient
time.sleep(10)
zk.stop()
```
### :paperclip: [CreatingAZNode.py](./examples/CreatingAZNode.py) 
```python
from kazoo.client import KazooClient

def node_exists(path):
    if zk.exists(path):                    # Determina se um node existe
        print("Founded znode = " + path)

zk = KazooClient(hosts='127.0.0.1:2181')   # Salva na var **zk** o host onde será feita a conexão (e onde se encontra o zkServer rodando)
zk.start()                                 # Inicia-se uma conexão KazooCLient
# Cria nodes
zk.create("/node2")
zk.create("/node2/children1")
# Verifica se os nodes existem
node_exists("/node2")
node_exists("/node")
node_exists("/node2/children1")
zk.stop()
```
### :paperclip: [ReadingData.py](./examples/ReadingData.py)
```python
from kazoo.client import KazooClient

path = "/node2"
zk = KazooClient(hosts='127.0.0.1:2181')   # Salva na var **zk** o host onde será feita a conexão (e onde se encontra o zkServer rodando)
zk.start()                                 # Inicia-se uma conexão KazooCLient

# Determina se o node existe
if zk.exists(path):
    print("Founded znode!")

# Printa a versão do node e seus dados
data, stat = zk.get(path)
print("Version: %s, data: %s" % (stat.version, data.decode("utf-8")))

# Lista os nodes filhos
children = zk.get_children(path)
print("There are %s children with names %s" % (len(children), children))

zk.stop()
```
### :paperclip: [UpdatingData.py](./examples/UpdatingData.py)
```python
from kazoo.client import KazooClient

zk = KazooClient(hosts='127.0.0.1:2181')  # Salva na var **zk** o host onde será feita a conexão (e onde se encontra o zkServer rodando)
zk.start()                                # Inicia-se uma conexão KazooCLient

zk.set("/node1", b"some data")            # Altera o dado do node

zk.stop()
```
### :paperclip: Deletando Dados
Semelhante à atualizar os dados, porém, utiliza-se **delete()**

`zk.delete("/my/favorite/node", recursive=True)`

### :paperclip: [DefaultWatcher.py](./examples/DefaultWatcher.py)
```python
from kazoo.client import KazooClient

def  watchEvent ( event ): 
    print("Children has change")


zk = KazooClient(hosts='127.0.0.1:2181')
zk.start()

# Call my_func when the children change 
children  =  zk.get_children ( "/node2" ,  watch = watchEvent)

zk.stop()
```
### :paperclip: [Watcher.py](./examples/Watcher.py)
```python
from kazoo.client import KazooClient
import time

@zk.ChildrenWatch(path[1][1])
def watch_children(children):
    print("Children are now: %s" % children)
# Above function called immediately, and from then on

@zk.DataWatch(path[1][0])
def watch_node(data, stat):
    print("Version: %s, data: %s" % (stat.version, data.decode("utf-8")))

path=[["/node1"], ["/node2", "/node2/children1"]]
zk = KazooClient(hosts='127.0.0.1:2181')
zk.start()
time.sleep(10)
zk.stop()
```
## :boom: Sobre o Kazoo
### Estados Kazoo
- Lost;
- Connected;
- Suspended.

Quando uma instância do KazooClient é criada, ela está no estado LOST. Quando for estabilizada, passa para o CONNECTED. Se houver algum problema ou precisa conectar a outro cluster do Zookeeper, vai passar para o estado SUSPENDED (comandos não podem ser rodados por essa razão) e também quando o nó não mais pertence ao quórum.

### Whatchers
Whatchers no Zookeeper requere que a função Watch seja re-configurada toda vez que ocorra um evento. No kazoo, é possível utilizar este tipo de watcher, mas também possui uma API mais simples, que não necessita desta re-configuração recorrente.

### Transictions
A versão Zookeeper 3.4 e acima permitem que sejam enviados vários comandos de uma vez que serão commitados como uma unidade. O resultado desta transação será então uma lista de sucessos e/ou falhas resultantes de cada comando desta transação. 
> Obs.: Ou todos os comandos irão falhar ou serão bem sucedidos. 

Exemplo.:
```python
from kazoo.client import KazooClient
from kazoo.client import KazooState

zk = KazooClient(hosts='127.0.0.1:2181')
zk.start()

transaction = zk.transaction()
transaction.check('/node1', version=3)
transaction.create('/node2/children2', b"a value")
results = transaction.commit()

zk.stop()
```
## :warning: Progresso :warning: 
- [X] Basic Usage
- [ ] Asynchronous Usage 
- [ ] Implementation Details
- [ ] Testing
