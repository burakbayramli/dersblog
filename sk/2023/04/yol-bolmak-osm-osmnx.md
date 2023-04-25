# Yol Bulmak, OSMNX

OpenStreetMap dünya coğrafi verilerini içeren açık kaynak, herkesin
bilgi ekleyebildiği devasa bir kaynaktır, verisi açık, bedava olarak
paylaşılır. İçinde yollar, restoranlar, dükkanlar, önemli yerler gibi
pek çok coğrafi bilgileri içerir. Fakat veriyi işlemek bazıları için
zor olabilir.

Bu verinin daha rahat işlenmesini sağlayan bir paket OSMNX. Özellikle
yol ağ yapısını rahat şekilde indirilmesini ve çizit (graph) olarak
doğru şekilde gelmesini sağlıyor. Çizitler bilindiği gibi matematiğin
bir dalidir, bize düğüm-bağlantı yapılarını işleyen algoritmalar
sağlar, tabii ki bir yol ağı çizit teorisinin en bariz uygulama
alanıdır, düğümler duraklar, köşe başları vs olabilir bağlantılar
onlar arasındaki yollar olacaktır.

OSMNX sadece kullanicinin tanimladigi bolgeler icindeki yol yapisini
dondurme kabiliyetine sahiptir, ve bu veriyi diskte onbellekleme yaparak
saklayabilir, boylece ayni bolge icin sonraki yukleme cagrilarinin OSM'e
baglanmasi gerekmez. Örnek olarak [1]'deki şehre bakalım,

```python
import matplotlib.pyplot as plt
import osmnx as ox

ox.config(use_cache=True, cache_folder='/tmp/osmnx')

north, south, east, west = 37.79, 37.78, -122.41, -122.43

G = ox.graph_from_bbox(north, south, east, west, network_type="walk")
```

```python
fig, ax = ox.plot_graph(G, node_color="r",show=False, figsize=(15,7))
plt.savefig('osmnx-01.jpg',quality=50)
```

![](osmnx-01.jpg)


`cache_folder` ile önbellek dosyalarının yazılacağı yer tanımlanır. Üstteki çağrı
için baktık `30 520ecdb05972a5893b8a541266157cd0b30a6381.json` diye bir dosya
oraya yazılmış, büyüklüğü 1.8 MB. Fena değil. 


```python
print (list(G)[0])
print (list(G)[20])
```

```text
65281835
65295347
```

```python
print (list(G)[:10])
```

```text
[65281835, 65281838, 65282081, 65282083, 65282130, 65282133, 65282136, 65282140, 65282144, 65285109]
```


```python
origin = (40.969615352945354,29.07036154764545)
destination = (40.96660865138665,29.086701750114123)
origin_node = ox.distance.nearest_nodes(graph, origin[1], origin[0])
destination_node = ox.distance.nearest_nodes(graph, destination[1], destination[0])
print (origin_node)
print (destination_node)
```

```text
455860527
455860791
```

```python
route = ox.shortest_path(graph, origin_node, destination_node)
#fig, ax = ox.plot_graph_route(graph, route, route_color="c", node_size=3)
#plt.savefig('/tmp/out2.jpg')
for r in route: print (r)
```

```text
455860527
455860629
455860619
6928189233
6928189232
455860627
448779470
2244437518
10023487057
2373133718
448779466
448779460
448779457
448779453
448779456
448779463
448779455
455860791
```

[devam edecek]

Kaynaklar

[1] [Geoff Boeing](https://geoffboeing.com/2016/11/osmnx-python-street-networks/)

[2] [OSRM Yol Tarifi](../../2016/11/yol-tarifi-harita-bilgisi-osrm-backend.html)

[3] [NetworkX Multidigraph](https://networkx.org/documentation/stable/reference/classes/multidigraph.html)

[4] [OSMNX Belge 1](https://github.com/gboeing/osmnx-examples/blob/main/notebooks/01-overview-osmnx.ipynb)

[5] [OSMNX Belge 2](https://github.com/bryanvallejo16/shortest-path-osm/blob/main/shortest_path_osm_updated_example.ipynb)

[6] [OSMNX Belge 3](https://github.com/gboeing/osmnx-examples/blob/main/notebooks/02-routing-speed-time.ipynb)
