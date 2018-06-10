# Dead simple timing of caget speeds
# Goal is to simply connect and get value from 2 PVs, record time taken for 2nd
# This cuts out all possible library "setup" time and represents the expected
# scaling per-pv cost for the object-oriented model
# We want to record two things:
#   1. time to set up the object (must steal main thread)
#   2. time to get a value back (can wait for io in a thread)
# We want to compare the following interfaces:
#   1. pyepics PV
#   2. caproto threading obj from context
#   3. caproto pyepics compat layer
#   4. pyca capv
#   5. psp Pv
import sys
import subprocess

import numpy as np

tests = ('pyepics', 'caproto_context', 'caproto_compat', 'pyca', 'psp')

if __name__ == '__main__':
    num = int(sys.argv[1])
    for i, test in enumerate(tests):
        obj_test = []
        data_test = []
        for n in range(num):
            res = subprocess.check_output(('python', 'test.py', str(i+1)),
                                             universal_newlines=True)
            spl = res.split('\n')
            obj_test.append(float(spl[0]))
            data_test.append(float(spl[1]))
        print('{} test results (average of {} tries):'.format(test, num))
        print('obj_test: {}'.format(np.mean(obj_test)))
        print('data_test: {}'.format(np.mean(data_test)))
