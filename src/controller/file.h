#ifndef FILE_H
#define FILE_H

#include<stdio.h>
#include<string.h>

typedef struct file {
    FILE *fp;
    char *filename;
    char** attributes;
    int num_of_cols;
    int num_of_rows;
} file_t;

file_t* create_file(char* filename, char* mode, char** attributes, int cols);
int add_row(file_t *file, char **values, int size);
int build_row(char **values, char *row, int max_bytes, int size);
void delete(file_t* file);

#endif  // FILE_H