import json
import os
import tkinter

import matplotlib.pyplot as pl
from matplotlib.figure import Figure
import matplotlib.animation as animation
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
    t=0
    
    def __init__(self, masse, x, y, z, vx, vy, vz, nom = ""):
        self.x=[]
        self.y=[]
        self.z=[]
        self.x=[]
        self.y=[]
        self.z=[]
        self.vx=[]
        self.vy=[]
        self.vz=[]
        self.nom=nom
        self.masse=masse
        if isinstance(x, list):
            self.x = x.copy()
            self.y = y.copy()
            self.z = z.copy()
        else:
            self.x.append(x)
            self.y.append(y)
            self.z.append(z)
        if isinstance(vx, list):
            self.vx = vx.copy()
            self.vy = vy.copy()
            self.vz = vz.copy()
        else:
            self.vx.append(vx)
            self.vy.append(vy)
            self.vz.append(vz)
    
    def __str__(self):
        return "{0} : masse = {1}, (x,y,z) = ({2}, {3}, {4}), v(x, y, z) = ({5}, {6}, {7})".format(self.nom, self.masse, self.x[self.t], self.y[self.t], self.z[self.t], self.vx[self.t], self.vy[self.t], self.vz[self.t])
    
    def setTemps(self, tps):
        self.tps = tps
    def getTemps(self):
        return self.tps
    def setCoeur(self, cr):
        self.nbCoeur = cr
    def getCoeur(self):
        return self.nbCoeur
    
    
    def next(self):
        toadd = 60*6
        if self.t + toadd < len(self.x):
            self.t+=toadd
        else:
            self.t=0
        
    def getPosition(self, i=None):
        i = self.t if i==None else i
        return [self.x[i],self.y[i],self.z[i]]
    
    def getVitesse(self, i=None):
        i = self.t if i==None else i
        return [self.vx[i],self.vy[i],self.vz[i]]
    
    def addPosition(self, x, y, z):
        self.x.append(x)
        self.y.append(y)
        self.z.append(z)
    
    def getName(self):
        return self.nom
    
    def getMasse(self):
        return self.masse
        
