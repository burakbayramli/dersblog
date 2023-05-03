# Web Sayfaları, HTML ve CSS

Görsel HTML sayfalarının arkasında aslında pür metin bazlı bir komut
serisi var. Bu komutları düz dosyaya (text) yazabilen herkes bir
görsel Web programcısı olabilir. Mevcut sayfalarda bu kodlari
gorebiliriz, mesela Chrome, Firefox gibi tarayicilarda Ctrl+U tuslarina
basinca View Source isletilir ve HTML kaynagi burada gorulebilir.
Mesela bu blog'un ana sayfasinin HTML kodları soyle,

[Çıktı](web1.jpg)

Sıfırdan bir HTML yaratalım;

```
<h1>Merhaba Dunya</h1>
<p>Burada bazi yazilar</p>
<p>Satir 2</p>
```

Windows üzerinde Notepad var, üsttekileri oraya yazıp `index.html`
diye bu dosyayı kaydedebiliriz ve o dosyaya tıklayınca otomatik olarak
çıktı tarayıcıyı başlatır.

Mac üzerinde TextEdit mevcut, File > New seçilir, sonra Format > Make
Plain Text. Üstteki HTML kodu buraya girilir, şimdi File > Save seçilir,
sonu .html ile biten bir dosya ismi seçilir, (mesela index.html), ve Save
tıklanır. Eğer hangi sonek (extension) kullanılacağı soruluyorsa to
“Use .html.” seçilir.

Görüntü şöyle olacak

[Link](webtest1.html)

HTML'de görüntü çıktısı etiketler ile kontrol edilir. Her etiketin bir
başlangıcı ve bitişi var, aradaki metin bu etiketin yarattığı görsel
ortamı yansıtır. Büyük harfli başlık için `<h1>` ile başlarız `</h1>`
ile bitiririz, ve aradaki tüm metin büyük harflerle gösterilir.

Benzer şekilde sırasıyla gittike daha küçük boyutlarda `<h2>`, `<h3>`
etiketleri de var.

Paragraflar `<p>`, `</p>` arasına yazılır. 

Tıklanabilir bağlantılar `<a href="">... </a>` arasında, tıklama
sonrası atlanacak adres `href=""` içinde ve bağlantının kullanıcıya
gösterdiği metin `<a href="...">` ve </a> arasına konulur.

```
<h1>Başlık</h1>
<p>Satır 1</p>
<p>Satır 2</p>
<p><a href="https://joinmastodon.org">Mastodon Burada</a></p>
```

[Link](webtest2.html)

Stiller

Web standartının (HTML, CSS bunların parçası) güzel bir tarafı
"içeriği stilden ayırma" özellikleri. Stil bir etikete uygulanan ek
komutlar olabilir, bu komutlar `style=".."` içine gider, mesela
başlığın arka plan rengini değiştirmek istiyorsam bunu `style="background: #1abc9c;"`
olarak `<h1>` etiketine ekleyebilirim. Stil pek çok özelliği kontrol edebilir,
mesela üstteki tıklanabilir bağlantıda üzerinde durunca alt çizgi gösterilmesin
istiyorsam bunu da `style="text-decoration:none;"` ile etikete söyleyebilirim.

```
<h1 style="background: #1abc9c;">Başlık</h1>
<p>Satır 1</p>
<p>Satır 2</p>
<p><a style="text-decoration:none;" href="https://joinmastodon.org">Mastodon Burada</a></p>
```

[Link](webtest4.html)

Tüm stiller ayrılıp HTML içinde ayrı bir bölüme de konabilir. Bu noktada bir HTML
sayfasının nihai formatını göstermek gerekli, bir `<head>..</head>` bölümü var,
bir de `<body>..</body>` bölümu var, bizim şimdiye kadar gördüklerimiz `<body>`
altına gidecek komutlardı. Stil komutları `<head>` altında ayrı bir `<style>`
etiketi altına konuyor. O zaman üstteki HTML şöyle değişir,

```
<!DOCTYPE html>
<html>
  <head>
    <style>
      h1 { background: #1abc9c; }
      a { text-decoration:none; }
    </style>
  </head>
</html>

<body>
  <h1>Başlık</h1>
  <p>Satır 1</p>
  <p>Satır 2</p>
  <p><a href="https://joinmastodon.org">Mastodon Burada</a></p>
</body>
```

[Link](webtest5.html)


Stil kodlarını bir CSS stil dosyası (stylesheet) olarak ayrı bir dosyaya da
yazabilirdik, bu durumda `<head>` içinde o dosyanin yüklenmesini söylemek
yeterli, stili `style6.css` içine yazalım,

```
<!DOCTYPE html>
<html>
  <head>
    <link rel="stylesheet" type="text/css" href="style6.css">
  </head>
</html>
<body>
  ...
</body>
```

[Link](webtest6.html)

Tabii her noktada ustteki ciktilari tarayicida gosterirken Ctrl+U ile
o sayfaya tekabul eden kodlari gorebiliriz,

![](web2.jpg)






[devam edecek]

