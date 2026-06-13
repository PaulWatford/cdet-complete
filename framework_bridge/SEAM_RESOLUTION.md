# The Seam: where the Watford and Nielsen frameworks meet, and where they don't

A measured account of the transcendental boundary between the cyclotomic/modular
framework (Watford) and the Topological Unified Field Theory on the complex Hopf
fibration (Nielsen), and how it resolves under supersymmetry. Epistemic labels
follow the convention of the companion papers: [Proven] complete here, [Measured]
established by computation to stated precision, [Open] acknowledged not derived.

## The two machines
- Watford: every dimensionless quantity is 12-gon geometry — cyclotomic ladder
  values in Q(zeta_12) and their chords; the one transcendental is the nome
  |q(tau_0)| = e^{-pi sqrt 3} at the order-3 point tau_0 = omega.
- Nielsen: particles are stable knotted eigenmodes of the Beltrami operator
  B = d|xi on the complex Hopf fibration; intrinsic mass scales come from
  Gaussian functional determinants on the S^1/S^3/S^5 shells, regularized via
  spectral zeta functions.

The seam is the transcendental layer: do Nielsen's zeta-regularized determinants
live in Watford's modular world, or are they an independent transcendental?

## The bridge exists for the EVEN part [Proven mechanism + Measured]
A zeta-regularized functional determinant of a Laplacian on an elliptic/CM
geometry IS a modular form — this is the Kronecker limit formula:
        det' Delta (torus tau) = (Im tau)^2 |eta(tau)|^4.
At the order-3 anchor omega the Chowla-Selberg formula turns eta(omega) into
Gamma(1/3) values — the same Chowla-Selberg terms the Watford paper already
carries (the 0.89998 Kahler curvature, Omega_m = 0.31437). So the even-weight
spectral data folds directly into the modular forms.

Measured (PSLQ, 60 digits): the even zeta values reduce to the modular (pi) data
        zeta(2) = pi^2/6     [PSLQ relation -6, 1]
        zeta(4) = pi^4/90    [PSLQ relation -90, 1]
i.e. they ARE Watford-geometry. The even sector of Nielsen's determinants is
Watford's modular forms in a different arrangement.

## The odd part does NOT arrange in [Measured]
The odd spheres S^3, S^5 contribute odd zeta values (zeta(3), zeta(5)) to the
determinants. Tested whether zeta(3) arranges into the order-3 modular/CM data:
PSLQ over {pi^3, varpi^3, pi^2 varpi, pi varpi^2}, with the omega CM period
        varpi = Gamma(1/3)^3 / (2^{4/3} pi),
found NO integer relation to coefficient 10^12. zeta(3) is independent of the
order-3 modular data. This is not a defect of either framework: zeta(3) (Apery,
1979 — only irrationality) is conjectured not to be a period expressible through
pi and CM/Gamma values. The odd zetas are the genuinely hard transcendentals.

So the raw seam is real and located precisely: the EVEN spectral data is shared;
the ODD-zeta sector (zeta(3) from the S^3/S^5 shells) is the residue.

## The resolution: supersymmetry cancels the odd zeta [Measured]
A single field's determinant on S^3 carries zeta(3): the scalar and fermion
log-determinants run through zeta'(-2) = -zeta(3)/(4 pi^2) (verified to 45+
digits). But in a SUPERSYMMETRIC multiplet the boson and fermion contributions
cancel. Computed the SUSY-exact way (3D N=2 localization, the l-function):
        F_chiral(Delta) = l(1 - Delta),
        F_chiral(free, Delta=1/2) = l(1/2) = -(1/2) ln 2   exactly.
PSLQ of F against {1, ln 2, zeta(3)/pi^2} returns [2, 1, 0] — the zeta(3)
coefficient is identically zero. The boson's zeta(3) and the fermion's zeta(3)
cancel.

Mechanism: SUSY localization replaces the odd-zeta heat-kernel term
(zeta'(-2) -> zeta(3)) with the dilogarithm Li_2, whose special values are pi^2/6
and logarithms — EVEN data only. There is no slot left for zeta(3).

## What survives, and where it lives
The residue of the supersymmetric S^3 free energy is
        F = -(1/2) ln 2 = -(1/2) ln(k_H),
the logarithm of the Watford Higgs seed k_H = 2. After cancellation the only
transcendentals are pi-powers (even -> Watford modular forms via
Kronecker/Chowla-Selberg) and ln(k_H). The odd-zeta seam is gone.

## The seam, resolved as far as the math allows
- even spectral data  -> Watford modular forms        [Measured: zeta(2,4) reduce]
- odd spectral data zeta(3) -> NOT in the modular forms [Measured: no PSLQ relation to 1e12]
- under SUSY the odd part CANCELS, leaving even + ln(k_H) [Measured: F = -1/2 ln2, zeta(3)-free]

The bridge closes not by forcing zeta(3) into the modular forms (it genuinely will
not go) but the way the lead proposed: the supersymmetric physics never uses it.

## Status
[Proven/Measured] The cancellation mechanism: the canonical 3D N=2 chiral
multiplet on S^3 is zeta(3)-free (F = -1/2 ln 2), while its individual fields are
not. The Kronecker/Chowla-Selberg bridge for the even sector.

[Open] Whether the Nielsen construction's fields — the Beltrami eigenmodes on the
S^1/S^3/S^5 shells — assemble into exactly the supersymmetric multiplets that
trigger this cancellation. Her abstract gives the field content but not a
manifest N=2 localization structure. Confirming the shells pair up SUSY-style is
the remaining item; if they do, the transcendental bridge between the two
frameworks is complete.

## Verification
PSLQ relations and the l-function at 60-digit precision; zeta'(-2) = -zeta(3)/(4
pi^2) and l(1/2) = -(1/2) ln 2 each matched to >45 digits. Methods reproducible
from the scripts accompanying the cdet archive (the same DiagMC/determinant tools
used throughout).
