#Question 4

import numpy as np
from matplotlib import pyplot as plt

class Particles:
    def __init__(self,npart=300,xmax=1.0,u=1.0):
        self.x=np.arange(npart)/(0.0+npart)*xmax
        self.u=u*(xmax-self.x)/xmax
        
    def update(self,dt=0.01):
        self.x+=self.u*dt
        
    def my_density(self,dx=0.01):
        xmin=np.min(self.x)
        xmax=np.max(self.x)
        nbin=np.round(1+(xmax-xmin)/dx)
        myind=np.round( (self.x-xmin)/dx)
        rho=np.zeros(nbin)

        assert(myind.max()<nbin) 
        for i in np.arange(0,myind.size):
            rho[myind[i]]+=1.0
        xvec=np.arange(0,nbin)*dx+xmin
        return rho,xvec
        
if __name__=='__main__':
    part=Particles(npart=30000)
    plt.ion()
    plt.plot(part.x)
    plt.show()
    plt.clf()
    
    for ii in range(0,200):
        part.update(dt=0.01)
        rho,x=part.my_density()
        plt.plot(x,rho)
        plt.draw()