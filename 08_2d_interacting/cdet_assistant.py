"""cdet_assistant.py -- a self-contained, rule-based help assistant for the cdet console.

No external models, no API calls, no downloads, no ML inference. A knowledge graph of the package's commands, parameters,
physics concepts, and workflows, plus a keyword matcher. The user types a question or an intent; the assistant matches it
against the graph and returns a plain-language answer, the exact commands to try, and pointers to the existing docs. It
runs instantly and entirely offline. It complements QUICKSTART/README/INDEX -- it does not replace them, and it never
invents capabilities: every command and concept below corresponds to something real in the package.
"""
import difflib
import math
import re

# ----------------------------------------------------------------------------------------------------------------------
# knowledge base
# ----------------------------------------------------------------------------------------------------------------------
COMMANDS = {
    "validate": {
        "desc": "Runs the frozen reference engine (194 gates) and the 5-gate validation suite. Run this first to confirm everything agrees to machine precision.",
        "params": {}, "example": "cdet validate", "related": ["info", "crosscheck", "converge"],
    },
    "converge": {
        "desc": "The 2D thermodynamic-limit demo: the free lattice propagator as L grows, reaching 100x100 instantly via the plane-wave path.",
        "params": {}, "example": "cdet converge", "related": ["wall", "run"],
    },
    "eos": {
        "desc": "SU(N) equation of state -- density n at interaction U for the 2-site reference, with conformal-Borel resummation, checked against exact diagonalization.",
        "params": {"N": "flavors (2-8)", "U": "interaction strength", "K": "series order (default 10)"},
        "example": "cdet eos --N 4 --U 1", "related": ["docc", "chi", "resum"],
    },
    "docc": {
        "desc": "Double occupancy <n_up n_dn> vs U -- the Mott observable; the interaction energy per site is U times this.",
        "params": {"N": "flavors", "U": "interaction (one or several values)", "K": "series order"},
        "example": "cdet docc --N 2 --U 1", "related": ["eos", "chi"],
    },
    "chi": {
        "desc": "Linear-response susceptibilities: charge compressibility kappa and spin susceptibility chi_s vs U. Opposite trends mark Mott physics.",
        "params": {"N": "flavors", "U": "interaction (one or several values)"},
        "example": "cdet chi --N 2 --U 1", "related": ["docc", "eos"],
    },
    "resum": {
        "desc": "Compares resummation schemes (conformal-Borel vs Pade) on the series -- shows how resummation reaches past the radius where the bare series diverges.",
        "params": {"N": "flavors", "U": "interaction (several values)", "K": "series order"},
        "example": "cdet resum --N 4 --U 0.6 1 1.5", "related": ["eos", "wall", "trueradius"],
    },
    "wall": {
        "desc": "The convergence wall U_c = 1/chi0_max, the leading real-axis (RPA/Stoner) instability, as a function of lattice size L.",
        "params": {"beta": "inverse temperature", "mu": "chemical potential"},
        "example": "cdet wall --beta 5 --mu 0", "related": ["tide", "primes", "twist", "trueradius"],
    },
    "tide": {
        "desc": "Shows the wall U_c(L) oscillating with L; the period measures the Fermi nesting vector. A finite-size sampling effect.",
        "params": {"beta": "inverse temperature", "mu": "chemical potential"},
        "example": "cdet tide --beta 5 --mu 0", "related": ["wall", "primes", "twist"],
    },
    "primes": {
        "desc": "The Diophantine sieve: prime lattice sizes are the worst q-grid samplers of the nesting vector. A number-theoretic finite-size artifact.",
        "params": {"beta": "inverse temperature", "mu": "chemical potential"},
        "example": "cdet primes --beta 5 --mu -0.6", "related": ["wall", "tide", "twist"],
    },
    "twist": {
        "desc": "Half-integer (twisted boundary) lattices and rectangular supercells: twist does NOT heal the sieve, rectangular supercells do.",
        "params": {"beta": "inverse temperature", "mu": "chemical potential"},
        "example": "cdet twist --beta 5 --mu -0.6", "related": ["wall", "primes", "trueradius"],
    },
    "trueradius": {
        "desc": "The true convergence radius: the nearest complex-U singularity of lnZ -- a thermal Fisher-zero pair at Im U ~ pi/beta, closer than the RPA wall, and free of the sieve.",
        "params": {"beta": "inverse temperature", "mu": "chemical potential"},
        "example": "cdet trueradius --beta 2 --mu 0.5", "related": ["wall", "resum", "connected"],
    },
    "diagmc": {
        "desc": "Rossi-style connected-determinant Monte Carlo. Samples the diagrammatic series (with the connected determinant as the weight), reproduces the exact answer on solvable systems within error bars, and MEASURES the fermionic sign problem: the across-order average sign <s> = |sum a_n U^n| / sum |a_n| U^n collapses toward zero as U approaches the convergence radius (cost ~ 1/<s>^2). It does not defeat the sign problem -- that wall is NP-hard -- it exhibits it honestly.",
        "params": {"system": "atom or 2site", "beta": "inverse temperature", "mu": "chemical potential", "U": "interaction", "nmax": "max diagram order", "samples": "MC samples per order"},
        "example": "cdet diagmc --system atom --U 1.5",
        "related": ["connected", "resum", "wall"],
        "docs": "Shares the validated connected-determinant kernel with the deterministic path; the reachable order is bounded by the 2^n recursion cost.",
    },
    "connected": {
        "desc": "The connected-determinant (CDet) recursion itself, validated to machine precision on the atom and the 2-site lattice. The method the package is named for.",
        "params": {}, "example": "cdet connected", "related": ["crosscheck", "info"],
    },
    "bench": {
        "desc": "Run the benchmark suite: the engine's connected-determinant evaluation vs a dense-LU cross-check (speedup scaling to ~1M, agreement to round-off), plus an index of the Monte-Carlo variance (control variate), the O(2^n n^2) fast-minors verification, and the size-axis locality/2D benchmarks.",
        "params": {},
        "example": "cdet bench",
        "related": ["validate", "converge", "connected"],
        "docs": "All benchmarks are reproducible and cross-checked; bench surfaces them from one command instead of scattered scripts.",
    },
    "crosscheck": {
        "desc": "Runs all the models side by side and verifies the cross-links between them (reference engine, plane-wave engine, surrogate, observables, wall).",
        "params": {}, "example": "cdet crosscheck", "related": ["validate", "connected"],
    },
    "run": {
        "desc": "The hybrid plane-wave production run on a beta grid -- the main lattice path. Choose the lattice size L, the beta range, and the sampling.",
        "params": {"L": "lattice size", "beta": "lowest beta", "beta-hi": "highest beta", "bstep": "beta step", "K": "max order", "NT": "samples"},
        "example": "cdet run --L 16 --beta 10 --beta-hi 40", "related": ["converge", "wall", "sweep"],
    },
    "sweep": {
        "desc": "Sweep one parameter over a list of values for a chosen target and method, with per-point progress.",
        "params": {"target": "what to compute", "var": "what to vary (L, mu, U, beta, N)", "values": "the list, e.g. 6 12 24"},
        "example": "cdet sweep --target eos --var U --values 0.5 1 1.5", "related": ["run", "lab"],
    },
    "export": {
        "desc": "Export a dataset (convergence, eos, docc, chi, resummation) to CSV, JSON, or HDF5.",
        "params": {"format": "csv, json, or hdf5"}, "example": "cdet export eos --format csv", "related": ["plot"],
    },
    "plot": {
        "desc": "Render the standard figures to files.", "params": {"out": "output directory"},
        "example": "cdet plot", "related": ["export"],
    },
    "info": {
        "desc": "Print the architecture and capabilities: the three-model design and what each layer does.",
        "params": {}, "example": "cdet info", "related": ["validate", "crosscheck"],
    },
    "gui": {
        "desc": "Launch this browser console -- a front-end that runs the real commands with sliders for the numbers.",
        "params": {"port": "port (default 8765)"}, "example": "cdet gui", "related": ["shell", "lab"],
    },
    "lab": {
        "desc": "The swappable control plane: list and run individual (target, method) components.",
        "params": {}, "example": "cdet lab list", "related": ["sweep", "shell"],
    },
    "shell": {
        "desc": "An interactive natural-language shell for quick queries to the lab.",
        "params": {}, "example": "cdet shell", "related": ["gui", "lab"],
    },
}

