from kazoo.client import KazooClient
import time
import psutil
import notify2


process_percent= 60
memory_percent= 80

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
    if(float(data.decode("utf-8"))>80):
        msg = "Utilizando mais de {}'%' da CPU:\t".format(memory_percent)
        with open('notify_send_cpu.txt', mode='a') as notify_log:
            notify_log.write(msg + (data.decode("utf-8")) + "'%'\n")
            notify2.init('foo')
            n = notify2.Notification("Atenção!", msg)
            n.show()

@zk.DataWatch('/disk_usage/')
def my_func(data, stat):
    print("Data is %s" % data)
    print("Version is %s" % stat.version)

@zk.DataWatch('/process_number/')
def my_func(data, stat):
    print("Data is %s" % data)
    print("Version is %s" % stat.version)
    #f = open("process_number_log.txt", "r")
    #if(f.readline() != ""):
    #    print(f.readline())
    #    print(type(f.readline()))
        #if(int(f.readline().trim("\n")) > int(data.decode("utf-8"))*process_percent/100):
        #    msg = "O número de processos aumentou em %f %:\t".format(process_percent)
        #    with open('notify_send_process.txt', mode='w') as notify_log:
        #        notify_log.write(msg + (data.decode("utf-8")) + "'%'\n")
        #        notify2.init('foo')
        #        n = notify2.Notification("Atenção!", msg)
        #        n.show()

while True:
    # Abre os arquivos de log
    memory_usage_log = open('memory_usage_log.txt', 'w')
    cpu_usage_log = open('cpu_usage_log.txt', 'w')
    disk_usage_log  = open ('disk_usage_log.txt', 'w') 
    process_number_log = open ('process_number_log.txt', 'w')

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

    memory_usage_log.close()
    cpu_usage_log.close()
    disk_usage_log.close()
    process_number_log.close()

    time.sleep(5)
zk.stop()

