from kazoo.client import KazooClient

def node_exists(path):
    # Determine if a node exists
    if zk.exists(path):
        # Do something
        print("Founded znode = " + path)

zk = KazooClient(hosts='127.0.0.1:2181')
zk.start()
# Create nodes
zk.create("/node2")
zk.create("/node2/children1")
# Check if nodes exists
node_exists("/node2")
node_exists("/node")
node_exists("/node2/children1")
zk.stop()