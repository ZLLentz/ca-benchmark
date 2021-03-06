import threading
import numpy as np
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
    pvobj.get_data(False, -1.0)
    pyca.flush_io()
    pvobj.getevt_cb.gev.wait()
    return pvobj.data['value']


class ArraySum(object):
    def __init__(self, pvobj):
        self.pvobj = pvobj
        self.sums = []

    def __call__(self, exception=None):
        if exception is None:
            data = self.pvobj.data['value']
            self.sums.append(np.sum(data))


def monitor_test(pvname):
    pv = get_pv(pvname)
    pv.use_numpy=True
    pv.monitor_cb = ArraySum(pv)
    pv.subscribe_channel(7, False, pv.count())
    return pv, pv.monitor_cb.sums
