import threading
import numpy as np
import epics

epics.ca.initialize_libca()


class ConnectCallback(object):
    def __init__(self):
        self.cev = threading.Event()

    def __call__(self, *, conn, **kwargs):
        if conn:
            self.cev.set()


def get_pv(pvname):
    cb = ConnectCallback()
    pv = epics.PV(pvname, connection_callback=cb)
    cb.cev.wait()
    return pv


def get(pvobj):
    return pvobj.get(use_monitor=False)


class ArraySum(object):
    def __init__(self, pvobj):
        self.pvobj = pvobj
        self.sums = []

    def __call__(self, *, value, **kwargs):
        self.sums.append(np.sum(value))


def monitor_test(pvname):
    pv = epics.PV(pvname, auto_monitor=True)
    cb = ArraySum(pv)
    pv.add_callback(cb)
    return pv, cb.sums
