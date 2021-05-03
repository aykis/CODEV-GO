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

from interface_NCorps import *
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

data2= {'masse': [110, 230, 400],
        'x': [1,2,3],
        'y': [3,8,6],
        'z': [21,49,90],
        'nom': ['Pluton', 'Centaure', 'Terre']
        }
with open('data2.txt', 'w') as outfile:
    json.dump(data2, outfile)
    
    
#chargement d'un fichier json
try:
    with open('data2.txt') as json_file:
        data2 = json.load(json_file)
        try:
            for p in data2['masse']:
                print('masse: ' + str(p))
        except KeyError:
            print('KeyError')
except FileNotFoundError:
    print('FileNotFound')


# =============================================================================
# #Affichage d'un plot avec des dataframe et FigureCanvas
# data2 = {'Year': [1920,1930,1940,1950,1960,1970,1980,1990,2000,2010],
#          'Unemployment_Rate': [9.8,12,8,7.2,6.9,7,6.5,6.2,5.5,6.3]
#         }
# df2 = DataFrame(data2,columns=['Year','Unemployment_Rate'])
# 
# #df = data
# figure2 = pl.Figure(figsize=(5,4), dpi=100)
# ax2 = figure2.add_subplot(111)
# line2 = FigureCanvasTkAgg(figure2, root)
# line2.get_tk_widget().pack(side=tkinter.LEFT, fill=tkinter.BOTH)
# df2 = df2[['Year','Unemployment_Rate']].groupby('Year').sum()
# df2.plot(kind='line', legend=True, ax=ax2, color='r',marker='o', fontsize=10)
# ax2.set_title('Year Vs. Unemployment Rate')
# =============================================================================


#____________________________________________________________

def file_handling(filename):
    try:
        with open(filename) as json_file:
            data = json.load(json_file)
            try:
                for p in data:
                    print(str(p) + str(data[p]))
            except KeyError:
                print('KeyError')
    except FileNotFoundError:
        print('FileNotFound')

#Recherche de fichier
def buttonGetFile(app, filename):
    def GetFiles(filename):
        filename = filedialog.askopenfilename()
        if filename:
            try:
                print("""here it comes: self.settings["template"].set(filename)""")
            except:                     # <- naked except is a bad idea
                tkinter.showerror("Open Source File", "Failed to read file\n'%s'" % filename)
        file_handling(filename)
    bouton_getfiles = tkinter.Button(app, text="Get Files", command=partial(GetFiles, filename))
    bouton_getfiles.pack(fill=tkinter.X)
    #return filename



def FFT():
    windowFFT = tkinter.Toplevel(root)
    windowFFT.title("Menu calcul d'une FFT")
    buttonGetFile(windowFFT)
    data()
            
        
# =============================================================================
# def data(app):
#     data2 = {'Year': [1920,1930,1940,1950,1960,1970,1980,1990,2000,2010],
#              'Unemployment_Rate': [9.8,12,8,7.2,6.9,7,6.5,6.2,5.5,6.3]
#             }
#     df2 = DataFrame(data2,columns=['Year','Unemployment_Rate'])
#     
#     #df = data
#     figure2 = pl.Figure(figsize=(5,4), dpi=100)
#     ax2 = figure2.add_subplot(111)
#     line2 = FigureCanvasTkAgg(figure2, app)
#     line2.get_tk_widget().pack(side=tkinter.LEFT, fill=tkinter.BOTH)
#     df2 = df2[['Year','Unemployment_Rate']].groupby('Year').sum()
#     df2.plot(kind='line', legend=True, ax=ax2, color='r',marker='o', fontsize=10)
#     ax2.set_title('Year Vs. Unemployment Rate')
# =============================================================================
    
    
    
def NCorps():
    windowNcorps = tkinter.Toplevel(root)
    windowNcorps.title("Menu : calcul d'un problème à N corps")
    buttonGetFile(windowNcorps)
    # filename=""
    # def GetFiles(filename):
    #     filename = filedialog.askopenfilename()
    # bouton_getfiles = tkinter.Button(windowNcorps, text="Get Files", command=partial(GetFiles, filename))
    # bouton_getfiles.pack()
    graph3DExemple(windowNcorps)
    #print(filename)
 
 
# bouton_getfiles = tkinter.Button(root, text="Get Files", command=GetFiles)
# bouton_getfiles.pack()

bouton_FFT = tkinter.Button(root, text="FFT", command=FFT)
bouton_FFT.pack()
bouton_NCorps = tkinter.Button(root, text="N Corps", command=NCorps)
bouton_NCorps.pack()


root.mainloop() # Lancement de la boucle principale