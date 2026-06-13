CC ?= gcc
CFLAGS ?= -O2 -std=c99
all: oracle_ring gdump_ring
oracle_ring: oracle_ring.c lattices.c ../engine/cdet_engine.c
	$(CC) $(CFLAGS) -I. -I../engine oracle_ring.c lattices.c ../engine/cdet_engine.c -lm -o oracle_ring
gdump_ring: gdump_ring.c lattices.c ../engine/cdet_engine.c
	$(CC) $(CFLAGS) -I. -I../engine gdump_ring.c lattices.c ../engine/cdet_engine.c -lm -o gdump_ring
clean:
	rm -f oracle_ring gdump_ring
.PHONY: all clean
