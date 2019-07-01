#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "cblas/cblas_dgemm.h"
#include "controller/utils.h"
#include "vectorization/blocked_dgemm_sse.h"
#include "controller/file.h"

double run_cblas_dgemm(int N, double* A, double* B, double* C) {
    clock_t start, stop;
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
    return elapsed_seconds;
}

double run_blocked_dgemm_sse(int N, double* A, double* B, double* C) {
    clock_t start, stop;
    init_arr(N, N, 2, A);
    init_arr(N, N, 1, B);
    init_arr(N, N, 0, C);
    start = clock();
    square_dgemm_blocked_sse(A, B, C, N, 2);
    stop = clock();
    double elapsed_seconds = ((double)(stop - start)) / CLOCKS_PER_SEC;
    printf("Elapsed time = %lf seconds\n", elapsed_seconds);
    return elapsed_seconds;
}

int main() {
    char* attributes[4] = {
            "program",
            "time_elapsed",
            "matrix_dim",
            "number_of_threads"
    };
    file_t* file = create_file("src/data/dgemm.csv", "w+", attributes, 4);
    int N = 400;
    double A[N*N];
    double B[N*N];
    double C[N*N];
    double elapsed_seconds;


    char elapsed_second_str[20];
    char* values[4] = {"cblas_dgemm", elapsed_second_str, "500", "1"};

    elapsed_seconds = run_cblas_dgemm(N, A, B, C);
    double_to_string(elapsed_second_str, elapsed_seconds, 20);
    add_row(file, values, 4);

    elapsed_seconds = run_blocked_dgemm_sse(N, A, B, C);
    double_to_string(elapsed_second_str, elapsed_seconds, 20);
    values[0] = "blocked_dgemm_sse";
    values[1] = elapsed_second_str;
    add_row(file, values, 4);
    delete(file);
    return 0;
}
