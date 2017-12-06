from psp import PV


def get_pv(pvname):
    pv = PV(pvname)
    pv.connect()
    pv._Pv__con_sem.wait()
    return pv


def get(pvobj):
    return pvobj.get()


def monitor_test(pvobj):
    pass
