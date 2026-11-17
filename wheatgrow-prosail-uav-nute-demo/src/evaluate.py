"""Accuracy metrics."""
from __future__ import annotations

import numpy as np


def rmse(observed, predicted) -> float:
    """Root mean square error."""
    obs = np.asarray(observed, dtype=float)
    pred = np.asarray(predicted, dtype=float)
    return float(np.sqrt(np.mean((pred - obs) ** 2)))


def rrmse(observed, predicted) -> float:
    """Relative RMSE in percent (normalised by the mean of observations)."""
    obs = np.asarray(observed, dtype=float)
    pred = np.asarray(predicted, dtype=float)
    mean_obs = float(np.mean(obs))
    if mean_obs == 0:
        raise ValueError("Mean of observations is zero; RRMSE undefined.")
    return rmse(obs, pred) / mean_obs * 100.0


def summary(observed, predicted) -> dict[str, float]:
    return {
        "n": int(np.asarray(observed).size),
        "mean_obs": float(np.mean(observed)),
        "rmse": rmse(observed, predicted),
        "rrmse": rrmse(observed, predicted),
    }
