from caproto.threading.client import get_pv  # NOQA


def get(pvobj):
    return pvobj.get()


def monitor_test(pvname):
    pass
