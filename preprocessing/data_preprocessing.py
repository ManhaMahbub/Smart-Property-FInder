import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer


def load_and_preprocess(file_path):
    """Load dataset and preprocess it."""
    df = pd.read_excel(file_path)

    # BUG FIX: df.fillna(method='ffill') is deprecated since pandas 2.x
    # Use df.ffill() instead
    df.ffill(inplace=True)

    X = df.drop("price", axis=1)
    y = df["price"]

    categorical_cols = ["property_type", "suburb"]

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols)
        ],
        remainder="passthrough"
    )

    X_processed = preprocessor.fit_transform(X)

    return df, X_processed, y, preprocessor
