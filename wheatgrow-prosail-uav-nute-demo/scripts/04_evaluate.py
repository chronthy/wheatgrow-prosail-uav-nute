"""Step 4: evaluate retrieval and prediction accuracy against reference values."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd

from src.evaluate import summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pred", default="outputs/nute_pred.csv")
    parser.add_argument("--truth", default="demo_data/traits_demo.csv")
    parser.add_argument("--out", default="outputs/metrics.csv")
    parser.add_argument("--figure", default="outputs/demo_scatter.png")
    args = parser.parse_args()

    pred = pd.read_csv(args.pred)
    truth = pd.read_csv(args.truth)
    merged = pred.merge(truth, on=["PlotID", "Stage"], how="inner")
    if merged.empty:
        raise RuntimeError("No overlapping PlotID/Stage between prediction and reference tables.")

    rows = []
    for target, obs_col, pred_col in (
        ("SLA", "SLA_true", "SLA_retrieved"),
        ("AMAX", "AMAX_true", "AMAX_retrieved"),
        ("NUtE", "NUtE_true", "NUtE_pred"),
    ):
        stats = summary(merged[obs_col], merged[pred_col])
        rows.append({"variable": target, "unit": "see data dictionary", **stats})

    metrics = pd.DataFrame(rows)[["variable", "unit", "n", "mean_obs", "rmse", "rrmse"]]
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    metrics.to_csv(out, index=False, encoding="utf-8")

    print(metrics.to_string(index=False))

    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception:
        return

    fig, axes = plt.subplots(1, 2, figsize=(9, 4.2))
    axes[0].scatter(merged["SLA_true"], merged["SLA_retrieved"], s=14)
    axes[0].set_xlabel("SLA observed (m2 g-1)")
    axes[0].set_ylabel("SLA retrieved (m2 g-1)")
    axes[1].scatter(merged["NUtE_true"], merged["NUtE_pred"], s=14, color="tab:orange")
    axes[1].set_xlabel("NUtE reference (kg kg-1)")
    axes[1].set_ylabel("NUtE predicted (kg kg-1)")
    for ax in axes:
        lim = [min(ax.get_xlim()[0], ax.get_ylim()[0]), max(ax.get_xlim()[1], ax.get_ylim()[1])]
        ax.plot(lim, lim, color="grey", lw=1, ls="--")
    fig.tight_layout()
    fig.savefig(args.figure, dpi=200)
    print(f"Scatter plot saved to {args.figure}")


if __name__ == "__main__":
    main()
