There is some confusion and indecision over which epics python module should be used by the collaboration. We can certainly support them all, but which one should we put effort into polishing? None of them are bad, but none of them are quite satisfactory.

The modules we will compare are:
- pyepics
- caproto
- psp/pyca

Guiding principles:
1. Need mechanism to fairly compare the modules and disambiguate the stages of the run, even if it isn't "normal" operation
2. Need a normal operation simulator to check memory usage
3. Easy to test gets, harder to test puts

The first pass through this will be testing the following stages, separated as much as each individual module allows:

1. import and set up code
2. create object
3. call create_channel
4. connection callback sets an Event flag
5. call get_data and store the value

To do this fairly (eliminate caching, etc.) I will start new python processes each time and run through n stages of this process before exiting. I will create a matrix of n vs module. I will use the same pvs for the same tests. I will run the tests several times at different times of days. I will pick a large number of reps to get an average (probably 1000 or 10000).

The ultimate goal isn't to evaluate which module is currently best overall, but rather to evaluate which module has the best approach.

We should also start by defining what kinds of performance differences matter, and what kinds don't. The timings that matter most are the combined 2-4 segment and step 5, since we will be connecting to many PVs and we will be getting data often.

Let's assume a typical high-level app needs to access 10^4 PVs, and we'll actually care enough about 1% of them to get the value. A total delay of greater than 1s compared to another module is not acceptable. Therefore, if the connection difference is greater than 10^-4 s per PV or the get difference is greater than 10^-2 s per PV, we have to choose the module that is faster. If the difference is less than this threshold, especially if it is significantly less, then we have to pick the simplest implementation (more Python, less C).

The other performance difference that I care about is total process and memory usage when monitoring large waveforms, which is a reasonable proxy to monitoring lots of PVs. For this, we will monitor a detector waveform at 10Hz and check the cpu load and memory usage. We will have a monitor callback that simply sums the numpy array and saves the results to confirm that "something" is happening.
