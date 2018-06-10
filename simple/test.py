# One step of the timing test
# Do this in subprocess to cut out potential caching
import sys
import time

from epics import PV as PyepicsPV
from caproto.threading.client import Context as CaprotoContext
from caproto.threading.pyepics_compat import PV as CaprotoPV
from pyca import capv as PycaPV
from psp.Pv import Pv as PspPV

# Yes, I appreciate the irony of using caproto as the server here
pvnamea = 'simple:A'
pvnameb = 'simple:B'


def base_test(cls):
    pva = cls(pvnamea)
    val = pva.get()
    start = time.time()
    pvb = cls(pvnameb)
    mid = time.time()
    val = pvb.get()
    end = time.time()
    print(mid-start)
    print(end-mid)


def pyepics_test():
    base_test(PyepicsPV)


def caproto_context_test():
    ctx = CaprotoContext()
    pva, = ctx.get_pvs(pvnamea)  # Ignore bulk conn option
    pva.read()
    start = time.time()
    pvb, = ctx.get_pvs(pvnameb)
    mid = time.time()
    val = pvb.read()
    end = time.time()
    print(mid-start)
    print(end-mid)


def caproto_compat_test():
    base_test(CaprotoPV)


def pyca_test():
    pva = PycaPV(pvnamea)
    pva.create_channel()
    while True:
        try:
            pva.get_data(False, 1.0, 1)
            break
        except Exception:
            pass
    val = pva.data['value']
    start = time.time()
    pvb = PycaPV(pvnameb)
    pvb.create_channel()
    mid = time.time()
    while True:
        try:
            pvb.get_data(False, 1.0, 1)
            break
        except Exception:
            pass
    val = pvb.data['value']
    end = time.time()
    print(mid-start)
    print(end-mid)


def psp_test():
    base_test(PspPV)


if __name__ == '__main__':
    arg = sys.argv[1]
    if arg == '1':
        pyepics_test()
    elif arg == '2':
        caproto_context_test()
    elif arg == '3':
        caproto_compat_test()
    elif arg == '4':
        pyca_test()
    elif arg == '5':
        psp_test()
