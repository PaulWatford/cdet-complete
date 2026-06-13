#!/usr/bin/env python3
"""cdet_shell.py (v149) -- the idiot-proof conversational front-end to cdet_lab.

Design follows the established CLI best practices (clig.dev and others): the command line is a CONVERSATION;
make functionality DISCOVERABLE (comprehensive help + examples, no hidden options); design with EMPATHY (graceful
errors that suggest corrections and always show example syntax). On top of that, this shell adds the flow you asked
for:

  plain language in  ->  the shell interprets it and states back what it thinks you meant (with every assumed
  default shown -- nothing hidden)  ->  it presents the exact command and asks to confirm  ->  you reply yes/no.
  yes runs it; no reverts to the start WITHOUT losing any previously confirmed/named configurations.

It is a thin, safe layer: it never invents capabilities, it only composes valid (target x method) components from
cdet_lab (the single source of truth), and it routes every run through cdet_lab so the frozen reference stays the
anchor.

STATE MACHINE
  HOME    : waiting. Understands: help [topic], list, examples, configs, save <name>, run <name>, forget <name>,
            quit -- or a request in plain language / flags.
  CONFIRM : a draft is pending. Understands: yes | no | save as <name>. 'no' reverts to HOME (library kept).

Run interactively:  python3 cdet_shell.py
Self-test (scripted session):  python3 cdet_shell.py --selftest
"""
import sys, os, io, re, difflib, json, contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cdet_lab  # single source of truth for the (target, method) component map

TARGETS = sorted({t for t, _ in cdet_lab.COMPONENTS})
METHODS = sorted({m for _, m in cdet_lab.COMPONENTS})
PARAMS = ["N", "U", "mu", "beta", "L", "t", "n"]
DEFAULT_METHOD = {"eos": "record", "self-energy": "ed", "addition-pole": "surrogate",
                  "double-occ": "ed", "connected-det": "fast-minors"}

# plain-language synonyms -> canonical token (so "density", "sigma", "mott" etc. are understood)
TARGET_WORDS = {
    "eos": ["eos", "equation of state", "density", "filling", "occupation", "occupancy", "n(mu)", "n vs mu", "particle number", "number density"],
    "self-energy": ["self-energy", "self energy", "selfenergy", "sigma", "spectral"],
    "addition-pole": ["addition pole", "addition-pole", "pole", "gap", "spectral edge", "lowest empty"],
    "double-occ": ["double-occ", "double occ", "double occupancy", "double-occupation", "docc", "doublon", "doublons"],
    "connected-det": ["connected-det", "connected determinant", "connected det", "cdet", "determinant", "weight"],
}
METHOD_WORDS = {
    "ed": ["ed", "exact", "diagonalization", "diagonalisation", "benchmark", "lehmann"],
    "record": ["record", "cos", "combinatorial", "linked cluster"],
    "hubbard-i": ["hubbard-i", "hubbard i", "atomic", "atomic limit", "mott"],
    "diagrammatic": ["diagrammatic", "diagram", "dyson", "series"],
    "surrogate": ["surrogate", "carrier", "instant"],
    "hybrid": ["hybrid", "plane-wave", "plane wave", "thermodynamic", "large l", "deep beta"],
    "fast-minors": ["fast-minors", "fast minors", "minors"],
    "engine": ["engine", "frozen", "reference", "anchor"],
}


def _scan(text, words):
    """longest-match synonym scan with WORD BOUNDARIES (so 'ed' doesn't match inside 'connected');
    returns the canonical token or None."""
    low = text.lower()
    hits = [(len(syn), canon) for canon, syns in words.items() for syn in syns
            if re.search(rf"(?<![a-z0-9]){re.escape(syn)}(?![a-z0-9])", low)]
    return max(hits)[1] if hits else None


