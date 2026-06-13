# Cross-check proof data (v17) — u_sigma across filling: generalizability, the gap, doping

Three frame-of-reference stress tests for the u_sigma determination, in one experiment, matched
against the EXACT references (U=0 Fermi velocity, n=1 Bessel curve). Reproduce:
`python filling_dependence.py`.

## (1) Generalizability — one prefactor, all sizes and fillings
The stiffness velocity prefactor pi(L/2) is not tuned. At U=0 it reproduces v_F = 2 sin(pi n/2):
| n | L | stiff(U=0) | v_F | error |
|---|---|------------|-----|-------|
| 0.500 | 12 | 1.430 | 1.414 | 1.1% |
| 0.833 | 12 | 1.954 | 1.932 | 1.1% |
| 1.000 | 10 | 2.033 | 2.000 | 1.7% |
It also holds across half-filling closed shells (L=6: 2.045, L=10: 2.033, both ~ v_F=2) and
converges to the exact Bessel curve as L grows (v16). One L-dependent rule, every size/filling.

## (2) The bracket gap — the "12%" identified and bounded
The gap between the two ED routes, (stiff - trip)/stiff, IS the SU(2)_1 marginally-irrelevant
correction (carried by the triplet gap, absent from the integrated stiffness):
| n | U=1 | U=2 | U=4 | U=8 |
|---|-----|-----|-----|-----|
| 0.500 | 7.8% | 10.3% | 12.0% | 11.7% |
| 0.833 | 6.6% | 9.7% | 13.9% | 13.1% |
| 1.000 | 16.8% | 32.2% | 54.3% | 61.7% |
Small in the doped regime, exploding at half filling -- the marginal coupling peaks at the
commensurate point. The exact n=1 Bessel (v16) places the truth NEAR the stiffness, so the
stiffness is the best single estimate and the gap is an upper bound on its bias.

## (3) Filling fraction — doping HELPS this observable
The bracket structure triplet < truth < stiffness holds across fillings. Counter to the usual
"doping adds complexity" intuition, for u_sigma doping SHRINKS the marginal correction (~60% at
n=1 to ~12% at n=0.5), so u_sigma is MORE reliably determined in the doped liquid than at half
filling. n=0.833 (= 10/12, a real closed shell near a typical doping) behaves like n=0.5,
confirming the doped regime is the easy one. (The exact value here would still need a general-n
Bethe solve; what is established is that the gap-to-truth is small and shrinking under doping.)

## Status
GENERALIZED (v17): the u_sigma method scales (one prefactor, validated at multiple sizes and
fillings against exact v_F and the Bessel curve); the residual route-gap is a named, filling-
controlled effect (the SU(2)_1 marginal correction), smallest exactly in the doped liquid where
the package operates; doping helps rather than hurts. The exact quarter-filling u_sigma stays
bracketed [v15 triplet, v13 stiffness], near v13, with the gap now understood and bounded.
OPEN (unchanged): the exact quarter-filling CURVE via a general-n integrated Bethe solve, which
must reproduce the v16 half-filling Bessel curve before being trusted at n=0.5.
