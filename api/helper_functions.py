import requests
from io import BytesIO
import pandas as pd
import calendar
import datetime
import xlrd

pd.set_option("future.no_silent_downcasting", True)


def get_data(tabel):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "*/*",
    }
    urls = [
        f"https://cors-proxy.sofyanhidayat48.workers.dev/?https://www.bi.go.id/SEKI/tabel/{tabel}.xls",
        f"https://www.bi.go.id/SEKI/tabel/{tabel}.xls",
    ]
    for url in urls:
        try:
            response = requests.get(url, headers=headers, timeout=20)
            if response.status_code == 200 and len(response.content) > 1000:
                if b"<html" not in response.content[:100].lower():
                    return pd.ExcelFile(BytesIO(response.content), engine="xlrd")
        except Exception:
            continue

    raise ValueError(
        f"Table '{tabel}' could not be retrieved from Bank Indonesia. Please check if the table ID is valid."
    )


def date(x):
    if isinstance(x, (datetime.datetime, datetime.date, pd.Timestamp)):
        return calendar.month_abbr[x.month]
    return x


def clean_data(df):
    df1 = df.copy()
    df1.dropna(axis=0, thresh=9, inplace=True)
    df1 = df1.reset_index(drop=True)
    df1 = df1.astype(object)

    if "Unnamed: 1" in df1.columns and "Unnamed: 2" in df1.columns:
        df2 = df1[["Unnamed: 1", "Unnamed: 2"]].copy()
        df1[["Unnamed: 1", "Unnamed: 2"]] = df2.ffill(axis=1)

    year = 0
    cek = ["Jan", "Jan*", "Jan**", "Q1", "Q1*", "Q1**"]
    for column in df1.columns:
        val0 = df1[column][0]
        if year == 0 and isinstance(val0, (int, float)) and not pd.isna(val0):
            try:
                year = int(val0)
            except (ValueError, TypeError):
                pass
        elif str(df1[column][1]).strip() in cek:
            year += 1
        df1.loc[0, column] = str(year)

    df1.loc[1] = df1.loc[1].apply(date)

    keterangan = df1.loc[0, df1.columns[2]]
    col_range = df1.columns[1:]
    combined = df1.loc[[0, 1], col_range].astype(str).apply("-".join)
    for col in col_range:
        df1.loc[0, col] = combined[col]
    df1.loc[0, df1.columns[2]] = keterangan

    d = df1.isna().any()
    cols_to_ignore = [df1.columns[2]]
    d[cols_to_ignore] = False
    df1 = df1.loc[:, ~d]

    df1.dropna(inplace=True)

    df1.columns = df1.loc[0]
    df1.set_index(df1.columns[0], inplace=True)

    df1.drop(df1.index[0], inplace=True)
    df1.columns = df1.columns.str.replace("*", "", regex=False)

    return df1
