# Makefile - CDet C port (modular: engine + per-lattice + test harness)
CC      ?= cc
CFLAGS  ?= -O2 -Wall -std=c99
LDLIBS  := -lm

OBJ = cdet_engine.o lattices.o momfreq.o qss_det.o quad.o symmetry.o rankone.o qss_parallel.o driver.o schur.o dyndet.o anchor_duality.o cyclo_ratios.o stress.o

.PHONY: all test clean bench fast omp

# opt-in multi-core build (OpenMP). Batch determinants run across cores.
omp: CFLAGS = -O2 -fopenmp -std=c99 -Wall
omp: clean test

# opt-in aggressive optimisation (non-portable: -march=native). Compile on the
# target machine. ~1.2x on the qss kernel.
fast: CFLAGS = -O3 -march=native -funroll-loops -std=c99 -Wall
fast: clean test

all: cdet test_cdet

cdet_engine.o: cdet_engine.c cdet_engine.h
	$(CC) $(CFLAGS) -c cdet_engine.c

lattices.o: lattices.c lattices.h cdet_engine.h
	$(CC) $(CFLAGS) -c lattices.c

momfreq.o: momfreq.c momfreq.h
	$(CC) $(CFLAGS) -c momfreq.c

qss_det.o: qss_det.c qss_det.h
	$(CC) $(CFLAGS) -c qss_det.c

quad.o: quad.c quad.h
	$(CC) $(CFLAGS) -c quad.c

symmetry.o: symmetry.c symmetry.h
	$(CC) $(CFLAGS) -c symmetry.c

rankone.o: rankone.c rankone.h
	$(CC) $(CFLAGS) -c rankone.c

qss_parallel.o: qss_parallel.c qss_parallel.h driver.h dyndet.h
	$(CC) $(CFLAGS) -c qss_parallel.c

driver.o: driver.c driver.h cdet_engine.h lattices.h quad.h
	$(CC) $(CFLAGS) -c driver.c

anchor_duality.o: anchor_duality.c anchor_duality.h
	$(CC) $(CFLAGS) -c anchor_duality.c
cyclo_ratios.o: cyclo_ratios.c cyclo_ratios.h
	$(CC) $(CFLAGS) -c cyclo_ratios.c
stress.o: stress.c qss_det.h
	$(CC) $(CFLAGS) -c stress.c

schur.o: schur.c schur.h
	$(CC) $(CFLAGS) -c schur.c

dyndet.o: dyndet.c dyndet.h schur.h
	$(CC) $(CFLAGS) -c dyndet.c

cdet: main.c $(OBJ) cdet_engine.h lattices.h qss_det.h qss_parallel.h dyndet.h driver.h
	$(CC) $(CFLAGS) main.c $(OBJ) -o cdet $(LDLIBS)

test_cdet: test_cdet.c $(OBJ) cdet_engine.h lattices.h momfreq.h qss_det.h quad.h symmetry.h rankone.h qss_parallel.h
	$(CC) $(CFLAGS) test_cdet.c $(OBJ) -o test_cdet $(LDLIBS)

bench_qss: bench_qss.c qss_det.o cdet_engine.o qss_det.h cdet_engine.h
	$(CC) $(CFLAGS) bench_qss.c qss_det.o cdet_engine.o -o bench_qss $(LDLIBS)

# Build and run the verification suite against the frozen golden values
test: test_cdet
	./test_cdet

# Build and run the qss-vs-dense determinant benchmark
bench: bench_qss
	./bench_qss

bench_scaling: bench_scaling.c qss_det.o cdet_engine.o
	$(CC) $(CFLAGS) bench_scaling.c qss_det.o cdet_engine.o -o bench_scaling $(LDLIBS)
	./bench_scaling

# multi-core scaling benchmark (run on real hardware to see the speedup curve)
bench_parallel: bench_parallel.c qss_det.o cdet_engine.o lattices.o qss_parallel.o
	$(CC) -O2 -std=gnu99 bench_parallel.c qss_det.o cdet_engine.o lattices.o qss_parallel.o -o bench_parallel -lm -lpthread
	./bench_parallel


# ---- OPTIONAL Eigen dense path (needs Eigen headers) ----
# Override EIGEN_INC if Eigen is elsewhere: make eigen EIGEN_INC=/path/to/eigen
EIGEN_INC ?= /usr/include/eigen3
CXX ?= c++
CXXFLAGS ?= -O2 -std=c++14 -DEIGEN_MPL2_ONLY

dense_eigen.o: dense_eigen.cpp dense_eigen.h
	$(CXX) $(CXXFLAGS) -I$(EIGEN_INC) -c dense_eigen.cpp

test_eigen.o: test_eigen.c dense_eigen.h cdet_engine.h
	$(CC) $(CFLAGS) -c test_eigen.c

test_eigen: test_eigen.o dense_eigen.o cdet_engine.o
	$(CXX) $(CXXFLAGS) test_eigen.o dense_eigen.o cdet_engine.o -o test_eigen $(LDLIBS)

# build + run the Eigen verification/benchmark (requires Eigen headers)
eigen: test_eigen
	./test_eigen

# head-to-head qss-vs-Eigen benchmark across the three matrix regimes
bench_eigen: bench_eigen.cpp qss_det.o cdet_engine.o dense_eigen.o
	$(CXX) $(CXXFLAGS) -I/usr/include/eigen3 bench_eigen.cpp qss_det.o cdet_engine.o dense_eigen.o -o bench_eigen $(LDLIBS)
	./bench_eigen

clean:
	rm -f *.o cdet test_cdet bench_qss demo_momfreq test_eigen bench_scaling bench_parallel bench_eigen
