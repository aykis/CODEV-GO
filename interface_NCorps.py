import json
import tkinter

import matplotlib.pyplot as pl
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# -*- coding: utf-8 -*-
"""
Created on Tue May  4 01:17:23 2021

@author: Malo
"""

class Planete():
    nom=""
    masse=0
    x=0
    y=0
    z=0
    def __init__(self, masse, x, y, z, nom = ""):
        self.nom=nom
        self.masse=masse
        self.x=x
        self.y=y
        self.z=z
    
    def __str__(self):
        return "{0} : masse = {1}, (x,y,z) = ({2}, {3}, {4})".format(self.nom, self.masse, self.x, self.y, self.z)
    
    def getPosition(self):
        return [self.x,self.y,self.z]
        
class DataNCorps():
    planetes = []
    
    def __init__(self, app):
        #Configuration de la zone du graphique
        self.fig = Figure(figsize=(5, 4), dpi=100)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=app)  # A tk.DrawingArea.
        self.canvas.draw()
        
        self.ax = self.fig.add_subplot(111, projection="3d")
        
        #Toolbar configuration for the 3D graph
        toolbar = NavigationToolbar2Tk(self.canvas, app)
        toolbar.update()
        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
        
        
        bouton_getfiles = tkinter.Button(app, text="Get Files", command=self.GetFiles)
        
        #Configuration de la zone de texte
        self.dataText = tkinter.StringVar(value = "No Planete to show")
        self.dataLabel = tkinter.Message(app, textvariable = self.dataText)
        
        bouton_getfiles.pack()
        self.dataLabel.pack()
        
        self.refresh()
        
    def __str__(self):
        res = ""
        for planete in self.planetes:
            res += str(planete) + "\n"
        return res
        
    def GetFiles(self):
        filename = tkinter.filedialog.askopenfilename()
        self.loadFile(filename)
    
    def loadFile(self, filename):

        #chargement du fichier json
        try:
            with open(filename) as json_file:
                data = json.load(json_file)
                for planete in data:
                    try:
                        self.planetes.append(Planete(data[planete][0], data[planete][1], data[planete][2], data[planete][3], planete))
                    except KeyError:
                        tkinter.messagebox.showerror("Error", "Error in the file. Please check key for N corps problem in the data file.")
        except FileNotFoundError:
            tkinter.messagebox.showerror("Error", "File not found ! There is an error, please check the path.")
        self.refresh()
            
    def addPlanete(self, planete):
        self.planetes.append(planete)
    
    def get(self, axis):
        #axis = 0 : x; 1 : y; 2 : z
        res = []
        for planete in self.planetes:
            res.append(planete.getPosition()[axis])
        return res
    
    def refresh(self):
        #Put the data on the graph
        #ax = self.fig.add_subplot(111, projection="3d")
        x = self.get(0)
        y = self.get(1)
        z = self.get(2)
        
        self.ax.scatter(x, y, z)
        self.canvas.draw()
        
        #Put the data on the text block
        self.dataText.set("\n".join([str(planete) for planete in self.planetes]))