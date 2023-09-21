import numpy as np
from scipy.integrate import quad, trapezoid

class bdecay():

    def __init__(self,tau=1.5,dm=0.5,C=0,S=0.7,omega=0):
        self.tau=tau
        self.dm=dm
        self.C=C
        self.S=S
        self.omega=omega

    def func(self,x,q=+1):
        return (1./(4*self.tau))*np.exp(-np.abs(x)/self.tau)*(1+(q*(1-2*self.omega))*(self.S*np.sin(self.dm*x)-self.C*np.cos(self.dm*x)))

    def pdf(self,x,q=+1):
        # normalized in x-range
        return self.func(x,q)/quad(self.func, x[0], x[-1], args=(q))[0]

    def generate(self, num_samples, xmin, xmax, q=+1, num_points=1000):
        pdf_gen = lambda x: self.pdf(x,q)
        cdf = np.cumsum(pdf_gen(np.linspace(xmin, xmax, num_points)))
        cdf = cdf / cdf[-1]
        uniform_samples = np.random.uniform(0, 1, num_samples)
        return np.interp(uniform_samples, cdf, np.linspace(xmin, xmax, num_points))


class resolution():
    def __init__(self,mean,sigma):
        self.mean=mean
        self.sigma=sigma
    
    def func(self,x):
        return np.exp(-(x-self.mean)**2/(2*self.sigma**2))
    
    def pdf(self,x):
        # normalized in x-range
        return self.func(x)/quad(self.func, x[0], x[-1])[0]
    

class exp_bdecay():

    def __init__(self,bdecay,resolution):
        self.bdecay = bdecay
        self.resolution = resolution

    def func(self,x,q=+1):
        return np.convolve(self.bdecay.pdf(x,q), self.resolution.pdf(x), mode='same') * (x[1] - x[0]) 
    
    def pdf(self,x,q=+1):
        # return self.func(x,q)/quad(self.func, x[0], x[-1], args=(q))[0]
        return self.func(x,q)/trapezoid(self.func(x,q), x)
    
    def generate(self, num_samples, xmin, xmax, q=+1, num_points=1000):
        pdf_gen = lambda x: self.pdf(x,q)
        cdf = np.cumsum(pdf_gen(np.linspace(xmin, xmax, num_points)))
        cdf = cdf / cdf[-1]
        uniform_samples = np.random.uniform(0, 1, num_samples)
        return np.interp(uniform_samples, cdf, np.linspace(xmin, xmax, num_points))
    

class gauss():

    def __init__(self,mean,sigma):
        self.mean = mean
        self.sigma = sigma
    
    def func(self,x):
        return np.exp(-0.5*((x-self.mean)/self.sigma)**2)
    
    def pdf(self,x):
        # normalized in x-range
        return self.func(x)/quad(self.func, x[0], x[-1])[0]
    
    def generate(self, num_samples, xmin, xmax, num_points=1000):
        pdf_gen = lambda x: self.pdf(x)
        cdf = np.cumsum(pdf_gen(np.linspace(xmin, xmax, num_points)))
        cdf = cdf / cdf[-1]
        uniform_samples = np.random.uniform(0, 1, num_samples)
        return np.interp(uniform_samples, cdf, np.linspace(xmin, xmax, num_points))
    
class cball():

    def __init__(self,mean,sigma,alpha,n,tail=+1):
        self.mean = mean
        self.sigma = sigma
        self.alpha = alpha
        self.n = n
        self.A = np.power((self.n/np.abs(self.alpha)),self.n)*np.exp(-0.5*(np.abs(self.alpha)**2))
        self.B = self.n/np.abs(self.alpha)-np.abs(self.alpha)
        self.tail = tail

    def func(self,x):
        return np.where((x-self.mean)/self.sigma<self.tail*self.alpha,np.exp(-0.5*((x-self.mean)/self.sigma)**2),self.A*np.power(self.B + self.tail*(x - self.mean)/self.sigma,-self.n))
    
    def pdf(self,x):
        # normalized in x-range
        return self.func(x)/quad(self.func, x[0], x[-1])[0]
    
    def generate(self, num_samples, xmin, xmax, num_points=1000):
        pdf_gen = lambda x: self.pdf(x)
        cdf = np.cumsum(pdf_gen(np.linspace(xmin, xmax, num_points)))
        cdf = cdf / cdf[-1]
        uniform_samples = np.random.uniform(0, 1, num_samples)
        return np.interp(uniform_samples, cdf, np.linspace(xmin, xmax, num_points))
    
class expo():

    def __init__(self,c):
        self.c = c

    def func(self,x):
        return np.exp(x)
    
    def pdf(self,x):
        return self.func(x)/quad(self.func, x[0], x[-1])[0]
    
    def generate(self, num_samples, xmin, xmax, num_points=1000):
        pdf_gen = lambda x: self.pdf(x)
        cdf = np.cumsum(pdf_gen(np.linspace(xmin, xmax, num_points)))
        cdf = cdf / cdf[-1]
        uniform_samples = np.random.uniform(0, 1, num_samples)
        return np.interp(uniform_samples, cdf, np.linspace(xmin, xmax, num_points))
