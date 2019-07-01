#include "testing.h"
#include <stdio.h>

static int _failure_count;

void real_print_test(const char* message, bool ok, const char* file,
        int line, const char* failed_expr) {
    if (ok) {
        printf(GREEN"%s... OK\n"RESET, message);
    } else {
        printf(RED"%s: ERROR\n"  "%s:%d: %s\n"RESET, message, file, line, failed_expr);
    }
    fflush(stdout);
    _failure_count += !ok;
}

int failure_count() {
    return _failure_count;
}
