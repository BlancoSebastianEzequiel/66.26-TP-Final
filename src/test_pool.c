#include <time.h>
#include <stdio.h>
#include "controller/file.h"
#include "controller/utils.h"

#define SIZE 10000000

int main() {
    clock_t start, stop;
    start = clock();
    unsigned long sum = 0;
    for (unsigned long i = 0; i < SIZE; i++) {
        sum += i;
    }
    stop = clock();
    char* attributes[4] = {
            "program",
            "time_elapsed (sec)",
            "iterations",
            "number_of_threads"
    };
    file_t* file = create_file("src/data/test_pool.csv", "w+", attributes, 4);
    double elapsed_seconds = ((double)(stop - start)) / CLOCKS_PER_SEC;
    printf("Elapsed time = %lf seconds\n", elapsed_seconds);

    char elapsed_second_str[20];
    char size_str[20];
    double_to_string(elapsed_second_str, elapsed_seconds, 20);
    int_to_string(size_str, SIZE, 20);
    char* values[4] = {"c program", elapsed_second_str, size_str, "1"};
    add_row(file, values, 4);
    return 0;
}
