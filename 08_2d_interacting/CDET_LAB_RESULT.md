# The unified end-to-end model: `cdet_lab.py` (v148)

A complete end-to-end model that contains **every feature** as **swappable components**, driven purely from the
terminal after unzipping. Nothing from the program is lost; the frozen reference stays the untouched anchor and
the C components validate against it. This is the "new additional model" — a control plane, not a fourth engine.

## Why a control plane (not a merged engine)

The frozen reference `engine/` must stay frozen (it is the 194/194 validation anchor). The capabilities live in
different artifacts — two C engines, a surrogate, and ~a dozen analysis modules — each best kept separate
(different languages, different precision regimes, different physics scope). A control plane unifies them at the
**interface** level: the user composes a run from orthogonal choices instead of editing code.

## The three orthogonal choices (the swappable interface)

```
python3 cdet_lab.py --target <observable> --method <solver> --model <system> [params]
```

- **`--target`** = WHAT (the physics observable physicists actually want):

  | target | observable | grounded in |
  |---|---|---|
  | `eos` | equation of state ⟨n⟩(μ) | SU(N) cold-atom benchmark — ⟨n⟩(μ) at T/t=0.3, U/t=2.3, N=6 (Pasqualetti PRL 132.083401; Kozik CoS arXiv 2309.13774) |
  | `self-energy` | Σ(iωₙ) | DMFT / spectral workflows (DCore, TRIQS) |
  | `addition-pole` | lowest-empty level / z(∞) | single-particle gap, spectral edge |
  | `double-occ` | ⟨n↑n↓⟩ | Mott physics, thermometry (DiagMC observable, PRB 87.205102) |
  | `connected-det` | Rossi connected determinant | the DiagMC sampling kernel |

- **`--method`** = HOW (the swappable solver component):

  | method | component | regime |
  |---|---|---|
  | `ed` | exact diagonalization (`hubbard_ed`, `sun_lattice_record`) | benchmark, small systems |
  | `record` | SU(N) record × g0 amplitude (`sun_lattice_production`) | N-independent EoS, any flavor number incl 6 |
  | `hubbard-i` | atomic-limit rational Σ = nU + n(1−n)U²/(iω+μ−U(1−n)) | Mott / large-U, real-frequency, **exact rational** |
  | `diagrammatic` | Dyson/contour Σ series (`self_energy_irreducible`) | weak–intermediate U (radius ~π/β) |
  | `surrogate` | fast pure-arithmetic carrier (`csurrogate.c`) | instant, large L |
  | `hybrid` | plane-wave engine (`cdet_planewave_engine.c`) | thermodynamic limit, deep β, `-fast`/`-DUSE_LD` |
  | `fast-minors` | O(2ⁿn²) connected determinant (`fast_minors`) | efficient kernel |
  | `engine` | frozen-reference connected determinant (`engine/`) | the 194/194 anchor |

- **`--model` / params** = the system: `atom | dimer | lattice`, `--N`, `--U`, `--mu`, `--beta`, `--L`, `--t`.

The `(target, method)` map is enforced — undefined combinations are rejected with a pointer to `list`. This is
exactly the physicist's mental model: pick an observable, pick a solver appropriate to the regime, set the
parameters. The Hubbard-I method, for instance, is the right tool for the Mott regime (the atomic-limit solver is
known to be valid at integer filling / large U — arXiv 0911.1422); the diagrammatic method is the
weak–intermediate-U tool; ED is the benchmark.

## Commands

```
python3 cdet_lab.py list        # the full component map
python3 cdet_lab.py validate    # the three-model health gate (consolidation_v147)
python3 cdet_lab.py --target eos --method record --N 6 --U 1.0 --mu 1.0
python3 cdet_lab.py --target self-energy --method hubbard-i --U 4.0 --mu 2.0 --beta 5.0
python3 cdet_lab.py --target self-energy --method ed --model dimer --U 1.0 --mu 0.5 --beta 5.0
python3 cdet_lab.py --target addition-pole --method surrogate --L 12 --mu 1.0
python3 cdet_lab.py --target connected-det --method fast-minors --n 5
```

## Capability ledger — nothing lost

Every capability from the program is reachable: the frozen-reference and plane-wave engines, the surrogate
carriers (incl. the SU(N) EoS coefficients), ED, the SU(N) record/production EoS, the Hubbard-I rational
self-energy, the diagrammatic self-energy, the physical mapping (addition pole), and the fast-minors connected
determinant. The analysis supplements remain individually runnable; `cdet_lab.py` is the single front door.

Reproduce: `python3 cdet_lab.py` runs the self-test across five representative components. Frozen engine untouched
(194/194); ED is the anchor for the python observables.