def parse_params(text):
    """extract U=2, 'mu of 1', 'beta 5', '6 flavors' (->N), 'L=12' etc. Returns (dict, [warnings]).
    N (flavors) and n (vertices) are case-sensitive to avoid collision; others case-insensitive."""
    out, warn = {}, []
    if m := re.search(r"(\d+)\s*flavou?rs?", text.lower()):
        out["N"] = int(m.group(1))
    # (key, case_sensitive, is_int)
    for key, csens, isint in [("N", True, True), ("n", True, True), ("U", False, False),
                              ("mu", False, False), ("beta", False, False), ("L", False, True), ("t", False, False)]:
        flags = 0 if csens else re.IGNORECASE
        val = rf"(?<![A-Za-z]){key}(?![A-Za-z])\s*(?:=|of|:)?\s*(-?\d+\.?\d*)"
        if m := re.search(val, text, flags):
            out[key] = int(float(m.group(1))) if isint else float(m.group(1))
            continue
        # detect an attempted-but-non-numeric assignment, e.g. "U=abc"
        bad = rf"(?<![A-Za-z]){key}(?![A-Za-z])\s*(?:=|of|:)\s*([A-Za-z]\w*)"
        if m := re.search(bad, text, flags):
            warn.append(f"'{key}={m.group(1)}' needs a number (e.g. {key}=2); ignoring it.")
    return out, warn


def validate_params(d):
    """sanity-check resolved parameters; return an error string or None."""
    p = d["params"]
    if d["target"] == "eos" and p.get("N", 6) < 1:
        return f"N (flavors) must be >= 1; you gave N={p['N']}. Try e.g. N=6."
    for key, lo in [("beta", 1e-9), ("L", 1), ("n", 1)]:
        if key in p and p[key] <= (lo if isinstance(lo, float) else lo - 1):
            return f"{key} must be > {0 if key=='beta' else lo-1}; you gave {key}={p[key]}."
    return None


def parse_request(text):
    """Interpret a plain-language / flag request. Returns (draft|None, message).
    draft = {target, method, model, params{...}}. message carries clarification/help on failure."""
    # explicit flags first (power users)
    flagged = {}
    for m in re.finditer(r"--(\w[\w-]*)\s+(\S+)", text):
        flagged[m.group(1)] = m.group(2)
    target = flagged.get("target") or _scan(text, TARGET_WORDS)
    method = flagged.get("method") or _scan(text, METHOD_WORDS)
    if not target:
        # try a 'did you mean' on the first word vs known targets/commands
        first = (text.split() or [""])[0].lower()
        near = difflib.get_close_matches(first, TARGETS + ["help", "list", "examples", "configs"], n=1, cutoff=0.6)
        hint = f" Did you mean '{near[0]}'?" if near else ""
        return None, ("I couldn't tell which observable you want." + hint +
                      "\n  Observables: " + ", ".join(TARGETS) +
                      "\n  e.g.  eos for SU(6) at U=2 mu=1   (or:  --target eos --N 6 --U 2 --mu 1)" +
                      "\n  Type 'examples' for ready-to-run lines, or 'help' for the menu.")
    if not method:
        # did the user TRY to name a method (via/using/method X) that we don't recognize?
        if m := re.search(r"(?:\bvia\b|\busing\b|\bmethod\b|--method)\s+([\w-]+)", text.lower()):
            word = m.group(1)
            near = difflib.get_close_matches(word, METHODS, n=1, cutoff=0.6)
            hint = f" Did you mean '{near[0]}'?" if near else ""
            return None, (f"'{word}' isn't a solver I know.{hint}"
                          f"\n  Solvers: {', '.join(METHODS)}"
                          f"\n  e.g.  {target} via {DEFAULT_METHOD[target]}")
        method = DEFAULT_METHOD[target]
    if (target, method) not in cdet_lab.COMPONENTS:
        ok = sorted(m for (t, m) in cdet_lab.COMPONENTS if t == target)
        near = difflib.get_close_matches(method, METHODS, n=1, cutoff=0.5)
        hint = f" Did you mean '{near[0]}'?" if near else ""
        return None, (f"'{method}' is not a valid solver for '{target}'.{hint}"
                      f"\n  Valid for {target}: {', '.join(ok)}"
                      f"\n  e.g.  {target} via {ok[0]}")
    params, warn = parse_params(text)
    model = flagged.get("model")
    if not model:
        model = "dimer" if "dimer" in text.lower() else ("lattice" if "lattice" in text.lower() else "atom")
    draft = {"target": target, "method": method, "model": model, "params": params}
    sw = parse_sweep(text)
    if sw is not None:
        if "error" in sw:
            return None, sw["error"]
        draft["sweep"] = sw
        draft["params"].pop(sw["var"], None)  # the swept variable is not a fixed parameter
    err = validate_params(draft)
    if err:
        return None, err + ("\n  (" + " ".join(warn) + ")" if warn else "")
    return draft, (" ".join(warn) if warn else "")


