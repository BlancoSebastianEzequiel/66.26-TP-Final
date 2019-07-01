#ifndef CBLAS_DGEMM
#define CBLAS_DGEMM

#include <stdio.h>
#include <cblas.h>

/*
    The arguments provide options for how Intel MKL performs the operation.
    In this case:

    CblasRowMajor:
    Indicates that the matrices are stored in row major order, with the elements
    of each row of the matrix stored contiguously as shown in the figure above.

    CblasNoTrans:
    Enumeration type indicating that the matrices A and B should not be
    transposed or conjugate transposed before multiplication.

    m, n, k:
    Integers indicating the size of the matrices:

    A: m rows by k columns

    B: k rows by n columns

    C: m rows by n columns

    alpha:
    Real value used to scale the product of matrices A and B.

    A:
    Array used to store matrix A.

    k:
    Leading dimension of array A, or the number of elements between successive
    rows (for row major storage) in memory. In the case of this exercise the
    leading dimension is the same as the number of columns.

    B:
    Array used to store matrix B.

    n:
    Leading dimension of array B, or the number of elements between successive
    rows (for row major storage) in memory. In the case of this exercise the
    leading dimension is the same as the number of columns.

    beta:
    Real value used to scale matrix C.

    C:
    Array used to store matrix C.

    n:
    Leading dimension of array C, or the number of elements between successive
    rows (for row major storage) in memory. In the case of this exercise the
    leading dimension is the same as the number of columns.
*/

int mult(double *A, double *B, double *C, double alpha, double beta, int m, int k, int n);

#endif  // CBLAS_DGEMM