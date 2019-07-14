#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "controller/utils.h"
#include "vectorization/blocked_dgemm_sse.h"
#include "controller/file.h"

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

int main(int argc, char **argv) {
    if (argc != 2) {
        return 1;
    }
    char* program_name = argv[1];
    char* attributes[4] = {
            "program",
            "time_elapsed",
            "matrix_dim",
            "number_of_threads"
    };
    file_t* file = create_file("src/data/dgemm.csv", "a", attributes, 4);
    int N = 400;
    double A[N*N];
    double B[N*N];
    double C[N*N];
    double elapsed_seconds;
    char elapsed_second_str[20];
    char* values[4] = {program_name, elapsed_second_str, "400", "1"};
    elapsed_seconds = run_blocked_dgemm_sse(N, A, B, C);
    double_to_string(elapsed_second_str, elapsed_seconds, 20);
    add_row(file, values, 4);
    delete(file);
    return 0;
}
