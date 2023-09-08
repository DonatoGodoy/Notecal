from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedStyle
from tkinter import filedialog
from tkinter import messagebox
from tkcalendar import *
import datetime
import pickle

root=Tk()
root.title("Notecal")
root.iconbitmap("ncicon.ico")
root.configure(bd=5, relief="groove")

indice=ttk.Notebook(root)
indice.grid(row=0, column=0, sticky="nswe")


miframe=Frame(indice)
framecalendario=Frame(indice)
configframe=Frame(indice)


indice.add(miframe, text="Notas")
indice.add(framecalendario, text="Calendario")
indice.add(configframe, text="Configuracion")


root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

#-------------------------------------------guardado-----------------
tags=[]
eventos=[]

try:
    eventospermanentes=open("eventosdecalendario", "ab+")
    eventospermanentes.seek(0)
    eventos=pickle.load(eventospermanentes)
except:
    pass
finally:
    eventospermanentes.close()
    
    
cal=Calendar(framecalendario, font=("IBM Plex sans", 12), selectmode="day", locale="es_ES", selectbackground="red")
cal.grid(row=0, column=0, sticky="nsew")
    
for fecha, texto, etiqueta in eventos:
    cal.calevent_create(fecha, texto, etiqueta)

def guardar():
    if areadetexto.get(0.0, "end-1c")!="":
        valor=messagebox.askquestion("Guardar", "¿Guardar evento en el calendario?")
        if valor=="yes":
            fecha=fechadateentry.get_date()
            horaevento=horaspin.get() + ":" + minutospin.get()
            infoevento=areadetexto.get(1.0, "end")
            #-----------guardadoencalendario-------------------
            eventos.append((fecha, infoevento, horaevento))
            eventospermanentes=open("eventosdecalendario", "wb")
            pickle.dump(eventos, eventospermanentes)
            eventospermanentes.close()
            del(eventospermanentes)
            #-------------guardadodetags-----------------
            tagspermanentes=open("{}".format(fecha), "wb")
            pickle.dump(tags, tagspermanentes)    
            tagspermanentes.close()
            del(tagspermanentes)
            #---------------------------------------------
            areadetexto.delete(1.0, "end")
    else:
        messagebox.showerror("Error", "No se pueden guardar eventos vacíos.")
        
def cancelar():
    if areadetexto.get(0.0, "end-1c")=="":
        root.destroy()
    else:
        valor=messagebox.askquestion("Aviso", "¿Desea salir sin guardar los cambios?")
        if valor=="yes":
            root.destroy()        
    
def infodeldia():
    infotext.config(state="normal")
    infotext.delete(1.0, "end")
    infotext1.config(state="normal")
    infotext1.delete(1.0, "end")
    for elemento in eventos:
        fechaguardada, textoguardado, horaguardada = elemento
        if fechaguardada==cal.selection_get():
            infotext1.insert(1.0, str(fechaguardada)+","+horaguardada+"/")
            infotext.insert(1.0, textoguardado+"----------------------------------\n")
            cargatag=open("{}".format(str(cal.selection_get())), "ab+")
            cargatag.seek(0)
            tagtag=pickle.load(cargatag)
            for nombre, valor, inicio, fin in tagtag:
                for i in nombre:
                    if i=="c":
                        infotext.tag_add(nombre, inicio, fin)
                        infotext.tag_config(nombre, foreground=valor)
                    if i=="e":
                        infotext.tag_add(nombre, inicio, fin)
                        infotext.tag_config(nombre, font=valor)
                    if i=="s":
                        infotext.tag_add(nombre, inicio, fin)
                        infotext.tag_config(nombre, background=valor)
                        
                
    infotext.config(state="disabled")
    infotext1.config(state="disabled")

