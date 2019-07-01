#include <stdbool.h>
#include "testing.h"
#include "../src/controller/utils.h"
#include "../src/cblas/cblas_dgemm.h"
#include "../src/vectorization/blocked_dgemm_sse.h"

void test_cblas_dgemm() {
    int N = 200;
    double A[N*N];
    double B[N*N];
    double C[N*N];
    double expected_result[N*N];
    double alpha = 1.0;
    double beta = 0.0;
    init_arr(N, N, 2, A);
    init_arr(N, N, 1, B);
    init_arr(N, N, 0, C);
    init_arr(N, N, 0, expected_result);
    mult(A, B, C, alpha, beta, N, N, N);
    multiply_matrices(A, B, expected_result, N);
    char msg[200] = "cblas_dgemm: matrices are equal";
    print_test(msg, matrix_compare(C, expected_result, N));
    // print_arr("A", N, N, A);
    // print_arr("B", N, N, B);
    // print_arr("C", N, N, C);
    // print_arr("expected", N, N, expected_result);
}
void test_blocked_dgemm_sse() {
    int N = 400;
    double A[N*N];
    double B[N*N];
    double C[N*N];
    double expected_result[N*N];
    init_arr(N, N, 2, A);
    init_arr(N, N, 1, B);
    init_arr(N, N, 0, C);
    init_arr(N, N, 0, expected_result);
    square_dgemm_blocked_sse(A, B, C, N, 2);
    multiply_matrices(A, B, expected_result, N);
    char msg[200] = "blocked_dgemm_sse: matrices are equal";
    print_test(msg, matrix_compare(C, expected_result, N));
    // print_arr("A", N, N, A);
    // print_arr("B", N, N, B);
    // print_arr("C", N, N, C);
    // print_arr("expected", N, N, expected_result);
}

int main() {
    test_cblas_dgemm();
    test_blocked_dgemm_sse();
    return 0;
}