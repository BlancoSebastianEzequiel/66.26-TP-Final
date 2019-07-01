#ifndef UTILS_H
#define UTILS_H

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

void init_arr(double m, double n, double off, double* a);
void print_arr(char *name, int m, int n, double *array);
void multiply_matrices(const double *a, const double *b, double *c, int n);
bool matrix_compare(const double *a, const double *b, int n);
int double_to_string(char* buffer, double num, int max_bytes);

#endif  // UTILS_H