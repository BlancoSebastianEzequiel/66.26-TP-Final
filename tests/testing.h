#ifndef TESTING_H
#define TESTING_H

#include <stdbool.h>

#define RED     "\x1b[31m"
#define GREEN   "\x1b[32m"
#define RESET   "\x1b[0m"

// Imprime el mensaje seguido de OK o ERROR y el número de línea. Contabiliza el
// número total de errores en una variable interna. Ejemplo:
#define print_test(message, expression) \
  do { \
    real_print_test(message, expression, __FILE__, __LINE__, #expression); \
  } while (0)

// Función auxiliar para print_test(). No debería ser usada directamente.
void real_print_test(const char* message, bool ok,
                     const char* file, int line, const char* failed_expr);

// Devuelve el número total de errores registrados por print_test().
int failure_count(void);

#endif // TESTING_H
