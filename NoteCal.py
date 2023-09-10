from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedStyle
from tkinter import filedialog
from tkinter import messagebox
from tkinter import colorchooser
from tkcalendar import *
import datetime
import pickle

root=Tk()
root.title("Notecal")
root.iconbitmap("ncicon.ico")
root.configure(bd=5, relief="groove")

indice=ttk.Notebook(root)
indice.grid(row=0, column=0, sticky="nswe")


miframe=ttk.Frame(indice, style="TFrame")
framecalendario=ttk.Frame(indice, style="TFrame")
configframe=ttk.Frame(indice, style="TFrame")


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
    
    
cal=Calendar(framecalendario, font=("IBM Plex sans", 12), selectmode="day", locale="es_ES", 
             selectbackground="red", showothermonthdays=False, showweeknumbers=False)
cal.grid(row=0, column=0, sticky="nsew")
    
def cargarcalendario():
    for fecha, texto, etiqueta in eventos:
        cal.calevent_create(fecha, texto, etiqueta)
             
def on_tab_changed(event):
    # Obtén el índice de la pestaña seleccionada
    cargarcalendario()

# Enlaza la función al evento <<NotebookTabChanged>>
indice.bind("<<NotebookTabChanged>>", on_tab_changed)


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
    
    miframetipo=ttk.Frame(miframe, width=50, relief="groove", style="TFrame")
    miframetipo.grid(row=0, rowspan=7, column=0, sticky="nsew")
    
    
    #------------------------------------------------
    
    colorlabel=ttk.LabelFrame(miframetipo, style="TLabelframe", text="Color", labelanchor="n")
    colorlabel.grid(row=0, column=0, sticky="nsew", pady=3, padx=2)
    
    colordetextos=StringVar
    def aplicarcolor():
        try:
            global colordetextos
            colortag(colordetextos)
        except:
            pass

    def cambiarcolor():
        global colordetextos
        elecciondecolor=colorchooser.askcolor("red")
        if elecciondecolor[1]:
            colordetextos=elecciondecolor[1]
            colortag(elecciondecolor[1])
            estilodeaplicarboton=ttk.Style()
            estilodeaplicarboton.configure("botoncolor.TButton", background=elecciondecolor[1], foreground=elecciondecolor[1], font=("IBM Plex Mono", 11, "normal bold"))
            aplicarcolorboton.config(style="botoncolor.TButton")
    
    
    aplicarcolorboton=ttk.Button(colorlabel, text="Color", width=6, style="TButton", command=lambda : aplicarcolor())
    aplicarcolorboton.grid(row=0, column=0, sticky="ew")
    aplicarcolorboton.config(takefocus=False)
    
    elegircolorboton=ttk.Button(colorlabel, text="↓", width=1, style="TButton", command=lambda : cambiarcolor())
    elegircolorboton.grid(row=0, column=1, sticky="ew")
    elegircolorboton.config(takefocus=False)
    
    #------------------------------------------------
    
    estilolabel=ttk.LabelFrame(miframetipo, style="TLabelframe", text="Estilo", labelanchor="n")
    estilolabel.grid(row=1, column=0, sticky="nsew", pady=3, padx=2)
    
    listadeestilos=["normal", "italic", "bold", "bold italic"]
    estilocombobox=ttk.Combobox(estilolabel, style="TCombobox", values=listadeestilos, width=11, justify="center")
    estilocombobox.grid(row=0, column=0, sticky="sew", padx=2)
    estilocombobox.set("normal")
    estilocombobox.config(state="readonly", takefocus=False, exportselection=False)
    
    estiloboton=ttk.Button(estilolabel, text="Aplicar", style="TButton", command=lambda : estilotag(estilocombobox.get()))
    estiloboton.grid(row=1, column=0, sticky="new", padx=2)
    estiloboton.config(takefocus=False)

    #------------------------------------------------
    
    marcadorlabel=ttk.LabelFrame(miframetipo, style="TLabelframe", text="Subrayar", labelanchor="n")
    marcadorlabel.grid(row=2, column=0, sticky="nsew", pady=3, padx=2)
    
    marcadordetextos=StringVar
    def aplicarmarcador():
        try:
            global marcadordetextos
            subrayadotag(marcadordetextos)
        except:
            pass

    def cambiarmarcador():
        global marcadordetextos
        elecciondemarcador=colorchooser.askcolor("yellow")
        if elecciondemarcador[1]:
            marcadordetextos=elecciondemarcador[1]
            subrayadotag(elecciondemarcador[1])
            estilodeaplicarmarcadorboton=ttk.Style()
            estilodeaplicarmarcadorboton.configure("botonmarcador.TButton", background=elecciondemarcador[1], foreground=elecciondemarcador[1], font=("IBM Plex Mono", 11, "normal bold"))
            aplicarmarcadorboton.config(style="botonmarcador.TButton")
    
    
    aplicarmarcadorboton=ttk.Button(marcadorlabel, text="Color", width=6, style="TButton", command=lambda : aplicarmarcador())
    aplicarmarcadorboton.grid(row=0, column=0, sticky="ew")
    aplicarmarcadorboton.config(takefocus=False)
    
    elegirmarcadorboton=ttk.Button(marcadorlabel, text="↓", width=1, style="TButton", command=lambda : cambiarmarcador())
    elegirmarcadorboton.grid(row=0, column=1, sticky="ew")
    elegirmarcadorboton.config(takefocus=False)
    
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

