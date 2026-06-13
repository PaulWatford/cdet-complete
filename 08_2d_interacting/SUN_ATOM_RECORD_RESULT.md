# Queue #2 (SU(N)), step 1: the atom EoS and the N-polynomial record (v142)

Kozik's 2024 CoS computes the SU(N) Hubbard equation of state (the N=6 ¹⁷³Yb experiment) at a cost
**independent of N**: the diagram kernel is N-independent, and the connectivity record carries N as a
polynomial (each closed flavor loop = one factor of N). This step establishes that structure on the
exactly-solvable SU(N) atom — the anchor for the lattice EoS to come.

## The SU(N) atom

Single site, N flavors, H = −μ Σ n_a + U Σ_{a<b} n_a n_b. The energy depends only on the occupation k:
E_k = −μk + U·k(k−1)/2, degeneracy C(N,k). At U=0 the flavors are independent, so k ~ Binomial(N, p),
p = e^{βμ}/(1+e^{βμ}).

## The record (verified)

The linked-cluster object ln Z(U) is where the N-structure is visible (the per-flavor density is a ratio and
is *not* polynomial in N; ln Z is). Its U-coefficients are c_j = κ_j(Y)·(−β)^j/j!, where Y_k = k(k−1)/2 is the
interacting-pair count and κ_j is its j-th cumulant under the U=0 binomial. Because binomial factorial moments
are polynomials in N, **each c_j(N) is an exact polynomial in N of degree j+1**.

| check | result |
|---|---|
| exact-cumulant ln Z coeffs vs ED contour (N=3) | 2.2e-11 |
| c_j(N) degree-(j+1) polynomial: N=2..7 → predict N=8,9,10 | 4.8e-9 |
| SU(6) atom per-flavor density at U=1 (Yb flavor number) | 0.308978 |

So: compute the N-independent cumulant kernel once, evaluate the polynomial at any flavor number N — the CoS
N-independence, demonstrated on the atom.

## Open (step 2)

The **lattice** SU(N) connected determinant, where the record is the closed-loop count of the actual diagrams
(this reuses the v132 fast minors). The atom fixes the N-polynomial principle and the EoS anchor; the lattice
EoS toward the N=6 ¹⁷³Yb curve is the next step.

Reproduce: `python3 sun_atom_record.py`. ED/closed form is the anchor only; frozen engine untouched (194/194).
