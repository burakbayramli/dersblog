# LaTeX 

Programlama dili gibi komut yazarak güzel formatlı doküman üretmenin
sanatını LaTeX mükemmeleştirdi. Microsoft Word gibi ürünler önünüzde
gördüğünüz elinize geçen sonuçtur (what you see iş what you get)
sloganı ile yaşarlar, fakat aslında bir doküman, bilgisayardaki pek
çok şey gibi, bir dil olarak görülebilir ve o şekilde kodlanabilir.
Özellikle zaten başka amaçlar için kod yazan bizler için bu yaklaşım
daha çekici olmuştur. Bir bakıma aslında dil-ile-doküman daha
optimaldir, az sayıda komut ile pek çok farklı şekilde belge
üretebildiğimize göre yaklaşımın faydası ortadan.

Kurmak için Ubuntu üzerinde

```
apt install texlive-latex-extra texlive-latex-recommended texlive-base
```

Bunlar oldukca buyuk programlar, şimdiden uyaralım.


### `\equiv`

Bir şeyin tanımı (defined as) için kullanılan sembol, eşitlik
işaretinin üçlü olanı.

### `\overline{kelime}`

Bazen `\bar` yeterli olmuyor, tüm kelimelerin üstünü kapsayacak bir
çizgi gerekiyor.

### `\underbrace{formül}_{altta ne söyleyecek}`

Formüllerin altına not olarak yazılacak şeyler için.

### `\cancel{ne}` ve `cancelto{neye}{neyi}`

Formullerde bazen bir seyin uzeri cizilip onun iptal edildigi
gosterilir. Sadece uzeri cizmek icin `\cancel`, eger cizip neye dogru
iptal oldugu icin `\cancelto` kullanilabilir. Kullanmak icin
`\usepackage{cancel}` ile cancel paketini almak lazim.

### `\leadsto`

Soldan sağa kıvrık ok işareti. Laplace Transformunu temsil etmek için
kullanılıyor bazen.

### `\stackrel{üst}{alt}`

Bir operatörü, işareti diğerinin üstüne koymak için kullanılabilir,
mesela biraz önceki `\leadsto` sembolünün hemen üstünde bir -1 sayısı
çıksın istiyorsam, `\stackrel{-1}{\leadsto}` kullanırım.

### `\buildrel`

Aynı şey, iki operatörü üst üste koymak. Üstteki örnek için `\buildrel
-1 \over \leadsto` kullanabilirdim.

### `\nabla`

Gradyan sembolü olan ters üçgen işareti

### `\oint`

Ortasında bir yuvarlak çizilmiş olan entegral işareti, eğri üzerinden
entegral alırken kullanılan sembol.

### `\mathbb{harf}`

Doğal sayılar N, reel sayılar R kümelerini gösterirken sol taraflarına
bir ekstra çizgi daha çekilir ve bu harfler daha "kalın" gözükür,
`\mathbb` bu işi yapıyor. `\usepackage{mathrsfs}` paketi dahil
edilmeli.

### `\mathscr{harf}`

Aşırı sükseli, bol kıvrımlı türden harfler için.

### Matris İçeriğini Büyütmek

Su sekilde bir matris ufak sekilde cikabilir,

```
\nabla u = \frac{\partial u_i}{\partial X_j} =
\left[\begin{array}{ccc}
\frac{\partial u_1}{\partial X_1} & \frac{\partial u_1}{\partial X_2} & \frac{\partial u_1}{\partial X_3} \\
\frac{\partial u_2}{\partial X_1} & \frac{\partial u_2}{\partial X_2} & \frac{\partial u_2}{\partial X_3} \\
\frac{\partial u_3}{\partial X_1} & \frac{\partial u_3}{\partial X_2} & \frac{\partial u_3}{\partial X_3} 
\end{array}\right]
```

İçeriği büyütmek için `\arraystretch` ve `\dfrac` lazım,

```
\renewcommand*{\arraystretch}{2.5}
\nabla u = \frac{\partial u_i}{\partial X_j} =
\left[\begin{array}{ccc}
\dfrac{\partial u_1}{\partial X_1} & \dfrac{\partial u_1}{\partial X_2} & \dfrac{\partial u_1}{\partial X_3} \\
\dfrac{\partial u_2}{\partial X_1} & \dfrac{\partial u_2}{\partial X_2} & \dfrac{\partial u_2}{\partial X_3} \\
\dfrac{\partial u_3}{\partial X_1} & \dfrac{\partial u_3}{\partial X_2} & \dfrac{\partial u_3}{\partial X_3} 
\end{array}\right]
```

Sonuç, öncesi solda sonrası sağda olacak şekilde,

![](latex1.png)




