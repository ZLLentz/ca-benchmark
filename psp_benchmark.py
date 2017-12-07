from psp import PV


def get_pv(pvname):
    pv = PV(pvname)
    pv.connect()
    pv._Pv__con_sem.wait()
    return pv


def get(pvobj):
    return pvobj.get()


class ArraySum(object):
    def __init__(self, pvobj):
        self.pvobj = pvobj
        self.sums = []

    def __call__(self, exception=None):
        if exception is None:
            data = self.pvobj.data['value']
            sums.append(np.sum(data))


def monitor_test(pvname):
    pv = PV(pvname, initialize=True, monitor=True)
    pv.wait_ready()
    pv.use_numpy=True
    cb = ArraySum(pv)
    pv.add_monitor_callback(cb)
    return pv, cb.sums
