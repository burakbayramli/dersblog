# Math.js

Javascript içinde matematik, lineer cebir hesapları için `math.js` [1]. Dahil
etmek için komut satırı ortamında

```javascript
var math = require('./math.js');
```

ve artık mesela `cos` hesabı için `math.cos()` çağrısı yapılır, ve
`node` ile script işletilir. HTML sayfa bağlamında standard `src
include` komutu gerekir. Yazının geri kalanı komut satırı farz
edecek. Bir matris işlemi,

```javascript
N = 20;
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

```javascript
console.log(math.add([2, 3, 4], [4,5,4]));
```

```
[ 6, 8, 8 ]
```

Bir vektörü bir sayıya bölmek,

```javascript
console.log(math.divide([2, 3, 4], 2));
```

```
[ 1, 1.5, 2 ]
```

Matris toplam işlemi

```javascript
const e = m.matrix([[5, 6], [5, 6]]);

const f = m.matrix([[10, 20], [10, 20]]);

console.log(m.add(e,f));
```

```
DenseMatrix {
  _data: [ [ 15, 26 ], [ 15, 26 ] ],
  _size: [ 2, 2 ],
  _datatype: undefined }
```

Özdeğer, Özvektör

```javascript
const H = m.matrix([[5, 3.5], [2.3, 1]]);

const res = m.eigs(H);

E = res.values;

V = res.vectors;

console.log(E);

console.log(V);
```

```
DenseMatrix {
  _data: [ -0.471310991541956, 6.471310991541956 ],
  _size: [ 2 ],
  _datatype: undefined }
DenseMatrix {
  _data: 
   [ [ 0.12599764007559078, 6.433303428263717 ],
     [ -0.19696350658683628, 2.704397155979702 ] ],
  _size: [ 2, 2 ],
  _datatype: undefined }
```

Devrik alma `transpose` ve tersine çevirme `inv` işlemleri de aynı
kütüphane üzerinde bulunabilir.

Tersini alma,

```
const H = math.matrix([[2, 0], [0, 2]]);

console.log(math.inv(H));
```

```
DenseMatrix {
  _data: [ [ 0.5, -0 ], [ -0, 0.5 ] ],
  _size: [ 2, 2 ],
  _datatype: undefined }
```

Devrik,

```
const H = math.matrix([[1, 2], [3, 4]]);

console.log(math.transpose(H));
```

```
DenseMatrix {
  _data: [ [ 1, 3 ], [ 2, 4 ] ],
  _size: [ 2, 2 ],
  _datatype: undefined }
```

Kaynaklar

[1] https://mathjs.org/examples/index.html