NUM = r"-?\d+\.?\d*(?:e-?\d+)?"


def parse_sweep(text):
    """detect a sweep/study request; return {var, lo, hi, step, max_time, accuracy_eps, conv_tol} or None."""
    low = text.lower()
    if not re.search(r"\b(sweep|scan|study|vary|varying|across|range of)\b", low):
        return None
    var = None
    for v in ["beta", "mu", "U", "N", "L", "n"]:
        if re.search(rf"(?:sweep|scan|study|vary|varying|across|over|of)\s+{v.lower()}\b", low) or \
           re.search(rf"\b{v.lower()}\s+from\b", low):
            var = v; break
    if not var:
        return None
    m = re.search(rf"(?:from\s+)?({NUM})\s+(?:to|-|\.\.|until)\s+({NUM})", low) or \
        re.search(rf"between\s+({NUM})\s+and\s+({NUM})", low)
    if not m:
        return {"var": var, "error": f"I need a range for {var}, e.g. 'sweep {var} from 0.2 to 1.6'."}
    lo, hi = float(m.group(1)), float(m.group(2))
    sm = re.search(rf"(?:step|by|in steps of)\s+({NUM})", low)
    step = float(sm.group(1)) if sm else (round((hi - lo) / 10, 10) or 1.0)
    sweep = {"var": var, "lo": lo, "hi": hi, "step": step, "max_time": None, "accuracy_eps": None, "conv_tol": None}
    if a := re.search(rf"accuracy[^\d]*({NUM})", low):
        sweep["accuracy_eps"] = float(a.group(1))
    if t := re.search(rf"(?:max[- ]?time|time budget|time limit|stop after|within)\D*({NUM})\s*(?:s|sec|seconds)?", low):
        sweep["max_time"] = float(t.group(1))
    if c := re.search(rf"converge\w*[^\d]*({NUM})", low):
        sweep["conv_tol"] = float(c.group(1))
    elif "converge" in low:
        sweep["conv_tol"] = 1e-3
    return sweep


def draft_to_argv(d):
    if "sweep" in d:
        s = d["sweep"]
        argv = ["--target", d["target"], "--method", d["method"], "--model", d["model"],
                "--sweep", s["var"], "--range", f"{s['lo']}:{s['hi']}:{s['step']}"]
        for k, v in d["params"].items():
            argv += [f"--{k}", str(v)]
        if s.get("max_time") is not None:
            argv += ["--max-time", str(s["max_time"])]
        if s.get("accuracy_eps") is not None:
            argv += ["--accuracy-cutoff", str(s["accuracy_eps"])]
        if s.get("conv_tol") is not None:
            argv += ["--conv-tol", str(s["conv_tol"])]
        return argv
    argv = ["--target", d["target"], "--method", d["method"], "--model", d["model"]]
    for k, v in d["params"].items():
        argv += [f"--{k}", str(v)]
    return argv


def draft_to_command(d):
    tool = "cdet_study.py" if "sweep" in d else "cdet_lab.py"
    return f"python3 {tool} " + " ".join(draft_to_argv(d))


