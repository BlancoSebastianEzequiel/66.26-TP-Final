#ifndef UTILS_H
#define UTILS_H

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

void init_arr(double m, double n, double off, double* a);
void print_arr(char *name, int m, int n, double *array);
int alloc_matrix(double **matrix, int m, int n);
void free_matrix(double **matrix);
void multiply_matrices(const double *a, const double *b, double *c, int n);
bool matrix_compare(const double *a, const double *b, int n);

#endif  // UTILS_H