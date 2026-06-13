#!/usr/bin/env python3
"""
anchor_bridge.py -- the bridge retargeted (v0.57 edit, June 2026): the tau0/tau1 anchor
question from the CDet program, run through this pipeline's own instruments.

THE QUESTION (imported from the CDet sign-problem program, v90-v92): the L=6 Hubbard
deep-mu sign object has a deep-beta static position a_inf. L=6 is the hexagon/tau0-side
lattice (single-particle spectrum in Q); the leading numerical candidate sqrt(2+sqrt(2)) =
|1 - zeta_8^3| is an OCTAGON chord in Q(sqrt2) -- the tau1-side field. If that
identification held, a tau1-field constant would govern a tau0-side lattice object
(cross-anchor mixing). The CDet measurement, after its heavy-tail audit (multi-draw
errors; single-draw CLT at the cancellation floor is invalid, kurtosis ~4500):

    HONEST DEEP-BETA RECORD (L=6, (1,2,4), value-level zeros, 4-draw inter-draw errors):
      beta=48: z = 1.846  +/- 0.009    (dense grid, clean crossing)   grade A
      beta=56: z = 1.8407 +/- 0.0103   (dense grid + bootstrap)       grade A
      beta=44: z ~ 1.84   +/- 0.012    (sparse, curvature-biased)     grade B
      beta=64: UNRESOLVED (|V| below honest errors across the window) grade --
    pooled A:  a_inf = 1.8437 +/- 0.0068   (constancy beyond beta=56 unverified)

THIS MODULE'S JOB (the pipeline's own rules, applied):
  1. null_model rule: "never report a search hit without the null number next to it."
     Build the framework-expressible alphabet in the anchor window, tag each member by
     FIELD (Q = tau0-side rational; Q(sqrt2) = tau1 chord field; Q(sqrt3) = 12-gon;
     mixed), and compute (a) the look-elsewhere-corrected meaning of any candidate hit at
     the current sigma, and (b) sigma* -- the precision at which the nearest-candidate
     spacing makes an identification unique.
  2. rigid_gate (kt_triage idiom): EXTERNAL object -> density-vs-control. control_rarity
     >= 10% -> NOT RIGID ("one-of-many"), whatever the best match looks like.
  3. crossover_method rule: a stubborn O(1)/anchor is NEVER resolved by matching it to a
     dense band; the resolution is STRUCTURAL (here: derive the static's position from
     the residue/background-zero structure -- the CDet program's queued derivation) or a
     measurement below sigma*.

DIAGNOSES, does not PROVE (Cardinal Rule).
"""
from math import sqrt, cos, pi, gcd
from itertools import product

WINDOW = (1.78, 1.92)
A_INF, S_INF = 1.8437, 0.0068          # the honest pooled measurement (grade A)
Z_RECORD = {48: (1.846, 0.009), 56: (1.8407, 0.0103)}

