import pandas as pd, datetime, numpy as np
from zipfile import ZipFile
from io import BytesIO
from pygeodesy.sphericalNvector import LatLon
import urllib.request as urllib2
import folium

base_conflict_url = "http://data.gdeltproject.org/events"

conf_cols = ['GlobalEventID', 'Day', 'MonthYear', 'Year', 'FractionDate',\
       'Actor1Code', 'Actor1Name', 'Actor1CountryCode', 'Actor1KnownGroupCode',\
       'Actor1EthnicCode', 'Actor1Religion1Code', 'Actor1Religion2Code',\
       'Actor1Type1Code', 'Actor1Type2Code', 'Actor1Type3Code', \
       'Actor2Code', 'Actor2Name', 'Actor2CountryCode', 'Actor2KnownGroupCode',
       'Actor2EthnicCode', 'Actor2Religion1Code', 'Actor2Religion2Code',
       'Actor2Type1Code', 'Actor2Type2Code', 'Actor2Type3Code', \
       'IsRootEvent','EventCode', 'EventBaseCode','EventRootCode',\
       'QuadClass', 'GoldsteinScale','NumMentions','NumSources', \
       'NumArticles', 'AvgTone','Actor1Geo_Type', 'Actor1Geo_FullName',\
       'Actor1Geo_CountryCode', 'Actor1Geo_ADM1Code','Actor1Geo_Lat', \
       'Actor1Geo_Long', 'Actor1Geo_FeatureID','Actor2Geo_Type', \
       'Actor2Geo_FullName','Actor2Geo_CountryCode', 'Actor2Geo_ADM1Code',\
       'Actor2Geo_Lat', 'Actor2Geo_Long']

#now = datetime.datetime.now()
now = datetime.datetime(2021,11,1)
dfs = []

clat,clon=33, 40

# North
poly1 = LatLon(36.230, 33.169),\
        LatLon(39.501, 37.768),\
        LatLon(38.565, 47.546),\
        LatLon(32.053, 48.609),\
        LatLon(28.332, 35.013),\
        LatLon(31.730, 32.023)

# Southern area around Yemen
poly2 = LatLon(18.328, 41.652),\
        LatLon(21.671, 54.553),\
        LatLon(15.145, 55.677),\
        LatLon(10.439, 42.370)


m = folium.Map(location=[clat, clon], zoom_start=4, tiles="Stamen Terrain")

def dist(x):
    if 'nan' in str(x['Actor2Geo_Lat']): return False
    elif 'nan' in str(x['Actor2Geo_Long']): return False
    p = LatLon(x['Actor2Geo_Lat'],x['Actor2Geo_Long'])
    return p.isenclosedBy(poly1) | p.isenclosedBy(poly2)

for i in range(5):
    d = now - datetime.timedelta(days=i+1)
    print (d)
    sd = "%d%02d%02d" % (d.year, d.month, d.day)
    url = base_conflict_url + "/%s.export.CSV.zip" % sd
    r = urllib2.urlopen(url).read()
    file = ZipFile(BytesIO(r))
    csv = file.open("%s.export.CSV" % sd)
    df = pd.read_csv(csv,sep='\t',header=None)    
    urls = df[57]        
    df2 = df[range(len(conf_cols))]
    df2 = pd.concat((df2,urls),axis=1)    
    df2.columns = conf_cols + ['url']
    df3 = df2[(df2.EventCode==190)|(df2.EventCode==195)|(df2.EventCode==194)]
    df3 = df3.reset_index()
    df3.loc[:,'dist'] = df3.apply(dist, axis=1)
    df3 = df3[df3.dist == True]
    dft = df3[['EventCode','Actor1CountryCode','Actor1Name','Actor2Name','Actor2Geo_Lat','Actor2Geo_Long','url']].copy()
    dfs.append(dft)

df4 = pd.concat(dfs,axis=0)

for index, row in df4.iterrows():
    if str(row['Actor2Geo_Lat'])=='nan': continue
    if str(row['Actor1CountryCode'])=='nan': continue
    folium.Marker(
        [row['Actor2Geo_Lat'], row['Actor2Geo_Long']], popup="<a href='%s' target='_blank' rel='noopener noreferrer'>Link</a>" % (row['url']), tooltip=row['Actor1CountryCode']
    ).add_to(m)

# add US bases
df = pd.read_csv('usbases.csv')
for index, row in df.iterrows():
    folium.CircleMarker(location=[row['lat'], row['lon']],
                        radius=6,
			color='red',
                        weight=1).add_to(m)

stitle = "<h3> Attacks in the ME <br/></h3> <h5>US Bases in <font color='red'>Red</font></h5>"
m.get_root().html.add_child(folium.Element(stitle))

m.save('conflict-out.html')

