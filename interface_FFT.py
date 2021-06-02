import json
import tkinter

import matplotlib.pyplot as pl
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# -*- coding: utf-8 -*-
"""
Created on Tue May  4 18:29:07 2021

@author: Malo
"""

class DataFFT():
    
    def __init__(self, app):
        self.app = app
        #Configuration de la zone du graphique
        self.fig = Figure(figsize=(5, 4), dpi=100)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=app)  # A tk.DrawingArea.
        self.canvas.draw()
        
        self.ax = self.fig.add_subplot(111)#, projection="2d")
        
        #Toolbar configuration for the 3D graph
        toolbar = NavigationToolbar2Tk(self.canvas, app)
        toolbar.update()
        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
        
        
        bouton_getfiles = tkinter.Button(app, text="Importer des données", command=self.getFiles)
        bouton_saveData = tkinter.Button(app, text="Exporter les données dans un fichier", command=self.askSaveData)
        
        #Configuration de la zone de texte
        self.dataText = tkinter.StringVar()
        self.dataLabel = tkinter.Message(app, textvariable = self.dataText)
        
        bouton_getfiles.pack()
        bouton_saveData.pack()
        self.dataLabel.pack()
        
        self.refresh()
    
    def __str__(self):
        res = ""
        for planete in self.planetes:
            res += str(planete) + "\n"
        return res


    #Fonctions des boutons    
    def getFiles(self):
        filename = tkinter.filedialog.askopenfilename()
        self.loadFile(filename)
    
    def askSaveData(self):
        filename = tkinter.filedialog.asksaveasfilename()
        self.saveData(filename)
    
    def saveData(self, filename):
        with open(filename, 'w') as outfile:
            json.dump(self.toJSON(), outfile)
    
    def loadFile(self, filename):
        #chargement du fichier json
        try:
            with open(filename) as json_file:
                data = json.load(json_file)
                for point in data:
                    try:
                        pass
                        #self.planetes.append(Planete(data[planete][0], data[planete][1], data[planete][2], data[planete][3], data[planete][4], data[planete][5], data[planete][6], planete))
                    except KeyError:
                        tkinter.messagebox.showerror("Error", "Error in the file. Please check key for N corps problem in the data file.")
        except FileNotFoundError:
            tkinter.messagebox.showerror("Error", "File not found ! There is an error, please check the path.")
        self.refresh()
        
    def refresh(self):
        #Put the data on the graph
        t = np.arange(0,10,0.1)
        self.ax.plot(t, np.sin(2 * np.pi * t))
        self.canvas.draw()
        
        #Put the parameters on the text block
        # if self.dataText.get() == '':
        #     self.dataText.set("No Planete to show.\n Add a new or import a file with data !")
        # else:
        #     self.dataText.set("\n".join([str(planete) for planete in self.planetes]))