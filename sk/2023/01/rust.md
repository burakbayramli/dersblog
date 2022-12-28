# Rust Programlama Dili

Rust diline ilk kez Rust'in Linux 6.1'e dahil edileceğini duyduktan
sonra [2] dikkat etmeye başladık; şimdiye kadar Linux çekirdek
seviyesinde sadece tek bir dili destekledi: C. Bir süre önce C++
dilini dahil etme çabaları hüsrana uğraşmıştı. Eğer çekirdek programcıları,
ki en alt seviye ve çetrefil türden kodlama ile uğraşıyorlar, bir dili
sevdilerse burada bu dilde faydalı özellikler olmalıdır.

Hakikaten de Rust dilinin pek çok farklı kitleye hitap edebildiğini
görüyoruz. Evet C, C++ dilleri kendilerini ispat ettiler fakat bunun
bedeli hafıza erişimindeki güvenlik oldu.  Java, C# gibi üst seviye
diller hafıza erişiminde güvenlik sağladılar, fakat doğal olarak
hafızaya direk erişime engel getirdiler, programlama esnekliğine
kısıtlama getirdiler ve ne zaman devreye gireceği belli olmayan çöp
toplayıcı (garbage collector) programa istenmeyen anlarda
duraksamalara, geciktirmelere sebep olduğu için istenmeyen bir
performans kaybını yanlarında getirmiş oldular [3]. Rust modern, açık
yazılım bir sistem programlama dilidir, ve üç dünyanin en iyi
özelliklerini taşır; Java'nın değişken tipleme güvenliği, C++'in
yapısal açıklığı, hızı, verimliliği, ve çöp toplayıcı olmadan hafıza
erişim güvenliği.

Linux programcılarının niye bu dili sevdiği açık; Bildiğimiz gibi C
ile hafızaya direk erişim yapabiliriz, bir dizine hafızada yer ayırıp
(allocate) erişiriz, ama gösterge (pointer) ile ayrılan yerden ötesine
geçmek mümkündür, ve bu bazen `segfault` denen istenmeyen hafıza
erişim hatalarına, hatta güvenlik açıklarına sebep olmakdadır. Rust bu
tür kullanımlarına hafıza erişimine performans kısıtlaması getirmeden,
ya da erişimi yasaklamadan bir kontrol mekanizması getirmiştir.

Bazı diller az tanım gerektirirler, ve yükü yorumlayıcıya verirler,
bazı diller güçlü tipleme üzerinden derleyiciye daha çok iş
yaptırırlar (potansiyel hataları önceden bulma, sonuç işler kod için
optimizasyonlar yapma) ve bu şekilde daha hızlı kod üretmeye
uğraşırlar. Rust bunlardan ikinci kategoriye daha yakındır. Mesela
derleyici metot çağrılarını statik olarak çözümlemeye uğraşır, bazı
diller bu çözümlemeyi işlem anında "dinamik" olarak yapmaya
uğraşabilir, birinci yöntem daha hızlıdır.

### İlk Kullanım

Ubuntu Linux uzerinde,

```
curl https://sh.rustup.rs -sSf | sh
 rustup update
```

yeterli. Tüm konsolları kapatıp yeni bir tane başlatalım, artık
`rustc` derleyicisini direk kullanabiliriz. Altta kodu yazılarda
göstermek için bir fonksiyon yazdık,


```python
def rcode(infile): print (open(infile).read())
```

```python
rcode("rust1.rs")
```

```text
fn main() {
    println!("Merhaba Dunya!");
}

```

```python
! rustc -o /tmp/rust1.exe rust1.rs
! /tmp/rust1.exe
```

```text
Merhaba Dunya!
```

Bir fonksiyon yazalım, bir sayı alsın ve ona bir sayı eklesin,

```python
rcode("rust2.rs")
```

```text
fn add_one(a: u8) -> u8 {
    let g = a + 1;
    g
}

fn main() {
    let x = 1;
    let z = add_one(x);
    println!("{}", z);
}

```

```python
! rustc -o /tmp/rust2.exe rust2.rs
! /tmp/rust2.exe
```

```text
2
```

Fonksiyonun dönüş değeri en son satırda ismi üzerinden belirtiliyor,
bir döndürme komutu mesela `return` gibi kullanılmamış. Bu durumda
fonksiyon ortasından değer döndürmek için içinde olunan bloktan bir
şekilde çıkılmalı, son satıra erişilmeli, oradan dönüş yapılmalı
herhalde.

### Hafiza Degisken Idaresi

Not: İlerlemeden önce bu yazıda Rust kodu gösteren, derleyen ve işleten
bir yardımcı kod yazalım,

```python
import subprocess, os, sys

def rshow_comp_run(infile):
   print (open(infile).read())
   file = os.getcwd() + "/" + infile
   cmd = "rustc -o /tmp/%s %s" % (infile.replace(".rs",".exe"),file)
   print (cmd)
   process = subprocess.Popen(cmd.split(" "), stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False)
   (output, _) = process.communicate()
   res = str(output).split("\\n")
   for x in res: print (x)
```

Artik tek cagri ile uc isi birarada yapacagiz.

Değişken idaresine gelelim; Rust'in hafıza hatalarının önüne geçmek
için getirdiği bir değişiklik sahiplenme özelliği. İlginç bir özellik
bu, mesela eğer obje üzerinde kopyalama desteği yok ise eşittir
işareti bir objeyi bir değişkenden diğerine taşır, kopyalamaz,
referens arttırmaz. Birinden alıp diğerine verir. Bu durum aynı kapsam
(scope) içinde bile gerçekleşebilir. Mesela,

```python
rshow_comp_run("rust3.rs")
```

```text

fn main() {
    let num1 = 1;
    let num2 = num1;
    let s1 = String::from("meep");
    let s2 = s1;
    println!("Number num1 is {}", num1);
    println!("Number num2 is {}", num2);
    println!("String s1 is {}", s1);
    println!("String s2 is {}", s2);
}

rustc -o /tmp/rust3.exe /home/burak/Documents/classnotes/sk/2023/01/rust3.rs
b'error[E0382]: borrow of moved value: `s1`
 --> /home/burak/Documents/classnotes/sk/2023/01/rust3.rs:9:33
  |
5 |     let s1 = String::from("meep");
  |         -- move occurs because `s1` has type `String`, which does not implement the `Copy` trait
6 |     let s2 = s1;
  |              -- value moved here
...
9 |     println!("String s1 is {}", s1);
  |                                 ^^ value borrowed here after move
  |
  = note: this error originates in the macro `$crate::format_args_nl` which comes from the expansion of the macro `println` (in Nightly builds, run with -Z macro-backtrace for more info)

error: aborting due to previous error

For more information about this error, try `rustc --explain E0382`.
'
```

Burada hata ortaya çıktı çünkü String tipi kopyalama özelliğini kodlamamış,
ama 1 değerinin tipi tam sayıların bu desteği var, bu sebeple String s1'den
s2'ye taşındı, taşınınca ilk referans geçersiz hale geldi.


[devam edecek]

[1] https://doc.rust-lang.org/reference/destructors.html

[2] https://www.zdnet.com/article/linus-torvalds-rust-will-go-into-linux-6-1/

[3] Eshwarla, Practical System Programming for Rust Developers

[4] https://stackoverflow.com/questions/36136201/how-does-rust-guarantee-memory-safety-and-prevent-segfaults

[5] McNamara, Rust In Action

[6] Kaihlavirta, Mastering Rust


