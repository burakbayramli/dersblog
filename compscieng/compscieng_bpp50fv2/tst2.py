import numpy as np
import scipy.integrate as integrate
from scipy.optimize import fsolve
import matplotlib.pyplot as plt

# returns the initial condition of the PDE
def initial_condition(z, alpha, beta):
    return alpha + beta*np.sin(z)

# flux function for the conservation law
#	u_t + f(u)_x = 0
#
def flux(u):
    return 0.5*u**2

# Godunov numerical flux
def godunov_flux(um, up):
    fhat = np.zeros((len(um),1))

    for i in range(0,len(um)):
        if (um[i]*up[i]<0.0 and um[i]<=up[i]):
            fhat[i] = 0.0
        elif (um[i]*up[i]<0.0 and um[i]>up[i]):
            fhat[i] = np.fmax(flux(um[i]), flux(up[i]))
        elif (um[i]*up[i]>=0.0 and um[i]<=up[i]):
            fhat[i] = np.fmin(flux(um[i]), flux(up[i]))
        elif (um[i]*up[i]>=0.0 and um[i]>up[i]):
            fhat[i] = np.fmax(flux(um[i]), flux(up[i]))
    return fhat


# specify domain
a = 0
b = 2*np.pi

# initial condition: u(x,0) = alpha + beta*sin(x)
alpha = 0.0
beta  = 1.0

# number of grid points in spatial discretization
N  = 80

# stopping time
T = 1.5

# setup grid points
x = np.linspace(a,b,N)     
dx = (b-a)/(N-1);  

# setup array to store cell averages; due to periodicity, we omit the last cell
u = np.zeros((len(x)-1,1)); 

# compute cell averages at t=0
for i in range(0,N-1):
    u[i] = (1.0/dx)*integrate.quad(initial_condition, x[i], x[i+1], args=(alpha,beta))[0]

# set the time step
dt = dx/(2*np.amax(np.amax(u)))

# this is the main time-stepping loop
t = 0.0
i = 0
while t < T:
    # alpha for the Lax-Friedrichs flux
        A  = np.amax(np.amax(u));

        # compute numerical fluxes fhat_{j+1/2}
        um = u
        up = np.roll(u,-1)
        fR = godunov_flux(um, up) 
        # compute numerical fluxes fhat_{j-1/2} (assuming periodic BCs)
        fL = np.roll(fR,1)
        # first order explicit time-stepping
        u -= dt/dx*(fR - fL)

        # increment time step
        t = t+dt
        i += 1

        if i % 5 == 0:
            plt.figure()
            plt.plot(u)
            plt.savefig('/tmp/out-%02d.png' % i)

