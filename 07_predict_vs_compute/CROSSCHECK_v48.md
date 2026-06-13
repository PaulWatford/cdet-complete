# Cross-check (v48) — does the shift improve the sign, or only convergence? A competing-optima trade-off

Reproduce: 08_2d_interacting (make signtradeoff). Addresses the reviewer's central question. Convergence side
ED-exact; sign side live mc2d.

## Setup
2x2 square (levels {-4,0,0,+4}), beta=4, U=4, mu=0.5 (just above the shell at 0). One knob: mu_ref = mu - alpha.

## Results
- CONVERGENCE-optimal (ED, min trunc err @K=8): alpha_conv=+1.50 (mu_ref=-1.00), near Hartree U<n_s>=1.32;
  err 5.6e-3, radius ~2.16.
- SIGN-optimal (mc2d, max |R_2|): mu_ref=0.00 (alpha_sign=+0.50), the closed shell; |R_2|=0.82.
- TRADE-OFF across orders 2-4:
    SIGN-opt mu_ref=0.0:   conv err 6.3e-2 | |R_2,3,4| = 0.820, 0.336, 0.809
    CONV-opt mu_ref=-1.0:  conv err 5.6e-3 | |R_2,3,4| = 0.046, 0.215, 0.407
    physical mu_ref=+0.5:  conv err 4.6e-1 | |R_2,3,4| = 0.718, 0.342, 0.751
  The convergence-optimal shift (~10x better trunc error) has the WORST sign (|R_2|=0.05 vs 0.82).

## Mechanism / verdict
Convergence <-> nearest pole in complex U (Hartree shift moves it out); sign <-> real-axis shell/detuning
(best on a closed shell). Different physics -> different optimal mu_ref -> they compete. Pole-moving
accelerates convergence (v45-v47) but does NOT move the sign wall, and the convergence-optimal shift degrades
the sign. The reviewer's "same control parameter" is correct as a statement about mu_ref, but the two effects
want different settings -- a trade-off, not a free lunch. No expert-surprising sign result.

## Honesty / scope
Single case (2x2, mu=0.5, U=4, beta=4) confirmed across orders 2-4; the pole-vs-shell mechanism argues the
tension is generic but genericity is NOT proven. A filling where the Hartree point coincides with a closed
shell could align the optima (the only route to "both at once") -- that search is v49. Frozen engine untouched
(194/194; cdet_order constants bit-identical).
