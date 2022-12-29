import pandas as pd
from .slack import connect_slack


def reverse_list(numbers: list[int]) -> list[int]:
    return list(reversed(numbers))


def process_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df.columns = df.columns.str.lower()

    df["person_id"] = pd.to_numeric(df.person_id, errors="coerce")
    df = df.dropna(subset=["person_id"])
    df["person_id"] = df.person_id.astype(int)

    df["date"] = pd.to_datetime(df.date)
    df["avg"] = df.groupby("person_id")["value"].transform("mean")

    return df


def send_slack_message(env: str) -> None:
    if env == "prod":
        slack = connect_slack()
        slack.send_message()