class DataNCorps():
    planetes = []
    
    def __init__(self, app, root):
        self.app = app
        self.root = root
        #Configuration de la zone du graphique
        self.fig = Figure(figsize=(5, 4), dpi=100)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=app)  # A tk.DrawingArea.
        self.canvas.draw()
        
        self.ax = self.fig.add_subplot(111, projection="3d")
        
        #Toolbar configuration for the 3D graph
        toolbar = NavigationToolbar2Tk(self.canvas, app)
        toolbar.update()
        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
        
        
        bouton_getfiles = tkinter.Button(app, text="Importer des données", command=self.getFiles)
        bouton_newPlanete = tkinter.Button(app, text="Ajouter un corps", command=self.addPlanete)
        bouton_saveData = tkinter.Button(app, text="Exporter les données dans un fichier", command=self.askSaveData)
        bouton_resultat = tkinter.Button(app, text="Afficher un résultat", command=self.askResult)
        bouton_executer = tkinter.Button(app, text="Executer une résolution N-corps", command=self.executer)
        
        #Configuration de la zone de texte
        self.dataText = tkinter.StringVar()
        self.dataLabel = tkinter.Label(app, textvariable = self.dataText, width=150)
        #self.dataLabel.pack(fill=tkinter.BOTH)
        
        bouton_getfiles.pack(expand=1)
        bouton_newPlanete.pack(expand=1)
        bouton_saveData.pack(expand=1)
        bouton_resultat.pack(expand=1)
        bouton_executer.pack(expand=1)
        self.dataLabel.pack(expand=1,fill=tkinter.BOTH)
        
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
    
    def addPlanete(self):
        newForm = FormNewPlanete(title="Ajouter une planète", parent=self.app)
        self.planetes.append(newForm.constructPlanete())
        self.refresh()
    
    def askSaveData(self):
        filename = tkinter.filedialog.asksaveasfilename()
        self.saveData(filename)
    
    def saveData(self, filename):
        with open(filename, 'w') as outfile:
            json.dump(self.toJSON(), outfile)
    
    def askResult(self):
        filename = tkinter.filedialog.askopenfilename()
        
        windowNcorpsResult = tkinter.Toplevel(self.root)
        windowNcorpsResult.title("Résulat : calcul d'un problème à N corps / {0}".format(filename))
        result = Result(windowNcorpsResult, filename)
    
    def executer(self):
        filenameFFT = tkinter.filedialog.askopenfilename()
        self.runGo(filenameFFT, self.filename)
    
    def runGo(self, filenameFFT, filenameRes):
        print(os.system("go run " + filenameFFT + filenameRes))
    
    def loadFile(self, filename):

        #chargement du fichier json
        try:
            with open(filename) as json_file:
                data = json.load(json_file)
                for cle in data:
                    if cle == "Temps" : self.planetes.setTemps(data[cle])
                    elif cle == "nombreCoeur" : self.planetes.setCoeur(data[cle])
                    else:
                        try:
                            self.planetes.append(Planete(data[cle][0], data[cle][1], data[cle][2], data[cle][3], data[cle][4], data[cle][5], data[cle][6], cle))
                        except KeyError:
                            tkinter.messagebox.showerror("Error", "Error in the file. Please check key for N corps problem in the data file.")
        except FileNotFoundError:
            tkinter.messagebox.showerror("Error", "File not found ! There is an error, please check the path.")
        self.refresh()
    
    def getPosition(self, axis):
        #axis = 0 : x; 1 : y; 2 : z
        res = []
        for planete in self.planetes:
            res.append(planete.getPosition()[axis])
        return res
    
    def getVitesse(self, axis):
        #axis = 0 : x; 1 : y; 2 : z
        res = []
        for planete in self.planetes:
            res.append(planete.getVitesse()[axis])
        return res
    
    def refresh(self):
        #Put the data on the graph
        #ax = self.fig.add_subplot(111, projection="3d")
        x = self.getPosition(0)
        y = self.getPosition(1)
        z = self.getPosition(2)
        
        # vx = self.getVitesse(0)
        # vy = self.getVitesse(1)
        # vz = self.getVitesse(2)
        
        self.ax.scatter(x, y, z)
        self.canvas.draw()
        
        #Put the data on the text block
        if self.dataText.get() == '':
            self.dataText.set("No Planete to show.\n Add a new or import a file with data !")
        else:
            self.dataText.set("\n".join([str(planete) for planete in self.planetes]))
    
    def toJSON(self):
        jsonDict = {}
        def addPlanete(planete, copy=0):
            if copy == 0 and planete.getName() not in jsonDict:
                jsonDict[planete.getName()] = [planete.getMasse()] + planete.getPosition() + planete.getVitesse()
            elif copy !=0 and planete.getName() + " ({0})".format(copy) not in jsonDict:
                jsonDict[planete.getName() + " ({0})".format(copy)] = [planete.getMasse()] + planete.getPosition() + planete.getVitesse()
            else:
                addPlanete(planete, copy=copy+1)
                
        for planete in self.planetes:
            addPlanete(planete)
        return jsonDict



#===============================================================


class Result():
    planetes = []
    
    def __init__(self, app, filename):
        self.app = app
        #Configuration de la zone du graphique
        self.fig = Figure(figsize=(5, 4), dpi=100)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=app)  # A tk.DrawingArea.
        self.canvas.draw()
        
        self.ax = self.fig.add_subplot(111, projection="3d")
        
        
        self.ax.axis(xmin = -1.5e11, xmax=1.5e11, ymin=-1.5e11, ymax=1.5e11)
        
        
        #Toolbar configuration for the 3D graph
        toolbar = NavigationToolbar2Tk(self.canvas, app)
        toolbar.update()
        self.canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)
        
        self.filename = filename
        self.loadData(filename)
        
        print(self.tps)
        
        self.pos = self.ax.scatter([0], [0], [0])
        
        
        self.dataText = tkinter.StringVar()
        self.dataLabel = tkinter.Label(app, textvariable = self.dataText, width=150)
    
    
        self.dataLabel.pack()
        
        self.app.after(40, self.refresh())
        
        #self.refresh()
        
    
    def animate(self, i):
        self.refresh(i)
        #x = getPosition(0, i)
        #y = np.cos(k*x - w*t)
        #line.set_data(x, y, z)
        #self.ax.scatter(x, y, z)
        self.canvas.draw()
    
    def getPosition(self, axis):
        #axis = 0 : x; 1 : y; 2 : z
        res = []
        for planete in self.planetes:
            res.append(planete.getPosition()[axis])
        return res
     
    def loadData(self, filename):
        #chargement du fichier json
        try:
            with open(filename) as json_file:
                data = json.load(json_file)
                for cle in data:
                    if cle == "Temps" : self.tps = data[cle]
                    elif cle == "nombreCoeur" : self.coeur = data[cle]
                    else:
                        x = []
                        y = []
                        z = []
                        for pos in data[cle]:
                            x.append(pos[0])
                            y.append(pos[1])
                            z.append(pos[2])
                        try:
                            self.planetes.append(Planete(0, x, y, z, 0, 0, 0, cle))
                        except KeyError:
                            tkinter.messagebox.showerror("Error", "Error in the file. Please check key for N corps problem in the data file.")
        except FileNotFoundError:
            tkinter.messagebox.showerror("Error", "File not found ! There is an error, please check the path.")
        
    def refresh(self, i=0):
        #Put the data on the graph
        #ax = self.fig.add_subplot(111, projection="3d")
        x = self.getPosition(0)
        y = self.getPosition(1)
        z = self.getPosition(2)
        for planete in self.planetes:
            planete.next()
        
        #self.canvas.delete
        #self.pos = self.ax.scatter(x, y, z)
        self.pos.remove()
        self.pos = self.ax.scatter(x,y,z)
        self.canvas.draw()
        self.app.after(40, self.refresh())
        
        if self.tps != None and self.coeur != None:
            self.dataText.set("Temps : {0} , nombre de coeur : {1}".format(self.tps, self.coeur))
        self.dataText.set("Temps : {0}".format(self.tps))