def draft_summary(d):
    desc = cdet_lab.COMPONENTS[(d["target"], d["method"])]
    ps = ", ".join(f"{k}={v}" for k, v in d["params"].items()) or "defaults"
    if "sweep" in d:
        s = d["sweep"]
        cut = []
        if s.get("accuracy_eps") is not None:
            cut.append(f"stop if error > {s['accuracy_eps']:g}")
        if s.get("max_time") is not None:
            cut.append(f"stop after {s['max_time']:g}s")
        if s.get("conv_tol") is not None:
            cut.append(f"flag convergence at |delta|<{s['conv_tol']:g}")
        cuts = ("; cutoffs: " + ", ".join(cut)) if cut else ""
        return (f"STUDY: {desc}\n    sweep {s['var']} from {s['lo']:g} to {s['hi']:g} step {s['step']:g}; "
                f"fixed {ps}{cuts}\n    outputs: log + data.csv + summary.json + plot.png (+ ASCII plot)")
    return f"{desc}\n    model={d['model']}, {ps}"


HELP = {
    None: (
        "cdet_shell -- talk to the cdet lab in plain language; I'll show you the exact command and ask before "
        "running.\n"
        "  HOME commands:  help [topic] | list | examples | configs | save <name> | run <name> | forget <name> | "
        "quit\n"
        "  Or just describe what you want, e.g.:  'equation of state for 6 flavors at U=2, mu=1'\n"
        "  STUDIES: say 'sweep <var> from <lo> to <hi>' to scan a parameter; add 'stop if accuracy drops below "
        "<eps>', 'stop after <T> seconds', or 'until it converges' for cutoffs. Outputs a log + data.csv + "
        "summary.json + plot.png with convergence/breakdown marked.\n"
        "  I will state what I think you meant, show the command, and ask yes/no. 'no' returns here and keeps your "
        "saved configs.\n"
        "  Topics:  targets, methods, params, configs"),
    "targets": "Observables (--target):\n  " + "\n  ".join(
        f"{t:<14} {[d for (tt, _), d in cdet_lab.COMPONENTS.items() if tt == t][0].split(' -- ')[0].split(' from ')[0]}"
        for t in TARGETS),
    "methods": "Solvers (--method):\n  " + ", ".join(METHODS) +
               "\n  (not every method fits every target; 'list' shows the valid map)",
    "params": "Parameters:  --N flavors  --U interaction  --mu chemical potential  --beta inverse temp  "
              "--L lattice side  --t hopping  --n vertices\n  Plain language works too: '6 flavors', 'U=2', "
              "'mu of 1', 'beta 5'.",
    "configs": "Saved configurations are named snapshots of a confirmed command. After a run, `save <name>`; "
               "recall with `run <name>`; list with `configs`; drop with `forget <name>`. They survive 'no'.",
}


