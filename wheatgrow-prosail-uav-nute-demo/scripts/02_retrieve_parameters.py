"""Step 2: retrieve SLA and AMAX from observed spectra using the LUT."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd

from src.lut import retrieve
from src.prosail_simple import BAND_NAMES
from src.vi import compute_vis

DEFAULT_INDICES = ("GRVI", "OSAVI", "SAVI", "RVI")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lut", default="outputs/lut.csv")
    parser.add_argument("--reflectance", default="demo_data/reflectance_demo.csv")
    parser.add_argument("--metric", choices=("vi", "spectral"), default="vi")
    parser.add_argument("--out", default="outputs/retrieved.csv")
    args = parser.parse_args()

    lut_table = pd.read_csv(args.lut)
    lut = {
        "SLA": lut_table["SLA"].to_numpy(),
        "AMAX": lut_table["AMAX"].to_numpy(),
        "reflectance": lut_table[list(BAND_NAMES)].to_numpy(),
        "vi": {
            key: lut_table[key].to_numpy()
            for key in ("NDVI", "SAVI", "OSAVI", "RVI", "GRVI")
        },
    }

    obs = pd.read_csv(args.reflectance)
    sla, amax, dist = retrieve(
        obs[list(BAND_NAMES)].to_numpy(), lut, indices=DEFAULT_INDICES, metric=args.metric
    )

    result = obs[["PlotID", "Stage"]].copy()
    result["SLA_retrieved"] = sla
    result["AMAX_retrieved"] = amax
    result["distance"] = dist

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(out, index=False, encoding="utf-8")
    print(f"Retrieved parameters for {len(result)} observations -> {out}")


if __name__ == "__main__":
    main()
