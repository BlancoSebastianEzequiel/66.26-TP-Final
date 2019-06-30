#include "cblas_dgemm.h"

int mult(double *A, double *B, double *C, double alpha, double beta, int m, int k, int n) {
    cblas_dgemm(CblasRowMajor, CblasNoTrans, CblasNoTrans, m, n, k, alpha, A, k, B, n, beta, C, n);
    return 0;
}