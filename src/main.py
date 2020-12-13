from kazoo.client import KazooClient
import time
import psutil

zk = KazooClient(hosts='127.0.0.1:2181')
zk.start()

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

with open('memory_usage_log.txt', 'w') as memory_usage_log, open('cpu_usage_log.txt', 'w') as cpu_usage_log, open ('disk_usage_log.txt', 'w') as disk_usage_log, open ('process_number_log.txt', 'w') as process_number_log:
    while True:
        # Obtém os dados, transforma em string, codifica para bits
        memory_usage = (str(psutil.virtual_memory())).encode()
        cpu_usage = (str(psutil.cpu_percent(1, percpu=False))).encode()
        disk_usage = (str(psutil.disk_usage('/'))).encode()
        process_number =  (str(len(psutil.pids()))).encode()

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

