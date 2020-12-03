from kazoo.client import KazooClient
import time
import psutil



def node_exists(path):
    # Determine if a node exists
    if zk.exists(path):
        print("Founded znode = " + path)
    else:
        print("znode not found")



zk = KazooClient(hosts='127.0.0.1:2181')
zk.start()
#zk.create("/memory_usage/", b"oi")
#zk.create("/cpu_usage/")
#zk.create("/disk_usage/")
#zk.create("/process_number/")
memory_usage = str(psutil.virtual_memory())
memory_usage = memory_usage.encode()
zk.set("/memory_usage/", b"" + memory_usage)
data, stat = zk.get("/memory_usage")
print("Version: %s, data: %s" % (stat.version, data.decode("utf-8")))
# Check if nodes exists
node_exists("/memory_usage")
node_exists("/cpu_usage")
node_exists("/disk_usage")
node_exists("/process_number")

zk.stop()

