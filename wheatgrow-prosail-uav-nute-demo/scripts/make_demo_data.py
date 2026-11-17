"""Generate synthetic demo reflectance and reference trait tables.

The demo is fully self-contained: (SLA, AMAX) are drawn from the JPDS prior,
canopy reflectance is produced with the simplified forward model, and the
reference NUtE is produced with the WheatGrow proxy. Output files mimic the
field layout used in the manuscript (PlotID / Stage / bands).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np
import pandas as pd

from src.jpds import sample_jpds
from src.prosail_simple import BAND_NAMES, simulate_reflectance
from src.wheatgrow_proxy import predict_nute

STAGES = ("TS", "HS", "MS")
LAI_DEMO = 4.0


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-plots", type=int, default=30, help="number of demo plots")
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--outdir", default="demo_data")
    parser.add_argument("--noise", type=float, default=0.01, help="absolute reflectance noise")
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(args.seed)
    n_rows = args.n_plots * len(STAGES)
    sla, amax = sample_jpds(n=args.n_plots, seed=args.seed)

    plot_ids = [f"D{i:02d}" for i in range(1, args.n_plots + 1)]

    refl_rows = []
    trait_rows = []
    for pid, s, a in zip(plot_ids, sla, amax):
        for stage in STAGES:
            clean = simulate_reflectance(s, a, lai=LAI_DEMO)
            noisy = np.clip(clean + rng.normal(0.0, args.noise, size=6), 0.0, 1.0)
            row = {"PlotID": pid, "Stage": stage}
            row.update({name: round(float(v), 4) for name, v in zip(BAND_NAMES, noisy)})
            refl_rows.append(row)

            nute_true = float(predict_nute(s, a, stage)) + rng.normal(0.0, 0.5)
            trait_rows.append(
                {
                    "PlotID": pid,
                    "Stage": stage,
                    "SLA_true": round(float(s), 5),
                    "AMAX_true": round(float(a), 2),
                    "NUtE_true": round(nute_true, 2),
                }
            )

    refl = pd.DataFrame(refl_rows)
    traits = pd.DataFrame(trait_rows)
    refl.to_csv(outdir / "reflectance_demo.csv", index=False, encoding="utf-8")
    traits.to_csv(outdir / "traits_demo.csv", index=False, encoding="utf-8")

    print(f"Wrote {len(refl)} reflectance rows and {len(traits)} trait rows to {outdir}")


if __name__ == "__main__":
    main()
