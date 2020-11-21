# Testing_zk.py
## :clipboard: Requerimentos
Ter tudo instalado conforme o [readme.md](https://github.com/rarants/Estudo_Zookeeper_Kazoo/blob/main/README.md) e a bilioteca [psutil](https://psutil.readthedocs.io/en/latest/).
### :wrench: Instalando
- **Psutil:** `$ pip3 install psutil`
## :paperclip: [Testing_zk.py](https://github.com/rarants/Estudo_Zookeeper_Kazoo/blob/main/src/testing_zk.py) 
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
    # Se memory_usage > 80%
    if p.get("memory_usage") > 80:
        print("ATENTION: Memory usage more than 80%!")
    # Se process_number (now) > valor inicial encontrado em 10%
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

# Criar uma árvore de zenodes, salvar os parâmetros iniciais na árvore e setar um watcher # (ainda não funcional)
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
## :boom: Sobre a biblioteca [psutil](https://psutil.readthedocs.io/en/latest/)
### :zap: Funções utilizadas
- psutil.virtual_memory();
- psutil.cpu_percent(1, percpu=True);
- psutil.disk_usage("/");
- len(psutil.pids())
#### :mag_right: psutil.virtual_memory()
Retorna estatísticas sobre o uso da memória do sistema, em forma de tupla, com os seguintes campos (em bytes):
- Total: total de memória física (exclusive swap);
- Avaiable: memória que pode ser fornecida instantaneamente para processos sem que o sistema entre em swap;
- Used: memória utilizada;
- Free: memória que não está sendo utilizada que está disponível (mas não reflete a memória real disponível, que no caso, é o  parâmetro **avaiable**;
- Active: memória que está atualmente em uso ou foi recentemente utilizada (e por isso se encontra na RAM);
- Inactive: memória marcada que não está em uso;
- Buffers: cache utilizada para itens como metadados dos arquivos do sistema (file system metadata);
- Cached: cache usada para vários propósitos;
- Shared: Memória que pode ser acessada simultaneamente por vários processos;
- Slab: Cache de estruturas de dados no kernel.
#### :mag_right: psutil.cpu_percent(1, percpu=True)
Quando o percpu é True, ele retorna uma lista de tuplas nomeadas para cada CPU lógica no sistema.
Retorna um float que representa a utilização atual da CPU de todo o sistema como uma porcentagem. 
- Intervalo > 0.0: compara os tempos de CPU do sistema decorridos antes e depois do intervalo (bloqueio). 
- Intevalo = 0.0 ou None: compara os tempos de CPU do sistema decorridos desde a última chamada ou importação do módulo, retornando imediatamente. 
#### :mag_right: psutil.disk_usage(path)
Retorna estatísticas de uso do disco a respeito da partição contida no caminho dado (path), no formato de tupla, incluindo espaço total, usado e livre - expresso em bytes, mais o uso percentual do disco. 
#### :mag_right: psutil.pids()
Retorna uma lista em forma de tupla com todos os pid (process id/ ids dos processos). Ao utilizar a função len(), estamos contando quantos pids há naquele momento e, portanto, quantos processos.
#### :warning: Progresso :warning: 
- [X] Criar árvore de znodes
- [X] Coletar os dados
- [ ] Salvar os dados na árvore de znodes
- [ ] Salvar os dados no log
- [ ] Implementar verificação dos thresholds
- [ ] Implementar ação a ser tomada ao receber uma notificação do wathcer
- [ ] Realizar a análise dos dados
