#include "utils.h"

void init_arr(double m, double n, double off, double* a) {
    int i;
    for (i = 0; i < (m*n); i++) {
        // a[i] = (i + 1) * off;
        a[i] = (i % 10) * off;
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

int double_to_string(char* buffer, double num, int max_bytes) {
    return snprintf(buffer, max_bytes, "%lf", num);
}

int int_to_string(char* buffer, int num, int max_bytes) {
    return snprintf(buffer, max_bytes, "%d", num);
}