#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Paolo De Mori
"""
import tkinter as tkt
#Questa funzione controlla che l'indirizzo inserito sia un indirizzo ipv4 plausibile
def checkIp(ip):
    if(len(ip)>6 and len(ip)<16):
        iptolist=ip.split(".")
        if (len(iptolist)==4):
            for elem in iptolist:
                try:
                    elemtocheck=int(elem)
                except ValueError:
                    return False
                if(elemtocheck>=256 or elemtocheck<0):
                    return False
            return True
    return False

#Questa funzione controlla che la porta inserita sia un porta disponibile e non sia una well-known port
def checkPort(Port):
    try:
        porta=int(Port)
    except ValueError:
        return False
    if (porta>=49152 and porta<=65535):
        return True
    else:
        return False

#Questa funzione controlla che l'indirizzo a cui ci si vuole connettere sia plausibile
def checkAddress(ip,Port):
    if(checkIp(ip)):
        if(checkPort(Port)):
            return True
    return False    

#Questa funzione controlla che inviando un messaggio a un socket esso lo riceva in caso contrario segnala che la connessione è stata probabilmente persa
def send_with_connection_test(clsocket,name,msg,message_screen):
    try:
        clsocket.send(bytes(msg,"utf8"))
        return "1"
    except:
        m="connessione persa con " + name
        message_screen.insert(tkt.END,m)
        return "__LOST_CONNECTION__"
