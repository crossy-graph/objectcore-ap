"""Step generate: LinkML profile -> JSON Schema, SHACL (raw and merged), OWL in dist/."""
import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from objectcore_utils import DIST, ROOT, SCHEMA, ensure_dirs  # noqa: E402

BIN = pathlib.Path(sys.executable).parent


def tool(name):
    return str(BIN / name) if (BIN / name).exists() else name


def run(cmd, out=None):
    print("  $", " ".join(pathlib.Path(c).name if i == 0 else str(c) for i, c in enumerate(cmd)))
    res = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    if res.returncode != 0:
        sys.exit(res.stdout + res.stderr)
    if out:
        pathlib.Path(out).write_text(res.stdout, encoding="utf-8", newline="\n")


def main():
    ensure_dirs()
    run([tool("gen-json-schema"), "--include-range-class-descendants", "-t", "ObjectCoreDataset", str(SCHEMA)],
        DIST / "objectcore_ap.schema.json")
    run([tool("gen-shacl"), "--non-closed", str(SCHEMA)], DIST / "objectcore_ap.shacl.ttl")
    run([sys.executable, "tools/postprocess_shacl.py", "dist/objectcore_ap.shacl.ttl", "dist/objectcore_ap.shacl.merged.ttl"])
    run([tool("gen-owl"), str(SCHEMA)], DIST / "objectcore_ap.owl.ttl")
    print("generate: 4 artefacts in dist/")


if __name__ == "__main__":
    main()
