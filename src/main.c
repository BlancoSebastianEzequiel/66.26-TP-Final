#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "cblas/cblas_dgemm.h"
#include "controller/utils.h"
#include "vectorization/blocked_dgemm_sse.h"

int run_cblas_dgemm() {
    clock_t start, stop;
    int N = 500;
    double A[N*N];
    double B[N*N];
    double C[N*N];
    double alpha = 1.0;
    double beta = 0.0;
    init_arr(N, N, 2, A);
    init_arr(N, N, 1, B);
    init_arr(N, N, 0, C);
    start = clock();
    mult(A, B, C, alpha, beta, N, N, N);
    stop = clock();
    double elapsed_seconds = ((double)(stop - start)) / CLOCKS_PER_SEC;
    printf("Elapsed time = %lf seconds\n", elapsed_seconds);
    return 0;
}

int run_blocked_dgemm_sse() {
    clock_t start, stop;
    int N = 500;
    double A[N*N];
    double B[N*N];
    double C[N*N];
    init_arr(N, N, 2, A);
    init_arr(N, N, 1, B);
    init_arr(N, N, 0, C);
    start = clock();
    square_dgemm_blocked_sse(A, B, C, N, 2);
    stop = clock();
    double elapsed_seconds = ((double)(stop - start)) / CLOCKS_PER_SEC;
    printf("Elapsed time = %lf seconds\n", elapsed_seconds);
    return 0;
}

int main() {
    run_cblas_dgemm();
    run_blocked_dgemm_sse();
    return 0;
}
