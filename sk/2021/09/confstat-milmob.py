import numpy.linalg as lin, numpy as np
from collections import defaultdict
from scipy import sin, cos, tan, arctan, arctan2, arccos, pi
import pandas as pd, datetime, numpy as np
from zipfile import ZipFile
from io import BytesIO
import urllib.request as urllib2, mygeo, sys
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request, folium, re, requests

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

headers = { 'User-Agent': 'UCWEB/2.0 (compatible; Googlebot/2.1; +google.com/bot.html)'}

def tag_visible(element):
    if element.parent.name in ['option','style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)

countries = pd.read_csv('countries.csv')
countries['latlon'] = countries.apply(lambda x: list(x[['latitude','longitude']]),axis=1)
countries['name2'] = countries.apply(lambda x: x['name'].replace(' ','').lower(),axis=1)
cdict = countries.set_index('name2')['latlon'].to_dict()

rlist = []
for x in list(countries['name']):
    a = x.lower()
    b = a.replace(' ','')
    if a == b: continue
    rlist.append([a,b])
    
now = datetime.datetime.now()
#now = datetime.datetime(2021,11,1)
dfs = []

clat,clon=33.01136975577918, 40.98527636859822

m = folium.Map(location=[clat, clon], zoom_start=3, tiles="Stamen Terrain")

for i in range(7):
    d = now - datetime.timedelta(days=i+1)
    sd = "%d%02d%02d" % (d.year, d.month, d.day)
    print (sd)
    url = base_conflict_url + "/%s.export.CSV.zip" % sd
    r = urllib2.urlopen(url).read()
    file = ZipFile(BytesIO(r))
    csv = file.open("%s.export.CSV" % sd)
    df = pd.read_csv(csv,sep='\t',header=None)    
    urls = df[57]        
    df2 = df[range(len(conf_cols))]
    df2 = pd.concat((df2,urls),axis=1)    
    df2.columns = conf_cols + ['url']
    df3 = df2[(df2.EventCode==154)]
    df3 = df3.reset_index()
    df3.drop_duplicates('url',inplace=True)
    dft = df3[['EventCode','Actor1Geo_Lat','Actor1Geo_Long','url']].copy()
    dfs.append(dft)

df4 = pd.concat(dfs,axis=0)

for index, row in df4.iterrows():
    rowurl = row['url']
    if 'troop' not in rowurl: continue
    print (rowurl)
    try:
        resp = requests.get(rowurl, headers=headers, timeout=4)
        s = text_from_html(resp.text)
        s = s[:2000]
        tokens = re.split("\s|(?<!\d)[,.](?!\d)",s)
        s = s.lower()
        for (a,b) in rlist:
            s = s.replace(a,b)        

        for urlt in re.split("[/-]",rowurl): tokens.append(urlt)

        tokens2 = [t.lower() for t in tokens]
        
        c_in_tokens = defaultdict(int)
        for t in tokens2: c_in_tokens[t] += 1

        res = {}
        for t in c_in_tokens: 
            if t in cdict: res[t] = c_in_tokens[t]

        total = []
        lat,lon=None,None
        if len(res)>0:
            for c in res:
                lat,lon = cdict[c]
                newcoord = mygeo.latlon2vec(lat,lon)
                total.append(list(newcoord * res[c]))

            total = np.array(total)
            ma = np.mean(total,axis=0)
            ma = ma / lin.norm(ma)
            lat,lon = mygeo.vec2latlon(ma)
        else:
            if str(row['Actor1Geo_Lat'])=='nan': continue
            lat,lon = row['Actor1Geo_Lat'], row['Actor1Geo_Long']
        print (lat,lon)
        folium.Marker(
            [lat,lon], popup="<a href='%s' target='_blank' rel='noopener noreferrer'>Link</a>" % (row['url'])
        ).add_to(m)
    except:
        print (sys.exc_info()[0])
        continue

    
m.save('conflict-milmob.html')

