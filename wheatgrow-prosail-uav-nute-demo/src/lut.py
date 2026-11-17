"""Look-up-table construction and nearest-neighbour retrieval.

The LUT is built by drawing joint (SLA, AMAX) samples with JPDS and running
the forward model for each sample. Retrieval matches an observed spectrum
(or its vegetation-index vector) to the closest LUT entry.
"""
from __future__ import annotations

import numpy as np

from .jpds import sample_jpds
from .prosail_simple import simulate_reflectance
from .vi import compute_vis

DEFAULT_INDICES = ("GRVI", "OSAVI", "SAVI", "RVI")


def build_lut(n: int = 5000, lai: float = 4.0, seed: int = 42) -> dict:
    """Build a demo LUT of n entries."""
    sla, amax = sample_jpds(n=n, seed=seed)
    reflectance = simulate_reflectance(sla, amax, lai=lai)
    vis = compute_vis(reflectance)
    return {
        "SLA": sla,
        "AMAX": amax,
        "reflectance": np.atleast_2d(reflectance),
        "vi": vis,
    }


def retrieve(
    reflectance,
    lut: dict,
    indices=DEFAULT_INDICES,
    metric: str = "vi",
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Retrieve SLA and AMAX for each observed spectrum.

    Parameters
    ----------
    reflectance : array_like, shape (m, 6) or (6,)
    lut : dict produced by build_lut
    indices : tuple of str
        Vegetation indices used when metric="vi".
    metric : {"vi", "spectral"}

    Returns
    -------
    sla, amax, distance : ndarray, shape (m,)
    """
    obs = np.atleast_2d(np.asarray(reflectance, dtype=float))
    if obs.shape[1] != 6:
        raise ValueError("Expected six bands per spectrum.")

    if metric == "spectral":
        lut_mat = lut["reflectance"]
        obs_mat = obs
    elif metric == "vi":
        obs_vis = compute_vis(obs)
        keys = list(indices)
        lut_mat = np.column_stack([np.asarray(lut["vi"][k]) for k in keys])
        obs_mat = np.column_stack([np.asarray(obs_vis[k]) for k in keys])
    else:
        raise ValueError("metric must be 'vi' or 'spectral'.")

    # z-score normalisation keeps indices with different magnitudes comparable.
    mu = lut_mat.mean(axis=0)
    sd = lut_mat.std(axis=0) + 1e-9
    lut_z = (lut_mat - mu) / sd
    obs_z = (obs_mat - mu) / sd

    # Squared Euclidean distance for every observation / LUT entry pair.
    dist = ((obs_z[:, None, :] - lut_z[None, :, :]) ** 2).sum(axis=-1)
    best = dist.argmin(axis=1)

    return lut["SLA"][best], lut["AMAX"][best], np.sqrt(dist[np.arange(len(obs)), best])
