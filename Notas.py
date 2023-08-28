from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
#from tkcalendar import Calendar
#from tkcalendar import DateEntry
from tkcalendar import *
import datetime
root=Tk()
root.title("Notecal")
root.iconbitmap("ncicon.ico")
root.configure(bd=5, relief="groove", bg="cyan")


miframe=Frame(root)
miframe.grid(row=0, column=0, sticky="nswe")

root.rowconfigure(0, weight=8)
root.columnconfigure(0, weight=8)

def guardar():
    evento=fechadateentry.get_date()
    horaevento=horaspin.get() + minutospin.get()
    #calendariogrande.calevent_create(evento,"pepegordo", horaevento)
    
def cancelar():
    if areadetexto.get(0.0, "end-1c")=="":
        root.destroy()
    else:
        valor=messagebox.askquestion("NoteCal-Recordatorio", "¿Salir sin guardar los cambios?")
        if valor=="yes":
            root.destroy()

def pesotag(peso):
    inicio=areadetexto.index(SEL_FIRST)
    fin=areadetexto.index(SEL_LAST)
    areadetexto.tag_add("esti"+str(inicio+fin), inicio, fin)
    areadetexto.tag_config("esti"+str(inicio+fin), font=("IBM Plex Mono", 11, "{}".format(peso)))

def estilotag(estilo):
    try:
        inicio=areadetexto.index(SEL_FIRST)
        fin=areadetexto.index(SEL_LAST)
        areadetexto.tag_add("esti"+str(inicio+fin), inicio, fin)
        areadetexto.tag_config("esti"+str(inicio+fin), font=("IBM Plex Mono", 11, "normal {}".format(estilo)))
    except:
        inicio=areadetexto.index("insert")
        fin=areadetexto.index("end-1c")
        espacio=areadetexto.get("insert-1c", "insert")
        if inicio==fin and espacio!=" ":
            areadetexto.insert("insert", " ")
            inicio=areadetexto.index("insert-1c")
            fin=areadetexto.index("end")
            areadetexto.tag_add("esti"+str(inicio+fin), inicio, fin)
            areadetexto.tag_config("esti"+str(inicio+fin), font=("IBM Plex Mono", 11, "normal {}".format(estilo)))
        if inicio==fin and espacio==" ":
            inicio=areadetexto.index("insert-1c")
            fin=areadetexto.index("end")
            areadetexto.tag_add("esti"+str(inicio+fin), inicio, fin)
            areadetexto.tag_config("esti"+str(inicio+fin), font=("IBM Plex Mono", 11, "normal {}".format(estilo)))

def colortag(color):
    try:
        inicio=areadetexto.index(SEL_FIRST)
        fin=areadetexto.index(SEL_LAST)
        areadetexto.tag_add("col"+str(inicio+fin), inicio, fin)
        areadetexto.tag_config("col"+str(inicio+fin), foreground=color)
    except:
        inicio=areadetexto.index("insert")
        fin=areadetexto.index("end-1c")
        espacio=areadetexto.get("insert-1c", "insert")
        if inicio==fin and espacio!=" ":
            areadetexto.insert("insert", " ")
            inicio=areadetexto.index("insert-1c")
            fin=areadetexto.index("end")
            areadetexto.tag_add("col"+str(inicio+fin), inicio, fin)
            areadetexto.tag_config("col"+str(inicio+fin), foreground=color)
        if inicio==fin and espacio==" ":
            inicio=areadetexto.index("insert-1c")
            fin=areadetexto.index("end")
            areadetexto.tag_add("col"+str(inicio+fin), inicio, fin)
            areadetexto.tag_config("col"+str(inicio+fin), foreground=color)
        
