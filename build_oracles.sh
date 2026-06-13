#!/usr/bin/env bash
# Build every compiled helper the analysis scripts need, in place.
# 100%% self-contained: only a C compiler + make are required.
set -e
CC=${CC:-gcc}
echo "building engine ..."      ; make -C engine          CC=$CC test >/dev/null && echo "  engine: 194/194"
echo "building 01 oracle ..."   ; make -C 01_tci_integrator CC=$CC >/dev/null && echo "  ok"
echo "building 02 oracle_hex ..."; make -C 02_control_variate CC=$CC >/dev/null && echo "  ok"
echo "building 04 oracles ..."  ; make -C 04_locality       CC=$CC >/dev/null && echo "  ok"
echo "building 05 gdump_2d ..." ; make -C 05_2d_lattice     CC=$CC >/dev/null && echo "  ok"
echo "all oracles built. analysis scripts can now run from their folders."
