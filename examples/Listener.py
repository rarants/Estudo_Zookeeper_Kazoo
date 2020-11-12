from kazoo.client import KazooClient
from kazoo.client import KazooState

def my_listener(state):
    if state == KazooState.LOST:
        print("State = lost")
    elif state == KazooState.SUSPENDED:
        print("State = suspended")
    elif state == KazooState.CONNECTED:
        print("State = connected")
    else:
        print("other")


zk = KazooClient(hosts='127.0.0.1:2181')
zk.add_listener(my_listener)
zk.start()
#time.sleep(10000)
zk.stop()