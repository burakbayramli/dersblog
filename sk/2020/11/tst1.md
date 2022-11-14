
```python
N = 100
c1 = np.random.multivariate_normal(np.array([-3,-3,-3]), np.eye(3), size=N)
c2 = np.random.multivariate_normal(np.array([3,3,3]), np.eye(3), size=N)
c = np.vstack((c1,c2))
```


```python
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig=plt.figure()
ax=Axes3D(fig)
ax.plot(c[:, 0], c[:, 1], c[:, 2],'.')
plt.savefig('/tmp/out1.png')
```

```python
fig = mlab.figure(fgcolor=(0., 0., 0.), bgcolor=(1, 1, 1), size=(640, 360))
r = np.ones(2*N)*0.2
color=(0.2, 0.4, 0.5)
mlab.points3d(c[:, 0], c[:, 1], c[:, 2], r, color=color,
              colormap = 'gnuplot', scale_factor=1, figure=fig)
mlab.outline()
mlab.view(azimuth=00, elevation=80, focalpoint=[1, 1, 1], distance=30.0, figure=fig)
mlab.savefig(filename='/tmp/out2.png')
```

```text
(100, 3)
(200, 3)
```










