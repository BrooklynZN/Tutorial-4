#Question 2 and Bonus 

import numpy as np
from matplotlib import pylab as plt

def simulate_gaussian(t,sig=0.5,amp=1,cent=0):
    dat=np.exp(-0.5*(t-cent)**2/sig**2)*amp
    dat+=np.random.randn(t.size)
    return dat

def get_trial_offset(sigs):
    return sigs*np.random.randn(sigs.size)

class Gaussian:
    def __init__(self,t,sig=0.5,amp=1.0,cent=0,offset=0):
        self.t=t
        self.y=simulate_gaussian(t,sig,amp,cent)+offset
        self.err=np.ones(t.size)
        self.sig=sig
        self.amp=amp
        self.cent=cent
        self.offset=offset

    def get_chisq(self,vec):
        sig=vec[0]
        amp=vec[1]
        cent=vec[2]
        off=vec[3]

        pred=off+amp*np.exp(-0.5*(self.t-cent)**2/sig**2)
        chisq=np.sum(  (self.y-pred)**2/self.err**2)
        return chisq
				
class Lorentzian:
    def get_y(self):
        tmp=1+((self.t-self.cent)/self.sig)**2
        self.y=self.offset+self.amp/tmp

    def __init__(self,t,sig=0.5,amp=1.0,cent=0,offset=0):
        self.t=t
        self.err=np.ones(t.size)
        self.sig=sig
        self.amp=amp
        self.cent=cent
        self.offset=offset
        self.get_y()
        self.y+=np.random.randn(t.size)
    def get_chisq(self,vec):
        sig=vec[0]
        amp=vec[1]
        cent=vec[2]
        offset=vec[3]
        tmp=1+((self.t-cent)/sig)**2
        pred=offset+amp/tmp
        chisq=np.sum( (self.y-pred)**2/self.err**2)
        return chisq

def run_mcmc(data,start_pos,nstep,scale=None):
    nparam=start_pos.size
    params=np.zeros([nstep,nparam+1])
    params[0,0:-1]=start_pos
    cur_chisq=data.get_chisq(start_pos)
    cur_pos=start_pos.copy()
    if scale==None:
        scale=np.ones(nparam)
    for i in range(1,nstep):
        new_pos=cur_pos+get_trial_offset(scale)
        new_chisq=data.get_chisq(new_pos)
        if new_chisq<cur_chisq:
            accept=True
        else:
            delt=new_chisq-cur_chisq
            prob=np.exp(-0.5*delt)
            if np.random.rand()<prob:
                accept=True
            else:
                accept=False
        if accept: 
            cur_pos=new_pos
            cur_chisq=new_chisq
        params[i,0:-1]=cur_pos
        params[i,-1]=cur_chisq
    return params


if __name__=='__main__':
    plt.ion()
    t=np.arange(-5,5,0.01)
    
    dat=Lorentzian(t,amp=5.0)
    
    guess=np.array([0.3,1.2,0.3,-0.2])
    scale=np.array([0.1,0.1,0.1,0.1])
    nstep=100000
    chain=run_mcmc(dat,guess,nstep,scale)
    nn=np.round(0.2*nstep)
    chain=chain[nn:,:]
    param_true=np.array([dat.sig,dat.amp,dat.cent,dat.offset])
    for i in range(0,param_true.size):
        val=np.mean(chain[:,i])
        scat=np.std(chain[:,i])
        print [param_true[i],val,scat]