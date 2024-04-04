import requests
import pandas as pd


response = requests.get("https://api.ofx.com/PublicSite.ApiService/SpotRateHistory/5year/USD/EUR?DecimalPlaces=6&ReportingInterval=daily&format=json")
df_e = pd.DataFrame(response.json()["HistoricalPoints"])
df_e["date"] = pd.to_datetime(df_e["PointInTime"].astype(str).str[:-3].astype(int), unit="s")
df_e.set_index("date", inplace=True)
df_e.rename(columns={"InterbankRate": "EUR"}, inplace=True)
df_e.drop(["PointInTime", "InverseInterbankRate"], axis=1, inplace=True)

response = requests.get("https://api.ofx.com/PublicSite.ApiService/SpotRateHistory/5year/USD/GBP?DecimalPlaces=6&ReportingInterval=daily&format=json")
df_p = pd.DataFrame(response.json()["HistoricalPoints"])
df_p["date"] = pd.to_datetime(df_p["PointInTime"].astype(str).str[:-3].astype(int), unit="s")
df_p.set_index("date", inplace=True)
df_p.rename(columns={"InterbankRate": "GBP"}, inplace=True)
df_p.drop(["PointInTime", "InverseInterbankRate"], axis=1, inplace=True)

df_g = pd.read_excel("lecture_03/data/exratesyearsgeo.xlsx", sheet_name="2001-2023", header=3, usecols=["Unnamed: 0", "აშშ დოლარი"])
df_g.drop([0, 1], inplace=True)
df_g["GEL"] = df_g["აშშ დოლარი"].astype(float)
df_g.rename(columns={"Unnamed: 0": "date"}, inplace=True) 
df_g.drop(["აშშ დოლარი"], inplace=True, axis=1)
df_g.set_index("date", inplace=True)

pd.concat([df_e, df_p, df_g], join="inner", axis=1).to_csv("lecture_03/data/usd_exchange_rate_history.csv")
