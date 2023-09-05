from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkcalendar import *
import datetime
import pickle
root=Tk()
root.title("Notecal")
root.iconbitmap("ncicon.ico")
root.configure(bd=5, relief="groove", bg="cyan")


miframe=Frame(root)
miframe.grid(row=0, column=1, sticky="nswe")

root.rowconfigure(0, weight=1)
root.columnconfigure(1, weight=50)
 

tags=[]
eventos=[]

try:
    eventospermanentes=open("eventosdecalendario", "ab+")
    eventospermanentes.seek(0)
    eventos=pickle.load(eventospermanentes)
    print(eventos)
except:
    pass
finally:
    eventospermanentes.close()

def guardar():
    if areadetexto.get(0.0, "end-1c")!="":
        valor=messagebox.askquestion("Guardar", "¿Guardar evento en el calendario?")
        if valor=="yes":
            fecha=fechadateentry.get_date()
            horaevento=horaspin.get() + ":" + minutospin.get()
            infoevento=areadetexto.get(1.0, "end")
            #print(fecha,", ", horaevento,"\n",infoevento,sep="")
            #-----------guardadoencalendario-------------------
            eventos.append((fecha, infoevento, horaevento))
            eventospermanentes=open("eventosdecalendario", "wb")
            pickle.dump(eventos, eventospermanentes)
            eventospermanentes.close()
            del(eventospermanentes)
            calendario()
            #-------------guardadodetags-----------------
            tagspermanentes=open("{}".format(fecha), "wb")
            pickle.dump(tags, tagspermanentes)    
            tagspermanentes.close()
            del(tagspermanentes)
    else:
        messagebox.showerror("Error", "No se pueden guardar eventos vacíos.")
        
    
def calendario():
    framecalendario=Frame(root, bg="grey")
    framecalendario.grid(row=0, column=2, sticky="nsew")
    
    cal=Calendar(framecalendario, font=("IBM Plex sans", 12), selectmode="day", locale="es_ES", selectbackground="red")
    cal.grid(row=0, column=0, sticky="nsew")
    
    for fecha, texto, etiqueta in eventos:
        cal.calevent_create(fecha, texto, etiqueta)
    
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
    
    root.columnconfigure(2, weight=50)
    
    botoncalendario.config(state=DISABLED)
    
def cancelar():
    if areadetexto.get(0.0, "end-1c")=="":
        root.destroy()
    else:
        valor=messagebox.askquestion("Aviso", "¿Desea salir sin guardar los cambios?")
        if valor=="yes":
            root.destroy()

def estilotag(estilo):
    try:
        inicio=areadetexto.index(SEL_FIRST)
        fin=areadetexto.index(SEL_LAST)
        areadetexto.tag_add("e{},{}".format(inicio, fin), inicio, fin)
        areadetexto.tag_config("e{},{}".format(inicio, fin), font=("IBM Plex Mono", 11, "{}".format(estilo)))
        ntag="e{},{}".format(inicio, fin)
        vtag="IBM Plex Mono", 11, "{}".format(estilo)
        tags.append((ntag,vtag,inicio,fin))
        print(tags)
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
            
def tipografia():
    miframetipo=Frame(root, width=50, relief="groove")
    miframetipo.grid(row=0, column=0, sticky="nsew")
    
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
    
    botonmarcadormagenta=Button( marcadorlabel, text="Magenta", command=lambda: subrayadotag("magenta"), background="magenta")
    botonmarcadormagenta.grid(row=0, column=0, sticky="nsew")
    
    botonmarcadorcyan=Button( marcadorlabel, text="Cyan", command=lambda: subrayadotag("cyan"), background="cyan")
    botonmarcadorcyan.grid(row=1, column=0, sticky="nsew")
    
    botonmarcadoramarillo=Button( marcadorlabel, text="Amarillo", command=lambda: subrayadotag("yellow"), background="yellow")
    botonmarcadoramarillo.grid(row=2, column=0, sticky="nsew")
    
    botonmarcadorborrar=Button( marcadorlabel, text="Borrar\nSubrayado", command=lambda: subrayadotag("white"), background="white")
    botonmarcadorborrar.grid(row=3, column=0, sticky="nsew")
    
    
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

    
    root.columnconfigure(0, weight=1)
    
    botontipografia.config(state=DISABLED)

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

areadetexto=Text(miframe, width=50, bd=5, relief="groove", font=("IBM Plex Mono", 11), tabs=("1c"), fg="black", bg="white")
areadetexto.grid(row=1, column=0, columnspan=5, sticky="nsew")
areadetexto.focus_force()

#---------------------Botones inferiores----------------------------------

botonguardar=Button(miframe, text="Guardar", width=7, height=2, command=guardar)
botonguardar.grid(row=2, column=0, sticky="ew")

botontipografia=Button(miframe, text="Tipografía", width=7, height=2, command=tipografia)
botontipografia.grid(row=2, column=1, sticky="ew")

botoncalendario=Button(miframe, text="Calendario", width=7, height=2, command=calendario)
botoncalendario.grid(row=2, column=2, columnspan=2, sticky="ew")

botoncancelar=Button(miframe, text="Cancelar", height=2, command=cancelar)
botoncancelar.grid(row=2, column=4, sticky="ew")


#---------------------Calendario----------------------------------


root.mainloop()