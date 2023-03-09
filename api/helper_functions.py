import requests
from io import BytesIO
import pandas as pd
import calendar
import datetime
import xlrd

def get_data(tabel):
  url = "https://cors-proxy.sofyanhidayat48.workers.dev/?https://www.bi.go.id/SEKI/tabel/"+tabel+".xls"
  response = requests.get(url).content
  f = pd.ExcelFile(BytesIO(response))
  return f

def date(x):
  if type(x) == datetime.datetime:
    x = calendar.month_abbr[x.month]
  return x

def clean_data(df):
  df1 = df
  df1.dropna(axis=0,thresh=9,inplace=True)
  df1 = df1.reset_index(drop=True)

  if 'Unnamed: 1' in df1.columns:
    df2 = df1[['Unnamed: 1','Unnamed: 2']] 
    df1[['Unnamed: 1','Unnamed: 2']] = df2.fillna(axis=1,method='ffill')
  
  year = 0
  cek = ['Jan', 'Q1']
  for column in df1.columns:
      if year == 0 and isinstance(df1[column][0], int):
          year = df1[column][0]
      elif df1[column][1] in cek:
          year += 1
      df1.loc[0, column] = year

  df1.loc[1] = df1.loc[1].apply(date)

  keterangan = df1.loc[0,df1.columns[2]]
  df1.loc[0]= df1.loc[[0,1],df1.columns[1]:df1.columns[len(df1.columns)-1]].astype(str).apply('-'.join)
  df1.loc[0,df1.columns[2]] = keterangan

  d= df1.isna().any()
  cols_to_ignore = [df1.columns[2]]
  d[cols_to_ignore] = False
  df1 = df1.loc[:,~d]

  df1.dropna(inplace=True)

  df1.columns = df1.loc[0]
  df1.set_index(df1.columns[0],inplace=True)

  df1.drop(df1.index[0],inplace=True)
  df1.columns = df1.columns.str.replace('*','')

  return df1
