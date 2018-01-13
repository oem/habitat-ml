import pandas as pd
import numpy as np
import datetime
import pytz

UTC = pytz.UTC
CET_CEST = pytz.timezone('Europe/Prague')
RUSH_HOURS_MORNING_WORKINGDAY = [8,9]
RUSH_HOURS_EVENING_WORKINGDAY = [18,19]
NIGHT_START = 22
NIGHT_END = 1
NIGHT_END_FR_SA = 5

# raw = add_date_features(raw)
def add_date_features(raw):
  
  df = pd.DataFrame()
  date_column=raw.dt_time
  # convert date_column to the local datetime
  df['date']=pd.DatetimeIndex(date_column).tz_localize(UTC).tz_convert(CET_CEST)
  
  # compute weekday
  df['weekday'] = df.date.dt.dayofweek
  print(datetime.datetime.now(),'feature weekday created')
  
  # compute day of year
  df['dayofyear'] = df.date.dt.dayofyear
  print(datetime.datetime.now(),'feature dayofyear created')
  
  df['dayofyear_sin'] = np.sin(df.dayofyear / 366.0 * 2 * np.pi)
  df['dayofyear_cos'] = np.cos(df.dayofyear / 366.0 * 2 * np.pi)
  
  # index days chronologically from the earliest day (=1)
  min_date = df.date.min()
  df['dayfromstart'] = (df.date - min_date).astype('timedelta64[D]')
  print(datetime.datetime.now(),'feature dayfromstart created')
  
  df['hour'] = df.date.dt.hour
  print(datetime.datetime.now(),'feature hour created')
  
  # turn time into seconds from midnight (UTC)
  df['seconds_from_midnight'] = df.date.dt.hour * 3600 + df.date.dt.minute * 60 + df.date.dt.second
  print(datetime.datetime.now(),'feature seconds_from_midnight created')
  
  #df['time_sin'] = df.seconds_from_midnight.apply(lambda x: np.sin(x / 86400.0))
  #df['time_cos'] = df.seconds_from_midnight.apply(lambda x: np.cos(x / 86400.0))
  df['time_sin'] = np.sin(df.seconds_from_midnight / 86400.0 * 2 * np.pi)
  df['time_cos'] = np.cos(df.seconds_from_midnight / 86400.0 * 2 * np.pi)
  print(datetime.datetime.now(),'features time_sin and time_cos created')
  
  df['seconds_from_midnight_monday_01'] = df.seconds_from_midnight / 7.0 / 86400.0 + df.weekday/7.0
  print(datetime.datetime.now(),'feature seconds_from_midnight_monday_01 created')
  
  df['seconds_from_midnight_monday_sin'] = np.sin(df.seconds_from_midnight_monday_01 * 2 * np.pi)
  df['seconds_from_midnight_monday_cos'] = np.cos(df.seconds_from_midnight_monday_01 * 2 * np.pi)
  print(datetime.datetime.now(),'features seconds_from_midnight_monday_sin and seconds_from_midnight_monday_cos created')
  
  df['rush_hour_morning_workingday'] = (df.date.dt.weekday < 5) & (df.date.dt.hour.isin(RUSH_HOURS_MORNING_WORKINGDAY))
  print(datetime.datetime.now(),'feature rush_hour_morning_workingday created')
  
  df['rush_hour_evening_workingday'] = (df.date.dt.weekday < 5) & (df.date.dt.hour.isin(RUSH_HOURS_EVENING_WORKINGDAY))
  print(datetime.datetime.now(),'feature rush_hour_evening_workingday created')
  
  df['night'] = (df.hour <= NIGHT_END) | (df.hour >= NIGHT_START)
  print(datetime.datetime.now(),'feature night created')
  
  df['workingday'] = df.weekday < 5
  print(datetime.datetime.now(),'feature workingday created')
  
  df['friday_night'] = ((df.hour >= NIGHT_START) & (df.weekday == 4)) | ((df.hour < NIGHT_END_FR_SA) & (df.weekday == 5))
  print(datetime.datetime.now(),'feature friday_night created')
  
  df['saturday_night'] = ((df.hour >= NIGHT_START) & (df.weekday == 5)) | ((df.hour < NIGHT_END_FR_SA) & (df.weekday == 6))
  print(datetime.datetime.now(),'feature saturday_night created')
  
  df['silvester'] = (df.date.dt.month == 12 ) & (df.date.dt.day == 31 )
  df['new_year'] = df.dayofyear == 1

  raw =  pd.concat([raw,df],axis=1)
  return raw

# raw = add_date_features(raw)
def add_weather_features(raw):
  # TODO: scale more weather features?
  
  df_result = pd.DataFrame()
  
  df_result['relative_humidity'] = raw.humidity / 100.0
  print(datetime.datetime.now(),'feature humidity transformed')
  
  df_result['wind_deg_sin'] = np.sin(raw.wind_deg / 180.0 * np.pi)
  df_result['wind_deg_cos'] = np.cos(raw.wind_deg / 180.0 * np.pi)
  print(datetime.datetime.now(),'features wind_deg_sin and wind_deg_cos created')
  
  df_result['relative_clouds'] =raw.clouds_all / 100.0
  print(datetime.datetime.now(),'feature clouds_all transformed')
  
  return pd.concat([raw,df_result],axis=1)