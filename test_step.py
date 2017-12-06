#!/usr/bin/python
import sys
import importlib

def import_shim(name):
    """
    Returns an array of the four functions we're expecting from the module
    we're currently testing.
    1. get_pv(pvname): returns (pv object, conn Event) where the pv
                       object is set up to mark the Event flag at the
                       appropriate time.
    2. connect(pvobj): starts connecting the pv object
    3. get(pvobj): gets and returns the value
    4. monitor_test(pvname): sets up the object to monitor pvname and sum the
                             elements
    """
    module = importlib.import_module(name + "_benchmark")
    return [module.get_pv, module.connect, module.get, module.monitor_test]

if __name__ == "__main__":
    module_name = sys.argv[1]
    pvname = sys.argv[2]
    test_level = int(sys.argv[3])
    if test_level > 0:
        funcs = import_shim(module_name)
        get_pv = funcs[0]
        connect = funcs[1]
        get = funcs[2]
    if test_level > 1:
        pvobj, conn_ev = get_pv(pvname)
    if test_level > 2:
        connect(pvobj)
    if test_level > 3:
        conn_ev.wait()
    if test_level > 4:
        value = None
        while value is None:
            value = get(pvobj)
