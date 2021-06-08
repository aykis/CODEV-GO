import json
import tkinter

import matplotlib.pyplot as pl
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import os

# -*- coding: utf-8 -*-
"""
Created on Tue May  4 18:29:07 2021

@author: Malo
"""

class Signal():
    #pas = pas de temps, échantillonnage
    #int n = len(Y) #nombre d'échantillonage
    # t = [pas*i for i in range(n)]
    Y = [] #amplitude du signal
    
    
    def __init__(self, pas, Y):
        self.pas = pas
        self.Y = list.copy(Y)
    
    def getY(self):
        return self.Y
    
    def setFreq(self, freq):
        self.freq = freq
    
    def getFreq(self, t):
        return self.freq[t]

    def getN(self):
        return len(self.Y)
    
    def getFinalTime(self):
        return self.pas*len(self.Y)
    
    def getTime(self):
        return [self.pas*i for i in range(len(self.Y))]
    
    def getPas(self):
        return self.pas;
    
    def addAmplitude(self, toAdd):
        if isinstance(toAdd, list):
            self.Y = self.Y + toAdd
        else:
            self.Y.append(toAdd)
        

class DataFFT():
    
    def __init__(self, app, root):
        self.app = app
        self.root = root
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
        #bouton_saveData = tkinter.Button(app, text="Exporter les données dans un fichier", command=self.askSaveData)
        bouton_askResult = tkinter.Button(app, text="Afficher un résultat", command=self.askResult)
        bouton_execute = tkinter.Button(app, text="Executer un script FFT", command=self.execute)
        
        #Configuration de la zone de texte
        self.dataText = tkinter.StringVar()
        self.dataLabel = tkinter.Message(app, textvariable = self.dataText)
        
        bouton_getfiles.pack()
        #bouton_saveData.pack()
        bouton_askResult.pack()
        bouton_execute.pack()
        self.dataLabel.pack()
        
        self.refresh()
    
    def __str__(self):
        res = ""
        for planete in self.planetes:
            res += str(planete) + "\n"
        return res


    #Fonctions des boutons    
    def getFiles(self):
        self.filename = tkinter.filedialog.askopenfilename()
        self.loadFile(self.filename)
    
    def askSaveData(self):
        self.filename = tkinter.filedialog.asksaveasfilename()
        self.saveData(self.filename)
    
    def saveData(self, filename):
        with open(filename, 'w') as outfile:
            json.dump(self.toJSON(), outfile)
            
    def askResult(self):
        self.filename = tkinter.filedialog.askopenfilename()
        
        windowFFTResult = tkinter.Toplevel(self.root)
        windowFFTResult.title("Résulat : transformation de Fourier / {0}".format(self.filename))
        result = Result(windowFFTResult, self.filename)
    
    def execute(self):
        filenameFFT = tkinter.filedialog.askopenfilename()
        self.runGo(filenameFFT, self.filename)
    
    def runGo(self, filenameFFT, filenameRes):
        print(os.system("go run " + filenameFFT + filenameRes))
    
    def loadFile(self, filename):
        #chargement du fichier json
        try:
            with open(filename) as json_file:
                file = json.load(json_file)
                for cle in file:
                    if cle == "Y": Y = file[cle]
                    elif cle == "pas" : pas = file[cle]
                    elif cle == "Temps" : self.tps = file[cle]
                    elif cle == "nombreCoeur" : self.nbCoeur = file[cle]
                self.signal = Signal(pas, Y)
        except FileNotFoundError:
            tkinter.messagebox.showerror("Error", "File not found ! There is an error, please check the path.")
        self.refresh()
        
    def refresh(self):
        #Put the data on the graph
        t = np.arange(0, self.signal.getFinalTime(), self.signal.getPas())
        self.ax.plot(t, self.signal.getY())
        self.canvas.draw()
        
class Result():
    
    def __init__(self, app, filename):
        self.fig = Figure(figsize=(5, 4), dpi=100)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=app)
        self.canvas.draw()
        
        self.ax = self.fig.add_subplot(111)
        
        #Toolbar configuration for the 3D graph
        toolbar = NavigationToolbar2Tk(self.canvas, app)
        toolbar.update()
        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
        
        self.loadData(filename)
        
        self.w = tkinter.Scale(app, from_=0, to=self.signal.getN(), orient = tkinter.HORIZONTAL)
        self.w.pack()
        
        self.refresh()
     
    def loadData(self, filename):
        #chargement du fichier json
        try:
            with open(filename) as json_file:
                file = json.load(json_file)
                for cle in file:
                    if cle == "Y": Y = file[cle]
                    elif cle == "pas" : pas = file[cle]
                    elif cle == "Temps" : tps = file[cle]
                    elif cle == "nombreCoeur" : nbCoeur = file[cle]
                self.signal = Signal(pas, Y)
                self.signal.setTemps(tps)
                self.signal.setCoeur(nbCoeur)
        except FileNotFoundError:
            tkinter.messagebox.showerror("Error", "File not found ! There is an error, please check the path.")
        self.refresh()
            
    def refresh(self):
        #Put the data on the graph
        t = np.arange(0, self.signal.getFinalTime(), self.signal.getPas())
        self.ax.plot(t, self.signal.getY())
        self.ax.plot(t, self.signal.getFreq(self.w.get()))
        self.canvas.draw()

