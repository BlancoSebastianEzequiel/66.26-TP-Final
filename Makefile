# CONFIGURACION
################

# Extensión de los archivos a compilar (c para C, cpp o cc o cxx para C++).
extension = c


# CONFIGURACION "AVANZADA"
###########################

# Opciones para el compilador C/C++ para tratamiento de errores y warnings.
CFLAGS = -Wall -Werror -pedantic -pedantic-errors

# Opciones del cblas.
CFLAGS += -lblas

# autovectorization
AUTOVECTORIZATION += -O2 -ftree-vectorize -ftree-vectorizer-verbose=3
# AUTOVECTORIZATION += -fopt-info-vec-all

# Estandar de C a usar
CSTD = c99

CFLAGS += -std=$(CSTD)
LD = $(CC)

occ := $(CC)
ocxx := $(CXX)
orm := $(RM)
old := $(LD)
RM := $(RM) -v
CC =  @echo "  CC  $@"; $(occ)
CXX = @echo "  CXX $@"; $(ocxx)
RM =  @echo "  CLEAN"; $(orm)
LD =  @echo "  LD  $@"; $(old)

sources := $(wildcard src/*.$(extension) src/*/*.$(extension))
cblas_sources = $(filter-out src/vectorization/* src/test_pool.$(extension) src/mmx.$(extension), $(sources))
mmx_sources = $(filter-out src/cblas/* src/test_pool.$(extension) src/cblas.$(extension), $(sources))
test_sources := $(wildcard tests/*.$(extension) src/*/*.$(extension))
test_pool_sources := $(wildcard src/controller/utils.h src/controller/utils.c src/controller/file.h src/controller/file.c src/test_pool.$(extension))

# REGLAS
#########

.PHONY: all clean

all: compile_cblas compile_mmx compile_test test_pool

test_pool:
	$(LD) $(test_pool_sources) -o test_pool $(CFLAGS)

run_test_pool:
	./test_pool
	python src/test_pool.py

compile_cblas:
	$(LD) $(cblas_sources) -o cblas $(CFLAGS)

compile_mmx:
	$(LD) $(mmx_sources) -o mmx $(CFLAGS) $(AUTOVECTORIZATION)

run_code:
	./cblas
	./mmx

run_valgrind_code:
	valgrind --show-leak-kinds=all --leak-check=full ./app

compile_test:
	$(LD) $(test_sources) -o test $(CFLAGS)

run_test:
	./test

run_valgrind_test:
	valgrind --show-leak-kinds=all --leak-check=full ./test

clean:
	$(RM) -f cblas mmx test test_pool

