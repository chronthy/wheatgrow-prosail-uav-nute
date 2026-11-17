"""Step 3: drive the WheatGrow proxy with retrieved parameters to predict NUtE."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd

from src.wheatgrow_proxy import predict_nute


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--retrieved", default="outputs/retrieved.csv")
    parser.add_argument("--out", default="outputs/nute_pred.csv")
    args = parser.parse_args()

    df = pd.read_csv(args.retrieved)
    df["NUtE_pred"] = [
        float(predict_nute(row.SLA_retrieved, row.AMAX_retrieved, row.Stage))
        for row in df.itertuples(index=False)
    ]

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False, encoding="utf-8")
    print(f"NUtE predicted for {len(df)} observations -> {out}")


if __name__ == "__main__":
    main()
