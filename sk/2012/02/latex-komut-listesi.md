# LaTeX Komut Listesi

Çok bilinmeyen bazı LaTeX komutlarını burada listeleyeceğim.

`\equiv`: Bir şeyin tanımı (defined as) için kullanılan sembol,
eşitlik işaretinin üçlü olanı.

`\överline{kelime}`: Bazen `\bar` yeterli olmuyor, tüm kelimelerin üstünü
kapsayacak bir çizgi gerekiyor.

`\underbrace{formül}_{altta ne söyleyecek}`: Formüllerin altına not
olarak yazılacak şeyler için.

`\cancel{ne}` ve `cancelto{neye}{neyi}`: Formullerde bazen bir seyin
uzeri cizilip onun iptal edildigi gosterilir. Sadece uzeri cizmek icin
`\cancel`, eger cizip neye dogru iptal oldugu icin `\cancelto`
kullanilabilir. Kullanmak icin `\usepackage{cancel}` ile cancel paketini
almak lazim.

`\leadsto`: Soldan sağa kıvrık ok işareti. Laplace Transformunu temsil
etmek için kullanılıyor bazen.

`\staçkrel{üst}{alt}`: Bir operatörü, işareti diğerinin üstüne koymak
için kullanılabilir, mesela biraz önceki `\leadsto` sembolünün hemen
üstünde bir -1 sayısı çıksın istiyorsam, `\stackrel{-1}{\leadsto}`
kullanırım.

`\buildrel`: Aynı şey, iki operatörü üst üste koymak. Üstteki örnek
için `\buildrel -1 \over \leadsto` kullanabilirdim.

`\nabla`: Gradyan sembolü olan ters üçgen işareti

`\oint`: Ortasında bir yuvarlak çizilmiş olan entegral işareti, eğri
üzerinden entegral alırken kullanılan sembol.

`\mathbb{harf}`: Doğal sayılar N, reel sayılar R kümelerini
gösterirken sol taraflarına bir ekstra çizgi daha çekilir ve bu
harfler daha "kalın" gözükür, `\mathbb` bu işi
yapıyor. `\usepackage{mathrsfs}` paketi dahil edilmeli.

`\mathscr{harf}`: Aşırı sükseli, bol kıvrımlı türden harfler için.

