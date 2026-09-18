# Green Roof Detection in Baden-Württemberg

A reproducible machine-learning workflow for detecting vegetated roof planes across Baden-Württemberg, Germany, by integrating **LoD2 CityGML roof geometry** with **seasonal PlanetScope multispectral imagery**.

This repository contains the publication-oriented Random Forest workflow developed from the master's thesis:

> **Detecting Green Roofs in Baden-Württemberg by Integrating LoD2 CityGML and PlanetScope Imagery in a Supervised Machine Learning Framework**  
> Lukman Hakim — M.Sc. Photogrammetry and Geoinformatics, Hochschule für Technik Stuttgart

## Overview

The project classifies individual **LoD2 roof planes** as:

- `0` — non-vegetated roof
- `1` — vegetated / green roof

The workflow combines geometric, spectral, and semantic attributes into a tabular supervised-learning model. The final production classifier is a **Random Forest** implemented as a scikit-learn `Pipeline`, so preprocessing and classification are stored together in the exported model.

The public repository intentionally focuses on the final model workflow rather than reproducing every intermediate data-engineering step used during thesis development.

## Study design

Training labels were produced for four cities in Baden-Württemberg:

- Stuttgart
- Karlsruhe
- Freiburg im Breisgau
- Tübingen

After quality filtering, the final labelled dataset contained **18,216 roof planes**, including **2,953 vegetated roofs** (~16.2%).

Spatial transferability was evaluated using **Leave-One-City-Out (LOCO)** cross-validation. A repeated stratified mixed-sample evaluation was additionally used as a conventional non-spatial benchmark.

## Data sources

The original research workflow used:

- **LoD2 CityGML building data** from Landesamt für Geoinformation und Landentwicklung Baden-Württemberg (LGL BW)
- **PlanetScope monthly basemap imagery** for February 2025 and August 2025
- **Administrative boundaries** from Bundesamt für Kartographie und Geodäsie (BKG)
- **Google and Bing imagery** for manual visual interpretation during labelling only

All geospatial processing was performed in **ETRS89 / UTM Zone 32N (EPSG:25832)**.

Raw and intermediate datasets are **not distributed in this repository** because of their size and/or licensing constraints.

## Final model

The final classifier is a `RandomForestClassifier` with:

```python
RandomForestClassifier(
    n_estimators=600,
    min_samples_leaf=2,
    n_jobs=-1,
    random_state=42,
    class_weight="balanced_subsample",
)
```

Class imbalance during training is additionally addressed using balanced sample weights.

### Final feature set

The final C3 configuration contains **14 predictors**.

#### Geometry

- `slope_deg`
- `area_m2`
- `height_m`
- `height_relief_m`

#### Winter spectral features

- `G_avg_Winter`
- `B_avg_Winter`
- `NDVI_avg_Winter`
- `NDVI_std_Winter`

#### Summer spectral features

- `G_avg_Summer`
- `B_avg_Summer`
- `NDVI_avg_Summer`
- `NDVI_std_Summer`

#### Semantic attributes

- `roofType`
- `function`

Raw Red and NIR band means and roof aspect were excluded from the final configuration after feature-selection and ablation experiments.

## Preprocessing

Numeric predictors are processed using:

- median imputation
- missing-value indicators

Categorical predictors are processed using:

- most-frequent imputation
- one-hot encoding
- `handle_unknown="ignore"`

The complete preprocessing stage is stored inside the exported scikit-learn pipeline.

## Model performance

The thesis reports approximately:

| Evaluation protocol | PR-AUC |
|---|---:|
| Leave-One-City-Out (final C3 feature set) | 0.694 ± 0.096 |
| Repeated Stratified K-Fold, 5×3 | 0.844 ± 0.008 |

LOCO is the primary evaluation because it tests transfer to an entirely unseen city rather than to randomly mixed samples from the same cities.

The difference between spatial and mixed-sample performance should therefore be interpreted as an indication of the difficulty of geographic transfer.

## Repository structure

```text
green-roof-detection-bw/
│
├── README.md
├── LICENSE
├── environment.yml
├── requirements.txt
├── .gitignore
│
├── models/
│   ├── green_roof_rf_v1.0.0.joblib
│   └── model_metadata.json
│
├── notebooks/
│   └── green_roof_rf_workflow.ipynb
│
├── examples/
│   └── example_input.csv
│
└── data/
    └── README.md
```

## Installation

Miniforge / Conda is recommended because the project uses geospatial Python libraries.

```bash
git clone https://github.com/lukmanspace/green-roof-detection-bw.git
cd green-roof-detection-bw

conda env create -f environment.yml
conda activate geo
```

Alternatively:

```bash
pip install -r requirements.txt
```

For Windows geospatial environments, Conda/Miniforge is generally the safer option.

## Using the publication notebook

Open:

```text
notebooks/green_roof_rf_workflow.ipynb
```

The notebook demonstrates:

1. training-data loading and quality filtering
2. final feature definition
3. preprocessing
4. Random Forest construction
5. Leave-One-City-Out validation
6. repeated stratified validation
7. validation/test threshold selection
8. final model training
9. model export
10. model reload and inference

The training data are not included. See [`data/README.md`](data/README.md) for the expected schema.

## Using the pretrained model

```python
import joblib
import pandas as pd

model = joblib.load("models/green_roof_rf_v1.0.0.joblib")

X = pd.read_csv("examples/example_input.csv")

probability = model.predict_proba(X)[:, 1]

result = X.copy()
result["green_roof_probability"] = probability

print(result[["green_roof_probability"]])
```

The model expects the same 14 columns listed under **Final feature set**.

> `joblib` uses pickle-based serialization. Only load model files from sources you trust.

## Output interpretation

The model predicts a continuous:

```text
P(green roof)
```

for each roof plane.

The original thesis investigated several ways to transform these probabilities into inventory products, including:

- a validation-selected best-F1 threshold
- fixed high-confidence thresholds such as `p >= 0.85` and `p >= 0.90`
- top-percentage candidate selections per city

These thresholds represent different precision/completeness trade-offs and should not be interpreted as universal probability cut-offs for all applications.

## Data limitations

The model should be interpreted in the context of its source data.

PlanetScope monthly basemaps have a spatial resolution of approximately **4.77 m**. Small, narrow, or geometrically unusual roof planes may therefore contain too little reliable spectral information for classification.

The final analytical domain retains roof planes for which both winter and summer zonal statistics were successfully produced using the conservative extraction methods used in the thesis.

The labelled dataset also emphasizes relatively clear examples of vegetated and non-vegetated roofs. Borderline or ambiguous roofs are consequently less represented.

## Reproducibility

The publication notebook uses project-relative paths and does not depend on the original local thesis directory structure.

To reproduce model training, provide a compatible prepared training dataset at:

```text
data/training_roofs.parquet
```

and run:

```text
notebooks/green_roof_rf_workflow.ipynb
```

The exported model will be written to:

```text
models/green_roof_rf_v1.0.0.joblib
```

## Citation

If you use this repository in academic work, please cite the associated master's thesis:

```text
Hakim, L. (2026).
Detecting Green Roofs in Baden-Württemberg by Integrating LoD2 CityGML
and PlanetScope Imagery in a Supervised Machine Learning Framework.
Master's Thesis, Hochschule für Technik Stuttgart.
```

## License

Code licensing is defined in the repository `LICENSE` file.

Third-party datasets and imagery retain their original licenses and are **not** redistributed by this repository.

## Author

**Lukman Hakim**  
M.Sc. Photogrammetry and Geoinformatics  
Hochschule für Technik Stuttgart

GitHub: `https://github.com/lukmanspace`
