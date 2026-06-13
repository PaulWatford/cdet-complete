# The wall is a tide: its finite-size waves (v173)

**Question (Paul).** Vary the lattice size up and down and see how the wall "tide" reacts -- work out its waves.

**Setup.** The weak-coupling wall U_c(L)=1/chi0_max(L) (v172) is a Brillouin-zone quadrature on a discrete L x L grid.
Whether the peak (nesting) momentum q* lands on a grid point depends on commensuration with L, so U_c(L) does not drift
smoothly to its thermodynamic limit -- it **oscillates like a tide**. We swept every integer L and worked out the waves.

**Wave 1 -- PERIOD = 2*pi / q* (the wavelength measures the Fermi surface).**
The oscillation period in L equals 2*pi divided by the peak momentum:

| filling | peak q* (pi units) | predicted period 2/q* | measured (FFT) |
|---|---|---|---|
| half-filling (mu=0)   | (1.00, 1.00) | 2.00 | 2.04 |
| doped (mu=-2.8)       | (0.54, 0.00) | 3.69 | 3.68 |

Half-filling nests at (pi,pi), which sits on the grid only for **even** L -> a period-2 even/odd parity wave. Doping
moves q* off (pi,pi) and stretches the wavelength. So the tide's period is a direct readout of the nesting vector.

**Wave 2 -- TWO BRANCHES, TWO CONVERGENCE LAWS (half-filling).** The interleaved branches converge differently:
- **even L (peak on-grid): exponential.** Deviation from the TD wall falls by ~0.51 every dL=2 -- the spectral
  accuracy of the BZ quadrature for the smooth finite-T integrand.
- **odd L (peak missed by ~pi/L): 1/L^2.** Fitted power p = -1.89. The grid maximum sits a distance ~pi/L from the true
  peak, and a smooth peak's curvature turns that into an O(1/L^2) deficit.

Even L approaches the wall **from below** (1.64 -> 1.975), odd L **from above** (3.13 -> 1.99); both meet at
U_inf = 1.9752.

**Wave 3 -- AMPLITUDE decays with L (deep vs shallow water).** The wave height (odd-even split at neighbouring L):

  L~4: 1.49   L~8: 0.50   L~16: 0.13   L~32: 0.035   L~40: 0.023

The tide is violent in "shallow water" (small lattices) and calm in "deep water" (large lattices). **Decreasing the
lattice amplifies the waves; increasing it calms them** -- which is why a small cluster gives such an unreliable wall.

**Validation (pre-registered gates, all pass).** (1) half-filling period == 2; (2) incommensurate period == 2*pi/q*
(measured 3.68 vs predicted 3.69); (3) odd-branch power p in (-2.4,-1.5); (4) even-branch ratio < 0.7 (exponential);
(5) amplitude decays (L~4 split > 5x L~32 split) and the two branches meet at a common U_inf. Frozen reference engine
untouched (194/194). `wall_tide.py`, `cdet tide`.
