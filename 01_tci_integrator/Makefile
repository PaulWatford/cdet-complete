CC ?= gcc
CFLAGS ?= -O2 -std=c99
oracle: oracle.c ../engine/cdet_engine.c ../engine/cdet_engine.h
	$(CC) $(CFLAGS) -I../engine oracle.c ../engine/cdet_engine.c -lm -o oracle
clean:
	rm -f oracle
.PHONY: clean
