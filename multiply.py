#Author: Daniel Pacheco
#Description: This script multiplies 2 matrices
#To run: run this script directly, no arguments needed.

import matrixUtils
import time
import numpy as np

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

if __name__ == '__main__':
    #Generate matrices
    matrixA = matrixUtils.genMatrix2(size=250, value=7)
    matrixB = matrixUtils.genMatrix2(size=250, value=6)

    #Multiply the matrices
    startTime = time.time()
    result = multiplySerial(matrixA, matrixB)
    runningTimeSerial = time.time() - startTime

    #Print results
    print("MatrixA shape: %s" % str(matrixA.shape))
    print("MatrixA subarray:")
    matrixUtils.printSubarray(matrixA, size=3)
    print("\nMatrixB shape: %s" % str(matrixA.shape))
    print("MatrixB subarray:")
    matrixUtils.printSubarray(matrixB, size=3)

    expResultShape = (matrixA.shape[0], matrixB.shape[1])
    print("\nExpected result matrix shape: %s" % str(expResultShape))
    print("Actual result matrix shape: %s" % str(result.shape))
    print("Computation Time: %.3f seconds" % runningTimeSerial)
    print("Result matrix subarray:")
    matrixUtils.printSubarray(result, size=3)
    print("\n")
    