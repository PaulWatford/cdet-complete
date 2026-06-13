# "Half-integer" lattices: twisted BC and rectangular supercells (v175)

**Question (Paul).** Is it possible to make lattices that are half-integer?

**Answer.** Not as a site count -- a periodic lattice needs an integer number of sites. But "half-integer" has two
precise, standard meanings, and using them resolves what the v173 tide and v174 sieve actually are.

**(A) Twisted boundary conditions.** Single-particle momenta become k = 2*pi*(n+theta)/L, where theta in [0,1) is a flux
through the torus. theta=0 is periodic; **theta=1/2 is anti-periodic -- the literal half-integer, half-shifted grid.**
This is physical and standard (twist-averaging is a routine finite-size technique).

**(B) Rectangular / tilted supercells.** An Lx x Ly cell has momentum-transfer grid (2*pi*mx/Lx, 2*pi*my/Ly) -- a
non-square, effectively non-integer linear resolution.

**Do they heal the tide/sieve? A clean verdict (beta=5, mu=-0.6, peak q*=(0.783,1.000)pi).**

| construction | error vs TD wall | healed? |
|---|---|---|
| square 17x17 (periodic)            | 0.063  | -- |
| square 17x17 (anti-periodic θ=1/2) | 0.063  | no |
| square 17x17 (twist-averaged 4×4)  | 0.058  | no (~7%) |
| **rectangular 23x46** (prime dim)  | **0.0004** | **yes** |

- **Twist does NOT heal it.** In the particle-hole susceptibility the twist cancels in k -> k+q differences, so the
  momentum-TRANSFER grid q = 2*pi*m/L is theta-INDEPENDENT (verified: the peak q-index is identical for theta=0 and
  theta=1/2). Anti-periodic BC therefore does not flip the even/odd parity, and twist-averaging trims the prime error by
  only ~7%. **The sieve is a q-resolution effect, not a k-quadrature one.**
- **Rectangular supercells DO heal it.** A non-square q-grid can land a point exactly on q*: 23x46 hits
  q*=(18/23, 46/46) and the error collapses to 4e-4 -- even though one dimension (23) is PRIME -- where the square 17x17
  misses by 6e-2.

**The unifying rule is Diophantine.** A lattice captures q* in a direction iff q*_comp * L / 2 is near an integer.
Composite/even L satisfy this more often when q* sits near a low-denominator rational (the v174 sieve); a rectangular
cell lets you satisfy it per-direction for any size. Sizes with q*_x L/2 near an integer have small error (0.008) vs far
(0.017).

**Conclusion.** The tide (v173) and the prime sieve (v174) are finite-size SAMPLING artifacts of the q-grid relative to
the nesting vector q* -- not properties of the true thermodynamic-limit wall. The right cure is not a finer twist but a
supercell whose q-grid hits q*. (The deeper open probe remains whether the TRUE radius -- the complex-U branch point of
v146, beyond the RPA instability -- inherits the same structure.)

**Validation (pre-registered gates, all pass).** (1) anti-periodic doesn't flip the parity and the peak q-index is
theta-independent; (2) twist-averaging leaves the prime error > 0.7x; (3) rectangular 23x46 error < 0.01 while 17x17 >
0.05; (4) Diophantine: q*_x L/2 near integer => smaller error. Frozen reference engine untouched (194/194).
`wall_twist.py`, `cdet twist`.
