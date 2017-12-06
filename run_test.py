#!/usr/bin/python
import sys
import subprocess  # NOQA
import timeit


if __name__ == "__main__":
    max_test_level = sys.argv[1]
    pvname = sys.argv[2]
    modules = sys.argv[3:]

    times = {}
    cmd = 'subprocess.run([python, test_step.py, {}, {}, {}])'
    for module in modules:
        times[module] = {}
        for level in range(max_test_level):
            this_cmd = cmd.format(module, pvname, level)
            duration = timeit.timeit(this_cmd, number=10000)
            times[module][level] = duration

    print(times)