CONCEPTS = {
    "sign problem": {
        "keys": ["sign problem", "fermion sign", "monte carlo sign"],
        "text": "The sign problem is the exponential cost of Monte Carlo for interacting fermions when contributions cancel. The connected-determinant (CDet) method reduces it by summing all connected diagrams at once. This package implements and explores CDet, but does not solve the sign problem -- the strong-coupling, low-temperature frontier is untouched.",
        "see": ["connected", "info"],
    },
    "cdet": {
        "keys": ["cdet", "connected determinant", "connected-determinant", "the method", "diagram"],
        "text": "CDet (connected determinant, Rossi 2017) sums all connected diagram topologies at fixed vertex positions via a determinant recursion C(V) = D(V) - sum over subsets C(S) D(V\\S). 'cdet connected' implements it and checks it to machine precision on the atom and 2-site lattice.",
        "see": ["connected", "crosscheck"],
    },
    "wall": {
        "keys": ["wall", "u_c", "uc", "convergence radius", "radius of convergence", "stoner", "rpa", "instability", "lindhard"],
        "text": "The 'wall' is the finite radius in U beyond which the bare series stops converging. The leading real-axis cause is the RPA/Stoner instability U_c = 1/chi0_max (chi0 the free Lindhard susceptibility). It moves with lattice size, and that motion (the tide and the prime sieve) is a q-grid sampling artifact -- not the true radius.",
        "see": ["wall", "tide", "primes", "twist", "trueradius"],
    },
    "true radius": {
        "keys": ["true radius", "fisher", "complex-u", "complex u", "lee-yang", "thermal radius", "zeros"],
        "text": "The TRUE convergence radius is the nearest complex-U singularity of lnZ -- a complex-conjugate Fisher-zero pair near Im U = pi/beta (a thermal scale). It is closer than the RPA wall and, having no q-grid maximisation, does not inherit the prime sieve. See 'cdet trueradius'.",
        "see": ["trueradius", "wall"],
    },
    "resummation": {
        "keys": ["resummation", "conformal", "borel", "pade", "diverge", "extend the series"],
        "text": "When the bare U-series diverges past its radius, resummation rescues it. Conformal-Borel (the package's default) maps the cut plane and tracks the exact answer well past where naive summation blows up; 'cdet resum' compares it to Pade.",
        "see": ["resum", "eos", "wall"],
    },
    "mott": {
        "keys": ["mott", "double occupancy", "compressibility", "local moment", "insulator"],
        "text": "Mott physics: as U grows, double occupancy and charge compressibility kappa fall (the system resists adding/doubling particles) while the spin susceptibility chi_s rises (local moments form). 'cdet docc' and 'cdet chi' show these opposite trends.",
        "see": ["docc", "chi", "eos"],
    },
    "thermodynamic limit": {
        "keys": ["thermodynamic limit", "infinite lattice", "l to infinity", "large lattice", "100x100", "plane-wave"],
        "text": "The plane-wave propagator gives the free lattice result at huge sizes (to 100x100) instantly, because it needs only the O(L) dispersion. 'cdet converge' shows the approach to the L -> infinity limit.",
        "see": ["converge", "run"],
    },
    "architecture": {
        "keys": ["architecture", "three model", "three-model", "frozen engine", "reference engine", "surrogate", "how does it work", "trust"],
        "text": "Three models are cross-validated: a FROZEN reference engine (194/194, never edited -- the anchor), a fast plane-wave production engine (matches the reference at 0.00e+00), and an arithmetic surrogate (bit-identical constants). Every result traces back to the one anchor. 'cdet validate' and 'cdet crosscheck' enforce it.",
        "see": ["validate", "crosscheck", "info"],
    },
    "parameters": {
        "keys": ["parameter", "beta", "mu", "what is u", "what does n", "flavors", "chemical potential", "inverse temperature", "temperature", "filling", "lattice size"],
        "text": "Common knobs: N = number of SU(N) flavors; U = interaction strength; mu = chemical potential (filling); beta = inverse temperature (1/T); L = lattice size. In the console, each slider sets one of these on the real command.",
        "see": ["eos", "wall", "run"],
    },
    "lattice": {
        "keys": ["lattice", "what is a lattice", "grid", "sites", "square lattice", "torus", "lattice work"],
        "text": "A lattice is the regular grid of sites the electrons live on (here a 2D square torus). Its size L sets how many sites there are (L x L). This toolkit computes lattice observables and shows that past ~12x12 a local quantity already equals the infinite-lattice answer -- so you don't need huge lattices. See 'cdet converge'.",
        "see": ["converge", "run", "wall"],
    },
    "hubbard model": {
        "keys": ["hubbard model", "hubbard", "what is the hubbard model", "the model", "physics model", "interacting electrons"],
        "text": "The Hubbard model is the standard minimal model of interacting electrons on a lattice: they hop between sites (kinetic energy t) and pay an energy U when two share a site. It is the workhorse for Mott physics and the sign problem. Everything here solves the SU(N) Hubbard problem with the connected-determinant method.",
        "see": ["eos", "docc", "connected"],
    },
    "exact diagonalization": {
        "keys": ["exact diagonalization", "exact diagonalisation", "ed", "diagonalization", "small system exact"],
        "text": "Exact diagonalization (ED) solves a small system exactly by diagonalizing its Hamiltonian. It's limited to a few sites but gives a ground-truth answer -- so the toolkit uses a 2-site ED as the reference that every series result (eos, docc, chi) is checked against.",
        "see": ["eos", "validate", "crosscheck"],
    },
    "monte carlo": {
        "keys": ["monte carlo", "diagmc", "sampling", "stochastic", "qmc", "quantum monte carlo"],
        "text": "Monte Carlo estimates high-dimensional sums by random sampling. For interacting fermions it hits the sign problem: contributions cancel and the cost blows up. The connected-determinant method sums all connected diagrams at once to soften that; this package implements it deterministically at low order.",
        "see": ["connected", "info"],
    },
}

