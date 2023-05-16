import requests
from io import BytesIO
import pandas as pd
import calendar
import datetime
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from flask import send_file


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
  cek = ['Jan','Jan*' ,'Q1','Q1*']
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

def corelation(data1,data2,data_type=12,year_from=2010,year_to=2023):
  base = 2010
  f = (year_from-base)*12
  t = f+data_type+(year_to-year_from)*data_type

  y = data1[f:t]
  x = data2 [f:t]

  # Create and fit the linear regression model
  model = LinearRegression()
  model.fit(x.reshape(-1, 1), y)

  # Get the slope and intercept of the regression line
  slope = model.coef_[0]
  intercept = model.intercept_

  # Make predictions
  x_new = np.array([6, 7, 8])  # New data points
  y_pred = model.predict(x_new.reshape(-1, 1))

  # Visualize the regression line and predictions
  plt.scatter(x, y, label='Data')
  plt.plot(x, model.predict(x.reshape(-1, 1)), color='red', label='Regression Line')
  plt.xlabel('X')
  plt.ylabel('Y')
  plt.legend()

  # Save the plot to a BytesIO object
  image_stream = BytesIO()
  plt.savefig(image_stream, format='png')
  image_stream.seek(0)


  return{
     
     'slope':slope,
     'intercept':intercept,
     'image': send_file(image_stream, mimetype='image/png')
  }
