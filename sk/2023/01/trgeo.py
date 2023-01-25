import pandas as pd, folium, numpy as np, json

m = folium.Map(location=[40,33], tiles='Stamen Terrain', zoom_start=7)

def camp():
    df = pd.read_csv('kamp/kampyerleri.csv',sep=';')
    for index, row in df.iterrows():
        lat,lon = (float(x) for x in row['location'].split(","))
        folium.CircleMarker(location=[lon,lat],
                            tooltip=row['description'],
                            radius=6,
                            color='red',
                            weight=4).add_to(m)                
        
        
    df = pd.read_csv('kamp/trkamp.csv',sep=';')
    for index, row in df.iterrows():
        lat,lon = (float(x) for x in row['location'].split(","))
        folium.CircleMarker(location=[lat,lon],
                            tooltip=row['name'],
                            radius=6,
                            color='blue',
                            weight=4).add_to(m)                

def park():        
    files = ['millipark/milli_parklar.json',
             'millipark/tabiat_anitlari.json',
             'millipark/ozel_cevre_koruma_alanlari.json',
             'millipark/tabiati_koruma_alanlari.json',
             'millipark/tabiat_parklari.json',
             'millipark/yaban_hayati_gelistirme_sahalari.json',
             'millipark/sulak_alanlar.json']

    for f in files:
        print (f)
        with open(f, encoding='utf-8') as fh:
            data = json.load(fh)
        for name in data.keys():
            data1 = data[name]
            data1 = np.array([[float(x[0]),float(x[1])] for x in data1])
            folium.Polygon(locations=data1,weight=2,color = 'blue').add_to(m)

camp()
park()
            
m.save("/tmp/index.html")
