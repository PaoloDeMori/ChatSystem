#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Paolo De Mori
"""
import socketinit
from threading import Thread
import tkinter as tkt
import guihelpers
import sys
import checkers

#questa funzione si occupa dell'invio del nome del client, della ricezione dei messaggi e della lista degli utenti online
def receivemessages():
    global isGoing
    global names
    ls=[]
    #questo ciclo viene eseguito fin quando la variabile globale isGoing non sara' posta come "False"
    while isGoing:
        #si mette in attesa della ricezione di un messaggio
        message=clsocket.recv(Buffer).decode("utf8")
        #controla che il messaggio non sia una stringa specifica che indica il corretto salvataggio del nome in fase di registrazione
        if(message=="nome accettato"):
            #in caso il client ha ricevuto la corretta ricezione del nome si occupa di ricevere la lista degli utenti online e formattarla per la visualizzazione
            n=clsocket.recv(Buffer).decode("utf8")
            ls=n.split(", ")
            chtochange=["'","{","}"]
            for nomi in ls:
                n=nomi
                for c in range(len(chtochange)):
                    n =n.replace(chtochange[c], "")
                name_screen.insert(tkt.END,n)
            clsocket.send(bytes("ready","utf8"))
            message="Server:  Utenti caricati correttamente"
        #ora la funzione trasforma il messaggio in una lista di  2 elementi il nome e il messagio in se' 
        ls=[]
        ls=message.split(":  ")
        namesneder=ls[0]
        try:
            #controlla la corretta ricezione del messaggio 
            msg=ls[1]
        except IndexError:
            #server offline
            exit()
        #in caso il messaggio sia la stringa __quit__ vuol dire che il server sta eseguendo la disconnessione da tutti i client
        if(msg=="__quit__"):
            isGoing=False
            #invia __quit2__ per riferire al server la ricevuta segnalazione di disconnesione
            clsocket.send(bytes("__quit2__","utf8"))
            message="il server ti ha cacciato, puoi chiudere il client"
            clsocket.close()
        #in caso il messaggio sia la stringa __join__ vuol dire che un nuovo client ha fatto l'accesso alla chatroom
        if(msg=="__join__"):
            name_screen.insert(tkt.END, namesneder)
            message="Nuovo utente in chat!!"
        #in caso il messaggio sia la stringa __quits__ vuol dire che il server sta comunicando la disconnessione di un client
        if(msg=="__quits__"):
            item=name_screen.get(0,tkt.END).index(namesneder)
            name_screen.delete(item)
            message=namesneder+" sta lasciando la chat"
        #la funzione mostra il messaggio ricevuto o la sua opportuna interpretazione sulla gui
        try:
            message_screen.insert(tkt.END, message)
        except:
            break
        
        

#questa funzione si occupa in caso di segnale dalla gui di provare ad inviare un messaggio al server, in caso di errore comunica l'avvenuta disconnessione dal server
def sendmessage(messageToSend):
    message=messageToSend.get()
    messageToSend.set("")
    try:
        clsocket.send(bytes(message,"utf8"))
    except:
        message_screen.insert(tkt.END,"Connessione persa col server")
        wantToQuit()
    
#questa funzione attivata via gui comunica al server la volonta' di disconnessione e interrompe il programma    
def wantToQuit(event=None):
    global isGoing
    isGoing=False
    try:
        clsocket.send(bytes("__quit__","utf8"))
    finally:
        clsocket.close()
        guihelpers.shutdown(client_window)
    
#questa funzione inizializza la gui
def clientGui():
    global client_window
    messageToSend=tkt.StringVar()
    client_window.geometry("600x700")
    client_window.title("Chat")
    scrollbar.pack(side=tkt.RIGHT, fill=tkt.Y)
    scrollbar2.pack(side=tkt.LEFT, fill=tkt.Y)
    message_screen.pack(side=tkt.RIGHT, fill=tkt.BOTH)
    name_screen.pack(side=tkt.LEFT, fill=tkt.BOTH)
    client_frame.pack()
    entry=tkt.Entry(client_window,textvariable=messageToSend)
    entry.pack()
    pulsante=tkt.Button(client_window,text="invia",command= lambda: sendmessage(messageToSend))
    pulsante.pack()
    pulsante2=tkt.Button(client_window,text="Abbandona la chat",command=wantToQuit)
    pulsante2.pack()
    tkt.mainloop()
    
#definisce l'azione da compiere in caso di chiusura della finestra della gui    
def on_closing(event=None):
    wantToQuit()

#------------------------------------------------------------#
#inizializzo il socket ed effettuo la connessione al server
clsocket=socketinit.start("client")
try:
    #test per l'effettiva connessione
    clsocket.send(bytes("1","utf8"))
except:
    sys.exit(0)

#dichiaro gli elementi fondamentali della gui
client_window=tkt.Tk()
client_frame=tkt.Frame(client_window)
scrollbar=tkt.Scrollbar(client_frame)
scrollbar2=tkt.Scrollbar(client_frame)
message_screen=tkt.Listbox(client_frame,height=30,width=50,yscrollcommand=scrollbar.set)
name_screen=tkt.Listbox(client_frame,height=30,width=20,yscrollcommand=scrollbar2.set)
name_screen.insert(tkt.END, "Utenti online")
client_window.protocol("WM_DELETE_WINDOW", on_closing)

#il set che conterra' i nomi di tutti gli utenti online
names={"Server"}
Buffer=1024
isGoing=True
#avvio il thread che si occuperà di gestire la ricezione dei messaggi
recThread =Thread(target=receivemessages)
recThread.start()
#avvio la gui che si occuperà anche dell'invio dei messaggi
clientGui()
clsocket.close()
sys.exit(0)

