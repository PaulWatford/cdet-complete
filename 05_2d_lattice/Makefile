CC ?= gcc
CFLAGS ?= -O2 -std=c99
gdump_2d: gdump_2d.c lattices.c ../engine/cdet_engine.c
	$(CC) $(CFLAGS) -I. -I../engine gdump_2d.c lattices.c ../engine/cdet_engine.c -lm -o gdump_2d
clean:
	rm -f gdump_2d
.PHONY: clean

square2d_pw_demo: square2d_pw_demo.c lattices.c ../engine/cdet_engine.c
	$(CC) $(CFLAGS) -I. -I../engine square2d_pw_demo.c lattices.c ../engine/cdet_engine.c -lm -o square2d_pw_demo
