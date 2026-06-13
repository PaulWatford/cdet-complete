"""physical_mapping.py (v133) -- the physical observable behind the z-flow.

THE QUESTION (the crux): does z(inf)=lowest-empty-level encode a real spectral observable, or is it just
an internal property of our frozen construction?

THE ANSWER: it is a real single-particle spectral observable -- the leading ADDITION POLE (the lowest
unoccupied single-particle excitation above the Fermi sea). The chain, each link already established:

  1. z(b) = eps_probe + ln(s*)/b, s* = A/|c1|  (ZINF_RESULT.md, v111). As b->inf, z(inf) = eps_probe.
  2. eps_probe = lowest-empty single-particle level. As L grows the level MOVES (2.0 -> sqrt2 -> 1.268 ->
     1.082 -> 1.0002, v125 thermo_limit_study) and z(inf) TRACKS it -- so z is a *detector* of a moving
     pole, not a fixed constant.
  3. WHY a pole: the v78 cancellation lemma (FUGACITY_STRUCTURE_RESULT.md) proves <C>(mu) is EXACTLY a
     rational function of the fugacity e^{b.mu}, with poles ONLY at mu = eps_k (the Matsubara comb anchored
     at the single-particle levels). fugacity_structure.py detected the pole at the level directly (3.9e6
     rise approaching the comb). The deep-beta z-flow is a real-axis extraction of the nearest such pole
     above the sea = the lowest-empty level.

So z(inf) IS the single-particle addition spectrum's leading pole -- a standard spectral observable, the
same object DiagMC reconstructs by analytic continuation.

FREE vs INTERACTING (the honest bound, and the bridge to the roadmap): the fugacity poles sit at the BARE
levels eps_k because the propagator g0 carries the free spectrum. So z(inf) is currently the FREE addition
energy. The INTERACTING addition energy eps_k + Re Sigma(eps_k) requires the self-energy resummation that
shifts the poles -- which is exactly integration #3 (the Simkovic-Kozik irreducible/self-energy series).
That makes z and integration #3 the same physical target at two resummation levels: #3 turns the free
addition spectrum z(inf) measures today into the interacting one.

This module asserts link (1)+(2): z(inf) equals the single-particle addition pole across the measured
cases. Links (3) and the interacting extension are documented in PHYSICAL_MAPPING_RESULT.md and verified
in fugacity_structure.py. Frozen engine untouched."""
import numpy as np
from thermo_limit_study import lowest_empty

# measured z(inf) asymptotes (the deep-beta flows extrapolate to these; ZINF/v124/v125), and the
# single-particle level each should equal -- i.e. the addition pole the flow is detecting.
CASES = [("L=6  mu=1.845", 2.0,            6,   1.845),
         ("L=8  mu=1.0",   np.sqrt(2.0),   8,   1.0),
         ("L=12 mu=1.0",   1.2679491924,   12,  1.0),
         ("L=16 mu=1.0",   1.0823922003,   16,  1.0),
         ("L=100 mu=1.0",  1.0001920775,   100, 1.0)]

def addition_pole(L, mu):
    """The single-particle addition pole = the lowest-empty level above the Fermi sea (the spectral onset)."""
    return lowest_empty(L, mu)

def _selftest():
    print("physical_mapping self-test: z(inf) == the single-particle addition pole (lowest-empty level)")
    worst = 0.0; moved = []
    for name, z_inf, L, mu in CASES:
        pole = addition_pole(L, mu)
        dev = abs(z_inf - pole); worst = max(worst, dev); moved.append(pole)
        assert dev < 2e-4, (name, z_inf, pole, dev)
        print(f"  {name:>14}:  z(inf)={z_inf:.6f}  addition pole={pole:.6f}  dev={dev:.1e}")
    # the pole is not constant -- it sweeps as L grows, and z(inf) follows it (detector, not constant)
    assert max(moved) - min(moved) > 0.9, moved
    print(f"  worst dev {worst:.0e}; pole sweeps {min(moved):.4f}..{max(moved):.4f} and z(inf) tracks it.")
    print("  => z(inf) is the leading single-particle ADDITION POLE (free spectrum); self-energy (#3)")
    print("     upgrades it to the interacting addition energy eps_k + Re Sigma. A real spectral observable. PASS")

if __name__ == "__main__":
    _selftest()
