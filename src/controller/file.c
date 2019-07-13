#include "file.h"
#include <stdlib.h>
#include "utils.h"

file_t* create_file(char* filename, char* mode, char** attributes, int cols) {
    file_t* file = (file_t*) malloc(sizeof(file_t));
    if (!file) {
        return NULL;
    }
    file->fp = fopen(filename, mode);
    file->filename = filename;
    file->num_of_cols = cols;

    if (strcmp("a", mode) != 0) {
        char file_header[256];
        if (build_row(attributes, file_header, 256, cols) < 0) {
            delete(file);
            return NULL;
        }
        add_row(file, attributes, cols);
    }
    file->attributes = attributes;
    file->num_of_rows = 0;
    return file;
}

int build_row(char **values, char *row, int max_bytes, int size) {
    int bytes = 0;
    int pos = 0;
    char* buff;
    for (int i = 0; i < size; i++) {
        buff = (row)+pos;
        if (i == size-1) {
            bytes = snprintf(buff, max_bytes, "%s", values[i]);
        } else {
            bytes = snprintf(buff, max_bytes, "%s, ", values[i]);
        }
        if (bytes < 0) {
            return bytes;
        }
        pos += bytes;
    }
    return bytes;
}

int add_row(file_t *file, char **values, int size) {
    if (size != file->num_of_cols) {
        return 1;
    }
    char file_header[256];
    int bytes = build_row(values, file_header, 256, file->num_of_cols);
    if (bytes < 0) {
        delete(file);
        return bytes;
    }
    fprintf(file->fp,"%s\n", file_header);
    file->num_of_rows +=1;
    return 0;
}

void delete(file_t* file) {
    fclose(file->fp);
    free(file);
}
