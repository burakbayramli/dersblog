# NoSQL

NoSQL tabanları arka planda ilişkisel veri yapısı (SQL ile erişilen
türden) gerektirmeden veri depolamayı destekleyen tabanlardır. Bir
bakıma diske yazılmış Python sözlüğü gibi görülebilirler; tek ihtiyaç
duydukları bir anahtar ve ona tekabül eden değerdir, ki değer herhangi
bir obje olabilir. Mimarinin çekici tarafı veri ünitesini tek objeye
indirdediğimizde dağıtık ortamda çalışmanın kolaylaşması, ölçeklemek
için belli objeleri belli makinalara gönderdiğimizde problem
çözülüyor, çünkü ilişkisel bağlantıları takip etmek gerekmiyor.

Eger tek obje / tek surec bazli calismak istersek, basit dağıtık
çalışabilen bir NoSQL taban tasarımı şöyle olabilir.

- Yükü karşılıyabilmek için ayrı servisler başlatılır. Bağlanan taraf
  istemcide N tane servisten hangisine gidileceğine karar vermek için
  her anahtar üzerinde i = mod N işletilir, ve cevaba göre o veri için
  i servisine gidilir. Böylece veri bazlı yük dengesi yapılmış olur.
  Bildiğimiz gibi mod N sonucu N'yi geçemez, ve mod sona geldiğinde
  başa dönen bir yapıdadır bu şekilde dengeli bir dağıtım yapar.
  
- Her serviste ayrı bir Flask süreci işletilir, taban verisini Flask
  REST API'si üzerinden dışarı açarız, burada `get`, `set` çağrıları
  olacaktır, girdi ve sonuç alışveriş JSON üzerinden yapılır.
  
- Her Flask süreci içinde seri halde çalışılır (paralel değil), bu
  seri süreç kendi sqlite tabanına yazar ve oradan okur, böylece her
  servisin kendi içindeki eşzamanlı olmasından olabilecek çakışma
  problemleri engellenmiş olur. Servis tarafı basitleşir.
  
- Bir anahtarla beraber herhangi bir obje, ne olursa olsun, tabana
  yazılıp okunabilmelidir, objeleri `pickle` üzerinden string haline
  getirebiliriz, ve arka planda temel depolama sqlite `TEXT` kolonunda
  olur, [1]'de bunun örneğini gördük.

- Listeleme: onlar için ayrı bir SQL tablosu gerekir, bir kolonda
  liste ismi, diğerinde obje anahtarı. Liste ismi satırlarda
  tekrarlanabilir böylece çoka bir ilişki kuruyoruz. Listeyi
  istemciden almak için o isim üzerinde `where` işletiliriz. Sayfalama
  özelliği SQL LİMİT üzerinden sağlanır, çağıran tarafta liste obje
  anahtarlarını objeye çevirmek için servise tekrar sormak gerekecektir.

### Servis

Basit bir Flask servisi altta,

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

`start_check_db` ile taban yoksa baslangicta yaratilir.

Tabana tek bir bağlantı vardır, o bağlantı `OnlyOne` tekil obje
(singleton) içinde muhafaza ediliyor. Servises şzamanlı erişim
olmadığı için birden fazla bağlantıya da gerek yok.

REST arayüzüne `curl` ile eriselim,

```python
! curl -H "Content-Type: application/json" -d '{"key":"test1"}'  http://localhost:8080/get
```

```text
{"result":"value1"}
```

```python
curl -H "Content-Type: application/json" -d '{"key":"asdjflkajsf"}'  http://localhost:8080/get
```

```text
{"result":"None"}
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

Şimdi REST çağrılarını iki fonksiyon ile sarmalayalım, kullanıcıların
çağıracağı tek metotlar bunlar olacak.

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

[3] [MongoDB](../../2014/05/mongodb.html)

