# Testing_zk.py
## :clipboard: Requerimentos
Ter tudo instalado conforme o [readme.md](https://github.com/rarants/Estudo_Zookeeper_Kazoo/blob/main/README.md) e a bilioteca [psutil](https://psutil.readthedocs.io/en/latest/).
### :wrench: Instalando
- **Psutil:** `$ pip3 install psutil`
## :paperclip: [main.py](https://github.com/rarants/Estudo_Zookeeper_Kazoo/blob/main/src/main.py) 
- Primeiramente, são feitos os imports. É necessário incluir a biblioteca kazoo, para poder se estabelecer uma conexão cliente com o zookeeper, a biblioteca time, para poder esperar (função sleep) um tempo especificado antes de continuar a execução e também a biblioteca psutil para fazer a busca dos dados.
```python
from kazoo.client import KazooClient
import time
import psutil
```
- Agora, estabelecemos uma conexão com o zookeeper e iniciamos
```python
zk = KazooClient(hosts='127.0.0.1:2181')
zk.start()
```
- O próximo passo é definir os watchers e as funções que serão chamadas por eles. Foi definido um watcher para cada parâmetro a ser analisado (memory_usage, cpu_usage, disk_usage e process_number))
```python
@zk.DataWatch('/memory_usage/')
def my_func(data, stat):
    print("Data is %s" % data)
    print("Version is %s" % stat.version)

@zk.DataWatch('/cpu_usage/')
def my_func(data, stat):
    print("Data is %s" % data)
    print("Version is %s" % stat.version)

@zk.DataWatch('/disk_usage/')
def my_func(data, stat):
    print("Data is %s" % data)
    print("Version is %s" % stat.version)

@zk.DataWatch('/process_number/')
def my_func(data, stat):
    print("Data is %s" % data)
    print("Version is %s" % stat.version)
```
- Foi determinado pelo grupo que os dados vistos nos watchers iriam ser salvos em logs, e, portanto, utilizamos as funçoes open e write para trabalhar com arquivos. Ao utilizar with, a linguagem entenderá que todos os comandos que estiverem dentro do with (por meio da identação do código) irão ser tratados com os arquivos abertos. Após esse trecho, a linguagem automaticamente fechará o arquivo.
```python
with open('memory_usage_log.txt', 'w') as memory_usage_log, open('cpu_usage_log.txt', 'w') as cpu_usage_log, open ('disk_usage_log.txt', 'w') as disk_usage_log, open ('process_number_log.txt', 'w') as process_number_log:
```
- Os próximos comandos irão obter os dados, utilizando as funções da biblioteca psutil para tanto.
```python
    while True:
        # Obtém os dados, transforma em string, codifica para bits
        memory_usage = (str(psutil.virtual_memory())).encode()
        cpu_usage = (str(psutil.cpu_percent(1, percpu=False))).encode()
        disk_usage = (str(psutil.disk_usage('/'))).encode()
        process_number =  (str(len(psutil.pids()))).encode()

```
- A seguir os dados recebidos são salvos nos nós correspondentes e escritos no log de busca destas informações. Após, foi determinado um tempo de espera por meio da função *sleep* da biblioteca time.
```python
        # Salva os dados no árvore e no log
        zk.set("/memory_usage/", b"" + memory_usage)
        memory_usage_log.write((memory_usage.decode("utf-8"))+'\n')

        zk.set("/cpu_usage/", b"" + cpu_usage)
        cpu_usage_log.write((cpu_usage.decode("utf-8"))+'\n')

        zk.set("/disk_usage/", b"" + disk_usage)
        disk_usage_log.write((disk_usage.decode("utf-8"))+'\n')

        zk.set("/process_number/", b"" + process_number )
        process_number_log.write((process_number.decode("utf-8"))+'\n')

        time.sleep(5)

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
- [X] Salvar os dados na árvore de znodes
- [X] Salvar os dados no log
- [ ] Implementar verificação dos thresholds
- [ ] Implementar ação a ser tomada ao receber uma notificação do wathcer
- [ ] Realizar a análise dos dados
