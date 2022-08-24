# Genel Coğrafi Kordinat Kodları, HTML5, Javascript, Python

Mesafe hesabi yapmak

Iki enlem, boylam kordinati arasinda mesafe hesabi icin geopy kullanilabilir.

```python
import geopy.distance
dist = geopy.distance.vincenty((51.238689, 4.406747),(51.232246, 4.444266))
print (dist)
print (dist.km)
```

İkinci ifade float tıpınde mesafeyi verir, kilometre bazlıdır.

Ya da

```python
from pygeodesy.sphericalNvector import LatLon

p1 = LatLon(lat1, lon1)
p2 = LatLon(lat2, lon2)

p1.distanceTo(p2)
```

İki nokta arasında birinciden ikinciye olan açısal yön (bearing),

```python
def get_bearing(lat1,lon1,lat2,lon2):
    dLon = lon2 - lon1;
    y = math.sin(dLon) * math.cos(lat2);
    x = math.cos(lat1)*math.sin(lat2) - math.sin(lat1)*math.cos(lat2)*math.cos(dLon);
    brng = np.rad2deg(math.atan2(y, x));
    if brng < 0: brng+= 360
    return brng
```

Sonuç 0 derece kuzey olmak üzere 0-360 derece arasında saat yönüne
doğru artacak şekilde açı.

Bir kordinattan "10 km doguya, batiya, vs. adim atinca nereye
geliriz?" sorusunun cevabi icin

```python
import geopy
import geopy.distance
# baslangic noktasi
start = geopy.Point(48.853, 2.349)
# mesafe 1 km
d = geopy.distance.VincentyDistance(kilometers = 1)
# derece olarak adim atilacak yon, 0 derece kuzey, 90 dogu, ..
reached = d.destination(point=start, bearing=0)
print (reached.latitude)
print (reached.longitude)
```

Ya da

```python
from pygeodesy.sphericalNvector import LatLon
clat,clon=39.06084392603182, 34.274201977299
DIST = 1000
p1 = LatLon(clat,clon)
EARTH_RAD = 6371
upright = p1.destination (DIST, bearing=45, radius=EARTH_RAD)
lowleft = p1.destination (DIST, bearing=225, radius=EARTH_RAD)
print ( upright )
print ( lowleft )
```

```text
45.090707°N, 043.281808°E
32.450607°N, 026.747624°E
```

Örnekte Anadolu ortasından başlayıp 45 derece kuzeydoğuya ve 225
derece güneybatıya 1000 km adım atınca nereye geldiğimizi görüyoruz.

Bir GPS kordinat listesinin orta noktasını bulmak için,

Su [bağlantıdan](https://www.navlab.net/nvector/#example_7), enlem,
boylam bir üç boyutlu vektör haline getiriliyor, ve Kartezyen bazlı bu
vektörlerin ortalaması doğru ortalamayı veriyor. Kodun temel aldığı
makale [1].

```python
import numpy as np
import numpy.linalg as lin

E = np.array([[0, 0, 1],[0, 1, 0],[-1, 0, 0]])

def lat_long2n_E(latitude,longitude):
    res = [np.sin(np.deg2rad(latitude)),
           np.sin(np.deg2rad(longitude)) * np.cos(np.deg2rad(latitude)),
           -np.cos(np.deg2rad(longitude)) * np.cos(np.deg2rad(latitude))]
    return np.dot(E.T,np.array(res))

def n_E2lat_long(n_E):
    n_E = np.dot(E, n_E)
    longitude=np.arctan2(n_E[1],-n_E[2]);
    equatorial_component = np.sqrt(n_E[1]**2 + n_E[2]**2 );
    latitude=np.arctan2(n_E[0],equatorial_component);
    return np.rad2deg(latitude), np.rad2deg(longitude)

def average(coords):
    res = []
    for lat,lon in coords:
        res.append(lat_long2n_E(lat,lon))
    res = np.array(res)
    m = np.mean(res,axis=0)
    m = m / lin.norm(m)
    return n_E2lat_long(m)
        

n = lat_long2n_E(30,20)
print (n)
print (n_E2lat_long(np.array(n)))

# fransa ve libya ortasi
coords = [[30,20],[47,3]]
m = average(coords)
print (m)
```

Tabii paket kullanarak daha kolay olabilir,

```python
from pygeodesy.sphericalNvector import LatLon
b = LatLon(45, 1), LatLon(45, 2), LatLon(46, 2), LatLon(46, 1)
nvecs = np.array([a.toNvector() for a in b])
print (nvecs)
mid = nvecs.mean().toLatLon()
print (mid.lat, mid.lon)
```

```text
[Nvector(0.707, 0.01234, 0.70711) Nvector(0.70668, 0.02468, 0.70711)
 Nvector(0.69424, 0.02424, 0.71934) Nvector(0.69455, 0.01212, 0.71934)]
45.50109067812444 1.5
<class 'pygeodesy.sphericalNvector.LatLon'>
(0.700656, 0.018347, 0.713264)
```

Bir Coğrafi Nokta Bir Alan İçinde mi

Elde köşeleri bilinen bir üçgen, kare ya da dışbükey poligon var
diyelim, mesela Bermuda Ucgeni! Elimizdeki bir noktanın o alan içine
düşüp düşmediğini nereden bileceğiz?  Burada iyi bir yaklaşım
`pygeodesy` paketi, bu paket üstteki n-vektör yaklaşımını kullanıyor,
yani sağlam. Bir örnek altta, dörk köşesi verilmiş alan içine `45.1,
1.1` noktasının düşüp düşmediğini soruyoruz,

```python
from pygeodesy.sphericalNvector import LatLon

p = LatLon(45.1, 1.1)
b = LatLon(45, 1), LatLon(45, 2), LatLon(46, 2), LatLon(46, 1)
print (p.isenclosedBy(b))
```

HTML5 ve Javascript ile Yer Bulmak

Javascript icinden yer bulmak mumkun, bu cep telefonunda da isliyor,
Google'in Wifi, Telekom, GPS uzerinden yer bulan arayuzu ile
baglantili zannederim. Kalitesini kontrol etmedim, ama alttaki kod
isler ve yer rapor eder. Isletince tarayici 'yer bilgisine erisim'
icin izin isteyecek. Izin verince (allow), bilgi sayfada basilacak ve
kullanim ornegi olsun diye bir de URL baglantilardan birine parametre
olarak eklenecek.

```
<html>
  <script>
    var lat = "lat";
    var lon = "lon";
    function getLocation() {
       navigator.geolocation.getCurrentPosition(setPosition);
    }
    function setPosition(position) {
      lat = position.coords.latitude;
      lon = position.coords.longitude;
      document.getElementById("locpos").innerHTML = lat + " " + lon;
      document.getElementById("url1").href="/bir/baglanti/" + lat + ";" + lon;
    }
</script>
<body onload="init()">

  <div class="navmenu">
    <nav>
      <div id="locpos">
        <p></p>
      </div>
      <ul>
        <li><a id="grab" href="#" onclick='getLocation()'>Yer Bul</a></li>
        <li><a id="url1" href="/bir/baglanti/32324">Baglanti</a></li>
        <li><a id="vsvs" href="">Vs..</a></li>
      </ul>
    </nav>
  </div>

</html>
```

Kaynaklar

[1] Kenneth Gade (2010), A Non-singular Horizontal Position Representation,
    The Journal of Navigation, Volume 63, Issue 03, pp 395-417, July 2010.


