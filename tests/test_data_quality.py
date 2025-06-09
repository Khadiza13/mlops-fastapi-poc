# tests/test_data_quality.py

import pandas as pd
import great_expectations as gx

def test_data_quality_on_train_csv():
    # Load your CSV file
    df = pd.read_csv("data/raw/train.csv")

    # Set up GX Data Context
    context = gx.get_context()

    # Register Pandas data source
    datasource = context.data_sources.add_pandas("pandas_source")
    asset = datasource.add_dataframe_asset("train_asset")
    batch_def = asset.add_batch_definition_whole_dataframe("default_batch")

    # Load batch
    batch = batch_def.get_batch({"dataframe": df})

    # Add expectations
    expectations = [
        gx.expectations.ExpectColumnToExist(column="Age"),
        gx.expectations.ExpectColumnValuesToBeBetween(column="Age", min_value=0, max_value=100),
        gx.expectations.ExpectColumnToExist(column="Sex"),
        gx.expectations.ExpectColumnValuesToNotBeNull(column="Sex"),
        gx.expectations.ExpectColumnToExist(column="Embarked"),
        gx.expectations.ExpectColumnValuesToBeInSet(column="Embarked", value_set=["S", "C", "Q"]),
        gx.expectations.ExpectColumnToExist(column="Survived"),
        gx.expectations.ExpectColumnValuesToBeInSet(column="Survived", value_set=[0, 1]),
    ]

    # Validate all expectations
    for expectation in expectations:
        result = batch.validate(expectation)
        assert result.success, f"Expectation failed: {expectation}"

