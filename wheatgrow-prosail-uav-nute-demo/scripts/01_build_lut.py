"""Step 1: build the JPDS-based look-up table.

Draws joint (SLA, AMAX) samples, simulates six-band canopy reflectance for
each sample, and stores the LUT (parameters + spectra + vegetation indices).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd

from src.lut import build_lut
from src.prosail_simple import BAND_NAMES
from src.vi import compute_vis


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, default=5000, help="LUT size")
    parser.add_argument("--lai", type=float, default=4.0)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--out", default="outputs/lut.csv")
    args = parser.parse_args()

    lut = build_lut(n=args.n, lai=args.lai, seed=args.seed)
    vis = compute_vis(lut["reflectance"])

    table = pd.DataFrame({"SLA": lut["SLA"], "AMAX": lut["AMAX"]})
    for name, values in zip(BAND_NAMES, lut["reflectance"].T):
        table[name] = values
    for key, values in vis.items():
        table[key] = values

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(out, index=False, encoding="utf-8")
    print(f"LUT with {len(table)} entries written to {out}")


if __name__ == "__main__":
    main()
