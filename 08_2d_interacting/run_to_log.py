"""run_to_log.py (v124) -- stream a long engine run to a log file with crash detection.

For unattended day-long / large-L runs: launches the engine, streams every line to BOTH the console and
a log file as it arrives (line-buffered, so partial results survive a crash), and detects three failure
modes -- the engine's own NONFINITE precision-wall marker, a non-zero exit, and a killing signal --
writing a clear final status line either way. No run timeout is imposed here; the engine streams and the
log accumulates until it finishes or dies.

Usage:
    python3 run_to_log.py LOGFILE -- ENGINE arg1 arg2 ...
e.g.
    python3 run_to_log.py /tmp/run_L12.log -- ./cpw grid 24 200 4 16 4096 31 0.002 0 2 1 2 4 1.0 -L 12

The log gets every engine line plus a header (command, start time) and a footer (status, last good
beta, elapsed). Tail the log to watch progress live; if the process dies, the log holds all completed
points and the failure reason.
"""
import sys, os, time, subprocess, signal, datetime


def main(argv):
    if "--" not in argv:
        print("usage: python3 run_to_log.py LOGFILE -- ENGINE args...", file=sys.stderr)
        return 2
    cut = argv.index("--")
    logpath = argv[1] if len(argv) > 1 and argv[1] != "--" else os.path.join(tempfile.gettempdir(), 'engine_run.log')
    cmd = argv[cut + 1:]
    if not cmd:
        print("no engine command after --", file=sys.stderr)
        return 2

    start = time.time()
    last_good = None          # last beta with finite output
    npoints = 0
    status = "unknown"

    with open(logpath, "w", buffering=1) as log:   # line-buffered: each write hits disk
        def w(line):
            log.write(line)
            log.flush()
            os.fsync(log.fileno())                 # survive a hard crash / power loss
            sys.stdout.write(line)
            sys.stdout.flush()

        w(f"# run_to_log {datetime.datetime.now().isoformat()}\n")
        w(f"# cmd: {' '.join(cmd)}\n")
        try:
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                    text=True, bufsize=1)
        except FileNotFoundError:
            w(f"# STATUS: engine not found ({cmd[0]})\n")
            return 1

        try:
            for line in proc.stdout:               # streams as the engine flushes
                w(line if line.endswith("\n") else line + "\n")
                if line.startswith("# NONFINITE"):
                    status = "precision-wall (NONFINITE)"
                parts = line.split()
                if parts and parts[0][0].isdigit():
                    try:
                        beta = float(parts[0]); float(parts[1])   # a real data line
                        last_good = beta; npoints += 1
                    except (ValueError, IndexError):
                        pass
            rc = proc.wait()
        except KeyboardInterrupt:
            proc.send_signal(signal.SIGTERM); rc = proc.wait()
            status = "interrupted by user"

        if status == "unknown":
            if rc == 0:
                status = "completed"
            elif rc < 0:
                status = f"killed by signal {-rc} ({signal.Signals(-rc).name if -rc in [s.value for s in signal.Signals] else -rc})"
            else:
                status = f"nonzero exit {rc}"

        elapsed = time.time() - start
        w(f"# STATUS: {status}\n")
        w(f"# points: {npoints}  last_good_beta: {last_good}  elapsed: {elapsed:.1f}s\n")
    return 0


def _selftest():
    """Self-test: run a tiny engine-like producer that streams 3 lines then a NONFINITE, confirm the log
    captures all lines + the precision-wall status + last_good_beta, without any real engine."""
    import tempfile
    producer = ('import sys,time\n'
                'for b in (24,48,72):\n'
                '    print(f"{b}.0 1.0e+00 1e-2 -2.0e+02 1e0",flush=True)\n'
                'print("# NONFINITE at beta=96.0 (A=nan c1=nan) -- precision wall; stopping grid",flush=True)\n')
    pf = tempfile.NamedTemporaryFile("w", suffix=".py", delete=False); pf.write(producer); pf.close()
    log = tempfile.NamedTemporaryFile(suffix=".log", delete=False).name
    rc = main(["run_to_log.py", log, "--", sys.executable, pf.name])
    text = open(log).read()
    assert rc == 0
    assert "24.0" in text and "48.0" in text and "72.0" in text, "data lines missing"
    assert "precision-wall (NONFINITE)" in text, "NONFINITE not detected"
    assert "last_good_beta: 72.0" in text, "last_good_beta wrong"
    assert "points: 3" in text, "point count wrong"
    os.unlink(pf.name); os.unlink(log)
    print("run_to_log self-test: streamed 3 points + caught the precision wall, logged last_good_beta=72.0  PASS")


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "selftest":
        _selftest()
    else:
        sys.exit(main(sys.argv))
