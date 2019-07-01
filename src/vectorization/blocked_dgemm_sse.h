#ifndef BLOCKED_DGEMM_SSE_H
#define BLOCKED_DGEMM_SSE_H

void basic_dgemm_sse(const double *restrict A, const double *restrict B,
        double *restrict C, int N, int block_size);
void do_block_sse(const double *A, const double *B, double *C, int i, int j,
                  int k, int N, int block_size);
void square_dgemm_blocked_sse(const double *A, const double *B, double *C,
                              int N, int block_size);

#endif  // BLOCKED_DGEMM_SSE_H
