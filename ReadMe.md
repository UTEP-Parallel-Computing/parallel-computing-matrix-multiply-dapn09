# Parallel Computing Matrix Multiply Report

Daniel Pacheco #80451020

## Part 1 Report

This script will implement a proof of concept script that generates and multiplies two matrices in a serial fashion (not parallel).
Once the code finishes executing it will print to console a brief report of the results similar to this:

```
MatrixA shape: (250, 250)
MatrixA subarray:
7 7
7 7

MatrixB shape: (250, 250)
MatrixB subarray:
6 6
6 6

Expected result matrix shape: (250, 250)
Actual result matrix shape: (250, 250)
Computation Time: 16.950 seconds
Result matrix subarray:
10500 10500
10500 10500
```

## Part 2 Report
The parallel implementation of the matrix multiplication algorithm makes use of the pymp module to spawn a custom number of execution threads.

#### Problems encountered
When writing the parallel implementation of the matrix multiplication algorithm, the biggest challenge was to understand which parts of the computation were parallelizable. To solve this, i first experimented with how `pymp.range(limit)` would divide a range into the number of threads. After experimenting, I noticed that pymp divides the range into non-overlapping sets of values from the `limit`. Using this insight, I decided to only implement parallelization on the rows during the computation.

#### Existing problems and bugs
No known bugs, but i would like to know how to implement further more levels of parallelization on the computation.

#### Time to complete assignment
This assignment took about 5 hours to complete, from initial insight to report writing.

#### Performance measurements
When running the parallel version of the script:
```
$ python3 multiply.py parallel
```
The program will end by running a series of performance tests using 1,2,4,6 & 8 threads. The results will be plotted and stored in a file named `runtimes.png` which will look like this:

![runtime plot] (runtimes.png)

##### Plot analysis & cpuInfoDump.sh
It can be seen on the runtimes plot, that the running time of the algorithm is halved by doubling the number of threads from 1, to 2 and then 4. However, we can observe that for a thread number greater than 4 the running times do not significantly decrease, not only that, they even increase a little bit. This can be explained perhaps by looking at the output of `cpuInfoDump.sh`:
```
model name      : Intel(R) Core(TM) i7-8750H CPU @ 2.20GHz
      4      36     216
```
We can see that the VM has only 4 cores, which means that the most efficient number of threads is one per core (4 threads). Any more threads would be have to be managed by the 4 cores, decreasing efficiency. This is my reasoning behind the performance observations.

#### Observations
While this script performs its tests with a matrix of fixed size 250 by 250, for matrices smaller than 100 by 100 the parallel implementation of matrix multiplication introduces enough overhead to become slower than the serial version of the algorithm. The gains of parallelization start to become visible with large matrices. To this end, for matrices larger than 250 by 250, the relative performances of increasing the number of threads stayed relatively constant. This observation makes sense because for a VM with 4 cores, the most efficient number of threads will generally be 4 (one thread per core).


## To Run

To run the script enter the following command, selecting for either the serial or parallel version as an argument:

```
$ cd parallel-computing-matrix-multiply-dapn09
$ python3 multiply.py (serial | parallel)
```
