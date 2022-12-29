import hypothesis as hy
import numpy as np
import pandas as pd
import pytest

from pytesting import app

# BASIC TESTING WITH EXAMPLES


def test_process_data():
    df = pd.DataFrame(
        [
            {"person_id": "1", "date": "2022-12-26", "value": 4},
            {"person_id": 1, "date": "2022-12-27", "value": 5},
        ]
    )
    result = app.process_data(df)
    assert result.person_id.dtype == int
    assert np.issubdtype(result.date.dtype, np.datetime64)
    assert len(result.avg.unique()) == 1
    assert result.avg[0] == 4.5


# VALIDATING SCHEMA WITH PANDERA

import pandera as pa
from pandera.typing import Series


class ResultSchema(pa.SchemaModel):
    person_id: Series[int] = pa.Field(gt=0)
    date: Series[pa.DateTime]
    value: Series[int]
    avg: Series[float]

    @pa.dataframe_check
    def not_empty(cls, df):
        return not df.empty


def test_process_pandera():
    df = pd.DataFrame(
        [
            {"person_id": "1", "date": "2022-12-26", "value": 4},
            {"person_id": 1, "date": "2022-12-27", "value": 5},
        ]
    )
    result = app.process_data(df)
    ResultSchema.validate(result, lazy=True)

    assert len(result.avg.unique()) == 1
    assert result.avg[0] == 4.5


def test_process_pandera_fails():
    df = pd.DataFrame(
        [
            {"person_id": "1", "date": "2022-12-26", "value": 4},
            {"person_id": 1, "date": "2022-12-27", "value": 5},
        ]
    )
    result = app.process_data(df)
    result["avg"] = float("nan")

    class FailSchema(ResultSchema):
        name: Series[str]

    #with pytest.raises(pa.errors.SchemaErrors):
    FailSchema.validate(result, lazy=True)

def test_process_pandera_empty():
    df = pd.DataFrame()

    ResultSchema.validate(df, lazy=True)


# PANDERA + HYPOTHESIS


class InputSchema(pa.SchemaModel):
    id: Series[int] = pa.Field(gt=0, lt=1e9, unique=True)
    person_id: Series[int] = pa.Field(gt=0, lt=1e9, nullable=True)
    name: Series[str] = pa.Field(isin=("Juanse", "Gabi"))
    date: Series[pa.DateTime]
    value: Series[int]

    class Config:
        unique = ["id", "date"]


@hy.given(InputSchema.strategy(size=10))
@hy.settings(max_examples=50)
def test_process_pandera_hypothesis(df):
    result = app.process_data(df)

    class ResultSchema(InputSchema):
        avg: Series[float]

    ResultSchema.validate(result, lazy=True)

    assert len(result[["avg", "person_id"]].drop_duplicates()) == len(
        df.person_id.dropna().unique()
    )
