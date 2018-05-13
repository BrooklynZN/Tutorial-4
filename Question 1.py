#Question 1

import numpy

def my_sincos_mat(npt=100,order=5):
    xvec=numpy.arange(0,npt)/(0.0+npt)*2*numpy.pi
    mat=numpy.zeros((npt,2*order-1))
    mat[:,0]=1.0
    for j in range(1,order):
        mat[:,2*j-1]=numpy.cos(j*xvec)
        mat[:,2*j]=-numpy.sin(j*xvec)
    return numpy.matrix(mat)

if __name__=='__main__':
    n=100
    order=5
    data=numpy.random.randn(n)
    mat=my_sincos_mat(n,order)
    data=numpy.random.randn(n)
    datft=numpy.fft.fft(data)
    
    data=numpy.matrix(data).transpose()
    fitp=numpy.linalg.inv(mat.transpose()*mat)*(mat.transpose()*data)
    delta=numpy.complex(fitp[5],fitp[6])-datft[3]/(0.5*n)
    print ('error is') + repr(delta)
    
'''sin is an odd function'''