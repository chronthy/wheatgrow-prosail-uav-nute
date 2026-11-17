# WheatGrow–PROSAIL–UAV NUtE demo

A self-contained, runnable demonstration of the framework described in:

> **A WheatGrow–PROSAIL coupled framework assimilating UAV multispectral imagery
> for plot-scale winter wheat nitrogen utilization efficiency prediction and
> cultivar-specific parameter retrieval** *(manuscript under review)*

The demo reproduces the full analytical chain — **JPDS sampling → PROSAIL-type
forward simulation → LUT construction → SLA/AMAX retrieval from six-band
reflectance → WheatGrow-type assimilation → NUtE prediction → accuracy
evaluation** — on a small synthetic dataset.

## Scope and limitations (please read first)

1. This repository is a **method demonstration**. It contains **no** raw UAV
   imagery, ground hyperspectral measurements, field observations, or
   WheatGrow source code from the manuscript.
2. `src/prosail_simple.py` is a **simplified, pedagogical forward model**, not a
   radiative-transfer model. It is intentionally written with the same input
   signature as PROSAIL so it can be swapped for the official
   PROSAIL/PROSAIL-Py implementation.
3. `src/wheatgrow_proxy.py` is a **transparent surrogate** standing in for the
   WheatGrow interface. Replace `predict_nute` with a wrapper around the
   official model for production runs.
4. `demo_data/` is **synthetic**. Results obtained with it validate that the
   pipeline runs; they carry no agronomic meaning and must not be compared
   with the numbers reported in the paper.

## Repository layout

```
demo_data/   synthetic reflectance and reference-trait tables
src/         JPDS, forward model, LUT, vegetation indices, WheatGrow proxy, metrics
scripts/     four numbered pipeline steps + demo-data generator
tests/       end-to-end smoke test
docs/        workflow and data dictionary
outputs/     results written by the scripts
```

## Quick start

```bash
pip install -r requirements.txt

# (optional) regenerate the synthetic demo data
python scripts/make_demo_data.py --n-plots 30 --outdir demo_data

# 1. build the JPDS look-up table
python scripts/01_build_lut.py --n 5000 --out outputs/lut.csv

# 2. retrieve SLA / AMAX from observed spectra
python scripts/02_retrieve_parameters.py \
    --lut outputs/lut.csv \
    --reflectance demo_data/reflectance_demo.csv \
    --out outputs/retrieved.csv

# 3. predict NUtE with the WheatGrow proxy
python scripts/03_predict_nute.py \
    --retrieved outputs/retrieved.csv \
    --out outputs/nute_pred.csv

# 4. evaluate against the synthetic reference values
python scripts/04_evaluate.py \
    --pred outputs/nute_pred.csv \
    --truth demo_data/traits_demo.csv \
    --out outputs/metrics.csv \
    --figure outputs/demo_scatter.png
```

End-to-end runtime is well under two minutes. A smoke test is available:

```bash
pytest -q
```

## Expected demo output

With the default seed and 5 000 LUT entries, the demo reproduces the pipeline
with the following accuracy on the synthetic data (illustrative only):

| Variable | RMSE | RRMSE |
|---|---|---|
| SLA (m² g⁻¹) | 0.00076 | 15.9 % |
| AMAX (µmol m⁻² s⁻¹) | 4.18 | 11.0 % |
| NUtE (kg kg⁻¹) | 4.34 | 10.5 % |

## Method notes

- **JPDS**: 2-D truncated multivariate normal for (SLA, AMAX), with prior
  ranges, means, standard deviations and `r = 0.6` configured in
  `src/jpds.py`; 4-D is `correlation_r`.
- **Retrieval**: nearest neighbour in z-scored vegetation-index space
  (GRVI, OSAVI, SAVI, RVI) by default; `--metric spectral` uses the six bands
  directly.
- **Assimilation**: the surrogate maps retrieved SLA/AMAX and growth stage to
  NUtE, mirroring the call pattern of the coupled WheatGrow run.

See `docs/workflow.md` for the mapping between each script and the
corresponding section of the manuscript, and `docs/data_dictionary.md` for
field definitions.

## Data and code availability

This demo repository is intended as the companion code for the manuscript.
Raw data and the WheatGrow model are not included, for the reasons stated in
the Data Availability Statement of the paper.

## License

Code: MIT (see `LICENSE`). Demo data: CC BY 4.0.

## Citation

See `CITATION.cff`. Please also cite the manuscript once it is published.
