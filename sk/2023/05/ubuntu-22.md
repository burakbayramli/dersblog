# Ubuntu 22

Kurulum için

http://releases.ubuntu.com/22.04/

adresinden 64-bit iso ya da iso için torrent indirilir, iso'yu USB
flash disk'e "yakmak" için [3].

Bios'a bilgisayar başlarken F2'yi basılı tutarak girebiliriz,
girdikten sonra başlangıç şeklini "Legacy Mode" haline getirmek lazım,
ve USB dışkı yükleme sırasında en üste getirmek lazım. F10 ile
kaydedilir, tekrar başlatılır ve Ubuntu kurulur. 

Kurulum ardından hemen

```
sudo apt install emacs git build-essential python3 openssh-server python3-virtualenv
```

Alt+Space Problemi

Emacs üzerinde Alt-Space çok kullanıyoruz, fakat bu kombinasyon Ubuntu
tarafından "kapılmış". Bu kombinasyonu Ubuntu seviyesinde iptal etmek
için System Tools | System Settings | Keyboard ve Shortçüts | Windows
bölümunde "Activate the window menü" için Alt+Space seçilmiş, bu
satıra gidip çift tıklama yapın ve Silme (backspace) düğmesine basın.

Diger Tuslar

Biz CAPS tuşunu CTRL, varsa Windows tuşunu Alt olarak kullanıyoruz.
Package Manager'da "gnome tweaks" kurulur. `Additional Layout Options`
içinde `Alt and Win behaviour` altında `Alt is mapped to Win and the
usual Alt` seçilir. `Caps Lock behavior` altında `Make CAPS an
additional Ctrl`.

Python ile çok iş yapılacak, hemen sistem ve neredeyse tüm programcılık
işlerinin kullanacağı kütüphaneler için bir sanal ortam yaratmak iyidir.
Benimki `$HOME/Documents` altında,

```
virtualenv -p /usr/bin/python3 env3
```

Şimdi `.bashrc` içinde bazı iyi kısayol komutlar,

alias env3='source /home/burak/Documents/env3/bin/activate'
alias em='source /home/burak/Documents/env3/bin/activate; emacs & disown'
alias emnw='source /home/burak/Documents/env3/bin/activate; emacs -nw '

### Pymacs

```
git clone git@github.com:/pinard/Pymacs.git
```

Dizinde `make` ve `python setup.py build` ve `python setup.py install`.

Fakat Ubuntu 22 olağan kurulum Python versiyon 3.10.6 yapar, Pymacs'in
bu versiyon ile ufak bir problemi var, ya geriye 3.6 versiyonuna
gidilir, ya da hemen kod uzerinde ufak bir degisiklik,

Satir 43

```python
def callable(value):
    return isinstance(value, collections.Callable)
```

alttaki satıra değiştirilir [2],

```python
def callable(value):
    return isinstance(value, collections.abc.Callable)
```

Kaynaklar

[1] https://fostips.com/remap-keys-ubuntu-22-04/

[2] https://stackoverflow.com/questions/69515086/error-attributeerror-collections-has-no-attribute-callable-using-beautifu

[3] http://www.pendrivelinux.com/universal-usb-installer-easy-as-1-2-3/