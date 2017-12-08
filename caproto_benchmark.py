import numpy as np
from caproto.threading.client import get_pv  # NOQA


def get(pvobj):
    return pvobj.get(use_monitor=False)


class ArraySum(object):
    def __init__(self, pvobj):
        self.pvobj = pvobj
        self.sums = []

    def __call__(self, *, value, **kwargs):
        self.sums.append(np.sum(value))


def monitor_test(pvname):
    pv = get_pv(pvname, auto_monitor=True)
    cb = ArraySum(pv)
    pv.add_callback(cb)
    return pv, cb.sums
