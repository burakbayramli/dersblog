# convert -delay 20 -loop 0 /tmp/out-*.png wave.gif
import scipy.integrate as integrate
import matplotlib.pyplot as plt
import numpy as np

def init(z, alpha, beta):
    return alpha + beta*np.sin(z)

# akis fonksiyonu 
#	u_t + f(u)_x = 0
#
def flux(u):
    return 0.5*u**2

def godunov_flux(um):
    fhat = np.zeros((len(um),1))

    for i in range(0,len(um)-1):
        wl = um[i]; wr = um[i+1]

        if (wl*wr<0.0 and wl<=wr):
            fhat[i] = 0.0
        elif (wl*wr<0.0 and wl>wr):
            fhat[i] = np.fmax(flux(wl), flux(wr))
        elif (wl*wr>=0.0 and wl<=wr):
            fhat[i] = np.fmin(flux(wl), flux(wr))
        elif (wl*wr>=0.0 and wl>wr):
            fhat[i] = np.fmax(flux(wl), flux(wr))

    return fhat
            
"""        
        s=(wl+wr)/2;
        if wl > wr:
            if s < 0: fhat[i] = flux(wr)
        elif wl < wr:
            if wr < 0: fhat[i] = flux(wr)
            elif wl > 0.:
                fhat[i] = flux(wl)
            else:
                fhat[i] = 0
"""

        
        

a = 0
b = 2*np.pi

alpha = 0.0
beta  = 1.0

N  = 80
T = 2.0

x = np.linspace(a,b,N)     
dx = (b-a)/(N-1);  

u = np.zeros((len(x)-1,1)); 

for i in range(0,N-1):
    u[i] = (1.0/dx)*integrate.quad(init, x[i], x[i+1], args=(alpha,beta))[0]

dt = dx/(2*np.amax(np.amax(u)))

t = 0.0
i = 0
while t < T:
    um = u
    fR = godunov_flux(um) 
    fL = np.roll(fR,1)
    u -= dt/dx*(fR - fL)
    t = t+dt
    i += 1

    if i % 5 == 0:
        plt.figure()
        plt.plot(u)
        plt.ylim(-1,1)
        plt.savefig('/tmp/out-%03d.png' % i)
        plt.close('all')
