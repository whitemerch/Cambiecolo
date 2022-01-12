from multiprocessing.managers import BaseManager
from multiprocessing import Lock


class MyRemoteClass:

    def __init__(self, number):
        self.available = {}
        self.offer = {}
        self.lock = Lock()
        self.bell=Lock()

    def get_flag(self):
        return self.available

    def set_flag(self, pushed_bool, key):
        self.available[key] = pushed_bool

    def get_offers(self):
        return self.offers

    def set_offers(self, pushed_list, key):
        self.offers[key] = pushed_list

    def acquire_lock(self):
        self.lock.acquire()

    def acquire_bell(self):
        self.bell.acquire

    def release_lock(self):
        self.lock.release()

    def release_bell(self):
        self.bell.release()

class MyManager(BaseManager):
    pass


remote = MyRemoteClass()

MyManager.register('sm', callable=lambda: remote)
m = MyManager(address=("127.0.0.1", 8888), authkey=b'abracadabra')
s = m.get_server()
s.serve_forever()
