from kazoo.client import KazooClient

def  watchEvent ( event ): 
    print("Children has change")


zk = KazooClient(hosts='127.0.0.1:2181')
zk.start()

# Call my_func when the children change 
children  =  zk.get_children ( "/node2" ,  watch = watchEvent)

zk.stop()