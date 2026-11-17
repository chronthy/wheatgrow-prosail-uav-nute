# Workflow and mapping to the manuscript

This demo mirrors the analytical chain of the paper with lightweight,
dependency-free stand-ins for the two external models.

## Pipeline

```
demo_data/reflectance_demo.csv
        │
        ▼
[02] LUT retrieval ──────── uses outputs/lut.csv
        │  SLA_retrieved, AMAX_retrieved
        ▼
[03] WheatGrow proxy
        │  NUtE_pred
        ▼
[04] accuracy evaluation ── against demo_data/traits_demo.csv
        │  outputs/metrics.csv, outputs/demo_scatter.png
```

`[01]` builds the LUT consumed by `[02]`:

```
JPDS sampling (SLA, AMAX)  →  forward model (6 bands)  →  LUT table
```

## Mapping to manuscript sections

| Demo component | Manuscript section | Notes |
|---|---|---|
| `src/jpds.py` | 2.3 JPDS-based LUT | 2-D truncated multivariate normal, `r = 0.6` |
| `src/prosail_simple.py` | 2.3 PROSAIL forward simulation | simplified stand-in; replace with official PROSAIL |
| `src/lut.py` | 2.3 LUT construction and retrieval | nearest neighbour on z-scored indices |
| `src/vi.py` | 2.4 optimal vegetation indices | GRVI, OSAVI, SAVI, RVI, NDVI |
| `src/wheatgrow_proxy.py` | 2.2 / 2.5 assimilation | surrogate for the WheatGrow call |
| `src/evaluate.py` | 3.x accuracy assessment | RMSE / RRMSE |

## Replacing the stand-ins

- **PROSAIL**: keep the `simulate_reflectance(sla, amax, lai, soil) -> (n, 6)`
  signature and substitute a call to PROSAIL-Py.
- **WheatGrow**: keep `predict_nute(sla, amax, stage)` and wrap the official
  model, returning NUtE in kg kg⁻¹.

## Data flow conventions

- Band order everywhere: 450, 530, 570, 675, 730, 850 nm.
- Reflectance as fraction (0-1).
- SLA in m² g⁻¹; AMAX in µmol m⁻² s⁻¹; NUtE in kg kg⁻¹.
- `PlotID`/`Stage` are the join keys between tables.
