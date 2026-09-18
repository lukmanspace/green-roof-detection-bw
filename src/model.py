from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier


FEATURES = [
    "slope_deg",
    "area_m2",
    "height_m",
    "height_relief_m",
    "G_avg_Winter",
    "B_avg_Winter",
    "NDVI_avg_Winter",
    "NDVI_std_Winter",
    "G_avg_Summer",
    "B_avg_Summer",
    "NDVI_avg_Summer",
    "NDVI_std_Summer",
    "roofType",
    "function",
]

CATEGORICAL_FEATURES = [
    "roofType",
    "function",
]

NUMERIC_FEATURES = [
    feature
    for feature in FEATURES
    if feature not in CATEGORICAL_FEATURES
]


def create_model(random_state=42):

    numeric_pipeline = SimpleImputer(
        strategy="median",
        add_indicator=True
    )

    categorical_pipeline = Pipeline([
        (
            "imputer",
            SimpleImputer(strategy="most_frequent")
        ),
        (
            "encoder",
            OneHotEncoder(
                handle_unknown="ignore",
                sparse_output=True
            )
        ),
    ])

    preprocessing = ColumnTransformer(
        [
            (
                "numeric",
                numeric_pipeline,
                NUMERIC_FEATURES
            ),
            (
                "categorical",
                categorical_pipeline,
                CATEGORICAL_FEATURES
            ),
        ],
        remainder="drop",
        sparse_threshold=0.3,
    )

    classifier = RandomForestClassifier(
        n_estimators=600,
        min_samples_leaf=2,
        n_jobs=-1,
        random_state=random_state,
        class_weight="balanced_subsample",
    )

    return Pipeline([
        ("preprocessing", preprocessing),
        ("classifier", classifier),
    ])