WORKFLOWS = {
    "getting started": {
        "keys": ["start", "begin", "first", "new", "setup", "install", "get going", "where do i"],
        "steps": ["cdet validate   (confirm 194/194 + 5 gates)", "cdet info   (see the architecture)", "cdet converge   (a fast, satisfying first result)"],
        "text": "Start here to confirm the install and get oriented:",
    },
    "observables": {
        "keys": ["observable", "physics", "compute", "density", "equation of state", "occupancy", "susceptibility", "measure"],
        "steps": ["cdet eos --N 4 --U 1   (density)", "cdet docc --N 2 --U 1   (double occupancy)", "cdet chi --N 2 --U 1   (susceptibilities)", "cdet resum --N 4 --U 0.6 1 1.5   (resummation vs Pade)"],
        "text": "Compute the SU(N) observables (all at the 2-site reference, validated by ED):",
    },
    "benchmarks": {
        "keys": ["benchmark", "benchmarks", "performance", "speed", "timing", "how fast", "scaling", "run benchmarks", "test capabilities", "capabilities"],
        "steps": ["cdet bench   (engine speedup + the index)", "cd 02_control_variate && python3 cv.py   (MC variance ~70-80x)", "python3 08_2d_interacting/fast_minors.py   (O(2^n n^2) vs engine)", "cd 05_2d_lattice && python3 val2d.py   (2D vs numpy)"],
        "text": "Run the benchmarks and capability checks:",
    },
    "wall study": {
        "keys": ["wall", "convergence", "radius", "where does it break", "breakdown", "limit of u", "study the wall", "study wall"],
        "steps": ["cdet wall --beta 5 --mu 0   (U_c vs L)", "cdet tide --beta 5 --mu 0   (the oscillation)", "cdet primes --beta 5 --mu -0.6   (the prime sieve)", "cdet twist --beta 5 --mu -0.6   (what heals it)", "cdet trueradius --beta 2 --mu 0.5   (the true, thermal radius)"],
        "text": "Explore where the series converges and why (the wall-physics arc):",
    },
    "lattice run": {
        "keys": ["lattice", "run", "production", "grid", "big calculation", "simulate"],
        "steps": ["cdet converge   (the free thermodynamic limit)", "cdet run --L 16 --beta 10 --beta-hi 40   (the hybrid production run)", "cdet sweep --target eos --var U --values 0.5 1 1.5   (sweep a parameter)"],
        "text": "Run the lattice production path and parameter sweeps:",
    },
    "the method": {
        "keys": ["method", "learn", "how it works", "connected determinant", "understand", "theory"],
        "steps": ["cdet info   (the architecture)", "cdet connected   (the CDet recursion, validated)", "cdet crosscheck   (all models side by side)"],
        "text": "Learn how the connected determinant works and how it's validated:",
    },
    "export": {
        "keys": ["export", "save", "csv", "data out", "spreadsheet", "download", "file"],
        "steps": ["cdet export --format csv   (or json / hdf5)", "cdet plot   (render the figures)"],
        "text": "Get data and figures out of the toolkit:",
    },
}

