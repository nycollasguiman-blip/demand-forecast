import pandas as pd

RAW = "data/raw"
KEYS = ["store_nbr", "family"]

def load_train():
    df = pd.read_csv(f"{RAW}/train.csv", parse_dates=["date"])
    
    return df.drop(columns=["id"])
    
def complete_dates(df):
    """
    Guarantees one line per each possible combination of date, store and family. Missing dates (e.g., 12/25) result in 0 sales.
    """
    dates = pd.date_range(df["date"].min(), df["date"].max(), freq="D")
    idx = pd.MultiIndex.from_product(
    [dates, df["store_nbr"].unique(), df["family"].unique()],
    names=["date", "store_nbr", "family"],
    )
    df = df.set_index(["date"] + KEYS).reindex(idx).reset_index()
    df[["sales", "onpromotion"]] = df[["sales", "onpromotion"]].fillna(0)
    
    return df
    
def load_oil(dates):
    """
    Oil price, with days lacking a quote filled in using the most recent value.
    """
    oil = pd.read_csv(f"{RAW}/oil.csv", parse_dates=["date"]).set_index("date")
    oil = oil.reindex(dates).ffill().bfill() # Its danger use bfill in temporal series
    
    return oil.rename(columns={"dcoilwtico": "oil"}).rename_axis("date").reset_index()
    
def load_national_holidays():
    h = pd.read_csv(f"{RAW}/holidays_events.csv", parse_dates=["date"])
    h = h[(h["locale"] == "National") & (~h["transferred"]) & (h["type"] != "Work Day")] # Not transferred, possible improvement
    
    return pd.DataFrame({"date": h["date"].unique(), "is_holiday": 1})
    
def build_dataset():
    df = complete_dates(load_train())
    dates = pd.date_range(df["date"].min(), df["date"].max(), freq="D")
    df = df.merge(load_oil(dates), on="date", how="left")
    df = df.merge(load_national_holidays(), on="date", how="left")
    df["is_holiday"] = df["is_holiday"].fillna(0).astype(int)
    
    return df.sort_values(KEYS + ["date"]).reset_index(drop=True)