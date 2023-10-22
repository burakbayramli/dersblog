# Leaflet ile Haritalamak

Python bazlı haritalama paketi Folium yazılımından daha önce [1]
bahsettik, aslında Folium paketinin ilk çıkışı Javascript bazlı
Leaflet yazılımıdır. Hatta Folium Python çağrıları sonrası `save` ile
kaydedilebilen HTML dosyasına bakarsak orada leaflet Javascript
çağrıları olduğunu göreceğiz. Yani Folium aslında Leaflet'i
sarmalayan (wrap) ona arayüz sağlayan ince bir tabakadır.

Leaflet'in en avantajlı tarafı Javascript bazlı, yani tarayıcıda
işleyen kodları sayesinde dinamik görüntülenen haritaları
yaratabilmesidir. Yakınlaştırma (zoom), sağa sola kaydırma gibi pek
çok işlemi bir Leaflet haritası üzerinde yapabiliriz. Ayrıca leaflet
arka planda "fayans (tile)" denen görüntüleri basabilir, bunlar mevcut
bir haritalama veri tabanı tarafından önceden üretilmiş farklı
yakınlık seviyelerindeki görüntülerdir, yakınlık seviyesi kullanıcı
tarafından arttırıldıkça gerekli görüntü haritalama servisinden alinip
arka plana koyulur. Leaflet tüm bu işlemleri otomatik olarak yapar.
Fayanslar mesela dağları, nehirler gösteren bir doğa tabakası olabilir,
ya da tüm caddeleri, dükkanları gösteren bir şehir tabakası olabilir.
Kullanıcı istediği fayans tabakasını haritayı oluştururken seçebilir.

En basit leaflet kodu alttaki gibi,

```html
<html>
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
          integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
          crossorigin=""/>
    <style>
      #map {
        height: 500px;
      }
    </style>
  </head>

  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
          integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo="
          crossorigin=""></script>

  <script>
    function init() {
      map = L.map('map').setView([40,30], 6);
      L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
                   maxZoom: 19,
                   attribution: 'OSM'
      }).addTo(map);
   }
  </script>
  
  <body onload='init()'>    
    <div id="map"></div>    
  </body>

</html>
```

[HTML](leaf1.html)

Bu haritaya gösterime sunmadan önce bazı ekler yapabiliriz. Mesela
farklı renklerde işaretleyici (marker) kullanabiliriz. Bu işaretler
için imaj dosyaları lazım, altta bu dosyalar bulunabilir,


[marker-icon-2x-black.png](marker-icon-2x-black.png),
[marker-icon-2x-blue.png](marker-icon-2x-blue.png),
[marker-icon-2x-gold.png](marker-icon-2x-gold.png),
[marker-icon-2x-green.png](marker-icon-2x-green.png),
[marker-icon-2x-grey.png](marker-icon-2x-grey.png),
[marker-icon-2x-orange.png](marker-icon-2x-orange.png),
[marker-icon-2x-red.png](marker-icon-2x-red.png),
[marker-icon-2x-violet.png](marker-icon-2x-violet.png),
[marker-icon-2x-yellow.png](marker-icon-2x-yellow.png),
[marker-shadow.png](marker-shadow.png)

İşaretleyici ekleme kodları,

```javascript
var LeafIcon = L.Icon.extend({
       	options: {
             shadowUrl: 'marker-shadow.png',
             iconSize:     [20, 40],
             shadowSize:   [25, 30],
             iconAnchor:   [10, 45],
             shadowAnchor: [2, 30],
             popupAnchor:  [-1, -30]
        }
});
   
var orangeIcon = new LeafIcon({iconUrl: 'marker-icon-2x-orange.png'});
var yellowIcon = new LeafIcon({iconUrl: 'marker-icon-2x-yellow.png'});
var greenIcon = new LeafIcon({iconUrl: 'marker-icon-2x-green.png'});

L.marker([41,31], {icon: orangeIcon}).addTo(map);
L.marker([41,32], {icon: yellowIcon}).addTo(map);
L.marker([42,32], {icon: greenIcon}).addTo(map);
```

Kordinate listesi vererek o noktaları birleştiren çizgiler çizebiliriz,

[HTML](leaf2.html)

```javascript
path = [[40,31],[41,31],[41,30]];
var line = new L.Polyline(path, {
	     color: 'red', weight: 3, opacity: 0.5, smoothFactor: 1
});
line.addTo(map);
```

[HTML](leaf3.html)







[devam edecek]

Kaynaklar

[1] [Haritalamak](../../2020/02/haritalamak.html)
