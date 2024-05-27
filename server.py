#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Paolo De Mori
"""
from socket import AF_INET, socket, SOCK_STREAM
import socketinit
import socket
from threading import Thread
import sys
import tkinter as tkt
import checkers

#questa funzione si occupa di gestire le richieste di connessione
def gestisci_connessioni():
    global names
    message_screen.insert(tkt.END, "in attesa...")
    while(True):
        try:
            try:
                #aspetta di ricevere una richiesta di connessione
                clsocket,clsocketAddress=srSocket.accept()
                #richiede l'invio di un primo messaggio di conferma di connessione avvenuta
                m=clsocket.recv(BUFFER).decode("utf8")
                #controlla che il messaggio appena ricevuto non sia una stringa specifica utilizzata in fase di chiusura del server per terminare il thread
                if(m!="1"):
                    break
            except:
                break
            message_screen.insert(tkt.END, "accettata una connessione")
            msg="Server:  Benvenuto nella chatroom come ti chiami?"
            #invia un messaggio di benvenuto e avvia un thread specifico per la gestione dei messaggi
            clsocket.send(bytes(msg,"utf8"))
            IOthread=Thread(target=IOclient, args=(clsocket,))
            IOthread.start()
        except:
            break
    clsocket.close()
    srSocket.close()
        
#questa funzione serve per gestire la richiesta del nome al client, l'invio degli utenti online e la ricezione e invio di messaggi
def IOclient(clsocket):
    global names
    global na_cl
    global isOn
    isRunning=True
    test="1"
    #questo prima parte di codice aspetta la ricezione del nome dell'utente e se non esiste nessun client con lo stesso nome lo autorizza e segnala a tutti gli altri client l'accesso
    nameIsValid=False
    while(nameIsValid==False):
        name=clsocket.recv(BUFFER).decode("utf8")
    
        nameIsValid=True
        for nn in names:
            if(nn==name or name=="__quit__" or name=="__join__" or name=="__quits__"):
                nameIsValid=False
                test=checkers.send_with_connection_test(clsocket,name,"Server:  stai usando un nome invalido riprovare",message_screen)
                if(test=="__LOST_CONNECTION__"):
                    exit()
    tmp="nome accettato "+name
    message_screen.insert(tkt.END, tmp)
    #inserisco nel dizionario il socket correlandolo al nome in modo da poterlo accedere in ogni momento
    na_cl[name]=clsocket
    accmessage="__join__"
    #segnalo al client che il suo nome è stato salvato correttamente
    clsocket.send(bytes("nome accettato","utf8"))
    sendtoall(accmessage,name)
    names.add(name)
    name_screen.insert(tkt.END, name)
    
    #invio al client la lista degli utenti online e successivamente attendo che risponda con una stringa specifica in modo da confermare l'esatta ricezione
    test=checkers.send_with_connection_test(clsocket,name,str(names),message_screen)
    if(test=="__LOST_CONNECTION__"):
        names.remove(name)
        del na_cl[name]
        exit()
    m=clsocket.recv(BUFFER).decode("utf8")
    if(m!="ready"):
        message_screen.insert(tkt.END, "errore nella connesione ad un client")
        names.remove(name)
        del na_cl[name]
        exit()
    #questo ciclo gestisce la ricezione dei messaggi del client controlla che i messaggi non sono delle stringhe che devono causare dei particolari effetti
    #e in caso negativo invia il messaggio a tutti gli altri client con la funzione sendtoall
    while(isRunning==True):
        if(isOn==False):
            exit()
        #riceve il messaggio
        msg=clsocket.recv(BUFFER).decode("utf8")
        #la stringa __quit2__ è quella che il client restituisce al server dopo che quest'ultimo ha notificato la disconnessione
        if(msg=="__quit2__"):
            try:
                clsocket.close()
            except:
                exit()
            exit()
        #la stringa __quit__ è la stringa che il client invia quando afferma la volontà di disconnettersi dal server, quindi il server si occupa di eliminare le informazioni
        #del client, segnalare a tutti i client la disconnessione e successivamente disconnetterlo
        if(msg=="__quit__"):
            tmp=name + " abbandona la chat"
            message_screen.insert(tkt.END, tmp)
            clsocket.close()
            del na_cl[name]
            names.remove(name)
            item=name_screen.get(0,tkt.END).index(name)
            name_screen.delete(item)
            sendtoall("__quits__",name)
            isRunning=False
            break
        else:
            tmp= name + " ha mandato un messaggio->" + msg
            message_screen.insert(tkt.END, tmp)
            sendtoall(msg,name)

    
#questa funzione si attiva tramite gui per spegnere il server
#invia a tutti i client la stringa __quit__ che comunica la imminente disconnessione, inizializza il thread intthr che si occupa di effettuare una connessione
#al server e inviare la stringa quit che effettua la terminazione del thread "connthread"
def closeall(event=None):
    sendtoall("__quit__","Server")
    intThread=Thread(target=intthr)
    intThread.start()
    intThread.join()
    srSocket.close()
    mainwindow.destroy()
        
#questa funzione si occupa di terminare il "connthread"
def intthr():
    intsocket=socket.socket(AF_INET,SOCK_STREAM)
    intsocket.connect(add2)
    intsocket.send(bytes("quit","utf8"))
    intsocket.close()

#questa funzione si occupa di inviare a tutti i client il messaggio di uno di loro o una comunicazione del server
def sendtoall(msg,name):
    test="1"
    msg=name + ":  " + msg
    for nome in names:
        if(nome!="Server"):
            test=checkers.send_with_connection_test(na_cl[nome],nome,msg,message_screen)
            if(test=="__LOST_CONNECTION__"):
                names.remove(nome)
                del na_cl[nome]

#questa funzione di occupa di inizializzare il thread  che si occupa della gestione della gui che fornisce informazioni sullo stato del server e sui client connessi
def serverGui():
    global mainwindow
    message_screen.pack(side=tkt.LEFT, fill=tkt.BOTH)
    scrollbar.pack(side=tkt.LEFT, fill=tkt.Y)
    scrollbar2.pack(side=tkt.RIGHT, fill=tkt.Y)
    main_frame.pack()
    name_screen.pack(side=tkt.LEFT, fill=tkt.BOTH)
    pulsante=tkt.Button(mainwindow,text="Stop il server",command= closeall)
    pulsante.pack()
    tkt.mainloop()
    
#questa funzione avvia lo spegnimento del server se la scheda viene chiusa
def on_closing(event=None):
    closeall()
    

def start():
    serverGui()

#-------------------------------------#
    
#creo il socket e eseguo il bind grazie al modulo socketinit
srSocket,add2=socketinit.start("server")
#Inizializzo gli elementi fondamentali della GUI   
mainwindow = tkt.Tk()
mainwindow.title("server")
mainwindow.geometry("900x700")
main_frame = tkt.Frame(mainwindow)
scrollbar=tkt.Scrollbar(main_frame)
scrollbar2=tkt.Scrollbar(main_frame)
message_screen=tkt.Listbox(main_frame,height=30,width=70,yscrollcommand=scrollbar.set)
name_screen=tkt.Listbox(main_frame,height=30,width=20,yscrollcommand=scrollbar2.set)
name_screen.insert(tkt.END, "Utenti online")
mainwindow.protocol("WM_DELETE_WINDOW", on_closing)

#Creo un set in cui memorizzerò i nomi con cui si identificano i client connessi
names={"Server"}
#Creo un dizionario in cui memorizzerò per ogni nome fornito dal client il suo socket
na_cl={}
clientaddresses={}
#buffer per ricezione di messaggi
BUFFER=1024
isOn=True
#metto in ascolto il socket
srSocket.listen(10)
#avvio un tread che si occuperà di gestire le richieste di connessione
ConnThread=Thread(target=gestisci_connessioni)
ConnThread.start()
start()
#aspetto la terminazione del thread
ConnThread.join()
isOn=False
srSocket.close()
sys.exit(0)
