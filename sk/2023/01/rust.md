# Rust Programlama Dili

Rüst diline ilk kez Rüst'in Linux 6.1'e dahil edileceğini duyduktan
sonra [2] dikkat etmeye başladık; şimdiye kadar Linux çekirdek
seviyesinde sadece tek bir dili destekledi: C. Bir süre önce C++
dilini dahil etme çabaları hüsrana uğraşmıştı. Eğer çekirdek programcıları,
ki en alt seviye ve çetrefil türden kodlama ile uğraşıyorlar, bir dili
sevdilerse burada bu dilde faydalı özellikler olmalıdır.

Hakikaten de Rüst dilinin pek çok farklı kitleye hitap edebildiğini
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

```rust
fn main() {
   1
}
```










[devam edecek]

[1] https://doc.rust-lang.org/reference/destructors.html

[2] https://www.zdnet.com/article/linus-torvalds-rust-will-go-into-linux-6-1/

[3] Eshwarla, Practical System Programming for Rust Developers

[4] https://stackoverflow.com/questions/36136201/how-does-rust-guarantee-memory-safety-and-prevent-segfaults