DOCS_HINT = "For more: cdet info, the README, QUICKSTART.md, and INDEX.md (the full map)."


# ----------------------------------------------------------------------------------------------------------------------
# matcher
# ----------------------------------------------------------------------------------------------------------------------
def _norm(q):
    return " " + re.sub(r"[^a-z0-9_\- ]", " ", q.lower()) + " "


def _cmd_help(name):
    c = COMMANDS[name]
    lines = [f"**cdet {name}** -- {c['desc']}"]
    if c["params"]:
        lines.append("Parameters: " + "; ".join(f"--{k} ({v})" for k, v in c["params"].items()))
    lines.append("Try:  " + c["example"])
    if c.get("related"):
        lines.append("Related: " + ", ".join(c["related"]))
    return "\n".join(lines), [c["example"]]


# ---- best-practice matcher: idf-weighted scoring, typo tolerance, gating, disambiguation, fallback, follow-ups ----
_STOP = {"the", "a", "an", "of", "to", "is", "are", "do", "does", "i", "what", "how", "for", "and", "in", "on",
         "me", "my", "it", "that", "this", "with", "can", "you", "your", "please", "tell", "show", "want", "need",
         "whats", "which", "when", "be", "or", "about", "explain", "give", "get", "would", "should", "could", "us"}
