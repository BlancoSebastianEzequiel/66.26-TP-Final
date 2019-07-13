#include <time.h>
#include <stdio.h>

#define SIZE 1000000000
// #define SIZE 1000000

int main() {
    clock_t start, stop;
    unsigned long sum = 0;
    for (unsigned long i = 0; i < SIZE; i++) {
        sum += i;
    }
    start = clock();
    stop = clock();
    double elapsed_seconds = ((double)(stop - start)) / CLOCKS_PER_SEC;
    printf("Elapsed time = %lf seconds\n", elapsed_seconds);
    return 0;
}
