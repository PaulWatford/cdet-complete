# A hierarchy of scales in R(delta): a thermal near-shell feature on a band-structure background (v42)

Prompted by the observation that the v41 collapse holds only near the shell (|delta|<~0.5) -- an intuition
that this looks like "different forces with different ranges." The honest version: R(delta) is not one
object but a superposition of contributions with different ENERGY SCALES / ranges. This is ordinary
condensed-matter spectral structure (a hierarchy of scales), NOT the fundamental forces -- but the
structural intuition (distinct contributions, distinct ranges) is correct, and measurable.

## The near-shell feature has a thermal RANGE
On L=2 (a single shell at eps=0, isolated by huge gaps to +/-4), the sign-flip detuning delta* of the
near-shell feature scales as the thermal length T=1/beta:
  beta=2 (T=0.500): delta*=0.609 (delta*/T=1.22)
  beta=4 (T=0.250): delta*=0.234 (delta*/T=0.94)
  beta=8 (T=0.125): delta*=0.109 (delta*/T=0.88)
delta* ~ T to order one: the feature narrows as the temperature drops. Its RANGE is the thermal scale.

## It is thermal: shape collapses vs beta*delta on an isolated shell
beta*delta:  -1.0   -0.5   0.0    +0.5   +1.0   +2.0
 beta=4:    +0.79  +0.83  +0.82  +0.67  -0.05  -0.71
 beta=8:    +0.92  +0.92  +0.91  +0.76  -0.35  -0.86
Same shape vs beta*delta (the amplitude grows as T drops). So the near-shell piece is a function of
beta*delta -- a genuine thermal scaling variable for THAT contribution. (This is why v41 saw a clean
delta-collapse at fixed beta: the near-shell thermal piece dominates there.)

## Why it is only PART of the story (the background)
On dense-spectrum clusters (L>=3) neighbouring shells sit within ~T and interfere; that cluster-specific
contribution is the BACKGROUND, a separate scale (the shell spacing / gaps). It dominates in the wings,
where R does not collapse, and it is why beta*delta is not a GLOBAL scaling variable (v41): the total is
thermal-feature + background, and only the feature is a function of beta*delta.

## The hierarchy (the honest structure)
  thermal  T = 1/beta        -> RANGE of the universal near-shell feature (measured: delta* ~ T)
  shell spacing / gaps       -> where shells sit; the cluster-specific background and wing scatter
  bandwidth 8t               -> overall energy scale
Which contribution dominates at a given mu depends on |delta|/T (is mu within a thermal width of a shell?).
That multi-scale separation -- distinct contributions with distinct ranges -- is the real content of the
"miniature forces" image. The substance is band structure and thermal occupation, with no connection to
the actual strong/weak/electromagnetic forces; the analogy is structural only.

## Consequence
The near-shell thermal feature is the clean, universal object (function of beta*delta); the background is
the cluster-specific remainder. A controlled size benchmark therefore lives at delta=0 on an ISOLATED shell
(feature only, no background interference) -- sharpening the v41/v42 target for v43: measure the delta=0
amplitude A(N,beta) along an isolated-shell family and characterise its scaling. Reproduce: make scales.
