# Why Benchmark?
There is some confusion and indecision over which epics python module should be used by the collaboration. We can certainly support them all, but which one should we put effort into polishing? None of them are bad, but none of them are quite satisfactory.

## Modules to compare:
- pyepics
- caproto
- psp/pyca

## Guiding principles:
1. Need mechanism to fairly compare the modules and disambiguate the stages of the run, even if it isn't "normal" operation
2. Need a normal operation simulator to check memory usage
3. Easy to test gets, harder to test puts

## Procedure
The first pass through this will be testing the following stages:

1. import and set up code
2. create object, connect, and verify connected
3. get data and store the value
4. get data again

We will not be recording the time of step 1 because it's largely irrelevant to operation.
Step 2 gives us the scaling factor for instantiating N pv objects and having them be ready to use.
Step 3 gives us the time to get a value, plus the first-get setup time (ctrl vars, etc.)
Step 4 factors out the first-get setup time

Ideally I would test the clients with finer granularity, but different PV object interfaces don't allow the user to decide to not connect, not wait for connection, etc.

To do this fairly (eliminate caching, etc.) I will start new python processes each time and run through the whole process before exiting.

## Goals
The ultimate goal isn't to evaluate which module is currently best overall, but rather to evaluate which module has the best approach.

We should define what kinds of performance differences matter, and what kinds don't.

Let's assume a typical high-level app needs to access 10^4 PVs, and we'll actually care enough about 1% of them to get the value. A total delay of greater than 1s compared to another module is not acceptable. Therefore, if the connection difference is greater than 10^-4 s per PV or the get difference is greater than 10^-2 s per PV, we have to choose the module that is faster. If the difference is less than this threshold, especially if it is significantly less, then we have to pick the simplest implementation (more Python, less C).

The other performance difference that I care about is total process and memory usage when monitoring large waveforms, which is a reasonable proxy to monitoring lots of PVs. For this, we will monitor a detector waveform at 10Hz and check the cpu load and memory usage. We will have a monitor callback that simply sums the numpy array and saves the results to confirm that "something" is happening.

# Results
## Get test: time elapsed (s)
Module | Connect | Get 1 | Get 2
--- | --- | --- | ---
pyca | 2.84e-2 | 3.04e-4 | 2.09e-5
psp | 2.85e-2 | 7.83e-4 | 4.59e-4
pyepics | 2.92e-2 | 1.25e-3 | 6.42e-4
caproto | 1.03e-1 | 7.16e-4 | 6.07e-4
### Methodology
- Import everything, special module init, start timer
- Create PV object, connect, wait for connection, record time
- Get pv, check value, record time
- Get pv, check value, record time
### Comments
- Performance penalty of using caproto's threading interface (pyepics-like) at application initialization is about 0.07s per PV compared to the other modules
- All of these interfaces can create PVs faster than this if you distribute the connection task across threads or wait asynchronously.
- This benchmark completely ignores the fact that caproto has performance gains in real applications by leveraging better async support. I only checked the threading interface here due to the easier comparison.
- The differences in get times are completely insignificant in all cases. The performance win here by pyca is never felt by the user.

## Monitor test: cpu usage
Module | Mean | Median | Max | Min
--- | --- | --- | --- | ---
psp | 28.78 | 29.5 | 32.6 | 24.8
pyepics | 32.29 | 31.9 | 38.4 | 30.4
caproto | 78.06 | 77.8 | 81.8 | 76.8
### Methodology
- Start monitoring the PV, sum the array to ensure we're getting real data
- Watch `top` and record all value changes after the initial startup spike
- PV is 120Hz, 680x480 image waveform, uint16
- Repeat and collect statistics
### Comments
- The differences between psp and pyepics here are marginal or nonexistent
- I expect that the caproto values can improve by a factor of two with some effort
- Anecdotally, with slower rates none of these libraries have any problems. Since we don't typically run image processing callbacks at 120Hz in python applications, I'm willing to call this test a wash
- I neglected to run this test for pure pyca because there appears to be an issue where callbacks are dropped if they come in too quickly, but the psp test is a nice proxy because psp is really just a python wrapper around pyca.

## Preliminary Conclusions
- pyca/psp currently has an advantage in the case where your application must create thousands of PV objects, but this has only a marginal advantage over pyepics. In all other cases, it doesn't really matter which library you use.
- caproto is very promising but isn't mature enough to start using 100%