# ---------------------------------------------------------------- alphabet
def chords(n):
    """squared-chord family of the regular n-gon: 2-2cos(2 pi k/n), k=1..n//2; return sqrt."""
    return [sqrt(2 - 2 * cos(2 * pi * k / n)) for k in range(1, n // 2 + 1)]

def build_alphabet(qmax=12, imax=4):
    """framework-expressible constants in WINDOW, field-tagged.
    Families: rationals p/q (q<=qmax)  -> field Q (tau0-side);
              r +/- c and r*c, r rational (small), c a 6/8/12-gon chord
              -> field of the chord (Q(sqrt2) for 8-gon odd chords = tau1-side;
                 Q(sqrt3) for 12-gon; Q for 6-gon)."""
    lo, hi = WINDOW
    out = {}   # value -> (label, field); dedupe by 1e-9 rounding
    def put(v, label, field):
        if lo <= v <= hi:
            key = round(v, 9)
            if key not in out:
                out[key] = (label, field)
    for q in range(1, qmax + 1):
        for p in range(int(lo * q), int(hi * q) + 2):
            if gcd(p, q) == 1:
                put(p / q, f"{p}/{q}", "Q")
    fam = {6: ("Q", chords(6)), 8: ("Q(sqrt2)", chords(8)), 12: ("Q(sqrt3)", chords(12))}
    for n, (field, cs) in fam.items():
        for ci, c in enumerate(cs, 1):
            put(c, f"chord_{n}gon[{ci}]", field)
            for a in range(-imax, imax + 1):
                for b in range(1, imax + 1):
                    put(a / b + c, f"{a}/{b}+chord_{n}[{ci}]", field if a == 0 else f"{field} (shifted)")
                    put(a / b - c, f"{a}/{b}-chord_{n}[{ci}]", field if a == 0 else f"{field} (shifted)")
                    if a != 0:
                        put(a / b * c, f"({a}/{b})*chord_{n}[{ci}]", field)
    return sorted((v, lab, f) for v, (lab, f) in out.items())

# ---------------------------------------------------------------- the gates
def nearest(alpha, x):
    return min(alpha, key=lambda t: abs(t[0] - x))

def control_rarity(alpha, sigma, k=1.0, grid=4001):
    """fraction of random positions in WINDOW landing within k*sigma of SOME alphabet
    member -- the null number that must accompany any hit (null_model rule)."""
    lo, hi = WINDOW
    vals = [t[0] for t in alpha]
    hitc = 0
    for i in range(grid):
        x = lo + (hi - lo) * i / (grid - 1)
        if any(abs(x - v) <= k * sigma for v in vals):
            hitc += 1
    return hitc / grid

def sigma_star(alpha, x, kid=2.0):
    """precision at which the nearest candidate is uniquely identified: half the gap to
    the second-nearest, divided by kid (demand the runner-up sit >= kid sigma away)."""
    ds = sorted(abs(t[0] - x) for t in alpha)
    return (ds[1] - ds[0]) / (2 * kid), ds[0], ds[1]

def run():
    print("=" * 76)
    print("ANCHOR BRIDGE -- the tau0/tau1 question through the pipeline's own gates")
    print("=" * 76)
    alpha = build_alphabet()
    print(f"alphabet: {len(alpha)} framework-expressible constants in {WINDOW} "
          f"(rationals q<=12; 6/8/12-gon chords +/-/* small rationals), field-tagged")
    dens = len(alpha) / (WINDOW[1] - WINDOW[0])
    print(f"density: {dens:.0f} per unit -> mean spacing {1/dens*1000:.2f} e-3")
    v, lab, fld = nearest(alpha, A_INF)
    ns = abs(v - A_INF) / S_INF
    print(f"\nmeasured a_inf = {A_INF} +/- {S_INF}")
    print(f"nearest alphabet member: {lab} = {v:.5f}  [{fld}]  at {ns:.2f} sigma")
    top = sorted(alpha, key=lambda t: abs(t[0] - A_INF))[:6]
    print("candidate table (sigma):")
    for tv, tl, tf in top:
        print(f"   {tl:>22s} = {tv:.5f}  [{tf:<18s}]  {abs(tv-A_INF)/S_INF:.2f}")
    r1 = control_rarity(alpha, S_INF, k=1.0)
    r2 = control_rarity(alpha, S_INF, k=2.0)
    print(f"\nNULL (the rule: never report a hit without this number):")
    print(f"   P(random window position within 1 sigma of SOME member) = {r1:.0%}")
    print(f"   P(within 2 sigma) = {r2:.0%}")
    gate = "NOT RIGID -- one-of-many" if r1 >= 0.10 else "FORCED-LIKE (rarity < 10%)"
    print(f"   rigid_gate verdict at sigma = {S_INF}: {gate}")
    ss, d1, d2 = sigma_star(alpha, A_INF)
    print(f"\nsigma* for a UNIQUE identification at this value: {ss:.4f} "
          f"(nearest gap {d1:.4f}, runner-up {d2:.4f})")
    need = control_rarity(alpha, ss, k=1.0)
    print(f"   at sigma*, null rarity would be {need:.0%}")
    print("\nVERDICT (the crossover_method rule applied):")
    print(f" - At sigma = {S_INF} the alphabet saturates the window: ANY measured value")
    print(f"   matches something. The chord hit carries ~no information at this precision;")
    print(f"   the tau0/tau1 question is OPEN, and band-matching cannot close it.")
    print(f" - Two honest routes remain: (a) measurement below sigma* ~ {ss:.4f}")
    print(f"   (multi-draw dense protocol; sample cost scales ~(0.0068/{ss:.4f})^2 = "
          f"{(S_INF/ss)**2:.0f}x the current A-pool), or")
    print(f" - (b) the STRUCTURAL route: derive the static's position from the residue /")
    print(f"   background-zero structure (the CDet queue item) -- the analogue of forcing")
    print(f"   the O(1) as a Clebsch instead of matching the band. The field tag of the")
    print(f"   DERIVED form then answers tau0-vs-tau1 exactly, with no sigma at all.")
    return dict(alphabet=len(alpha), nearest=(lab, v, fld, ns), rarity1=r1,
                sigma_star=ss, verdict="OPEN; not rigid at current sigma")

if __name__ == "__main__":
    run()
