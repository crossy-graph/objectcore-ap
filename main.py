#!/usr/bin/env python3
"""ObjectCore-AP orchestrator: the only entry point.

    python main.py                  all steps, in order
    python main.py --list           print the steps and exit
    python main.py --only figures   one step
    python main.py --from model     this step and all after it
    python main.py --skip test      all but this step
    python main.py --dry-run        print the plan, run nothing
    python main.py --strict         warnings become errors (what CI runs)
    python main.py --dcatap PATH    also run the official DCAT-AP 3.0.1 SHACL (PATH = DCAT-AP/releases/3.0.1/shacl)
"""
import argparse
import importlib
import io
import os
import pathlib
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "py"))

STEPS = [
    ("generate", "step_generate", "LinkML profile -> JSON Schema, SHACL, OWL (dist/)"),
    ("test", "step_test", "validate the RDF examples against the profile shapes (dist/test_results.json)"),
    ("model", "step_model", "condense profile, crosswalk, examples and tests (dist/model.json)"),
    ("figures", "step_figures", "draw the figures (docs/visuals/img/)"),
    ("site", "step_site", "write the documentation and figure pages (docs/)"),
]


def run_step(name, module, extra):
    """Run a step module in a child process so that its output is captured and passed through line by line."""
    env = dict(os.environ, PYTHONIOENCODING="utf-8", SOURCE_DATE_EPOCH="0")
    cmd = [sys.executable, str(ROOT / "py" / (module + ".py"))] + extra
    p = subprocess.Popen(cmd, cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8")
    lines = []
    for line in p.stdout:
        line = line.rstrip("\n")
        print("   " + line)
        lines.append(line)
    return p.wait(), lines


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--only")
    ap.add_argument("--from", dest="from_")
    ap.add_argument("--skip", action="append", default=[])
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--dcatap")
    a = ap.parse_args()
    names = [s[0] for s in STEPS]
    if a.list:
        for n, _, d in STEPS:
            print("%-9s %s" % (n, d))
        return 0
    for n in ([a.only] if a.only else []) + ([a.from_] if a.from_ else []) + a.skip:
        if n not in names:
            sys.exit("unknown step %r; known: %s" % (n, ", ".join(names)))
    plan = [s for s in STEPS if (not a.only or s[0] == a.only) and s[0] not in a.skip]
    if a.from_:
        plan = [s for s in plan if names.index(s[0]) >= names.index(a.from_)]
    if a.dry_run:
        for n, m, d in plan:
            print("would run %-9s %s" % (n, d))
        return 0
    report, timing = [], []
    for n, m, d in plan:
        print("== %s: %s" % (n, d))
        extra = ["--dcatap", a.dcatap] if (n == "test" and a.dcatap) else []
        t0 = time.perf_counter()
        rc, lines = run_step(n, m, extra)
        timing.append((n, time.perf_counter() - t0))
        report += ["== " + n] + lines
        if rc:
            sys.exit("step %s failed (exit %d)" % (n, rc))
        if a.strict and any("warning" in l.lower() for l in lines):
            sys.exit("step %s printed warnings (--strict)" % n)
    tot = sum(t for _, t in timing) or 1
    print("\nstep       seconds  share")
    for n, t in timing:
        print("%-9s %8.1f  %4.0f%%" % (n, t, 100 * t / tot))
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
