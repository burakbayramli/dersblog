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
import pickle, base64
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

### Servis

```python
from flask import Flask, url_for, jsonify, request
import sys, os, sqlite3

app = Flask(__name__)

class OnlyOne(object):
    class __OnlyOne:
        def __init__(self):
            self.conn = None
        def __str__(self):
            return self.val
    instance = None
    def __new__(cls):
        if not OnlyOne.instance:
            OnlyOne.instance = OnlyOne.__OnlyOne()
        return OnlyOne.instance
    def __getattr__(self, name):
        return getattr(self.instance, name)
    def __setattr__(self, name):
        return setattr(self.instance, name)

@app.before_first_request
def start_check_db():
    sno = app.config.get('server_no')
    db = "/opt/Downloads/kvf-%d.db" % int(sno)
    conn = sqlite3.connect(db)
    OnlyOne().conn = conn
    if not os.path.isfile(db): 
        c = OnlyOne().conn.cursor()
        res = c.execute('''CREATE TABLE OBJ (key TEXT PRIMARY KEY, value TEXT); ''')
        c.execute('''INSERT INTO OBJ(key,value) VALUES(?,?)''', ("test1","value1"))
        conn.commit()    
    print ('server', sno)

@app.route('/get', methods=["PUT", "POST"])
def get():    
    data = request.get_json(force=True)   
    key = data['key']
    c = OnlyOne().conn.cursor()
    c.execute("SELECT value FROM OBJ WHERE key = ?", [key])
    res = list(c.fetchall())
    if len(res)==0: 
        return jsonify({'result': "None"})
    return jsonify({'result': res[0][0]})

@app.route('/set', methods=["PUT", "POST"])
def set():    
    data = request.get_json(force=True)   
    key = data['key']
    value = data['value']
    c = OnlyOne().conn.cursor()
    c.execute("insert or replace into OBJ (key,value) values (?,?)", [key,value])
    return jsonify({'result': "OK"})

if __name__ == "__main__":
    app.config['server_no'] = sys.argv[1]
    app.run(host="localhost", port=8080)   
```

```python
! curl -H "Content-Type: application/json" -d '{"key":"test1"}'  http://localhost:8080/get
```

```text
{"result":"value1"}
```

```python
curl -H "Content-Type: application/json" -d '{"key":"asdjflkajsf"}'  http://localhost:8080/get
```

```python
curl -H "Content-Type: application/json" -d '{"key":"3333", "value":"value333"}'  http://localhost:8080/set
curl -H "Content-Type: application/json" -d '{"key":"3333"}'  http://localhost:8080/get
```

### İstemci

Üstteki `curl` bazlı çağrıları pür Python içinde de yapabilirdik,

```python
import requests
response = requests.post('http://localhost:8080/get', json={"key":"test1"})
print("Status code: ", response.status_code)
print(response.json())
```

```text
Status code:  200
{'result': 'value1'}
```

```python
import requests, pickle, base64

def get(key):
    response = requests.post('http://localhost:8080/get', json={"key":key})
    print("Status code: ", response.status_code)
    res = response.json()
    res = pickle.loads(base64.decodestring(res['result'].encode('utf-8')))
    return res
    
def set(key,value):
    value = base64.encodestring(pickle.dumps(value)).decode()
    response = requests.post('http://localhost:8080/set', json={"key":key,"value":value})
    print("Status code: ", response.status_code)
    res = response.json()
    

set("2324","33333ddddd3")
o = get("2324")
print (o)
```



Kaynaklar

[1] [Obje String Olarak Kodlamak](../../2010/10/encoding-objeleri-yazip-okumak-pickle-base64.html)

[2] https://flask.palletsprojects.com/en/2.2.x/patterns/sqlite3/