# NoSQL

Basit dağıtık çalışabilen bir NoSQL taban tasarımı şöyle olabilir.

- Yükü karşılıyabilmek için ayrı servisler başlatılır. N tane servis
  için her anahtar üzerinden i = mod N işletilir, ve o veri için i
  servisine gidilir. Böylece veri bazlı yük dengesi yapılmış olur. 
  
- Her servis ayrı bir Flask süreci işletilir, onun get, set arayüzüne
  REST API üzerinden erişilir.
  
- Arka planda Flask paralel değil seri halde çalışır, ve kendi sqlite
  tabanına yazar ve okur, böylece her servisin kendi içindeki çakışma
  problemleri ile uğraşmaya gerek kalmaz.
  
- Bir anahtara tekabül eden herhangi bir obje, ne olursa olsun, yazılıp
  okunabilir, çünkü objeler `pickle` üzerinden string halne getirilirler.

```python
import pickle
a = list(range(10))
a = base64.encodestring(pickle.dumps(a))
print ('kodlama',a)
b = pickle.loads(base64.decodestring(a))
print (b)
```

```text
kodlama b'gANdcQAoSwBLAUsCSwNLBEsFSwZLB0sISwllLg==\n'
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```

Üstteki örnekte kodlama metni tabana yazılacaktır.

- Listeleri halletmek kolay; liste ismi, mesela `liste2`, ya da
`müşteriler` gibi, sqlite tabanında ayrı bir kolon olarak yazılır,
sonra bu tekrar eden liste ismine sahip tüm satırlar alinip liste
halinde döndürülebilir.

### Kodlama

```python
from flask import Flask, url_for, jsonify, request, Response
import sys

app = Flask(__name__)

@app.before_first_request
def start_check_db():
    sno = app.config.get('server_no')
    print ('server', sno)

@app.route('/get', methods=["PUT", "POST"])
def get():    
    data = request.get_json(force=True)   
    print (data)
    return jsonify({'result': "2423424"})

if __name__ == "__main__":
    app.config['server_no'] = sys.argv[1]
    app.run(host="localhost", port=8080)
    
```


Kaynaklar

[1] [Obje String Olarak Kodlamak](../../2010/10/encoding-objeleri-yazip-okumak-pickle-base64.html)