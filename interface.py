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
#https://vincent.developpez.com/cours-tutoriels/python/tkinter/apprendre-creer-interface-graphique-tkinter-python-3/


#______________________________________________

root = tkinter.Tk()
root.wm_title("Projet CODEV n°2")

def graph3DExemple(app):
    #Configuration de la zone du graphique
    fig = Figure(figsize=(5, 4), dpi=100)
    
    canvas = FigureCanvasTkAgg(fig, master=app)  # A tk.DrawingArea.
    canvas.draw()
    
    
    #Put the data on the graph
    ax = fig.add_subplot(111, projection="3d")
    t = np.arange(0, 3, .01)
    ax.plot(t, 2 * np.sin(2 * np.pi * t))
    
    
    #Toolbar configuration for the 3D graph
    toolbar = NavigationToolbar2Tk(canvas, app)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)


#______________________________________________


#Ecriture d'un fichier json
#data2 = {'Year': [1920,1930,1940,1950,1960,1970,1980,1990,2000,2010],
#         'Unemployment_Rate': [9.8,12,8,7.2,6.9,7,6.5,6.2,5.5,6.3]
#        }

#=============================================================================
# data2= {'masse': [110, 230, 400],
#         'x': [1,2,3],
#         'y': [3,8,6],
#         'z': [21,49,90],
#         'nom': ['Pluton', 'Centaure', 'Terre']
#         }

# data2 = {'Pluton':[110,1,3,21],
#          'Centaure':[230,2,8,49],
#          'Terre':[400,3,6,90]
#     }
# with open('data2.txt', 'w') as outfile:
#     json.dump(data2, outfile)
    
    
# #chargement d'un fichier json
# try:
#     with open('data2.txt') as json_file:
#         data2 = json.load(json_file)
#         try:
#             for p in data2['masse']:
#                 print('masse: ' + str(p))
#         except KeyError:
#             print('KeyError')
# except FileNotFoundError:
#     print('FileNotFound')
#=============================================================================


def FFT():
    windowFFT = tkinter.Toplevel(root)
    windowFFT.title("Menu calcul d'une FFT")
    buttonGetFile(windowFFT)
        

def NCorps():
    windowNcorps = tkinter.Toplevel(root)
    windowNcorps.title("Menu : calcul d'un problème à N corps")
    data = NC.DataNCorps(windowNcorps)
    
    


bouton_FFT = tkinter.Button(root, text="FFT", command=FFT)
bouton_FFT.pack()
bouton_NCorps = tkinter.Button(root, text="N Corps", command=NCorps)
bouton_NCorps.pack()


root.mainloop()