from tkinter import Tk, Label, filedialog
import tkinter
#from pandas import DataFrame
from functools import partial

import matplotlib.pyplot as pl
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

import json

import interface_NCorps as NC
import interface_FFT as FFTI
#https://vincent.developpez.com/cours-tutoriels/python/tkinter/apprendre-creer-interface-graphique-tkinter-python-3/


root = tkinter.Tk()
root.wm_title("Projet CODEV n°2")
root.geometry(f'600x400')


def FFT():
    windowFFT = tkinter.Toplevel(root)
    windowFFT.title("Menu : calcul d'une FFT")
    dataFFT = FFTI.DataFFT(windowFFT, root)
        

def NCorps():
    windowNcorps = tkinter.Toplevel(root)
    windowNcorps.title("Menu : calcul d'un problème à N corps")
    data = NC.DataNCorps(windowNcorps, root)
    

bouton_FFT = tkinter.Button(root, text="FFT", command=FFT)
bouton_FFT.pack(expand=1)
bouton_NCorps = tkinter.Button(root, text="N Corps", command=NCorps)
bouton_NCorps.pack(expand=1)


root.mainloop()