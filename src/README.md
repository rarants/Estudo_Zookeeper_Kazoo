# Testing_zk.py
## :clipboard: Requerimentos
Ter tudo instalado conforme o [readme.md](https://github.com/rarants/Estudo_Zookeeper_Kazoo/blob/main/README.md) e a bilioteca [psutil](https://psutil.readthedocs.io/en/latest/).
### :wrench: Instalando
- **Psutil:** `$ pip3 install psutil`
### :paperclip: [Testing_zk.py](./Testing_zk.py) 
```python
from kazoo.client import KazooClient
import psutil

def  watchEvent ( event ): 
    print("Children has change")
    
# Função responsável por buscar os parâmetros desejados (uso de memória, de cpu, de disco e o número de processos)
def search_params(p):
    p.update({"memory_usage" : psutil.virtual_memory()})
    p.update({"cpu_usage" : psutil.cpu_percent(1, percpu=True)})
    p.update({"disk_usage" : psutil.disk_usage("/")})
    p.update({"process_number" : len(psutil.pids())})

# Função para verificar se os thresholds estão sendo ultrapassados (AINDA NÃO TESTADA = é só o "algoritmo")
def check_thresholds(initial_p, p):
    # If memory_usage > 80%
    if p.get("memory_usage") > 80:
        print("ATENTION: Memory usage more than 80%!")
    # If process_number (now) > initial value found  in 10%
    if p.get("process_number") > initial_p.get("process_number") + 10:
        print("Number of process is like 10% more than initial value")

# "Variáveis"
initial_params = {
    "memory_usage": None, 
    "cpu_usage": None, 
    "disk_usage": None, 
    "process_number": None
}
params = { }
path = "/reports/"

# Iniciar uma conexão Cliente
zk = KazooClient(hosts='127.0.0.1:2181')
zk.start()

# Criar um nó pai
zk.create("/reports")

# Buscar os parâmetros e salvar em um dicionário inicial (cujos dados não irão ser alterados para referência)
# e fazer uma cópia deles para um diciconário que receberá novos valores ao passar do tempo
search_params(initial_params)
params = initial_params.copy()

# Create znode's tree, save params in znode's tree and set a watcher
for i in range (0, 4):
    zk.create(path+str(list(params.keys())[i]))
    zk.set(path+str(list(params.keys())[i]), str(list(params.values())[i]).encode('utf-8'))
    children = zk.get_children (path+str(list(params.keys())[i]),  watch = watchEvent)

# Busca constantemente os parâmetros e verifica se um threshold foi ultrapassado
 while True:
    search_params(params)
    check_thresholds(initial_params, params)

# Visualizar todos os nós filhos
# print(zk.get_children("/reports"))

# Termina a conexão
zk.stop()
```