def tipografia():
    miframetipo=Frame(root, width=50, relief="groove")
    miframetipo.grid(row=0, column=1, sticky="nsew")
    
    tipolabel=Label(miframetipo, text="Tipografía: ", relief="groove", bd=2, pady=5)
    tipolabel.grid(row=0, column=0, sticky="ew")
    
    botonrojo=Button(miframetipo, text="Rojo", command=lambda: colortag("red"), foreground="red")
    botonrojo.grid(row=1, column=0, sticky="ew")
    
    botonazul=Button(miframetipo, text="Azul", command=lambda: colortag("blue"), foreground="blue")
    botonazul.grid(row=2, column=0, sticky="ew")
    
    botonverde=Button(miframetipo, text="Verde", command=lambda: colortag("green"), foreground="green")
    botonverde.grid(row=3, column=0, sticky="ew")
    
    botonnegro=Button(miframetipo, text="Negro", command=lambda: colortag("black"), foreground="black")
    botonnegro.grid(row=4, column=0, sticky="ew")
    
    botonitalica=Button(miframetipo, text="Italica", command=lambda: estilotag("italic"), foreground="black")
    botonitalica.grid(row=5, column=0, sticky="ew")
    
    botonnormal=Button(miframetipo, text="Normal", command=lambda: estilotag("normal"), foreground="black")
    botonnormal.grid(row=6, column=0, sticky="ew")
    
    botonbold=Button(miframetipo, text="Bold", command=lambda: pesotag("bold"), foreground="black")
    botonbold.grid(row=7, column=0, sticky="ew")
    
    miframetipo.columnconfigure(0, weight=1)
    miframetipo.rowconfigure(1, weight=1)
    miframetipo.rowconfigure(2, weight=1)
    miframetipo.rowconfigure(3, weight=1)
    miframetipo.rowconfigure(4, weight=1)
    miframetipo.rowconfigure(5, weight=1)
    miframetipo.rowconfigure(6, weight=1)
    miframetipo.rowconfigure(7, weight=1)
    
    root.columnconfigure(1, weight=1)

#---------------------Panel Superior----------------------------------

fechalabel=Label(miframe, text="Fecha:")
fechalabel.grid(row=0, column=0, sticky="ew")

fechadateentry=DateEntry(miframe, locale="es_ES")
fechadateentry.grid(row=0, column=1, sticky="ew")

horalabel=Label(miframe, text="Hora:")
horalabel.grid(row=0, column=2, sticky="ew")


def hora():
    horaactual=datetime.datetime.now()
    horaspin.delete(0,"end")
    horaspin.insert(0, horaactual.strftime("%H"))

def minuto():
    horaactual=datetime.datetime.now()
    minutospin.delete(0,"end")
    minutospin.insert(0, horaactual.strftime("%M"))

horaspin=Spinbox(miframe, from_=0, to=23, wrap=True, width=2, repeatdelay=100, repeatinterval=50)
horaspin.grid(row=0, column=3, sticky="ew")
hora()

minutospin=Spinbox(miframe, from_=0, to=59, increment=5, wrap=True, width=2, repeatdelay=100, repeatinterval=150)
minutospin.grid(row=0, column=4, sticky="ew")
minuto()

miframe.rowconfigure(0, weight=0)
miframe.rowconfigure(1, weight=2)
miframe.rowconfigure(2, weight=0)
miframe.columnconfigure(0, weight=1)
miframe.columnconfigure(1, weight=1)
miframe.columnconfigure(2, weight=1)
miframe.columnconfigure(3, weight=1)
miframe.columnconfigure(4, weight=1)

#---------------------Nota/recordatorio----------------------------------

areadetexto=Text(miframe, width=40, bd=5, relief="groove", font=("IBM Plex Mono", 11, "normal normal"), tabs=("1c"), fg="black")
areadetexto.grid(row=1, column=0, columnspan=5, sticky="nsew")
areadetexto.focus_force()

#---------------------Botones inferiores----------------------------------

botonguardar=Button(miframe, text="Guardar", width=7, height=2, command=guardar)
botonguardar.grid(row=2, column=0, sticky="ew")

botontipografia=Button(miframe, text="Tipografía", width=7, height=2, command=tipografia)
botontipografia.grid(row=2, column=1, sticky="ew")

botoncancelar=Button(miframe, text="Cancelar", width=7, height=2, command=cancelar)
botoncancelar.grid(row=2, column=4, sticky="ew")


root.mainloop()