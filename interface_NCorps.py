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
        
class DataNCorps():
    planetes = []
    # def __init__(self):
    #     self.planetes = []
    
    
    def loadFile(self, filename):
        #chargement du fichier json
        try:
            with open(filename) as json_file:
                data = json.load(json_file)
                for planete in data:
                    try:
                        self.planetes.append(Planete(p['masse'], p['x'], p['y'], p['z'], p['nom']))
                    except KeyError:
                        self.planetes.append(Planete(p['masse'], p['x'], p['y'], p['z']))
        except FileNotFoundError:
            tkinter.messagebox.showerror("Error", "File not found ! There is an error, please check the path.")
            
    def addPlanete(self, planete):
        self.planetes.append(planete)
        
    def graphX():
        pass                
            