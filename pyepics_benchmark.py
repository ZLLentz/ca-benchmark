import threading
import epics


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
    return pvobj.get()


def monitor_test(pvname):
    pass