STARTERS = ["how do I start?", "what is the sign problem?", "study the wall", "compute double occupancy",
            "explain the connected determinant", "what can you do?"]
_FOLLOW = ("more", "detail", "details", "example", "elaborate", "expand", "go on", "continue", "params",
           "parameters", "tell me more")


def _tokens(n):
    return [w for w in n.split() if w not in _STOP and len(w) > 1]


def _stem(w):
    for suf in ("ing", "ed", "es", "s"):
        if len(w) > len(suf) + 2 and w.endswith(suf):
            return w[:-len(suf)]
    return w


def _build_index():
    pool = []
    for name, c in COMMANDS.items():
        dt = _tokens(_norm(c["desc"]))
        rw = _norm(c["desc"]).split()
        phr = []
        for w in (2, 3):
            for i in range(len(rw) - w + 1):
                a, b = rw[i], rw[i + w - 1]
                if a not in _STOP and b not in _STOP and len(a) > 1 and len(b) > 1:
                    phr.append(" ".join(rw[i:i + w]))
        pool.append(("command", name, [name] + list(c.get("related", [])) + dt + phr))
    for table, kind in ((CONCEPTS, "concept"), (WORKFLOWS, "workflow")):
        for key, e in table.items():
            terms = []
            for ph in e["keys"]:
                terms.append(ph)
                terms += ph.split()
            pool.append((kind, key, terms))
    df = {}
    for _, _, terms in pool:
        for t in {_stem(w) for w in terms if " " not in w}:
            df[t] = df.get(t, 0) + 1
    N = len(pool)
    imp = {t: 1.0 + math.log(N / d) for t, d in df.items()}
    return pool, imp


