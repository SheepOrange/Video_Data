import pandas as pd
import datetime

! ls

# import the raw data

df_raw_data = pd.read_csv("video_data.csv", quotechar='"', error_bad_lines = False)

df_raw_data.head()
df_raw_data.info()

def platform_name (name):
    if 'IPHONE' in name.upper():
        return 'iPhone'
    elif 'ANDROID' in name.upper():
        return 'Android Phone'
    elif 'IPAD' in name.upper():
        return 'iPad'
    elif 'WEB' in name.upper():
        return 'Web'
    elif 'NEW' in name.upper():
        return 'Desktop'
    else: return 'Unknown'

platform_name('App Web')
# clean the data

# remove the rows in events which don't have 206
df_raw_data = df_raw_data.loc[lambda df: df.events.apply(lambda l: '206' in l)]
df_raw_data['DateTime'] = df_raw_data['DateTime'].apply(lambda t: datetime.datetime.strptime(t[:-5], '%Y-%m-%dT%H:%M:%S'))
df_raw_data['DateTime'] = df_raw_data['DateTime'].apply(lambda dt: dt.strftime("%d/%m/%Y %H:%M"))
df_raw_data['events'] = df_raw_data['events'].str.split(",")
df_raw_data['Platform'] = df_raw_data['VideoTitle'].str.split("|").str[0].apply(lambda pn: platform_name(pn))
df_raw_data['Site'] = df_raw_data['VideoTitle'].str.split("|").str[0].apply(lambda si: 'News' if si.upper() == 'NEWS' else 'Unknown')
df_raw_data['Platform'].unique()
df_raw_data['Site'].unique()
df_raw_data['Video'] = df_raw_data['VideoTitle'].str.split("|").str[-1].str.upper()
df_raw_data.head()

df_raw_data.info()

dlt_DimDate = pd.DataFrame()
dlt_DimDate['DateTime'] = df_raw_data['DateTime']
dlt_DimDate.head()

df_DimDate = dlt_DimDate.drop_duplicates(['DateTime']).reset_index()
df_DimDate = df_DimDate.drop(columns='index')
df_DimDate['s_key'] = df_DimDate.index

df_DimDate.info()
df_DimDate.head()

df_DimPlatform = pd.DataFrame()
df_DimPlatform['Platform'] = df_raw_data['Platform'].unique()
df_DimPlatform['S_key'] = df_DimPlatform.index
df_DimPlatform

df_DimSite = pd.DataFrame()
df_DimSite['Site'] = df_raw_data['Site'].unique()
df_DimSite['S_key'] = df_DimSite.index
df_DimSite

df_DimVideo = pd.DataFrame()
df_DimVideo['Video'] = df_raw_data['Video'].unique()
df_DimVideo['S_key'] = df_DimVideo.index
df_DimVideo

df_fact_table = pd.DataFrame()

df_fact_table['DateTime_Skey'] = pd.merge(df_raw_data,df_DimDate, on = 'DateTime', how = 'left')['s_key']
df_fact_table['Platform_Skey'] = pd.merge(df_raw_data,df_DimPlatform, on = 'Platform', how = 'left')['S_key']
df_fact_table['Site_Skey'] = pd.merge(df_raw_data,df_DimSite, on = 'Site', how = 'left')['S_key']
df_fact_table['Video_Skey'] = pd.merge(df_raw_data,df_DimVideo, on = 'Video', how = 'left')['S_key']

df_fact_table

df_DimDate.to_csv("DimDate.csv", index=False)
df_DimPlatform.to_csv("DimPlatform.csv", index=False)
df_DimSite.to_csv("DimSite.csv", index=False)
df_DimVideo.to_csv("DimVideo.csv", index=False)
df_fact_table.to_csv("Fact_table.csv", index=False)