fechalabel=ttk.Label(miframe, text="Fecha:", style="TLabel")
fechalabel.grid(row=0, column=1, sticky="nsew", padx=5)

fechadateentry=DateEntry(miframe, locale="es_ES")
fechadateentry.grid(row=0, column=2, sticky="nsew")

horalabel=ttk.Label(miframe, text="Hora:", style="TLabel")
horalabel.grid(row=0, column=3, sticky="nsew", padx=5)


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

areadetexto=Text(miframe, width=50, height=15, bd=5, relief="groove", font=("IBM Plex Mono", 11), tabs=("1c"), fg="black", bg="white")
areadetexto.grid(row=1, column=1, columnspan=6, sticky="nsew")
areadetexto.focus_force()

#---------------------Botones inferiores----------------------------------

botonguardar=ttk.Button(miframe, text="Guardar", width=7,command=guardar, style="TButton")
botonguardar.grid(row=2, column=1, sticky="ew")

botontipografia=ttk.Button(miframe, text="Tipografía", width=7,command=tipografia, style="TButton")
botontipografia.grid(row=2, column=2, sticky="ew")

#botoncalendario=Button(miframe, text="Calendario", width=7, height=2, command=calendario)
#otoncalendario.grid(row=2, column=2, columnspan=2, sticky="ew")

botoncancelar=ttk.Button(miframe, text="Cancelar", width=7, command=cancelar, style="TButton")
botoncancelar.grid(row=2, column=5, sticky="ew")

#--------------------------------------------calframe--------------------

verboton=ttk.Button(framecalendario, text="Ver", command=infodeldia, style="TButton")
verboton.grid(row=1, column=0, sticky="we")
    
infotext1=Text(framecalendario,height=1, width=10, bd=5, relief="groove", font=("IBM Plex Mono", 11), tabs=("1c"), fg="black", bg="white", state="disabled")
infotext1.grid(row=2, column=0, sticky="nswe")
    
infotext=Text(framecalendario,height=13, width=10, bd=5, relief="groove", font=("IBM Plex Mono", 11), tabs=("1c"), fg="black", bg="white", state="disabled")
infotext.grid(row=3, column=0, sticky="nswe")
    
framecalendario.rowconfigure(0, weight=1)
#framecalendario.rowconfigure(1, weight=1)
framecalendario.rowconfigure(2, weight=1)
framecalendario.rowconfigure(3, weight=1)
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

eligathemelabel=ttk.Label(configframe, text="Estilo:", style="TLabel")
eligathemelabel.grid(row=0, column=0, sticky="nsew")

def cambiartheme():
    temaseleccionado=comboboxtheme.get()
    estilodelaapp.set_theme(temaseleccionado)

listadethemes=["adapta", "black", "blue", "clearlooks", 
               "elegance", "equilux", "itft1", "keramik", "kroc", "plastik", 
               "scidgrey", "scidmint", "scidpink", "smog", "ubuntu", "winxpblue", "yaru"]
comboboxtheme=ttk.Combobox(configframe, value=listadethemes, style="TCombobox")
comboboxtheme.grid(row=0, column=1, sticky="we")
comboboxtheme.set("adapta")

aplicartemaboton=ttk.Button(configframe, text="aplicar", command=lambda: cambiartheme(), style="TButton")
aplicartemaboton.grid(row=0, column=2, sticky="we")

#configframe.columnconfigure(0, weight=1)
#configframe.rowconfigure(0, weight=1)

#----------------------------frameconfig----------------------


root.mainloop()