_POOL, _IMP = _build_index()
_LABELS = ([(f"cdet {n}", f"explain {n}", f"cdet {n}") for n in COMMANDS]
           + [(k, k, None) for k in CONCEPTS] + [(k, k, None) for k in WORKFLOWS])


def _label(kind, key):
    return f"cdet {key}" if kind == "command" else key


def _prompt(kind, key):
    return f"explain {key}" if kind == "command" else key


_ACTION = {"compute", "run", "measure", "calculate", "calc", "make", "plot", "export",
           "sweep", "evaluate", "find", "generate"}


def _score(n, qtokens, cmd_boost=1.0, concept_boost=1.0):
    qstem = [_stem(t) for t in qtokens]
    qset = set(qstem)
    ranked = []
    for kind, key, terms in _POOL:
        s, seen = 0.0, set()
        for t in terms:
            if " " in t:
                if t in n:
                    s += 1.5 * len(t.split())
            else:
                ts = _stem(t)
                if ts in seen:
                    continue
                seen.add(ts)
                if ts in qset:
                    s += _IMP.get(ts, 1.0)
                elif len(ts) > 3 and difflib.get_close_matches(ts, qstem, n=1, cutoff=0.86):
                    s += 0.5 * _IMP.get(ts, 1.0)       # typo tolerance, at reduced weight
        if kind == "command":
            s *= cmd_boost
        elif kind == "concept":
            s *= concept_boost
        if s > 0:
            ranked.append((s, kind, key))
    ranked.sort(key=lambda r: r[0], reverse=True)
    return ranked


def _suggestions(kind, key):
    out = []
    if kind == "command":
        out += [f"explain {r}" for r in COMMANDS[key].get("related", [])[:2]]
        if COMMANDS[key]["params"]:
            out.append("what do its parameters mean?")
    elif kind == "concept":
        out += [f"explain {s}" for s in CONCEPTS[key].get("see", [])[:2]]
        out.append("how do I start?")
    else:
        out.append("what can you do?")
    res, seen = [], set()
    for o in out:
        if o not in seen:
            seen.add(o); res.append(o)
    return res[:3]


def _answer(kind, key, lead=""):
    if kind == "command":
        reply, cmds = _cmd_help(key)
    elif kind == "concept":
        e = CONCEPTS[key]; see = e.get("see", [])
        cmds = [COMMANDS[s]["example"] for s in see if s in COMMANDS][:3]
        reply = e["text"] + (("\nTry: " + ", ".join(see)) if see else "")
    else:
        e = WORKFLOWS[key]
        reply = e["text"] + "\n  " + "\n  ".join(e["steps"])
        cmds = [st.split("   ")[0].strip() for st in e["steps"]][:4]
    return {"reply": (lead + reply) if lead else reply, "commands": cmds,
            "suggestions": _suggestions(kind, key), "topic": f"{kind}:{key}"}