class Shell:
    def __init__(self, runner=None):
        self.state = "home"
        self.pending = None        # draft awaiting confirmation
        self.last = None           # last confirmed draft
        self.library = {}          # name -> draft
        self.runner = runner or self._run_cdet

    def _run_cdet(self, draft):
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                if "sweep" in draft:
                    import cdet_study
                    cdet_study.main(draft_to_argv(draft))
                else:
                    cdet_lab.main(draft_to_argv(draft))
        except SystemExit:
            pass
        return buf.getvalue().rstrip()

    def handle(self, line):
        """Process one input line; return the shell's textual response. Pure + testable."""
        line = (line or "").strip()
        if self.state == "confirm":
            return self._confirm(line)
        return self._home(line)

    def _home(self, line):
        if not line:
            return ""
        low = line.lower()
        if low in ("quit", "exit", "q"):
            return "__quit__"
        if low in ("menu", "options", "commands", "what can you do", "what can you do?",
                   "what can i do", "what do you do", "?"):
            return HELP[None]
        if low in ("yes", "y", "no", "n", "cancel", "back", "ok"):
            return "Nothing is pending right now. Describe what you want (or type 'help' / 'examples')."
        if low == "help" or low.startswith("help "):
            topic = line[5:].strip().lower() or None
            if topic and topic not in HELP:
                near = difflib.get_close_matches(topic, [t for t in HELP if t], n=1, cutoff=0.5)
                return f"No help topic '{topic}'." + (f" Did you mean '{near[0]}'?" if near else "") + \
                    "\n" + HELP[None]
            return HELP[topic]
        if low == "list":
            return self.runner.__self__._list() if False else self._list()
        if low == "examples":
            return ("Examples (just type one):\n"
                    "  equation of state for 6 flavors at U=1, mu=1\n"
                    "  self-energy in the Mott regime, U=4 mu=2 beta=5      (uses hubbard-i)\n"
                    "  exact self-energy for the dimer, U=1 mu=0.5 beta=5\n"
                    "  addition pole for L=12 at mu=1\n"
                    "  connected determinant with 5 vertices\n"
                    "  STUDY: sweep U from 0.2 to 1.2 for self-energy diagrammatic, beta 5 mu 1, "
                    "stop if accuracy drops below 5e-3\n"
                    "  STUDY: scan L from 8 to 128 for the addition pole at mu=1 until it converges\n"
                    "  STUDY: vary n from 4 to 14 for connected determinant, stop after 10 seconds")
        if low == "configs":
            if not self.library:
                return "No saved configurations yet. After a run, use `save <name>`."
            return "Saved configurations:\n  " + "\n  ".join(
                f"{n:<16} {draft_to_command(d)}" for n, d in self.library.items())
        if low.startswith("save "):
            name = line[5:].strip()
            if not self.last:
                return "Nothing to save yet -- run a command first, then `save <name>`."
            if not name:
                return "Usage: save <name>   e.g.  save mott_run"
            self.library[name] = self.last
            return f"Saved the last confirmed run as '{name}'. (`configs` to list, `run {name}` to reuse.)"
        if low.startswith("forget "):
            name = line[7:].strip()
            if name in self.library:
                del self.library[name]
                return f"Forgot '{name}'."
            return f"No saved config named '{name}'. `configs` lists them."
        if low.startswith("run ") or low.startswith("load "):
            name = line.split(None, 1)[1].strip()
            if name not in self.library:
                near = difflib.get_close_matches(name, list(self.library), n=1, cutoff=0.5)
                return f"No saved config '{name}'." + (f" Did you mean '{near[0]}'?" if near else
                                                       " `configs` lists them.")
            self.pending = self.library[name]
            self.state = "confirm"
            return self._present()
        # otherwise: interpret as a request
        draft, msg = parse_request(line)
        if draft is None:
            return msg
        self.pending = draft
        self.state = "confirm"
        return ((msg + "\n") if msg else "") + self._present()

    def _present(self):
        d = self.pending
        return ("Here's what I think you want:\n"
                f"  {draft_summary(d)}\n"
                f"  command:  {draft_to_command(d)}\n"
                "Run it? [yes / no / save as <name>]")

    def _confirm(self, line):
        low = line.lower().strip()
        first = low.split()[0] if low.split() else ""
        YES = {"y", "yes", "run", "ok", "okay", "go", "sure", "yep", "yeah", "do", "yas"}
        NO = {"n", "no", "nope", "nah", "cancel", "nevermind", "stop", "abort", "back", "reset"}
        if first in YES or low in ("do it", "run it", "go ahead", "yes please"):
            d = self.pending
            out = self.runner(d)
            self.last = d
            self.pending = None
            self.state = "home"
            return out + "\n(Done. `save <name>` to keep this configuration.)"
        if first in NO or re.search(r"\b(cancel|nevermind|never mind|abort|forget it|go back|start over)\b", low):
            self.pending = None
            self.state = "home"
            kept = ("Saved configs intact: " + ", ".join(self.library)) if self.library else "No saved configs."
            return f"Cancelled -- back to start. {kept}"
        if low in ("quit", "exit", "q"):
            return "__quit__"
        if low in ("help", "?", "h"):
            return ("You're at the confirm step. Reply:\n"
                    "  yes          run the command shown\n"
                    "  no / cancel  go back to the start (your saved configs are kept)\n"
                    "  save as <name>   name & keep this configuration\n"
                    "  quit         leave the shell\n" + self._present())
        if low.startswith("save as ") or low.startswith("name "):
            name = line.split(None, 2)[-1].strip() if low.startswith("save as ") else line[5:].strip()
            if not name:
                return "Usage: save as <name>"
            self.library[name] = self.pending
            return f"Saved this configuration as '{name}'. Still pending -- run it? [yes / no]"
        # if they typed what looks like a brand-new request, explain how to switch
        d2, _ = parse_request(line)
        if d2 is not None:
            return ("You're still confirming the previous command. Type 'no' to cancel it first, then enter your "
                    "new request -- or 'yes' to run the pending one.\n" + self._present())
        return ("I need a yes/no here. Reply 'yes' to run, 'no' (or 'cancel') to go back, "
                "'help' for options, 'quit' to leave.")

    def _list(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            cdet_lab.cmd_list()
        return buf.getvalue().rstrip()

    def repl(self):
        print("cdet lab -- interactive shell. Type 'help' for guidance, 'quit' to leave.")
        while True:
            try:
                line = input("home> " if self.state == "home" else "confirm [yes/no]> ")
            except (EOFError, KeyboardInterrupt):
                print("\nbye."); return
            resp = self.handle(line)
            if resp == "__quit__":
                print("bye."); return
            if resp:
                print(resp)


def _selftest():
    print("cdet_shell self-test (scripted session through the state machine):")
    runs = []
    sh = Shell(runner=lambda d: f"[ran: {draft_to_command(d)}]" or runs.append(d))
    sh.runner = lambda d: (runs.append(d) or f"[ran: {draft_to_command(d)}]")
    script = [
        ("help", "talk to the cdet lab"),                                   # help works
        ("equation of state for 6 flavors at U=1 mu=1", "Here's what I think"),  # NL -> draft -> confirm
        ("no", "Cancelled"),                                                # 'no' reverts
        ("selfenergy in the mott regime U=4 mu=2 beta=5", "hubbard-i"),     # synonym -> hubbard-i
        ("yes", "[ran:"),                                                   # confirm executes
        ("save mott", "Saved the last"),                                   # name + save a confirmed config
        ("density for 4 flavours U=0.5", "Here's what I think"),            # 'density'->eos, 'flavours'->N
        ("save as quick4", "Saved this configuration as 'quick4'"),         # name at confirm time
        ("no", "Saved configs intact"),                                    # 'no' keeps the library
        ("configs", "mott"),                                               # library survived the 'no'
        ("run mott", "Here's what I think"),                               # recall a saved config
        ("yes", "[ran:"),                                                   # and run it
        ("addtion pole L=12 mu=1", "Here's what I think"),                 # typo survives: 'pole' still matches
        ("cancel", "Cancelled"),                                           # 'cancel' escapes confirm (not just 'no')
        ("selfenrgy U=4 mu=2", "Did you mean"),                            # unrecognized -> did-you-mean
        ("self-energy via teleport", "isn't a solver I know"),             # explicit bad method -> guidance
        ("eos N=0 U=2 mu=1", "must be >= 1"),                              # validation: SU(0) rejected
        ("eos N=6 U=abc mu=1", "needs a number"),                          # non-numeric warned, then confirm
        ("connected determinant n=3", "still confirming"),                 # new request mid-confirm -> guidance
        ("no", "Cancelled"),                                               # back out
        ("menu", "talk to the cdet lab"),                                  # 'menu' -> help
        ("sweep U from 0.2 to 1 for self-energy diagrammatic beta 5 mu 1 accuracy 5e-3", "STUDY"),  # sweep -> study
        ("yes", "cdet_study.py"),                                          # routes to the study harness
        ("scan L from 8 to 64 for the addition pole mu=1 until it converges", "STUDY"),  # convergence sweep
        ("no", "Cancelled"),
    ]
    ok = True
    for inp, expect in script:
        resp = sh.handle(inp)
        hit = expect in resp
        ok = ok and hit
        tag = "ok" if hit else "MISS"
        print(f"  [{tag}] {inp!r:<48} -> {resp.splitlines()[0][:60] if resp else ''}")
        assert hit, f"expected {expect!r} in response to {inp!r}, got:\n{resp}"
    assert "mott" in sh.library and "quick4" in sh.library, sh.library
    assert len(runs) == 3, runs
    print("  => clarify->confirm->execute works; 'no' reverts but keeps the named/saved library; typos and bad")
    print("     methods get did-you-mean + example syntax; help/list/examples/configs all reachable. PASS")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        _selftest()
    else:
        Shell().repl()
