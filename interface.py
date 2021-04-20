from tkinter import Tk, Label
import tkinter
#from pandas import DataFrame
import matplotlib.pyplot as pl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#https://vincent.developpez.com/cours-tutoriels/python/tkinter/apprendre-creer-interface-graphique-tkinter-python-3/


root = Tk() # Création de la fenêtre racine
root.title("Codev projet n°2")

canvas= tkinter.Canvas(root, width=800, height=800, bg="red")
canvas.pack()

#Affichage conventionnel d'un plot de matplotlib
pl.plot([1,2,3,4])
pl.ylabel('Label 1')
pl.show()

#graph = FigureCanvasTkAgg(fig, master=app)

figure = pl.Figure(figsize=(6,5), dpi=100)
ax = figure.add_subplot(111)
chart_type = FigureCanvasTkAgg(figure, root)
chart_type.get_tk_widget().pack()


#Affichage d'un plot avec des dataframe et FigureCanvas
data2 = {'Year': [1920,1930,1940,1950,1960,1970,1980,1990,2000,2010],
         'Unemployment_Rate': [9.8,12,8,7.2,6.9,7,6.5,6.2,5.5,6.3]
        }
df2 = DataFrame(data2,columns=['Year','Unemployment_Rate'])

#df = data
figure2 = plt.Figure(figsize=(5,4), dpi=100)
ax2 = figure2.add_subplot(111)
line2 = FigureCanvasTkAgg(figure2, root)
line2.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
df2 = df2[['Year','Unemployment_Rate']].groupby('Year').sum()
df2.plot(kind='line', legend=True, ax=ax2, color='r',marker='o', fontsize=10)
ax2.set_title('Year Vs. Unemployment Rate')


#____________________________________________________________
#Recherche de fichier
 
def GetFiles():
    filename = filedialog.askopenfilename()
    print (filename)
 
def GetDir():
    dirname = filedialog.askdirectory()
    print (dirname)
 
 
bouton_getfiles = Button(fenetre, text="Get Files", command=GetFiles)
bouton_getfiles.pack()
bouton_getdir = Button(fenetre, text="Get Directory", command=GetDir)
bouton_getdir.pack()
 


root.mainloop() # Lancement de la boucle principale