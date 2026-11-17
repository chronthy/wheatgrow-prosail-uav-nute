"""Joint probability distribution sampling (JPDS) for SLA and AMAX.

Implements the 2-D truncated multivariate-normal sampling described in
Section 2.3 of the manuscript: the marginal distributions of SLA and AMAX
are assumed normal, linked by a linear correlation coefficient r.

Demo implementation only -- production runs should use the exact prior
parameters reported in the paper.
"""
from __future__ import annotations

import numpy as np

DEFAULT_CONFIG = {
    "SLA": {"min": 0.002, "max": 0.008, "mean": 0.005, "sd": 0.001},
    "AMAX": {"min": 20.0, "max": 60.0, "mean": 40.0, "sd": 10.0},
    "correlation_r": 0.6,
}


def build_covariance(sd_sla: float, sd_amax: float, r: float) -> np.ndarray:
    """Build the 2x2 covariance matrix for (SLA, AMAX)."""
    return np.array(
        [
            [sd_sla**2, r * sd_sla * sd_amax],
            [r * sd_sla * sd_amax, sd_amax**2],
        ]
    )


def sample_jpds(
    n: int = 5000,
    config: dict | None = None,
    seed: int = 42,
    max_iter: int = 100,
) -> tuple[np.ndarray, np.ndarray]:
    """Draw n joint samples of (SLA, AMAX) inside the prior range.

    Returns
    -------
    sla, amax : ndarray, shape (n,)
    """
    cfg = config or DEFAULT_CONFIG
    rng = np.random.default_rng(seed)

    mu = np.array([cfg["SLA"]["mean"], cfg["AMAX"]["mean"]])
    cov = build_covariance(cfg["SLA"]["sd"], cfg["AMAX"]["sd"], cfg["correlation_r"])
    lower = np.array([cfg["SLA"]["min"], cfg["AMAX"]["min"]])
    upper = np.array([cfg["SLA"]["max"], cfg["AMAX"]["max"]])

    kept = []
    total = 0
    it = 0
    while total < n and it < max_iter:
        draw = rng.multivariate_normal(mu, cov, size=n * 2)
        mask = np.all((draw >= lower) & (draw <= upper), axis=1)
        batch = draw[mask]
        if batch.size:
            kept.append(batch)
            total += len(batch)
        it += 1

    if total < n:
        raise RuntimeError(
            f"Only {total} samples inside the prior range after {max_iter} iterations."
        )

    samples = np.vstack(kept)[:n]
    return samples[:, 0], samples[:, 1]
