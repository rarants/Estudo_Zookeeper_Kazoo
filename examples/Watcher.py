from kazoo.client import KazooClient
import time

@zk.ChildrenWatch(path[1][1])
def watch_children(children):
    print("Children are now: %s" % children)
# Above function called immediately, and from then on

@zk.DataWatch(path[1][0])
def watch_node(data, stat):
    print("Version: %s, data: %s" % (stat.version, data.decode("utf-8")))

path=[["/node1"], ["/node2", "/node2/children1"]]
zk = KazooClient(hosts='127.0.0.1:2181')
zk.start()
time.sleep(10)
zk.stop()