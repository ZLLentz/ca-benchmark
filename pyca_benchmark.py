import threading
import pyca


class ConnectCallback(object):
    def __init__(self):
        self.cev = threading.Event()

    def __call__(self, is_connected):
        if is_connected:
            self.cev.set()


class GetCallback(object):
    def __init__(self):
        self.gev = threading.Event()

    def __call__(self, exception=None):
        if exception is None:
            self.gev.set()


def get_pv(pvname):
    pv = pyca.capv(pvname)
    pv.connect_cb = ConnectCallback()
    pv.getevt_cb = GetCallback()
    pv.create_channel()
    pv.connect_cb.cev.wait()
    return pv


def get(pvobj):
    pvobj.get_data()
    pvobj.getevt_cb.gev.wait()
    return pvobj.data['value']


def monitor_test(pvname):
    pass
