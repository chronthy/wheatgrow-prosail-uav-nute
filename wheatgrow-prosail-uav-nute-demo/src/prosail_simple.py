"""Simplified canopy-reflectance forward model (DEMO ONLY).

This module provides a lightweight, dependency-free stand-in for PROSAIL so
that the whole retrieval pipeline can be demonstrated end-to-end. It keeps
the same input signature as a PROSAIL call (SLA, AMAX, LAI, soil spectrum,
six spectral bands) so that users can replace it with the official
PROSAIL/PROSAIL-Py implementation.

WARNING: the formulation below is a pedagogical approximation, not a
radiative-transfer model. Quantitative results must be produced with the
official PROSAIL model.
"""
from __future__ import annotations

import numpy as np

# Central wavelengths used in this demo (nm).
BANDS = (450.0, 530.0, 570.0, 675.0, 730.0, 850.0)
BAND_NAMES = ("B450", "B530", "B570", "B675", "B730", "B850")

# Bare-soil reflectance assumed for the demo (fraction).
SOIL_REFLECTANCE = np.array([0.10, 0.14, 0.16, 0.18, 0.20, 0.22])


def simulate_reflectance(
    sla,
    amax,
    lai=4.0,
    soil: np.ndarray | None = None,
) -> np.ndarray:
    """Simulate six-band canopy reflectance from leaf traits.

    Parameters
    ----------
    sla : float or array_like
        Specific leaf area (m2 g-1).
    amax : float or array_like
        Maximum photosynthetic rate (umol m-2 s-1).
    lai : float or array_like
        Leaf area index.
    soil : ndarray, optional
        Six-band soil reflectance.

    Returns
    -------
    ndarray
        Shape (6,) for scalar input, (n, 6) for array input.
        Values are fractions between 0 and 1.
    """
    sla_arr = np.asarray(sla, dtype=float)
    amax_arr = np.asarray(amax, dtype=float)
    scalar = sla_arr.ndim == 0

    # Chlorophyll proxy scaled to [0, 1] and SLA proxy scaled to [-1, 1].
    c = (amax_arr - 20.0) / 40.0
    s = (sla_arr - 0.005) / 0.003

    # Leaf-level spectral response: pigments absorb in blue/red, NIR scatters.
    r_veg = np.stack(
        [
            0.050 - 0.020 * c + 0.010 * s,
            0.100 - 0.030 * c + 0.020 * s,
            0.120 - 0.030 * c + 0.020 * s,
            0.080 - 0.050 * c + 0.020 * s,
            0.180 + 0.080 * c - 0.040 * s,
            0.400 + 0.100 * c + 0.060 * s,
        ],
        axis=-1,
    )

    soil_arr = SOIL_REFLECTANCE if soil is None else np.asarray(soil, dtype=float)

    # Beer-Lambert style canopy/soil mixing.
    tau = np.exp(-0.5 * np.asarray(lai, dtype=float))
    if r_veg.ndim == 1:
        canopy = soil_arr * tau + r_veg * (1.0 - tau)
    else:
        canopy = soil_arr[None, :] * tau[..., None] + r_veg * (1.0 - tau[..., None])

    return canopy if not scalar else canopy.reshape(6)
