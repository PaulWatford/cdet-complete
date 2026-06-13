CC ?= gcc
CFLAGS ?= -O2 -std=c11
ENG=../engine
SRC=$(ENG)/lattices.c $(ENG)/cdet_engine.c $(ENG)/quad.c $(ENG)/schur.c $(ENG)/rankone.c $(ENG)/symmetry.c

all: cdet2d cdet_small mc2d cdet_vs_naive isign
cdet2d: cdet2d.c $(SRC)
	$(CC) $(CFLAGS) -I. -I$(ENG) cdet2d.c $(SRC) -lm -o cdet2d
cdet_small: cdet_small.c $(SRC)
	$(CC) $(CFLAGS) -I. -I$(ENG) cdet_small.c $(SRC) -lm -o cdet_small
mc2d: mc2d.c $(SRC)
	$(CC) $(CFLAGS) -I. -I$(ENG) mc2d.c $(SRC) -lm -o mc2d
cdet_vs_naive: cdet_vs_naive.c $(SRC)
	$(CC) $(CFLAGS) -I. -I$(ENG) cdet_vs_naive.c $(SRC) -lm -o cdet_vs_naive
isign: isign.c $(SRC)
	$(CC) $(CFLAGS) -I. -I$(ENG) isign.c $(SRC) -lm -o isign
validate: cdet_small
	PYTHONPATH=. python3 validate2d.py
mc-validate: mc2d
	PYTHONPATH=. python3 mc_validate.py
sign: mc2d
	PYTHONPATH=. python3 characterize_sign.py
buy-orders: cdet_vs_naive
	PYTHONPATH=. python3 buy_orders.py
scaling: mc2d
	PYTHONPATH=. python3 scaling_law.py
robust: mc2d isign
	PYTHONPATH=. python3 robust_observables.py
shell: mc2d
	PYTHONPATH=. python3 shell_collapse.py
scales: mc2d
	PYTHONPATH=. python3 scales.py
thermal: mc2d
	PYTHONPATH=. python3 thermal_tests.py
shift:
	PYTHONPATH=. python3 shifted_expansion.py
counterterm: cdet_small
	PYTHONPATH=. python3 counterterm_shift.py
sampler:
	PYTHONPATH=. python3 counterterm_sampler.py
signtradeoff: mc2d
	PYTHONPATH=. python3 sign_tradeoff.py
clean:
	rm -f cdet2d cdet_small mc2d cdet_vs_naive isign
.PHONY: all validate mc-validate sign buy-orders scaling robust shell scales thermal shift counterterm sampler signtradeoff clean
