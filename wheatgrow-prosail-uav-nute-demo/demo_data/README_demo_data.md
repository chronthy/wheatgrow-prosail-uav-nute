# Synthetic demo data

`reflectance_demo.csv` and `traits_demo.csv` are **generated**, not measured.

## How they are produced

1. Draw 30 pairs of (SLA, AMAX) with the JPDS sampler (`src/jpds.py`), using
   the prior ranges reported in the manuscript:
   - SLA: 0.002–0.008 m² g⁻¹, μ = 0.005, σ = 0.001
   - AMAX: 20–60 µmol m⁻² s⁻¹, μ = 40, σ = 10
   - correlation r = 0.6
2. For each plot and each of three stages (TS, HS, MS), simulate six-band
   canopy reflectance with `src/prosail_simple.py` at a fixed LAI of 4.0 and
   add absolute Gaussian noise (σ = 0.01).
3. Produce `NUtE_true` with the WheatGrow surrogate
   (`src/wheatgrow_proxy.py`) plus a small random error (σ = 0.5 kg kg⁻¹).

Scale: 30 plots × 3 stages = 90 rows per table.

## Why the numbers are plausible but not meaningful

Because reflectance and reference traits are produced by the same simplified
model family, retrieval errors stay moderate (RRMSE around 10–16 %).
This demonstrates that the pipeline is correctly wired; it says nothing about
the physical accuracy of PROSAIL or WheatGrow. Do not cite these values as
results.

## Regenerating

```bash
python scripts/make_demo_data.py --n-plots 30 --seed 7 --outdir demo_data
```