def respond(query, ctx=None):
    """Return {'reply','commands','suggestions','topic'} for a question. Pure offline rule matching."""
    if not query or not query.strip():
        return {"reply": "Ask me what you want to do -- e.g. 'how do I start?', 'what is the wall?', or "
                "'compute double occupancy'.", "commands": [], "suggestions": STARTERS[:3], "topic": None}
    n = _norm(query)
    qtokens = _tokens(n)
    words = set(n.split())

    if any(g in n for g in (" hi ", " hello ", " hey ", " yo ")) and len(words) <= 3:
        return {"reply": "Hi! I'm the cdet assistant. I can explain commands, parameters, and the physics, and suggest "
                "what to run. Try a question or tap a suggestion.", "commands": ["cdet validate"],
                "suggestions": STARTERS[:3], "topic": None}
    if "thank" in n:
        return {"reply": "Anytime.", "commands": [], "suggestions": [], "topic": ctx}

    # beginner SOS -- a lost newcomer gets the on-ramp directly, never a disambiguation
    _SOS = ("what do i do", "what should i do", "where do i start", "where to start", "how do i start",
            "how do i begin", "what should i run first", "what do i run first", " run first ", "i am new",
            "i m new", " im new ", "first year", "first-year", "i dont understand", "i do not understand",
            "understand any of this", "new to this", "new here", "just installed", "help me start",
            "help me get started", "what now", "i m lost", " im lost ", "beginner", "where do i begin")
    if any(p in n for p in _SOS):
        a = _answer("workflow", "getting started")
        a["reply"] = ("New here? Start with these -- they confirm the install and give a first result, no flags "
                      "needed:\n  " + a["reply"].split(":\n  ", 1)[-1])
        a["suggestions"] = ["what is the hubbard model?", "what is a lattice?", "what can you do?"]
        return a

    # benchmark intent -- "benchmark" must not collide with the `run` command
    if "benchmark" in n:
        return _answer("workflow", "benchmarks")

    # sampler intent -- "diagmc"/"sampler"/"monte carlo run" must not collide with the `run` command
    if "diagmc" in n or "sampler" in n or ("monte carlo" in n and any(w in n for w in (" run ", "sample"))):
        return _answer("command", "diagmc")

    if any(k in n for k in ("what can you do", "what can i do", "capabilities", "help me", " menu ",
                            "list commands", "what commands", "options")):
        return {"reply": "I help you drive the cdet toolkit. Ask about any command or concept, or an intent like "
                "'study the wall'.\nCommands: " + ", ".join(sorted(COMMANDS)) + "\n" + DOCS_HINT,
                "commands": ["cdet validate", "cdet info"], "suggestions": STARTERS[:3], "topic": None}

    # follow-up on the previous topic ("tell me more", "an example", "parameters")
    if ctx and ":" in ctx and (n.strip() in _FOLLOW or any(f" {f} " in n for f in _FOLLOW)):
        kind, key = ctx.split(":", 1)
        if kind == "command" and key in COMMANDS:
            c = COMMANDS[key]
            if "param" in n:
                body = ("\n".join(f"  --{k}: {v}" for k, v in c["params"].items())
                        if c["params"] else "  (this command takes no parameters)")
                return {"reply": f"Parameters of cdet {key}:\n" + body, "commands": [c["example"]],
                        "suggestions": _suggestions("command", key), "topic": ctx}
            return _answer("command", key, lead=(c["docs"] + "\n\n") if c.get("docs") else "")
        if kind == "concept" and key in CONCEPTS:
            return _answer("concept", key)
        if kind == "workflow" and key in WORKFLOWS:
            return _answer("workflow", key)

    # an explicit command name present -> that command's help (prefer longer names)
    for name in sorted(COMMANDS, key=len, reverse=True):
        if f" {name} " in n or n.strip() == name or f" cdet {name}" in n:
            return _answer("command", name)

    # a clear command-name typo with nothing else matching -> did-you-mean that command
    cmd_fuzzy = difflib.get_close_matches((qtokens[0] if qtokens else n.strip()), list(COMMANDS), n=1, cutoff=0.8)

    is_action = bool(set(qtokens) & _ACTION)
    is_defn = (not is_action) and (any(d in n for d in (" what is ", " what s ", " whats ", " define ",
                                                        " meaning ", " what are ", " what does ")) or n.endswith(" mean "))
    ranked = _score(n, qtokens, cmd_boost=(1.4 if is_action else 1.1),
                    concept_boost=(1.5 if is_defn else 1.0))
    STRONG, WEAK = 2.0, 1.0
    if ranked:
        top = ranked[0]
        if top[0] >= STRONG and (len(ranked) == 1 or top[0] >= 1.25 * ranked[1][0]):
            return _answer(top[1], top[2])
        if len(ranked) >= 2 and top[0] >= WEAK and ranked[1][0] >= 0.7 * top[0]:      # ambiguous -> disambiguate
            a, b = ranked[0], ranked[1]
            return {"reply": f"Did you mean **{_label(a[1], a[2])}** or **{_label(b[1], b[2])}**? Tap one and I'll "
                    "explain.", "commands": [], "suggestions": [_prompt(a[1], a[2]), _prompt(b[1], b[2])],
                    "topic": None}
        if top[0] >= WEAK:
            return _answer(top[1], top[2])

    if cmd_fuzzy:
        name = cmd_fuzzy[0]
        return _answer("command", name, lead=f"(Did you mean **cdet {name}**?)\n\n")

    # closest-match fallback -- surface the nearest topics instead of a generic miss
    qn = " ".join(qtokens) or n.strip()
    near = sorted(((difflib.SequenceMatcher(None, qn, disp).ratio(), disp, prm)
                   for disp, prm, _ in _LABELS), reverse=True)[:3]
    sugg = [prm for _, _, prm in near]
    return {"reply": "I'm not sure which you mean. Did you mean one of these, or try rephrasing? You can also ask "
            "'what can you do?'.", "commands": [], "suggestions": sugg, "topic": None}


