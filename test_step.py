#!/usr/bin/python
import sys
import time
import importlib
import numpy as np


def import_shim(name):
    """
    Returns an array of the functions we're expecting from the module
    we're currently testing.
    1. get_pv(pvname): returns pv object,  where the pv
                       object is fully connected
    2. get(pvobj): gets and returns the value
    3. monitor_test(pvname): sets up the object to monitor pvname and sum the
                             elements
    """
    module = importlib.import_module(name + "_benchmark")
    return [module.get_pv, module.get, module.monitor_test]


if __name__ == "__main__":
    module_name = sys.argv[1]
    pvname = sys.argv[2]
    funcs = import_shim(module_name)
    try:
        cmd = sys.argv[3]
    except IndexError:
        cmd = 'get'

    if cmd == 'monitor':
        try:
            pv, sum_array = funcs[2](pvname)
        except IndexError:
            raise RuntimeError('')
        time.sleep(5)
        print(len(sum_array))
        print(np.mean(sum_array))
    elif cmd == 'get':
        get_pv = funcs[0]
        get = funcs[1]
        t0 = time.time()
        pvobj = get_pv(pvname)
        t1 = time.time()
        value = None
        while value is None:
            value = get(pvobj)
        t2 = time.time()
        print(t1 - t0)
        print(t2 - t1)
    else:
        print("Invalid command {}".format(cmd))
