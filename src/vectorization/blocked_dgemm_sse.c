#include "blocked_dgemm_sse.h"
#include "../controller/utils.h"
/*
  In case you're wondering, dgemm stands for:
  Double-precision, GEneral Matrix-Matrix multiplication.
  A is M-by-K
  B is K-by-N
  C is M-by-N
  lda is the leading dimension of the matrix (the M of square_dgemm).
*/


void basic_dgemm_sse(const double *restrict A, const double *restrict B,
        double *restrict C, int N, int block_size) {
    unsigned i, j, k;
    for (i = 0; i < block_size; ++i) {
        for (j = 0; j < block_size; ++j) {
            double cij = C[j*N + i];
            for (k = 0; k < block_size; ++k) {
                cij += A[i + k * N] * B[k + j * N];
            }
            C[j*N + i] = cij;
        }
    }
}

void do_block_sse(const double *A, const double *B, double *C, int i, int j,
                  int k, int N, int block_size) {
    basic_dgemm_sse(A + i + k*N, B + k + j*N, C + i + j*N, N, block_size);
}

void square_dgemm_blocked_sse(const double *A, const double *B, double *C,
                              int N, int block_size) {
    unsigned bi, bj, bk;
    for (bi = 0; bi < (N / block_size); ++bi) {
        const unsigned i = bi * block_size;
        for (bj = 0; bj < (N / block_size); ++bj) {
            const unsigned j = bj * block_size;
            for (bk = 0; bk < (N / block_size); ++bk) {
                const unsigned k = bk * block_size;
                do_block_sse(A, B, C, i, j, k, N, block_size);
            }
        }
    }
}