class FormNewPlanete(tkinter.simpledialog.Dialog):
    def __init__(self, parent, title):
        self.nom = ""
        self.masse = 0
        self.x = 0
        self.y = 0
        self.z = 0
        self.vx = 0
        self.vy = 0
        self.vz = 0
        super().__init__(parent, title)

    def body(self, frame):
        # print(type(frame)) # tkinter.Frame
        self.nom_label = tkinter.Label(frame, width=25, text="Nom de la planète")
        self.nom_label.pack()
        self.nom_box = tkinter.Entry(frame, width=25)
        self.nom_box.pack()
        
        self.masse_label = tkinter.Label(frame, width=25, text="Masse de la planète")
        self.masse_label.pack()
        self.masse_box = tkinter.Entry(frame, width=25)
        self.masse_box.pack()
        
        self.coord_label = tkinter.Label(frame, width=25, text="Coordonnée de la planète : (x, y, z)")
        self.coord_label.pack()
        
        self.x_box = tkinter.Entry(frame, width=25)
        self.x_box.pack()
        self.y_box = tkinter.Entry(frame, width=25)
        self.y_box.pack()
        self.z_box = tkinter.Entry(frame, width=25)
        self.z_box.pack()
        
        self.coord_label = tkinter.Label(frame, width=25, text="Vitesse de la planète : (x, y, z)")
        self.coord_label.pack()
        
        self.vx_box = tkinter.Entry(frame, width=25)
        self.vx_box.pack()
        self.vy_box = tkinter.Entry(frame, width=25)
        self.vy_box.pack()
        self.vz_box = tkinter.Entry(frame, width=25)
        self.vz_box.pack()
        
        return frame

    def ok_pressed(self):
        self.nom = self.nom_box.get()
        try:
            self.masse = float(self.masse_box.get())
            self.x = float(self.x_box.get())
            self.y = float(self.y_box.get())
            self.z = float(self.z_box.get())
            self.vx = float(self.vx_box.get())
            self.vy = float(self.vy_box.get())
            self.vz = float(self.vz_box.get())
            self.destroy()
        except:
            tkinter.messagebox.showerror("Error", "There is an error, maybe a variable is not a float.")

    def cancel_pressed(self):
        # print("cancel")
        self.destroy()

    def buttonbox(self):
        self.ok_button = tkinter.Button(self, text='OK', width=5, command=self.ok_pressed)
        self.ok_button.pack(side="left")
        cancel_button = tkinter.Button(self, text='Cancel', width=5, command=self.cancel_pressed)
        cancel_button.pack(side="right")
        self.bind("<Return>", lambda event: self.ok_pressed())
        self.bind("<Escape>", lambda event: self.cancel_pressed())
        
    def constructPlanete(self):
        return Planete(self.masse, self.x, self.y, self.z, self.vx, self.vy, self.vz, self.nom)

