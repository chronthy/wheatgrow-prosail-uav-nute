"""End-to-end smoke test for the demo pipeline."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(script: str, *args: str) -> None:
    cmd = [sys.executable, str(ROOT / "scripts" / script), *args]
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    assert proc.returncode == 0, f"{script} failed:\n{proc.stdout}\n{proc.stderr}"


def test_pipeline(tmp_path: Path) -> None:
    lut = str(tmp_path / "lut.csv")
    retrieved = str(tmp_path / "retrieved.csv")
    pred = str(tmp_path / "nute.csv")
    metrics = str(tmp_path / "metrics.csv")

    run("01_build_lut.py", "--n", "400", "--out", lut)
    run(
        "02_retrieve_parameters.py",
        "--lut", lut,
        "--reflectance", str(ROOT / "demo_data" / "reflectance_demo.csv"),
        "--out", retrieved,
    )
    run("03_predict_nute.py", "--retrieved", retrieved, "--out", pred)
    run("04_evaluate.py", "--pred", pred, "--truth", str(ROOT / "demo_data" / "traits_demo.csv"),
        "--out", metrics)

    text = Path(metrics).read_text(encoding="utf-8")
    assert "SLA" in text and "NUtE" in text
