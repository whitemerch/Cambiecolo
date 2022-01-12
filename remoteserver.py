from multiprocessing.managers import BaseManager
from multiprocessing import Lock

class MyRemoteClass:

    def __init__(self, number):
        self.available= {}
        self.offer= {}
        self.lock= Lock()

    def get_flag(self):
        return self.available

    def set_flag(self, pushed_bool, key):
        self.available[key]=pushed_bool

    def get_offers(self):
        return self.offers

    def set_offers(self, pushed_list, key):
        self.offers[key] = pushed_list

class MyManager(BaseManager):
    pass

n = int(input("Combien de joueurs dans la partie : "))
remote = MyRemoteClass(n)

MyManager.register('MyList', callable=lambda:remote)
m = MyManager(address=("127.0.0.2", 8888), authkey=b'abracadabra')
s = m.get_server()
s.serve_forever()


#_______________________________________________________________________________#
#code a copier dans client
from multiprocessing.managers import BaseManager

class MyManager(BaseManager): pass
MyManager.register('MyList')
m = MyManager(address=("127.0.0.2", 8888), authkey=b'abracadabra')
m.connect()
#_______________________________________________________________________________#
