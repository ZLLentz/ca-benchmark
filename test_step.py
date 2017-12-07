#!/usr/bin/python
import sys
import time
import importlib


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
