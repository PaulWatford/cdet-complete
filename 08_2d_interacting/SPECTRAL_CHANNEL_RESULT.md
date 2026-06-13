# The "single de-confined mode" sharpening (v113): the channel is real and is level 2, but it saturates — it is not an exp(−ξ₂β) mode

An external suggestion sharpened v112 to its strongest form: prove c1(β) = Σₙ aₙ e^(−ξₙβ) with
ξ₂ < ξₙ for all n>2, so the phase fluctuations are *entirely* carried by the n=2 (level-2) sector —
"sign problem = one de-confined mode with gap (2−μ)." Tested against the data, it splits cleanly into
a true half and a false half.

## What survives — the compression is real (= v112)

**ξ₂ < ξₙ is TRUE.** The gaps are ξₙ = levelₙ − μ; level 2 (the probe) is the closest level to
μ=1.845, with gap ξ₂ = 2−μ = **0.155**, strictly smaller than every other level above μ (level 3:
1.155, level 4: 2.155, …). The phase response c1 = dC_V/ds is carried by this single smallest-gap
channel. The reframing — *the sign structure of this object compresses to one spectral channel, the
level closest to μ* — is correct, and is exactly the v112 mechanism. That is a real and striking
compression of an exponentially large cancellation into a single object.

## What is falsified — the literal exponential form

If c1(β) = Σₙ aₙ e^(−ξₙβ) with n=2 dominant, then |c1| would decay at **rate ξ₂ = 0.155**, a factor
e^(0.155·96) ≈ **2.9×10⁶** over β=24→120. **Measured: |c1| drops by 1.66×** (effective rate 0.0046,
34× too small). The exponential-mode form overpredicts the decay by ~10⁶ — **falsified**.

## The correction — saturation, not an exponential mode

c1 is a τ-**average** (A = (1/β³)∫dτ³). The level-2 exponential lives in the τ-*propagator*,
exp(−ξ₂|Δτ|), and **saturates** under integration:

  ∫₀^β exp(−ξ₂τ) dτ → 1/ξ₂ = 6.45  (converged by β≈48).

So the smallest-gap channel contributes a **β⁰ (rate-0) saturating factor**, not an e^(−ξ₂β) mode.
That is precisely why the integrated c1 is a power law (v112), and why z(β) → 2 as a ln β/β approach
rather than being pinned by an exponential gap. The gap (2−μ) enters in two correct ways — it sets
the de-confinement **range** 1/(2−μ) ≈ 6.5 in τ, and it fixes the **limit** z(∞)=2 (the probe level
sits at energy 2) — but it is **not** a β-decay rate.

## Net

The kernel of the proposal is right and is the real result: **the sign problem for this object is
one de-confined channel — the level closest to μ.** "With gap (2−μ)" is right for the range and the
limit, wrong as a β-rate. The honest statement is: *sign problem = one de-confined channel (the
level-2/probe sector, gap 2−μ) that de-confines by τ-saturation, yielding z(∞)=2 via a ln β/β law* —
a saturating spectral object, not an exponential mode. The distinction is not pedantic: it is exactly
why z is reached as a slow power-law approach (which drove the entire v93–v107 menu detour) rather
than as a clean exponential gap.

Reproduce: `python3 spectral_channel_test.py` (gap ordering, exp-form test, saturation; self-test
PASS). Frozen engine untouched (194/194).
