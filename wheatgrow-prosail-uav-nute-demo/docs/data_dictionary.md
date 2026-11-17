# Data dictionary

All tables are UTF-8 CSV with a single header row. Missing values are `NA`.

## demo_data/reflectance_demo.csv

| Field | Type | Unit | Description |
|---|---|---|---|
| PlotID | string | – | synthetic plot identifier (`D01`…`D30`) |
| Stage | string | – | growth stage code: `TS`, `HS`, `MS` |
| B450 | float | fraction | canopy reflectance at 450 nm |
| B530 | float | fraction | canopy reflectance at 530 nm |
| B570 | float | fraction | canopy reflectance at 570 nm |
| B675 | float | fraction | canopy reflectance at 675 nm |
| B730 | float | fraction | canopy reflectance at 730 nm |
| B850 | float | fraction | canopy reflectance at 850 nm |

## demo_data/traits_demo.csv

| Field | Type | Unit | Description |
|---|---|---|---|
| PlotID | string | – | synthetic plot identifier |
| Stage | string | – | growth stage code |
| SLA_true | float | m² g⁻¹ | reference specific leaf area |
| AMAX_true | float | µmol m⁻² s⁻¹ | reference maximum photosynthetic rate |
| NUtE_true | float | kg kg⁻¹ | reference nitrogen utilization efficiency |

## outputs/lut.csv

| Field | Type | Unit | Description |
|---|---|---|---|
| SLA | float | m² g⁻¹ | sampled specific leaf area |
| AMAX | float | µmol m⁻² s⁻¹ | sampled maximum photosynthetic rate |
| B450 … B850 | float | fraction | simulated six-band reflectance |
| NDVI, SAVI, OSAVI, RVI, GRVI | float | – | vegetation indices computed from the simulated spectrum |

## outputs/retrieved.csv

| Field | Type | Unit | Description |
|---|---|---|---|
| PlotID | string | – | observation identifier |
| Stage | string | – | growth stage code |
| SLA_retrieved | float | m² g⁻¹ | retrieved specific leaf area |
| AMAX_retrieved | float | µmol m⁻² s⁻¹ | retrieved maximum photosynthetic rate |
| distance | float | – | nearest-neighbour distance in normalised index space |

## outputs/nute_pred.csv

Same as `retrieved.csv` plus:

| Field | Type | Unit | Description |
|---|---|---|---|
| NUtE_pred | float | kg kg⁻¹ | predicted nitrogen utilization efficiency |

## outputs/metrics.csv

| Field | Type | Unit | Description |
|---|---|---|---|
| variable | string | – | `SLA`, `AMAX`, or `NUtE` |
| unit | string | – | placeholder text pointing to this document |
| n | integer | – | number of paired observations |
| mean_obs | float | variable | mean of reference values |
| rmse | float | variable | root mean square error |
| rrmse | float | % | RMSE normalised by `mean_obs` |
