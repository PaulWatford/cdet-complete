# Does the shift improve the sign, or only convergence? A trade-off, not a free lunch (v48)

The reviewer's million-dollar question: the shifted-reference work clearly accelerates convergence, but does
it move the SIGN -- the thing that dominates large-scale cost? Answer for the case studied: NO. Convergence
and sign are controlled by the SAME knob (mu_ref = mu - alpha) but with DIFFERENT, COMPETING optima. The
convergence-optimal (Hartree/pole-moving) shift lands OFF the closed shell and gives the WORST sign.

## Setup
2x2 square (single-particle levels {-4,0,0,+4}), beta=4, U=4, physical mu=0.5 -- just above the shell at 0
(the bad-sign side of the detuning, v41). Convergence side is ED-exact; sign side is the live mc2d sampler.

## The two optima are different
CONVERGENCE (ED, truncation error at order 8 vs shift):
  alpha:    0.00   0.50   1.00   1.50   2.00
  err@K8:  4.6e-1 6.3e-2 2.6e-1 5.6e-3 1.4e-2   -> alpha_conv = +1.50 (mu_ref=-1.00), near Hartree U<n_s>=1.32
SIGN (mc2d, |R_2| vs reference):
  mu_ref:  -1.00  -0.50  -0.25   0.00   0.25   0.50
  |R_2|:   0.046  0.569  0.788  0.820  0.056  0.718  -> sign-optimal mu_ref = 0.00 (alpha_sign=+0.50), the shell

## The trade-off (same knob, competing optima), across orders
  reference                       conv err@K8   |R_2|  |R_3|  |R_4|
  SIGN-opt  mu_ref= 0.0 (shell)      6.3e-2      0.820  0.336  0.809
  CONV-opt  mu_ref=-1.0 (Hartree)    5.6e-3      0.046  0.215  0.407
  physical  mu_ref=+0.5 (alpha=0)    4.6e-1      0.718  0.342  0.751
The convergence-optimal shift is ~10x better on truncation error but has the WORST sign (|R_2|=0.05 vs 0.82).
The sign-optimal shift sits on the closed shell with |R| ~ 0.8 but ~10x worse convergence.

## Why (the mechanism)
Convergence is governed by the nearest POLE in the complex-U plane (Wu-Ferrero-Georges-Kozik); a Hartree-scale
shift moves the reference to the mean-field solution and pushes that pole out. The per-order sign R is governed
by the real-axis SHELL/detuning (v41/v44 closed-shell "magic-density" effect): R is best when mu_ref sits ON a
closed shell. These are different objects -- analytic structure in complex U vs Fermi-surface shell structure
on the real axis -- so their optimal mu_ref differ, and here they pull in opposite directions.

## Verdict (honest)
- Pole-moving accelerates convergence (established, v45-v47) but does NOT move the sign wall; worse, the
  convergence-optimal shift actively DEGRADES the sign by moving off the closed shell.
- The reviewer's framing is refined: convergence and sign ARE the same control parameter (mu_ref), but their
  optima COMPETE -- you trade off, you do not get both. The "Hartree/closed-shell operating-point idea"
  affecting both through one parameter is real as a STATEMENT about the parameter, but the two effects want
  different settings of it.
- So: a substantially better perturbative method (fewer orders) that does not move the fundamental sign wall,
  exactly the cautious outcome anticipated. No expert-surprising sign result here.

## Scope / what is NOT shown
Single case (2x2, mu=0.5, U=4, beta=4), confirmed across orders 2-4. The mechanism (pole vs shell = different
physics) argues the tension is generic, but genericity across fillings/clusters/temperatures is NOT proven --
e.g. a filling where the Hartree point happens to coincide with a closed shell could align the optima, and
that special case (if it exists) would be the only route to "both at once". That search is v49. Reproduce:
make signtradeoff.