#-------------------------------------------guardado-----------------
#-------------------------------------------etiquetas-----------------
def estilotag(estilo):
    try:
        inicio=areadetexto.index(SEL_FIRST)
        fin=areadetexto.index(SEL_LAST)
        areadetexto.tag_add("e{},{}".format(inicio, fin), inicio, fin)
        areadetexto.tag_config("e{},{}".format(inicio, fin), font=("IBM Plex Mono", 11, "{}".format(estilo)))
        ntag="e{},{}".format(inicio, fin)
        vtag="IBM Plex Mono", 11, "{}".format(estilo)
        tags.append((ntag,vtag,inicio,fin))
    except:
        inicio=areadetexto.index("insert")
        fin=areadetexto.index("end-1c")
        espacio=areadetexto.get("insert-1c", "insert")
        if inicio==fin and espacio!=" ":
            areadetexto.insert("insert", " ")
            inicio=areadetexto.index("insert-1c")
            fin=areadetexto.index("end")
            areadetexto.tag_add("e{},{}".format(inicio, fin), inicio, fin)
            areadetexto.tag_config("e{},{}".format(inicio, fin), font=("IBM Plex Mono", 11, "normal {}".format(estilo)))
            ntag="e{},{}".format(inicio, fin)
            vtag="IBM Plex Mono", 11, "{}".format(estilo)
            tags.append((ntag,vtag,inicio,fin))
        if inicio==fin and espacio==" ":
            inicio=areadetexto.index("insert-1c")
            fin=areadetexto.index("end")
            areadetexto.tag_add("e{},{}".format(inicio, fin), inicio, fin)
            areadetexto.tag_config("e{},{}".format(inicio, fin), font=("IBM Plex Mono", 11, "normal {}".format(estilo)))
            ntag="e{},{}".format(inicio, fin)
            vtag="IBM Plex Mono", 11, "{}".format(estilo)
            tags.append((ntag,vtag,inicio,fin))

def colortag(color):
    try:
        inicio=areadetexto.index(SEL_FIRST)
        fin=areadetexto.index(SEL_LAST)
        areadetexto.tag_add("c{},{}".format(inicio, fin), inicio, fin)
        areadetexto.tag_config("c{},{}".format(inicio, fin), foreground=color)
        ntag="c{},{}".format(inicio, fin)
        vtag=color
        tags.append((ntag,vtag,inicio,fin))
    except:
        inicio=areadetexto.index("insert")
        fin=areadetexto.index("end-1c")
        espacio=areadetexto.get("insert-1c", "insert")
        if inicio==fin and espacio!=" ":
            areadetexto.insert("insert", " ")
            inicio=areadetexto.index("insert-1c")
            fin=areadetexto.index("end")
            areadetexto.tag_add("c{},{}".format(inicio, fin), inicio, fin)
            areadetexto.tag_config("c{},{}".format(inicio, fin), foreground=color)
            ntag="c{},{}".format(inicio, fin)
            vtag=color
            tags.append((ntag,vtag,inicio,fin))
        if inicio==fin and espacio==" ":
            inicio=areadetexto.index("insert-1c")
            fin=areadetexto.index("end")
            areadetexto.tag_add("c{},{}".format(inicio, fin), inicio, fin)
            areadetexto.tag_config("c{},{}".format(inicio, fin), foreground=color)
            ntag="c{},{}".format(inicio, fin)
            vtag=color
            tags.append((ntag,vtag,inicio,fin))
        
def subrayadotag(subrayado):
    try:
        inicio=areadetexto.index(SEL_FIRST)
        fin=areadetexto.index(SEL_LAST)
        areadetexto.tag_add("s{},{}".format(inicio, fin), inicio, fin)
        areadetexto.tag_config("s{},{}".format(inicio, fin), background=subrayado)
        ntag="s{},{}".format(inicio, fin)
        vtag=subrayado
        tags.append((ntag,vtag,inicio,fin))
    except:
        pass
    
#-------------------------------------------etiquetas-----------------
#-------------------------------------------tipografia-----------------
            
