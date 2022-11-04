

```python
import pandas as pd, random

n1,n2 = 70,30
N = n1+n2
height = [int(random.uniform(150,190)) for i in range(N)]
d = {"id": range(N), "height": height}
df = pd.DataFrame(d)

h1 = df.height.head(n1)
h2 = df.height.tail(n2)
m1,m2 = h1.mean(), h2.mean()
v1,v2 = h1.var(), h2.var()
print ('total', df.height.mean(), df.height.var())
```

```text
total 168.72 152.7288888888889
```

```python
bcm = (n1*m1 + n2*m2) / (n1+n2)
n1s,n2s = n1 / n2, 1.0
print (cm)
cm = (n1s*m1 + n2s*m2) / (n1s+n2s)
print (cm)
```

```text
168.72
168.72
```



```python
d1 = np.array([32, 36, 27, 28, 30, 31])
d2 = np.array([32, 34, 30, 33, 29, 36, 24])
d3 = np.array([39, 40, 42])
n1,n2,n3 = len(d1),len(d2),len(d3)
dp = np.hstack([d1,d2,d3])
m1,m2,m3,mp = d1.mean(), d2.mean(), d3.mean(),dp.mean()
v1,v2,v3,vp = d1.var(), d2.var(), d3.var(),dp.var()
print (m1,m2,m3,mp)
print (v1,v2,v3,vp)
ap = (n1*m1 + n2*m2 + n3*m3) / (n1+n2+n3) 
mean_of_var = (n1*v1 + n2*v2 + n3*v3) / (n1+n2+n3) 
var_of_means = (n1*(m1-ap)**2 + n2*(m2-ap)**2 + n3*(m3-ap)**2) / (n1+n2+n3)
print (mean_of_var)
print (var_of_means)
print (mean_of_var + var_of_means)
```

```text
30.666666666666668 31.142857142857142 40.333333333333336 32.6875
8.555555555555554 13.26530612244898 1.5555555555555554 22.83984375
9.303571428571427
13.536272321428578
22.839843750000007
```















