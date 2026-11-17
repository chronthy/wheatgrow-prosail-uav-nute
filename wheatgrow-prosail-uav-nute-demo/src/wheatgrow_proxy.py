"""WheatGrow proxy interface (DEMO ONLY).

The real WheatGrow model is not distributed with this repository. This
module exposes the same call signature and a transparent surrogate
relationship so that the full pipeline can run. Replace
``predict_nute`` with a wrapper around the official WheatGrow binary/API
when running production analyses.
"""
from __future__ import annotations

import numpy as np

# Relative adjustment of NUtE by growth stage (heading-anthesis = reference).
STAGE_ADJUSTMENT = {
    "TS": -3.0,
    "JS": -1.0,
    "HS": 0.0,
    "ANT": 0.0,
    "MS": -2.0,
}


def predict_nute(sla, amax, stage: str = "HS"):
    """Map cultivar parameters to NUtE (kg kg-1).

    The surrogate is linear in SLA and AMAX, with a stage offset. It is
    calibrated to the range reported in the manuscript (roughly 25-65
    kg grain per kg N) but carries no physiological validity.
    """
    sla_arr = np.asarray(sla, dtype=float)
    amax_arr = np.asarray(amax, dtype=float)

    base = 45.0 + 6000.0 * (sla_arr - 0.005) + 0.25 * (amax_arr - 40.0)
    return base + STAGE_ADJUSTMENT.get(stage, 0.0)
