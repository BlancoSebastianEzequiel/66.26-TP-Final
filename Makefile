# CONFIGURACION
################

# Extensión de los archivos a compilar (c para C, cpp o cc o cxx para C++).
ext = c


# CONFIGURACION "AVANZADA"
###########################

# Opciones para el compilador C/C++ para tratamiento de errores y warnings.
CFLAGS = -Wall -Werror -pedantic -pedantic-errors

# Opciones del cblas.
CFLAGS += -lblas

# autovectorization
AUTOVECTORIZATION += -LNO:simd[=2] -LNO:simd_verbose=ON -O2 -ftree-vectorize -ftree-vectorizer-verbose=3
# AUTOVECTORIZATION += -fopt-info-vec-all

# Ignore pragmas
IGNORE_PRAGMAS = -Wno-unknown-pragmas

# Estandar de C a usar
CSTD = c99

CFLAGS += -std=$(CSTD)
LD = $(CC)

occ := $(CC)
orm := $(RM)
old := $(LD)
RM := $(RM) -v
CC =  @echo "  CC  $@"; $(occ)
RM =  @echo "  CLEAN"; $(orm)
LD =  @echo "  LD  $@"; $(old)

cblas_sources := $(wildcard src/cblas.$(ext) src/cblas/*.$(ext) src/controller/utils.$(ext) src/controller/file.$(ext))
mmx_sources := $(wildcard src/mmx.$(ext) src/vectorization/*.$(ext) src/controller/utils.$(ext) src/controller/file.$(ext))
test_sources := $(wildcard tests/*.$(ext) src/*/*.$(ext))
test_pool_sources := $(wildcard src/controller/utils.$(ext) src/controller/file.$(ext) src/test_pool.$(ext))

# REGLAS
#########

.PHONY: all clean

all: compile_cblas compile_mmx compile_mmx_no_vec compile_test compile_test_pool

compile_test_pool:
	$(LD) $(test_pool_sources) -o test_pool $(CFLAGS)

run_test_pool:
	./test_pool
	python src/test_pool.py

compile_cblas:
	$(LD) $(cblas_sources) -o cblas $(CFLAGS)

compile_mmx:
	$(LD) $(mmx_sources) -o mmx $(CFLAGS) $(AUTOVECTORIZATION)

compile_mmx_no_vec:
	$(LD) $(mmx_sources) -o mmx_no_vec $(CFLAGS)

run_code:
	./cblas
	./mmx "vectorized blocked_dgemm_sse"
	./mmx_no_vec "not vectorized blocked_dgemm_sse"

run_valgrind_code:
	valgrind --show-leak-kinds=all --leak-check=full ./app

compile_test:
	$(LD) $(test_sources) -o test $(CFLAGS) $(IGNORE_PRAGMAS)

run_test:
	./test

run_valgrind_test:
	valgrind --show-leak-kinds=all --leak-check=full ./test

clean:
	$(RM) -f cblas mmx test test_pool

