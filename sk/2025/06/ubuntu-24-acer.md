# Ubuntu 24, Acer Swift 3

Yeni dizüstü yeni Ubuntu. Swift 3 kuvvetli makina. Kurulum icin en son
Ubuntu versiyonu iso olarak alttan indirilir,

https://ubuntu.com/download/alternative-downloads

Dosya 6 GB civarı. Sonra mevcut (eski) Ubuntu üzerinde bu iso Startup
Disk Creatör programı ile bir usb flash diske yazılır. Artık üzerinden
yükleme (boot) edilebilir bir diskimiz var.

Şimdi Acer'da açılış sırasında F2 basılı tutularak BIOS'a girilir
(sifre sorarsa boş ya da 0000 denenebilir). `Main` menüden `F12 Boot
Menü` seçeneği `Enable` yapılır. Kaydedilip tekrar başlatılır, bu
sırada ardı ardına F12 tuşuna basılmalı. Görülen ekranda sadece bir
yükleme seçeneği var, ama flask diski USB porta sokar sokmaz Ubuntu
seçeneği de görülecek. Bunu seçin ve kurulumu yapın.

Makina açılınca `sudo apt install` ile kurulacak programlar,

```
gnome-tweaks python3-virtualenv git emacs texlive-latex-base net-tools
mpv emacs chromium-browser texlive-base djvulibre-bin imagemagick
```

Biz CAPS tuşunu hep CTRL yaparız, bu versiyonda bunu Gnome Tweaks ile
yapmak kolay, `gnome-tweaks` işletelim, "Keyboard | Additional Layout
Options" seçelim, orada "Caps Lock Behavior" var, değişimi oradan
yaparız.  Biz ayrıca "Alt Win behavior" seçeneğinde "Ctrl is mapped to
Win and the usual Ctrl" dedik ama herkesin tercihi farklı olabilir.

Ayrıca boşluk tuşunun yanındaki Alt Gr ve Ctrl tuşlarını fare sol ve
sağ tıklaması yapmayı seviyoruz, fakat dikkat, bunun için daha önce
`.bashrc` içinde yaptığımız

```
xmodmap -e "keycode 108 = Pointer_Button1"
xmodmap -e "keycode 105 = Pointer_Button3"
xkbset m
```

komutları son Ubuntu üzerinde işlemedi. Sebebi son Ubuntu'nun olağan
ayarlarının kullandığı X yazılımı imiş, bu yazılımı masaüstü'ne giriş
sırasında kullanıcı/şifre girmeden önce alt sağdaki ufak dişli çark
ikonuna tıklayarak ve "Ubuntu on xorg" seçerek değiştirebiliriz, bu
seçim sonraki girişlerde de hatırlanacaktır, ve onun sayesinde üstteki
ayarlar işler hale gelir.

Her programı işlediği sırada soldaki çabuk erişim alanına
"yapıştırmak" mümkündür, mesela Firefox işlerken ikonu solda gözükür,
o ikonun üzerinde sağ tıklama yapıp "Pin" seçersek program kapansa da
ikonu orada kalır. Sonraki başlatımları artık oradan yapabiliriz.

Komut satırı Terminal programında bazı değişimler; `Preferences` ile
girilir, sol kısımda `Unnamed` bölümüne gidilip orada pencere, font
büyüklüğü (`Custom font` ile) ayarlanır.  Ayrıca "Terminal bell"
kapatmak iyi olur, sürekli dan dun sesler gelmesin.

Kaynaklar

[1] https://www.youtube.com/watch?v=eMHr9jsbJG4

