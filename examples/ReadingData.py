from kazoo.client import KazooClient

path = "/node2/children1"
zk = KazooClient(hosts='127.0.0.1:2181')
zk.start()

# Determine if a node exists
if zk.exists(path):
    print("Founded znode!")

# Print the version of a node and its data
data, stat = zk.get(path)
print("Version: %s, data: %s" % (stat.version, data.decode("utf-8")))

# List the children
children = zk.get_children(path)
print("There are %s children with names %s" % (len(children), children))

zk.stop()