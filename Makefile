# CONFIGURACION
################

# Extensión de los archivos a compilar (c para C, cpp o cc o cxx para C++).
extension = c

# Si usa funciones de math.h, descomentar (quitar el '#' a) la siguiente línea.
math = si

# Descomentar si se quiere ver como se invoca al compilador
#verbose = si


# CONFIGURACION "AVANZADA"
###########################

# Opciones para el compilador C/C++ para tratamiento de errores y warnings.
CFLAGS = -Wall -Werror -pedantic -pedantic-errors

# Para optimizar el binario resultante lo mejor posible
CFLAGS += -O3

# Para valgrind o debug
CFLAGS += -ggdb -DDEBUG -fno-inline

# Opciones del cblas.
LDFLAGS += -lblas

# Estandar de C a usar
CSTD = c99

# Linkea con libm de ser necesario.
ifdef math
LDFLAGS += -lm
endif

# Se reutilizan los flags de C para C++ también
CXXFLAGS += $(CFLAGS)

CFLAGS += -std=$(CSTD)
LD = $(CC)

occ := $(CC)
ocxx := $(CXX)
orm := $(RM)
old := $(LD)
ifdef verbose
RM := $(RM) -v
else
CC =  @echo "  CC  $@"; $(occ)
CXX = @echo "  CXX $@"; $(ocxx)
RM =  @echo "  CLEAN"; $(orm)
LD =  @echo "  LD  $@"; $(old)
endif

sources := $(wildcard src/*.$(extension) src/*/*.$(extension))
test_sources := $(wildcard tests/*.$(extension) src/*/*.$(extension))

# REGLAS
#########

.PHONY: all clean

all: compile_code compile_test

files:
	$(test_sources)

compile_code:
	$(LD) $(sources) -o app $(LDFLAGS)

run_code:
	./app

compile_test:
	$(LD) $(test_sources) -o test $(LDFLAGS)

run_test:
	./test

clean:
	$(RM) -f app test

