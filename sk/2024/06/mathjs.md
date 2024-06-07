# Math.js

Javascript içinde matematik, lineer cebir hesapları için `math.js` [1]. Dahil
etmek için komut satırı ortamında

```
var math = require('./math.js');
```

ve artık mesela `cos` çağırmak için `math.cos()` çağrısı yapılır, ve
`node` ile script çağrılır. HTML sayfa bağlamında standard `src include`
komutu gerekir. Yazının geri kalanı komut satırı farz edecek.

Bir matris işlemi,

```
let N = 20;
A = math.round(math.random([N,N]),5);
B = math.round(math.random([N,N]),5);

C = math.multiply(A, B);
```

Üstte bir lineer cebir matris çarpım işlemi yapmış olduk.

Bir vektörden tek bir sayı çıkarmak için 

```
console.log(math.subtract([2, 3, 4], 5));
```

```
[ -3, -2, -1 ]
```

İki vektörü toplamak,

```
console.log(math.add([2, 3, 4], [4,5,4]));
```

```
[ 6, 8, 8 ]
```

Bir vektörü bir sayıya bölmek,

```
console.log(math.divide([2, 3, 4], 2));
```

```
[ 1, 1.5, 2 ]
```

Kaynaklar

[1] https://mathjs.org/examples/index.html

