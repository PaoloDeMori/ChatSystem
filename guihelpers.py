#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Paolo De Mori
"""
import tkinter as tkt
import sys

   
#questa funzione attiva una gui di errore che permette di chiudere il programma
def errorGui(mainwindow):
    try:
        mainwindow.destroy()
    finally:
        errorwindow=tkt.Tk()
        error_frame=tkt.Frame(errorwindow)
        instruction=tkt.Label(error_frame,text="C'e stato un problema di connessione")
        instruction.pack(side=tkt.TOP)
        pulsante=tkt.Button(error_frame,text="ok",command= lambda: shutdown(errorwindow))
        pulsante.pack()
        error_frame.pack()
        tkt.mainloop()

#questa funzione permette di chiudere il programma
def shutdown(mainwindow):
    try:
        mainwindow.destroy()
    except:
        sys.exit(0)
    sys.exit(0)