def tipografia():
    miframetipo=Frame(miframe, width=50, relief="groove")
    miframetipo.grid(row=0, rowspan=7, column=0, sticky="nsew")
    
    
    #------------------------------------------------
    
    colorlabel=LabelFrame(miframetipo, text="Color", labelanchor="n")
    colorlabel.grid(row=0, column=0, sticky="nsew")
    
    botonrojo=Button(colorlabel, text="Rojo", command=lambda: colortag("red"), foreground="red")
    botonrojo.grid(row=0, column=0, sticky="nsew")
    
    botonazul=Button(colorlabel, text="Azul", command=lambda: colortag("blue"), foreground="blue")
    botonazul.grid(row=1, column=0, sticky="nsew")
    
    botonverde=Button(colorlabel, text="Verde", command=lambda: colortag("green"), foreground="green")
    botonverde.grid(row=2, column=0, sticky="nsew")
    
    botonnegro=Button(colorlabel, text="Negro", command=lambda: colortag("black"), foreground="black")
    botonnegro.grid(row=3, column=0, sticky="nsew")
    
    #------------------------------------------------
    
    estilolabel=LabelFrame(miframetipo, text="Estilo", labelanchor="n")
    estilolabel.grid(row=1, column=0, sticky="nsew")
    
    botonregular=Button(estilolabel, text="Regular", command=lambda: estilotag("normal"), foreground="black", font=("IBM Plex Mono", 9, "normal"))
    botonregular.grid(row=0, column=0, sticky="nsew")
    
    botonitalica=Button(estilolabel, text="Italica", command=lambda: estilotag("italic"), foreground="black", font=("IBM Plex Mono", 9, "italic"))
    botonitalica.grid(row=1, column=0, sticky="nsew")
    
    botonbold=Button(estilolabel, text="Negrita", command=lambda: estilotag("bold"), foreground="black", font=("IBM Plex Mono", 9, "bold"))
    botonbold.grid(row=2, column=0, sticky="nsew")
    
    botonbolditalic=Button(estilolabel, text="Negrita\nItalica", command=lambda: estilotag("bold italic"), foreground="black", font=("IBM Plex Mono", 9, "bold italic"), justify="center")
    botonbolditalic.grid(row=3, column=0, sticky="nsew")

    #------------------------------------------------
    
    marcadorlabel=LabelFrame(miframetipo, text="Subrayar", labelanchor="n")
    marcadorlabel.grid(row=2, column=0, sticky="nsew")
    
    botonmarcadormagenta=Button(marcadorlabel, text="Magenta", command=lambda: subrayadotag("magenta"), background="magenta")
    botonmarcadormagenta.grid(row=0, column=0, sticky="nsew")
    
    botonmarcadorcyan=Button(marcadorlabel, text="Cyan", command=lambda: subrayadotag("cyan"), background="cyan")
    botonmarcadorcyan.grid(row=1, column=0, sticky="nsew")
    
    botonmarcadoramarillo=Button(marcadorlabel, text="Amarillo", command=lambda: subrayadotag("yellow"), background="yellow")
    botonmarcadoramarillo.grid(row=2, column=0, sticky="nsew")
    
    botonmarcadorborrar=Button(marcadorlabel, text="Borrar\nSubrayado", command=lambda: subrayadotag("white"), background="white")
    botonmarcadorborrar.grid(row=3, column=0, sticky="nsew")
    
    #------------------------------------------------
    
    estilolabel.columnconfigure(0, weight=1)
    estilolabel.rowconfigure(0, weight=1)
    estilolabel.rowconfigure(1, weight=1)
    estilolabel.rowconfigure(2, weight=1)
    estilolabel.rowconfigure(3, weight=1)
    
    colorlabel.columnconfigure(0, weight=1)
    colorlabel.rowconfigure(0, weight=1)
    colorlabel.rowconfigure(1, weight=1)
    colorlabel.rowconfigure(2, weight=1)
    colorlabel.rowconfigure(3, weight=1)
    
    marcadorlabel.columnconfigure(0, weight=1)
    marcadorlabel.rowconfigure(0, weight=1)
    marcadorlabel.rowconfigure(1, weight=1)
    marcadorlabel.rowconfigure(2, weight=1)
    marcadorlabel.rowconfigure(3, weight=1)
    
    
    miframetipo.columnconfigure(0, weight=1)
    miframetipo.rowconfigure(0, weight=1)
    miframetipo.rowconfigure(1, weight=1)
    miframetipo.rowconfigure(2, weight=1)
    
    botontipografia.config(state=DISABLED)

#---------------------Panel Superior----------------------------------

fechalabel=Label(miframe, text="Fecha:")
fechalabel.grid(row=0, column=1, sticky="ew")

fechadateentry=DateEntry(miframe, locale="es_ES")
fechadateentry.grid(row=0, column=2, sticky="ew")

horalabel=Label(miframe, text="Hora:")
horalabel.grid(row=0, column=3, sticky="ew")


def hora():
    horaactual=datetime.datetime.now()
    horaspin.delete(0,"end")
    horaspin.insert(0, horaactual.strftime("%H"))

