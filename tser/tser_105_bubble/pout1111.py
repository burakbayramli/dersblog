
import numpy as np
import matplotlib.pyplot as plt

import statsmodels.tsa.stattools as st
import pandas as pd, zipfile
with zipfile.ZipFile('data.zip', 'r') as z:
    dfj =  pd.read_csv(z.open('djia.csv'),index_col='Date',parse_dates=True)
    dfs =  pd.read_csv(z.open('sp500.csv'),index_col='Date',parse_dates=True)
    dfi =  pd.read_csv(z.open('ibb.csv'),index_col='Date',parse_dates=True)

dfj['Adj Close'].plot()
plt.plot()
plt.savefig('tser_bubble_01.png')

import pandas as pd
from lmfit import Parameters, minimize
from lmfit.printfuncs import report_fit

def init_fit(min, max, init):
    fit_params = Parameters()
    fit_params.add('tc', value=init, max=max, min=min)
    fit_params.add('A', value=2.0, max=10.0, min=0.1)
    fit_params.add('m', value=0.5, max=1.0, min=0.01)
    fit_params.add('C', value=0.0, max=2.0, min=-2)
    fit_params.add('beta', value=0.5, max=1.0, min=0.1)
    fit_params.add('omega', value=20., max=40.0, min=0.1)
    fit_params.add('phi', value=np.pi, max=2*np.pi, min=0.1)
    return fit_params

def f(pars,x):
    tc = pars['tc'].value
    A = pars['A'].value
    m = pars['m'].value
    C = pars['C'].value
    beta = pars['beta'].value
    omega = pars['omega'].value
    phi = pars['phi'].value
    tmp1 = (1 + C*np.cos(omega*np.log(tc-x) + phi))
    model = A - ((m*((tc-x)**beta))*tmp1)
    return model
    
def residual(pars,y,t):
    return y-f(pars,t)

fit_params = init_fit(1922.0,1940.,1939)

dfj = dfj[(dfj.index >= '1922-01-01')&(dfj.index <= '1929-01-01')]
dfj['DecDate'] = np.linspace(1922,1929,len(dfj))

y = np.log(dfj['Adj Close'])
t = dfj['DecDate']
out = minimize(residual, fit_params, args=(y,t,))

report_fit(fit_params)

res = list(st.adfuller(out.residual,maxlag=1))
print (res[0], '%1,%5,%10', res[4]['1%'], res[4]['5%'], res[4]['10%'])

dfj['Sornette'] = np.exp(f(fit_params, dfj.DecDate))
dfj[['Adj Close','Sornette']].plot()
plt.savefig('tser_bubble_04.png')

fit_params2 = init_fit(1922.0,1940.,1939.)
dfj2 = dfj[:-600] # son iki sene verisini attik
y2 = np.log(dfj2['Adj Close'])
t2 = dfj2['DecDate']
out2 = minimize(residual, fit_params2, args=(y2,t2,))
res2 = list(st.adfuller(out2.residual,maxlag=1))
print (res2[0], '%1,%5,%10', res[4]['1%'], res[4]['5%'], res[4]['10%'])

print (fit_params2['tc'].value )

dfs['Adj Close'].plot()
plt.savefig('tser_bubble_02.png')

dfs = dfs[(dfs.index < '1987-10-18')] # kara ptesi oncesini al
beg_date = dfs.head(1).index[0].timetuple()
beg_date_dec = beg_date.tm_year + (beg_date.tm_yday / 367.)
end_date = dfs.tail(1).index[0].timetuple()
end_date_dec = end_date.tm_year + (end_date.tm_yday / 367.)
dfs['DecDate'] = np.linspace(beg_date_dec,end_date_dec,len(dfs))

fit_params3 = init_fit(1970.,1995.,1989.)
y3 = np.log(dfs['Adj Close'])
t3 = dfs['DecDate']
out3 = minimize(residual, fit_params3, args=(y3,t3,))
report_fit(fit_params3)

res3 = list(st.adfuller(out3.residual,maxlag=1))
print (res3[0], '%1,%5,%10', res[4]['1%'], res[4]['5%'], res[4]['10%'])

dfi['Adj Close'].plot()
plt.savefig('tser_bubble_03.png')

dfi = dfi[(dfi.index < '2015-07-01')] 
beg_date = dfi.head(1).index[0].timetuple()
beg_date_dec = beg_date.tm_year + (beg_date.tm_yday / 367.)
end_date = dfi.tail(1).index[0].timetuple()
end_date_dec = end_date.tm_year + (end_date.tm_yday / 367.)
dfi['DecDate'] = np.linspace(beg_date_dec,end_date_dec,len(dfi))

fit_params4 = init_fit(2012.,2018.,2017.)
y4 = np.log(dfi['Adj Close'])
t4 = dfi['DecDate']
out4 = minimize(residual, fit_params4, args=(y4,t4,))
print (fit_params4['tc'].value )

res4 = list(st.adfuller(out4.residual,maxlag=1))
print (res4[0], '%1,%5,%10', res[4]['1%'], res[4]['5%'], res[4]['10%'])

import pandas as pd
dfpop = pd.read_csv('wpop.csv',comment='#',sep='\\s',engine='python')
dfpop = dfpop[(dfpop['Year'] >= 0) & (dfpop['Year'] <= 1998)]

import pandas as pd
import statsmodels.tsa.stattools as st
from lmfit import Parameters, minimize
from lmfit.printfuncs import report_fit

def f(pars,t):
    tc = pars['tc'].value
    z = pars['z'].value
    A = pars['A'].value
    B = pars['B'].value
    model = A + B*((tc - t)**z)
    return model
    
def residual(pars,y,t):
    return y-f(pars,t)

fit_params = Parameters()
fit_params.add('tc', value=2100.0, min=2000.,max=2400.)
fit_params.add('z', value=-1., min=-5.0,max=5.0)
fit_params.add('A', value=0., min=0.0, max=10.0)
fit_params.add('B', value=20*1000., min=0.0,max=30*1000.0)
y = np.log(np.array(dfpop.Population.astype(float)))
t = np.array(dfpop.Year.astype(float))
out = minimize(residual, fit_params, args=(y,t,))
report_fit(fit_params)
res = list(st.adfuller(out.residual,maxlag=1))
print ('ADF testi', res[0], '%1,%5,%10', res[4]['1%'], res[4]['5%'], res[4]['10%'])

import pandas as pd
dfgdp = pd.read_csv('wgdpreal.csv',comment='#',sep='\\s',engine='python')
dfgdp = dfgdp[(dfgdp['Year'] >= 0) & (dfgdp['Year'] <= 1998)]

fit_params = Parameters()
fit_params.add('tc', value=2100.0, min=2000.,max=2400.)
fit_params.add('z', value=-1., min=-5.0,max=5.0)
fit_params.add('A', value=0., min=0.0, max=10.0)
fit_params.add('B', value=20*1000., min=0.0,max=30*1000.0)
y = np.log(np.array(dfgdp.GDPPC.astype(float)))
t = np.array(dfgdp.Year.astype(float))
out = minimize(residual, fit_params, args=(y,t,))
report_fit(fit_params)
res = list(st.adfuller(out.residual,maxlag=1))
print ('ADF testi', res[0], '%1-%10', res[4]['1%'], res[4]['5%'], res[4]['10%'])
