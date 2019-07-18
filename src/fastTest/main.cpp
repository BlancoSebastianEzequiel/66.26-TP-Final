#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <mutex>
#include <thread>
#include <chrono> 

//NOTE: THIS CODE NEEDS C++11 COMPILER TO COMPILE.

using namespace std;
int const size = 400;
int const blocks = 4;

thread myThread[blocks];

void MatrixMultiplication(int const * const * matrixA, int const * const * matrixB, int** matrixC, int from, int block){
      for(int row = from; row < block; row++){
        for(int col = 0; col < size; col++){
          for(int i=0; i < size ; i++){
            matrixC[row][col] += matrixA[row][i]*matrixB[i][col];
          }
        }
    }
}

int main()
{
    int** matrixA;
    int** matrixB;
    int** matrixC;

    matrixA = new int*[size];
    matrixB = new int*[size];
    matrixC = new int*[size];

    for(int i = 0; i<size; i++){
        matrixA[i] = new int[size];
        matrixB[i] = new int[size];
        matrixC[i] = new int[size];
    }

    //WE ARE INITIALIZING MATRICES.
    for(int i = 0; i<size; i++){
        for(int j = 0; j<size; j++){
            matrixA[i][j] = rand() % 100;;
            matrixB[i][j] = rand() % 100;;
            matrixC[i][j] = 0;
        }
    }

    auto start = std::chrono::high_resolution_clock::now();
    for(int i=0; i < blocks ; i++){
      int from = (size/blocks)*(i);
      int to = (size/blocks)*(i+1);
      myThread[i] = thread(MatrixMultiplication, matrixA, matrixB, matrixC, from, to);
    }

    for(int i=0; i < blocks ; i++){
      myThread[i].join();
    }
    auto finish = std::chrono::high_resolution_clock::now();

    std::chrono::duration<double> elapsed = finish - start;

    std::cout << "Elapsed time: " << elapsed.count() << " s\n";

    return 0;
}