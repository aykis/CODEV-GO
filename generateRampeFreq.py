# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 21:03:25 2021

@author: Malo
"""
import json
import numpy as np
import matplotlib.pyplot as plt
import cmath as cm
from scipy import signal

# paramètres du signal
L = 20.0             # durée du signal
fd = 1.0/L          # domaine fréquentiel du signal
a0 = 1.             # amplitude du signal
f0 = 1.0            # fréquence du signal
# paramètres de l'échantillonnage
N = 2048*64           # nombre de points d'échantillonnage
dt = L/N            # intervalle temporel entre deux points
fe = 1./dt          # fréquence d'échantillonnage
# construction du signal
t = np.linspace(0.0,L,N)

w = signal.chirp(t, f0=1, f1=10, t1=20, method='linear')
plt.plot(t, w)
plt.title("Linear Chirp, f(0)=1, f(10)=10")
plt.xlabel('t (sec)')
plt.show()

def toJSON():
    jsonDict = {}
    jsonDict["Y"] = list(w)
    jsonDict["pas"] = dt
    return jsonDict

with open('rampeFreq.json', 'w') as outfile:
    json.dump(toJSON(), outfile)
    
    
    