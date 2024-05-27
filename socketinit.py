#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Paolo De Mori
"""
from socket import AF_INET, socket, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import tkinter as tkt
import checkers
import guihelpers
import sys

#questa funzione si occupa di trasformare indirizzo e porta in una tupla in modo da poter essere utilizzati per fare il bind/connettere un socket
def setaddress(ip,port):
    global add2
    ServerIp=ip
    ServerPort=port
    address=(ServerIp,ServerPort)
    add2=address
    return address

def start(mod):
    global moda
    moda=mod
    setaddGui(mod)
    if(mod=="server"):
        return mainsocket,add2
    return mainsocket
    
#questa funzione si occupa o di avviare la connessione col server di un socket se richiesta la modalità "client" 
#o di eseguire il bind del socket in caso richiesta la modalità server 
def configuration(ip,port,mainwindow):
    address=setaddress(ip,port)
    if(moda=="client"):
        try:
            mainsocket.connect(address)
        except:
            guihelpers.errorGui(mainwindow)
    if(moda=="server"):
        try:
            mainsocket.bind(address)
        except:
            guihelpers.errorGui(mainwindow)
    
#questa funzione inizializza una gui con cui sarà possibile inserire indirizzo ip e porta, viene richiesta come argomento una stringa che indica
#se si vuole avviare un server o un client
def setaddGui(mod):
    mainwindow=tkt.Tk()
    mainwindow.geometry("400x400")
    mainwindow.protocol("WM_DELETE_WINDOW", on_closing)
    main_string=tkt.StringVar()
    main_string2=tkt.StringVar()
    main_frame=tkt.Frame(mainwindow)
    if(mod=="server"):
        mainwindow.title("Server Configuration")
        instruction=tkt.Label(main_frame,text="Scegli indirizzo ip e Porta su cui avviare il server")
        instruction.pack(side=tkt.TOP)
    if(mod=="client"):
        mainwindow.title("Client Configuration")
        instruction=tkt.Label(main_frame,text="Scegli indirizzo ip e Porta a cui connetterti")
        instruction.pack(side=tkt.TOP)
    campo=tkt.Entry(main_frame,textvariable=main_string)
    main_string.set("Indirizzo ip")
    campo.pack()
    campo2=tkt.Entry(main_frame,textvariable=main_string2)
    main_string2.set("Porta")
    campo2.pack()
    #creo 2 pulsanti che permettono o di verificare e successivamente settare l'indirizzo inserito o di terminare il programma
    pulsante=tkt.Button(main_frame,text="imposta",command= lambda: checkIpGui(main_string,main_string2,instruction,mainwindow))
    pulsante.pack()
    pulsante2=tkt.Button(main_frame,text="esci",command= lambda: guihelpers.shutdown(mainwindow))
    pulsante2.pack()
    main_frame.pack()
    tkt.mainloop()

#questa funzione si avvale delle funzioni del modulo checkers per testare indirizzo ip e porta inseriti
def checkIpGui(tkstring,tkstring2,label,mainwindow):
    ip=tkstring.get()
    Port=tkstring2.get()
    isvalid= checkers.checkAddress(ip, Port)
    if(isvalid==True):
        porta=int(Port)
        configuration(ip,porta,mainwindow)
        mainwindow.destroy()
    else: 
        label.configure(foreground="red",text="Indirizzo non valido o utilizzo di una well-known port riprovare")

def on_closing(event=None):
    sys.exit(0)


#inanzitutto creo il socket e verifico che sia stato creato correttamente
moda=""
try:
    mainsocket=socket(AF_INET,SOCK_STREAM) 
    #velocizza il riuso di indirizzi
    mainsocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
except:
    print("Errore nella creazione del socket")
    sys.exit(0)

add2=("",0)
