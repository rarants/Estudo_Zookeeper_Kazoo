from kazoo.client import KazooClient
import psutil

def  watchEvent ( event ): 
    print("Children has change")

def search_params(p):
    p.update({"memory_usage" : psutil.virtual_memory()})
    p.update({"cpu_usage" : psutil.cpu_percent(1, percpu=True)})
    p.update({"disk_usage" : psutil.disk_usage("/")})
    p.update({"process_number" : len(psutil.pids())})

def check_thresholds(initial_p, p):
    # If memory_usage > 80%
    if p.get("memory_usage") > 80:
        print("ATENTION: Memory usage more than 80%!")
    # If process_number (now) > initial value found  in 10%
    if p.get("process_number") > initial_p.get("process_number") + 10:
        print("Number of process is like 10% more than initial value")

# Variables
initial_params = {
    "memory_usage": None, 
    "cpu_usage": None, 
    "disk_usage": None, 
    "process_number": None
}
params = { }
path = "/reports/"

# Start the Client connection
zk = KazooClient(hosts='127.0.0.1:2181')
zk.start()

# Create parent node
zk.create("/reports")

# Search params
search_params(initial_params)
params = initial_params.copy()

# print(zk.get_children("/reports"))

# Create znode's tree, save params in znode's tree and set a watcher
for i in range (0, 4):
    zk.create(path+str(list(params.keys())[i]))
    zk.set(path+str(list(params.keys())[i]), str(list(params.values())[i]).encode('utf-8'))
    children = zk.get_children (path+str(list(params.keys())[i]),  watch = watchEvent)

# Search params and check if a threshold is trespassed
while True:
    search_params(params)
    check_thresholds(initial_params, params)

# Stop the Client connection
zk.stop()