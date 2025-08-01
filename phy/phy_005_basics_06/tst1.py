import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy.linalg as lin, sys, copy, os
from stl import mesh
sys.path.append("../phy_073_rot"); import euclid

def plot_vector1(fig, orig, v, color='blue'):
   orig = np.array(orig); v=np.array(v)
   ax.quiver(orig[0], orig[1], orig[2], v[0], v[1], v[2],color=color)

def plot_vector2(fig, torig, tend, color='blue'):
   v = tend - torig
   ax.quiver(torig[0], torig[1], torig[2], v[0], v[1], v[2],color=color)

mesh = mesh.Mesh.from_file('../../sk/2020/08/shapes/Prism_hexagon.stl')
cog = mesh.get_mass_properties()[1]
tidx = 7

m = 1 # kg
p = np.ones(3) * 0 # lineer momentum
L = np.ones(3) * 0 # acisal momentum
w = np.ones(3) * 0 # acisal hiz
q = np.ones(3) * 0 # durus (orientation)
f0 = np.array([40,20,10])
f1 = mesh.vectors[tidx][0]
a = f1-f0
b = cog-f0
flin = (a.dot(b) / (lin.norm(b)**2))*b
x = cog
S1,S2,N = 0,5,20
dt = (S2-S1) / N
q = euclid.Quaternion(1,0,0,0)
Jbodyinv = lin.inv(mesh.get_mass_properties()[2]*0.1)
F_ext  = f1-f0
tau_ext = np.cross(cog-f1,f1-f0)
#scale_factor = 0.1
#mesh.vectors *= scale_factor

print(f"Force Magnitude: {lin.norm(F_ext)}")
print(f"Lever Arm Magnitude: {lin.norm(f1 - cog)}")
print(f"Initial Torque Magnitude (after correction): {lin.norm(tau_ext)}")
print(f"Moment of Inertia Tensor (Jbody): {mesh.get_mass_properties()[2]}")
print(f"Inverse Moment of Inertia Tensor (Jbodyinv): {Jbodyinv}")

for i,t in enumerate(np.linspace(S1,S2,N)):
    fig, ax = plt.subplots(1, 1, subplot_kw={'projection': '3d'})
    # x ilk degeri cog, x degistikce cog'den ne kadar uzaklasmissa
    # o farki mesh.vectors uzerine eklersek figurde gorulen objeyi
    # o kadar yerinden oynatabiliriz.    
    R = q.get_rotation_matrix_3x3().to_numpy_array()
    currmesh = copy.deepcopy(mesh)
    currmesh.vectors = currmesh.vectors + (x - cog)
    currmesh.rotate_using_matrix(R)
    obj = mplot3d.art3d.Poly3DCollection(currmesh.vectors)
    obj.set_edgecolor('k')
    obj.set_alpha(0.3)
    ax.add_collection3d(obj)
    plot_vector2(ax, f0, f1)
    plot_vector1(ax, f0, flin, color='cyan')
    plot_vector1(ax, cog, tau_ext / 10, color='cyan')
    if t==0:
       # baslangicta p sifir, ve ilk F entegre edilerek ilk p
       # elde ediliyor. Ayni sekilde L.
       p = F_ext*dt
       L = tau_ext*dt
    x = x + dt*(p / m)
    R = q.get_rotation_matrix_3x3().to_numpy_array()
    Jinv = R.dot(Jbodyinv).dot(R.transpose())
    w = L.dot(Jinv)
    wq = euclid.Quaternion(0, w[0], w[1], w[2])
    qdiff = (wq * q).scalar_mul(1/2).scalar_mul(dt)
    q = q.add(qdiff).normalize()
    ax.set_xlabel('x');ax.set_ylabel('y');ax.set_zlabel('z')
    ax.set_xlim(30,70);ax.set_ylim(-10,30); ax.set_zlim(-10,30)
    ax.view_init(elev=20, azim=50)
    plt.savefig('/tmp/img/out-%02d.jpg' % i)
    plt.close(fig)