def minuto():
    horaactual=datetime.datetime.now()
    minutospin.delete(0,"end")
    minutospin.insert(0, horaactual.strftime("%M"))

horaspin=Spinbox(miframe, from_=0, to=23, wrap=True, width=2, repeatdelay=100, repeatinterval=50)
horaspin.grid(row=0, column=4, sticky="ew")
hora()

minutospin=Spinbox(miframe, from_=0, to=59, increment=5, wrap=True, width=2, repeatdelay=100, repeatinterval=150)
minutospin.grid(row=0, column=5, sticky="ew")
minuto()

miframe.rowconfigure(0, weight=0)
miframe.rowconfigure(1, weight=1)
miframe.rowconfigure(2, weight=0)
miframe.columnconfigure(0, weight=0)
miframe.columnconfigure(1, weight=1)
miframe.columnconfigure(2, weight=1)
miframe.columnconfigure(3, weight=1)
miframe.columnconfigure(4, weight=1)
miframe.columnconfigure(5, weight=1)

#---------------------Areadetexto----------------------------------

areadetexto=Text(miframe, width=50, bd=5, relief="groove", font=("IBM Plex Mono", 11), tabs=("1c"), fg="black", bg="white")
areadetexto.grid(row=1, column=1, columnspan=6, sticky="nsew")
areadetexto.focus_force()

#---------------------Botones inferiores----------------------------------

botonguardar=Button(miframe, text="Guardar", width=7, height=2, command=guardar)
botonguardar.grid(row=2, column=1, sticky="ew")

botontipografia=Button(miframe, text="Tipografía", width=7, height=2, command=tipografia)
botontipografia.grid(row=2, column=2, sticky="ew")

#botoncalendario=Button(miframe, text="Calendario", width=7, height=2, command=calendario)
#otoncalendario.grid(row=2, column=2, columnspan=2, sticky="ew")

botoncancelar=Button(miframe, text="Cancelar", height=2, command=cancelar)
botoncancelar.grid(row=2, column=5, sticky="ew")

#--------------------------------------------calframe--------------------

verboton=Button(framecalendario, text="Ver", command=infodeldia)
verboton.grid(row=1, column=0, sticky="we")
    
infotext1=Text(framecalendario,height=1, width=10, bd=5, relief="groove", font=("IBM Plex Mono", 11), tabs=("1c"), fg="black", bg="white", state="disabled")
infotext1.grid(row=2, column=0, sticky="nswe")
    
infotext=Text(framecalendario,height=13, width=10, bd=5, relief="groove", font=("IBM Plex Mono", 11), tabs=("1c"), fg="black", bg="white", state="disabled")
infotext.grid(row=3, column=0, sticky="nswe")
    
framecalendario.rowconfigure(0, weight=1)
#framecalendario.rowconfigure(1, weight=1)
framecalendario.rowconfigure(2, weight=1)
framecalendario.rowconfigure(2, weight=1)
framecalendario.columnconfigure(0, weight=1)
    
#--------------------------------------------calframe--------------------
#----------------------------configframe----------------------
estilodelaapp=ThemedStyle(root)
try:
    configfile=open("configfile", "ab+")
    configfile.seek(0)
    estiloguardado=pickle.load(configfile)
    estilodelaapp.set_theme(estiloguardado)
except:
    estilodelaapp.set_theme("adapta")
finally:
    configfile.close()

eligathemelabel=Label(configframe, text="Estilo:")
eligathemelabel.grid(row=0, column=0, sticky="we")

def cambiartheme():
    temaseleccionado=comboboxtheme.get()
    estilodelaapp.set_theme(temaseleccionado)

listadethemes=["adapta", "aquativo", "arc", "black", "blue", "breeze", "clearlooks", 
               "elegance", "equilux", "itft1", "keramik", "kroc", "plastik", 
               "radiance", "scidgrey", "scidmint", "scidpink", "smog", "ubuntu", "winxpblue", "yaru"]
comboboxtheme=ttk.Combobox(configframe, value=listadethemes)
comboboxtheme.grid(row=0, column=1, sticky="we")

aplicartemaboton=Button(configframe, text="aplicar", command=lambda: cambiartheme())
aplicartemaboton.grid(row=0, column=2, sticky="we")

#configframe.columnconfigure(0, weight=1)
#configframe.rowconfigure(0, weight=1)

#----------------------------frameconfig----------------------


root.mainloop()