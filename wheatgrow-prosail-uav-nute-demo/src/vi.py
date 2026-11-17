"""Vegetation index calculation (band order: 450, 530, 570, 675, 730, 850 nm)."""
from __future__ import annotations

import numpy as np

EPS = 1e-9


def compute_vis(reflectance) -> dict[str, np.ndarray]:
    """Compute the five vegetation indices used in the manuscript.

    Parameters
    ----------
    reflectance : array_like
        Shape (..., 6) with bands ordered 450, 530, 570, 675, 730, 850 nm.

    Returns
    -------
    dict of ndarray with keys NDVI, SAVI, OSAVI, RVI, GRVI.
    """
    r = np.asarray(reflectance, dtype=float)
    if r.shape[-1] != 6:
        raise ValueError("Expected 6 bands ordered 450/530/570/675/730/850 nm.")
    b450, b530, b570, b675, b730, b850 = (r[..., i] for i in range(6))

    ndvi = (b850 - b675) / (b850 + b675 + EPS)
    savi = (b850 - b675) / (b850 + b675 + 0.5) * 1.5
    osavi = (b850 - b675) / (b850 + b675 + 0.16)
    rvi = b850 / (b675 + EPS)
    grvi = b850 / (b570 + EPS)

    return {"NDVI": ndvi, "SAVI": savi, "OSAVI": osavi, "RVI": rvi, "GRVI": grvi}
