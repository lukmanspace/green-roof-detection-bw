# Data

The raw and intermediate datasets used in the master's thesis are **not distributed with this repository** because of file size and/or licensing constraints.

## Expected training file

The publication notebook expects:

```text
data/training_roofs.parquet
```

The file may be a regular Parquet or GeoParquet dataset. Geometry is not used directly by the Random Forest model.

## Required columns

### Target and grouping

| Column | Description |
|---|---|
| `label` | Binary target: `0` = non-vegetated, `1` = vegetated |
| `city` | City used as the grouping variable for LOCO evaluation |
| `method_winter` | Winter zonal-statistics extraction method |
| `method_summer` | Summer zonal-statistics extraction method |

The publication workflow retains records where:

```python
method_winter in {1, 2}
method_summer in {1, 2}
```

### Final model features

| Feature | Type | Description |
|---|---|---|
| `slope_deg` | numeric | Roof-plane slope in degrees |
| `area_m2` | numeric | 3D roof-plane surface area |
| `height_m` | numeric | Roof height proxy relative to building ground |
| `height_relief_m` | numeric | Internal vertical relief of roof plane |
| `G_avg_Winter` | numeric | Mean winter Green-band value |
| `B_avg_Winter` | numeric | Mean winter Blue-band value |
| `NDVI_avg_Winter` | numeric | Mean winter NDVI |
| `NDVI_std_Winter` | numeric | Winter NDVI standard deviation |
| `G_avg_Summer` | numeric | Mean summer Green-band value |
| `B_avg_Summer` | numeric | Mean summer Blue-band value |
| `NDVI_avg_Summer` | numeric | Mean summer NDVI |
| `NDVI_std_Summer` | numeric | Summer NDVI standard deviation |
| `roofType` | categorical | LoD2 roof-type code |
| `function` | categorical | Building-function code |

## Original research data sources

The thesis workflow used:

- LoD2 CityGML building data from LGL Baden-Württemberg
- PlanetScope monthly basemap imagery
- BKG administrative boundaries
- Google and Bing imagery as visual references during manual labelling

These data are not redistributed here.

Users who wish to reproduce the full preprocessing workflow must obtain the original datasets from their respective providers and comply with their licensing conditions.

## Coordinate reference system

The original geospatial workflow used:

```text
EPSG:25832 — ETRS89 / UTM zone 32N
```

## Training sample

After quality filtering, the thesis training dataset contained:

```text
18,216 roof planes
15,263 non-vegetated
 2,953 vegetated
```

across Stuttgart, Karlsruhe, Freiburg im Breisgau, and Tübingen.
