# GPU, CUDA, PyCuda

Bilgisayarımızda hesapları yapan işlemci var, bu işlemci son
zamanlarda çok çekirdekli hale de gelmeye başladı. Fakat
bilgisayarımızda işlem yapan çok kuvvetli bir parça daha var: grafik
işlemci (GPU).GPU paralel işlem açısından neredeyse pür mikroişlemci
kadar kuvvetlidir, hatta bazı açılardan daha hızlıdır, çünkü tarihsel
sebeplerle parallelliğe daha fazla yatkın olması gerekmiştir. GPU bir
görüntünün hızla çizilmesi (rendering) için piksel bazında paralelliğe
gitmek zorundaydı ve NVİDİA şirketinin ürünleri için artık bu normal
bir operasyondur.

Araştırmacılar bu paralellikten istifade etmeye karar vermişler, ve
grafiksel olmayan hesap işlemlerini sanki öyleymiş gibi GPU'ya
sunuyorlar, ve cevabı geri tercüme ediyorlar, böylece GPU'nun hızlı
paralel işlemci özelliğinden faydalanıyorlar. Pek çok matematiksel
hesabı bu şekilde yaptıran olmuş, mesela matris çarpımı, PDE çözümü,
simülasyon.

NVidia şirketi grafik kartlarının GPU'suna erişim için CUDA diye bir
kütüphane sağlıyor. Onun üstüne PyCUDA ile Python bazlı erişim de
var. Bazı ülkelerin üniversitelerinde CUDA eğitimini müfredata dahil
edilmiş. Dikkat: NVidia kartı piyasadaki grafik kartlarından bir
tanesidir, her laptop üzerinde NVidia olmayabilir (fakat NVidia
piyasadaki en ünlülerden birisi, bunu da ekleyelim). Şimdilik GPU
kodlaması için NVidia kartına sahip bir bilgisayar lazım.

(Derin Öğrenim) Deep Learning

Bu yaklasim oyle populerlesti ki video kart ureticisi NVidia disaridan
bilgisayara dahil edilebilen ayri bir ufak GPU unitesi bile
yaratti. Unitenin ismi Jetson karti.

https://developer.nvidia.com/buy-jetson

Kart üzerinde Ubuntu işleyebiliyor, network aktarıcısı (router) dahil
edilip hemen ssh ile alete bağlanabiliyorsunuz. Yapay öğrenim ile
uğraşanlar için müthiş haber GPU üzerinde mevcut 192 çekirdek aşırı
seviyede paralelism isteyen deep learning yaklaşımı için biçilmiş
kaftan, ki burada birisi denemiş, ve nasıl yapılabileceği
anlatılıyor. Blog sahibi Pete Warden imaj üzerinde yapay öğrenim
algoritmaları kullanma konusunda uzmanlardan biridir, bu iş için
kurduğu şirketini geçende Google satın aldı. Tabii ki Jetson üzerinde
direk CUDA kodlaması da yapılabilir.

Bir diğer seçenek Google bulutu üzerinde barındırılan not defteri
servisi [Google Collab](../../2018/11/gpu-tpu-saglayan-not-defter-ortami.md).
Bu servis [Jupyter](../../2018/09/jupyter-not-defterleri.md) teknolojisine İnternet
üzerinden erişim sağlıyor denebilir.

CUDA

Pek çok türde paralelizm, eşzamanlılaştırma tekniği var. Mesela disk
bazlı çalışan [eşle/indirge](../../2014/09/esle-indirge-mimarisi-mapreduce-mr.md)
bunlardan biri. Her teknik paralleliği hangi birim üzerinde, nerede,
ne zaman yaptırdığı bağlamında birbirinden farklı. GPU kodlaması ŞİMD
yaklaşımını benimser, ŞİMD = Single Instruction Multiple Data, yani
Tek Komut Pek Çok Veri yaklaşımı. ŞİMD ile bir işlem, ki bu çarpma,
toplama, vs gibi temel işlemler ya da onların toplamı olan bir hesap
ünitesi olabilir, aynı anda birden fazla veri noktası üzerinde
uygulanır. Bu yaklaşımın grafik kartları, grafikleme için nasıl
faydalı olacağını görmek zor değil, çünkü grafik kartları için veri
görüntü pikselleridir, ve her piksel üzerinde, resim kare kare
oluşturulurken tek bir işlemi pek çok piksel üzerinde aynı anda
uygulamak faydalı bir özellik.
