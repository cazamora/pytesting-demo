import hypothesis as hy
import numpy as np
import pandas as pd
import pytest
import pandera as pa
from pandera.typing import Series

from pytesting import app

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
