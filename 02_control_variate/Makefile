CC ?= gcc
CFLAGS ?= -O2
oracle_hex: oracle_hex.c cdet_engine.c lattices.c cdet_engine.h lattices.h
	$(CC) $(CFLAGS) -I. oracle_hex.c cdet_engine.c lattices.c -lm -o oracle_hex
clean:
	rm -f oracle_hex
.PHONY: clean
