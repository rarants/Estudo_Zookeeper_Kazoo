from kazoo.client import KazooClient
import time
import psutil



zk = KazooClient(hosts='127.0.0.1:2181')
zk.start()
@zk.DataWatch('/memory_usage/')
def my_func(data, stat):
    print("Data is %s" % data)
    print("Version is %s" % stat.version)


while True:
    memory_usage = (str(psutil.virtual_memory())).encode()#Obtem os dados, transforma em string, codifica para bits
    cpu_usage = (str(psutil.cpu_percent(1, percpu=False))).encode()
    disk_usage = (str(psutil.disk_usage('/'))).encode()
    process_number =  (str(len(psutil.pids()))).encode()
    zk.set("/memory_usage/", b"" + memory_usage)
    zk.set("/cpu_usage/", b"" + cpu_usage)
    zk.set("/disk_usage/", b"" + disk_usage)
    zk.set("/process_number/", b"" + process_number )

    #data, stat = zk.get("/memory_usage")
    #print("Version: %s, data: %s" % (stat.version, data.decode("utf-8")))
    #data, stat = zk.get("/cpu_usage")
    #print("Version: %s, data: %s" % (stat.version, data.decode("utf-8")))
    #data, stat = zk.get("/disk_usage")
    #print("Version: %s, data: %s" % (stat.version, data.decode("utf-8")))
    #data, stat = zk.get("/process_number")
    #print("Version: %s, data: %s" % (stat.version, data.decode("utf-8")))


    time.sleep(5)



zk.stop()

