#!/usr/bin/python
import sys
import subprocess
import timeit


def test(module, pvname, level):
    subprocess.run(['python', 'test_step.py', module, pvname, level])


if __name__ == "__main__":
    num_calls = int(sys.argv[1])
    pvname = sys.argv[2]
    modules = sys.argv[3:]
    max_test_level = 3

    times = {}
    cmd = "test('{}', '{}', '{}')"
    for module in modules:
        print("Testing {}".format(module))
        times[module] = {}
        for level in range(max_test_level):
            print("{} test level {}...".format(module, level))
            this_cmd = cmd.format(module, pvname, level)
            duration = timeit.timeit(this_cmd, number=num_calls,
                                     setup='from __main__ import test')
            times[module][level] = duration

    print("Results for {}, {} iterations:".format(pvname, num_calls))
    for module in modules:
        print(module + ":")
        print("  import:  {}s".format((times[module][0])/num_calls))
        print("  connect: {}s".format((times[module][1] -
                                       times[module][0])/num_calls))
        print("  get:     {}s".format((times[module][2] -
                                       times[module][1])/num_calls))
