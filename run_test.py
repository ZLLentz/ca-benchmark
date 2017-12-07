#!/usr/bin/python
import sys
import subprocess
import numpy as np


def test_once(module, pvname):
    pcompl = subprocess.run(['python', 'test_step.py', module, pvname],
                            stdout=subprocess.PIPE)
    return pcompl.stdout


def parse_test(txt):
    lines = txt.decode().split('\n')
    return float(lines[0]), float(lines[1])


if __name__ == "__main__":
    num_calls = int(sys.argv[1])
    pvname = sys.argv[2]
    modules = sys.argv[3:]

    times = {}
    cmd = "test('{}', '{}')"
    for module in modules:
        print("Testing {}".format(module))
        times[module] = {}
        conn_list = []
        get_list = []
        for i in range(num_calls):
            if i % 50 == 0:
                print('step {}'.format(i+1))
            output = test_once(module, pvname)
            t_conn, t_get = parse_test(output)
            conn_list.append(t_conn)
            get_list.append(t_get)
        times[module]['conn'] = np.mean(conn_list)
        times[module]['get'] = np.mean(get_list)

    print("Results for {}, {} iterations:".format(pvname, num_calls))
    for module in modules:
        print(module + ":")
        print("  connect: {}s".format(times[module]['conn']))
        print("  get:     {}s".format(times[module]['get']))