def _selftest():
    print("cdet_assistant self-test:")
    checks = [
        ("how do I start?", "validate"),
        ("what is the wall?", "U_c"),
        ("explain the connected determinant", "CDet"),
        ("compute double occupancy", "docc"),
        ("tell me about the true radius", "Fisher"),
        ("what does beta mean", "inverse temperature"),
        ("eos", "equation of state"),
        ("how do I export data", "csv"),
        ("what can you do", "Commands:"),
        ("asdfqwer nonsense", "not sure"),
        ("what should I run first", "start with these"),
        ("what is the hubbard model", "minimal model"),
        ("what is a lattice", "grid of sites"),
        ("I'm a first year, what do I do", "start with these"),
        ("what is diagmc", "Monte Carlo"),
        ("run the monte carlo sampler", "diagmc"),
    ]
    for q, expect in checks:
        r = respond(q)["reply"]
        assert expect.lower() in r.lower(), (q, expect, r[:80])
        print(f"  ok: {q!r} -> matched {expect!r}")

    # --- new-behaviour checks (best-practice upgrades) ---
    assert "wall" in respond("explain the wal")["reply"].lower(), "typo tolerance"          # difflib typo
    assert "Mott" in respond("susceptibility")["reply"] or respond("susceptibility")["commands"], "keyword intent"
    fb = respond("banana helicopter")                                                       # no match
    assert "not sure" in fb["reply"].lower() and fb["suggestions"], "fallback offers suggestions"
    assert respond("what is the wall?")["suggestions"], "answers carry a forward path"
    fu = respond("tell me more", ctx="concept:sign problem")                                # follow-up via ctx
    assert "sign problem" in fu["reply"].lower(), "follow-up uses context"
    dis = respond("compute double occupancy")
    assert dis["topic"] == "command:docc", "action verb biases to the command"
    print("  ok: typo tolerance, keyword intent, fallback suggestions, forward path, follow-up, intent bias")

    # every command example is a real command name; every answer returns the documented shape
    for name, c in COMMANDS.items():
        assert c["example"].startswith("cdet " + name), name
    for q in ("eos", "what is the wall", "banana"):
        r = respond(q)
        assert set(r) == {"reply", "commands", "suggestions", "topic"}, ("shape", q, set(r))
    print(f"  all {len(checks)} query checks + 6 behaviour checks pass; {len(COMMANDS)} commands, "
          f"{len(CONCEPTS)} concepts, {len(WORKFLOWS)} workflows. PASS")


if __name__ == "__main__":
    _selftest()
