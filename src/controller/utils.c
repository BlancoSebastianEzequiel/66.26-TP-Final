#include "utils.h"

void init_arr(double m, double n, double off, double* a) {
    int i;
    for (i = 0; i < (m*n); i++) {
        a[i] = (i + 1) * off;
    }
}
void print_arr(char *name, int m, int n, double *array) {
    int i, j;
    printf("\n%s\n", name);
    for (i = 0; i < m; i++){
        for (j = 0; j < n; j++) {
            printf("%g\t", array[i+j*n]);
        }
        printf("\n");
    }
}

int alloc_matrix(double **matrix, int m, int n) {
    *matrix = (double *) malloc(m * n * sizeof(double));
    if (*matrix == NULL) {
        printf("\n ERROR: Can't allocate memory for matrices. Aborting... \n\n");
        free(*matrix);
        return 1;
    }
    return 0;
}

void free_matrix(double **matrix) {
    free(*matrix);
}

void multiply_matrices(const double *a, const double *b, double *c, int n) {
    int i, j, k;
    for (i = 0; i < n; i++) {
        for (j = 0; j < n; j++) {
            for (k = 0; k < n; k++) {
                c[i+k*n] = c[i+k*n] + a[i+j*n] * b[j+k*n];
            }
        }
    }
}

bool matrix_compare(const double *a, const double *b, int n) {
    int i, j;
    for (i = 0; i < n; i++) {
        for (j = 0; j < n; j++) {
            if (a[i+j] != b[i+j]) {
                return false;
            }
        }
    }
    return true;
}
