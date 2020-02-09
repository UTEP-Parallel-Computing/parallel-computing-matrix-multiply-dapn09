#Author: Daniel Pacheco
#Description: This script multiplies 2 matrices
#To run: run this script directly, no arguments needed.

import matrixUtils
import time
import numpy as np
import pymp
import sys
import matplotlib.pyplot as plt

def multiplySerial(mA, mB):

    rowsA = mA.shape[0]
    rowsB = mB.shape[0]

    colsA = mA.shape[1]
    colsB = mB.shape[1]

    #for matrix multiplication colsA must equal rowsB
    if colsA != rowsB:
        raise Exception("These two matrices can't be multiplied, check shapes!!!")

    #Create resulting array
    result = [[0 for col in range(0,colsB)] for row in range(0,rowsA)]
    result = np.asarray(result)

    #populate
    for row in range(0, rowsA):
        for col in range(0, colsB):
            for i in range(0, rowsB):
                result[row][col] += mA[row][i]*mB[i][col]

    return result


def multiplyParallel(mA, mB, numThreads=4, verbose=False):

    rowsA = mA.shape[0]
    rowsB = mB.shape[0]

    colsA = mA.shape[1]
    colsB = mB.shape[1]

    #for matrix multiplication colsA must equal rowsB
    if colsA != rowsB:
        raise Exception("These two matrices can't be multiplied, check shapes!!!")

    #Create resulting array
    #result = [[0 for col in range(0,colsB)] for row in range(0,rowsA)]
    result = pymp.shared.array((rowsA, colsB), dtype="float64")
    #result = np.asarray(result)

    rowsList = []

    #populate
    with pymp.Parallel(numThreads) as p:
        for row in p.range(0, rowsA):
            for col in range(0, colsB):
                for i in range(0, rowsB):
                    result[row][col] += mA[row][i]*mB[i][col]
            rowsList.append(row)

        if verbose == True:
            print("Thread {} of {}, working on rows {} to {}".format(p.thread_num, p.num_threads, min(rowsList), max(rowsList)))

    return result

def usage():
    print("[ERROR] Check arguments, usage: \n\t$ python3 multiply.py (serial | parallel)")
    exit(1)

if __name__ == '__main__':
    #Generate matrices
    matrixA = matrixUtils.genMatrix2(size=250, value=7)
    matrixB = matrixUtils.genMatrix2(size=250, value=6)

    if len(sys.argv) != 2:
        usage()

    elif str.lower(sys.argv[1]) == 'serial':
        #Multiply the matrices
        startTime = time.time()
        result = multiplySerial(matrixA, matrixB)
        runningTimeSerial= time.time() - startTime

        #Print results
        print("MatrixA shape: %s" % str(matrixA.shape))
        print("MatrixA subarray:")
        matrixUtils.printSubarray(matrixA, size=4)
        print("\nMatrixB shape: %s" % str(matrixA.shape))
        print("MatrixB subarray:")
        matrixUtils.printSubarray(matrixB, size=4)

        expResultShape = (matrixA.shape[0], matrixB.shape[1])
        print("\nExpected result matrix shape: %s" % str(expResultShape))
        print("Actual result matrix shape: %s" % str(result.shape))
        print("Computation Time: %.3f seconds" % runningTimeSerial)
        print("Result matrix subarray:")
        matrixUtils.printSubarray(result, size=4)
        print("\n")

    elif str.lower(sys.argv[1]) == 'parallel':

        #Run in parallel with 4 threads and be verbose.
        startTime = time.time()
        print("Running in parallel with 4 threads:")
        result = multiplyParallel(matrixA, matrixB, verbose=True)
        runningTimeParallel = time.time() - startTime

        #Print results
        print("MatrixA shape: %s" % str(matrixA.shape))
        print("MatrixA subarray:")
        matrixUtils.printSubarray(matrixA, size=4)
        print("\nMatrixB shape: %s" % str(matrixA.shape))
        print("MatrixB subarray:")
        matrixUtils.printSubarray(matrixB, size=4)

        expResultShape = (matrixA.shape[0], matrixB.shape[1])
        print("\nExpected result matrix shape: %s" % str(expResultShape))
        print("Actual result matrix shape: %s" % str(result.shape))
        print("Computation Time: %.3f seconds" % runningTimeParallel)
        print("Result matrix subarray:")
        matrixUtils.printSubarray(result, size=4)
        print("\n")

        print("Running tests with 1, 2, 4, 6 & 8 threads...")
        #Save runtimes plot into a file
        threadsRunTimes = {}
        for i in range(0, 10, 2):
            startTime = time.time()
            if i==0:
                result = multiplyParallel(matrixA, matrixB, numThreads=1, verbose=False)
                runningTimeParallel = time.time() - startTime
                threadsRunTimes[1] = runningTimeParallel
            else:
                result = multiplyParallel(matrixA, matrixB, numThreads=i, verbose=False)
                runningTimeParallel = time.time() - startTime
                threadsRunTimes[i] = runningTimeParallel

        plt.style.use('ggplot')
        x_pos = [str(_) for _ in threadsRunTimes.keys()]
        plt.bar(x_pos, threadsRunTimes.values(), color='green')
        plt.xlabel("Threads")
        plt.ylabel("Time (seconds)")
        plt.title("Runtimes")
        plt.savefig("runtimes.png", format='png')

        print("Done!! Plot of test results stored in \'runtimes.png\'")

    else:
        usage()
