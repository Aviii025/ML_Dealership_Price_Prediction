"""Train the car and two-wheeler price models and save them to ``models/``.

Usage:  python -m training.train
"""

from __future__ import annotations

import json
import pickle
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd
import sklearn
from sklearn.compose import ColumnTransformer, TransformedTargetRegressor
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from src import features
from src.valuation import rule_based_value
from training.datasets import DATA_REFERENCE_YEAR, load_cars, load_two_wheelers

MODELS_DIR = Path(__file__).resolve().parent.parent / "models"
SEED = 42


def build_pipeline(categorical: list[str], numeric: list[str]) -> TransformedTargetRegressor:
    """One-hot encode categoricals, gradient-boost on log(price)."""
    pre = ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="infrequent_if_exist", min_frequency=3, sparse_output=False),
         categorical),
        ("num", "passthrough", numeric),
    ])
    model = HistGradientBoostingRegressor(
        learning_rate=0.06, max_iter=600, max_leaf_nodes=31, min_samples_leaf=10,
        l2_regularization=1.0, random_state=SEED,
    )
    return TransformedTargetRegressor(
        regressor=Pipeline([("pre", pre), ("model", model)]), func=np.log1p, inverse_func=np.expm1,
    )


def metrics(y_true, y_pred) -> dict:
    ape = np.abs(y_pred - y_true) / y_true
    return {
        "mae": round(float(mean_absolute_error(y_true, y_pred))),
        "median_ape_pct": round(float(np.median(ape) * 100), 1),
        "r2": round(float(r2_score(y_true, y_pred)), 3),
    }


def rule_based_baseline(vehicle_type_of_row, rows: pd.DataFrame) -> np.ndarray:
    """Market value from the existing rule-based estimator (needs original price)."""
    preds = []
    for _, r in rows.iterrows():
        details = {**r.to_dict(), "condition": "Good", "insurance": "Third Party"}
        # Ages in the data are relative to 2020, so shift the year to today's equivalent.
        details["year"] = int(r["year"]) + (date.today().year - DATA_REFERENCE_YEAR)
        preds.append(rule_based_value(vehicle_type_of_row(r), details).market_value)
    return np.array(preds)


def train(name: str, records: pd.DataFrame, make_features, categorical, numeric, baseline=None) -> dict:
    X = make_features(records, DATA_REFERENCE_YEAR)
    y = records["price"].to_numpy(dtype=float)
    idx_train, idx_test = train_test_split(np.arange(len(X)), test_size=0.2, random_state=SEED)

    pipe = build_pipeline(categorical, numeric).fit(X.iloc[idx_train], y[idx_train])
    report = {"rows": len(X), "test_rows": len(idx_test),
              "ml_test": metrics(y[idx_test], pipe.predict(X.iloc[idx_test]))}

    if baseline is not None:
        test = records.iloc[idx_test]
        has_price = test["original_price"].notna().to_numpy()
        sub = test[has_price]
        report["comparison_rows_with_original_price"] = int(has_price.sum())
        report["ml_test_same_rows"] = metrics(sub["price"].to_numpy(float),
                                              pipe.predict(X.iloc[idx_test[has_price]]))
        report["rule_based_same_rows"] = metrics(sub["price"].to_numpy(float), baseline(sub))

    # Refit on all rows for the shipped model.
    final = build_pipeline(categorical, numeric).fit(X, y)
    bundle = {
        "pipeline": final,
        "feature_set": name,
        "supported_fuels": sorted(records["fuel_type"].unique()) if "fuel_type" in records else ["Petrol"],
        "trained_on": date.today().isoformat(),
        "data_reference_year": DATA_REFERENCE_YEAR,
        "sklearn_version": sklearn.__version__,
        "metrics": report,
    }
    MODELS_DIR.mkdir(exist_ok=True)
    with (MODELS_DIR / f"{name}_model.pkl").open("wb") as fh:
        pickle.dump(bundle, fh)
    return report


def main() -> None:
    report = {
        "car": train("car", load_cars(), features.car_features,
                     features.CAR_CATEGORICAL, features.CAR_NUMERIC),
        "two_wheeler": train("two_wheeler", load_two_wheelers(), features.two_wheeler_features,
                             features.TWO_WHEELER_CATEGORICAL, features.TWO_WHEELER_NUMERIC,
                             baseline=lambda rows: rule_based_baseline(lambda r: r["segment"], rows)),
    }
    report["sklearn_version"] = sklearn.__version__
    (MODELS_DIR / "metrics.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
