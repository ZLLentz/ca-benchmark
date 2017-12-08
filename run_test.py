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
    return float(lines[0]), float(lines[1]), float(lines[2])


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
        get1_list = []
        get2_list = []
        for i in range(num_calls):
            if i % 50 == 0:
                print('step {}'.format(i+1))
            output = test_once(module, pvname)
            t_conn, t_get1, t_get2 = parse_test(output)
            conn_list.append(t_conn)
            get1_list.append(t_get1)
            get2_list.append(t_get2)
        times[module]['conn'] = np.mean(conn_list)
        times[module]['get1'] = np.mean(get1_list)
        times[module]['get2'] = np.mean(get2_list)

    print("Results for {}, {} iterations:".format(pvname, num_calls))
    for module in modules:
        print(module + ":")
        print("  connect: {}s".format(times[module]['conn']))
        print("  get1:    {}s".format(times[module]['get1']))
        print("  get2:    {}s".format(times[module]['get2']))
