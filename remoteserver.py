from multiprocessing.managers import BaseManager
from multiprocessing import Lock

<<<<<<< HEAD

class MyRemoteClass:

    def __init__(self):
        self.available = {}
        self.points = {}
        self.offers = {}
        self.lock = Lock()
        self.bell = Lock()
=======
class MyRemoteClass:

    def __init__(self):
        self.available= {}
        self.points={}
        self.offers= {}
        self.lock= Lock()
>>>>>>> 458945a564918f10f066eed5711a37f30fe356bc

    def get_flag(self):
        return self.available

    def set_flag(self, pushed_bool, key):
<<<<<<< HEAD
        self.available[key] = pushed_bool
=======
        self.available[key]=pushed_bool
>>>>>>> 458945a564918f10f066eed5711a37f30fe356bc

    def get_offers(self):
        return self.offers

    def set_offers(self, pushed_list, key):
        self.offers[key] = pushed_list

    def get_points(self):
        return self.points

    def set_points(self, pushed_int, key):
<<<<<<< HEAD
        self.points[key] = pushed_int
=======
        self.points[key]=pushed_int
>>>>>>> 458945a564918f10f066eed5711a37f30fe356bc

    def acquire_lock(self):
        self.lock.acquire()

    def release_lock(self):
        self.lock.release()

<<<<<<< HEAD
    def acquire_bell(self):
        self.bell.acquire

    def release_bell(self):
        self.bell.release()
=======
>>>>>>> 458945a564918f10f066eed5711a37f30fe356bc


class MyManager(BaseManager):
    pass

<<<<<<< HEAD

remote = MyRemoteClass()

MyManager.register('sm', callable=lambda: remote)
=======
remote = MyRemoteClass()

MyManager.register('sm', callable=lambda:remote)
>>>>>>> 458945a564918f10f066eed5711a37f30fe356bc
m = MyManager(address=("127.0.0.1", 8888), authkey=b'abracadabra')
s = m.get_server()
s.serve_forever()
