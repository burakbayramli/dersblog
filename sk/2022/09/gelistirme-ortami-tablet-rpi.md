# Klavye, Android, Raspberry Pi Geliştirme Ortamı

Mobil geliştirme ortamı hazırlamak için Bluetooth klavye, Android
Tablet, SSH, RPi üzerinde Ubuntu olabilir. Çoğu işi editör'de metin
girerek kodlama yapıyorsak (görsel çıktılar RPi mikro web servisi
üzerinden alınabilir) bu işler.

Powerbank RPi çalıştırır. Tablet ile Android üzerinde yazıyoruz,
Android hotspot üzerinden Raspberry'ye DHCP IP adresi verdiriyoruz
(192.168.43.x gibi bir adres bunu `ifconfig -a` ile RPi uzerinden
ögrenebiliriz, ve RPi üzerinde WiFi aktif hale getirmek
lazım). Ardından tablet üzerinden Termux [7] `ssh` ile RPi'a
bağlanırız. Kuruluş böyle.

[Resim](tablrpi1.jpg)

Assistant

Bizim tablet Lenovo M8, Eğer editör kullanacaksak, üstte görülen
tablet uzerinden, Windows tuşunu iptal etmek iyi fikir [2].

Adım 1: `Device Settings` açılır, sonra `Apps/Application Manager`.

Adım 2: `Default apps` tıklanır, sonra `Assist & voice input`.

Adım 3: `Assist app` seçeneği seçilir. Sonraki ekranda `Assist app`
için `Google` gösteren bir app listesi görüyoruz. Biz `home` düğmesi
için `None` seçiyoruz, böylece Assistant artık çıkmıyor.

Tuş Değişimi

Control tuşu Trust Bluetooth klavyelerinde rahat erişilen yerde değil,
Vim, Emacs kullanıcıları bu tuşu çok kullanır, CAPS tuşunu CTRL
yapabiliriz. Fakat Android seviyesinde değişiklik lazım. Şu [1]
uygulama ile web üzerinde bir .apk ürettiriliyor (arka planda derleme
vs işleri yapılıyor), bu .apk indirilip kurulunca (Android uyarılarını
dikkate almayız) artık CAPS tuşu CTRL haline gelir. Üretimden önce
seçeneklerde `Caps Lock as Left Ctrl` seçmiş olmak lazım, bu seçim
`map key 58 CTRL_LEFT` komutunu alttaki kutuya ekler. Bu tanım daha
sonra yaratılacak .apk içine koyulacak. Uygulamaya güvenmeyenler aynı
sayfadaki bağlantıdan kaynak koduna gidip Android kodunu derleyebilir.

SSH

Termux `ssh` ile RPİ'a bağlandık, fakat ikidebir bağlantı
kopuyor.. Tamir için Termux üzerinde `nano .ssh/config` dosyasına
gidilir,

```
Host *
    ServerAliveInterval 240
```

yazılır, artık `ssh` komut satırında 4 dakika hiçbir işlem olmasa bile
bağlantı koparılmayacaktır.

Yerel Ağ Baglantısı

Test ettik, Tablet -> RPi arasındaki bağlantı eğer dış İnternet
bağlantısı olmasa bile işliyor. DHCP sonuçta yerel ağlarda işleyen bir
teknolojidir, dış İnternet olmasa da Android Wifi hotspot bir İP
adresi (çoğunlukla hep aynı) üretip Raspberry Pi'a
verecektir. Alternatif arayanlar mesela direk kablo ile USB-USB ile
bağlantı kurmak isteyenler [3,4,5] yazılarına bakabilir.  [5] yazısı
için her iki ucun mikro USB olması lazım, genelde kablolar USB->mikro
USB, bir ucu mikro USB yapan adaptörler var. [5] için iki ucun
Ethernet olması lazım, RPi üzerinde zaten Ethernet var, bu durumda
tablet için Ethernet->mikro USB adaptörü gerekir.

Kaynaklar

[1] [exkeymo](https://exkeymo.herokuapp.com/)

[2] [Windows Button / Assist Disable](https://www.guidingtech.com/remove-google-assistant-home-button/)

[3] [Reddit](https://www.reddit.com/r/raspberry_pi/comments/3bpw4g/connecting_to_the_raspberry_pi_from_your_android/)

[4] [Circuit Basics](https://www.circuitbasics.com/how-to-connect-to-a-raspberry-pi-directly-with-an-ethernet-cable/)

[5] [elinux](https://elinux.org/How_to_use_an_Android_tablet_as_a_Raspberry_Pi_console_terminal_and_internet_router)

[6] [Raspberry Pi](../../2020/07/raspberrypi.html)

[7] [Android Uzerinde Linux - Termux](2018/09/android-uzerinde-linux-termux.html)





