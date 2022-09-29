from tkinter import Tk, Label,Button,Entry
import os
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import  showwarning
from Code_source_comparaison_with_listV2 import Ligne_DSN, Table_DSN

def cherche_path(option = 'A'):
    if option == 'A':
        chosen_Entry = EntryA
    elif option == 'B':
        chosen_Entry = EntryB
    elif option == 'read':
        chosen_Entry = Entry_read

    file_name = askopenfilename()
    chosen_Entry.config(state = 'normal')
    actual_file_name = chosen_Entry.get()
    chosen_Entry.delete(0,len(actual_file_name))
    chosen_Entry.insert(0,file_name)
    chosen_Entry.config(state = 'readonly')
    
    
def comparer():
    File_name_A = EntryA.get()
    File_name_B = EntryB.get()
    if File_name_A == '' or File_name_B == '':
        message = showwarning('Attention',"Au moins une des deux entrées ne pointe sur aucun fichier")
    elif File_name_A == File_name_B:
        message = showwarning('Attention',"le fichier A et le fichier B sont un seul et même fichier")
    elif (File_name_A[-3:] != 'dsn' and File_name_A[-3:] != 'txt') or (File_name_B[-3:] != 'dsn' and  File_name_B[-3:] != 'txt'):
        message = showwarning('Attention',"Au moins un des deux fichiers ne se termine pas par '.dsn' ou '.txt'")
    with open(File_name_A) as fileA: 
        contentA = fileA.read()
    with open(File_name_B) as fileB: 
        contentB = fileB.read()
    A_DSN = Table_DSN(contentA,fen)
    B_DSN = Table_DSN(contentB,fen)
    A_DSN.differences(B_DSN)

def lire():
    File_name_read = Entry_read.get()
    if File_name_read == '' or File_name_read == '':
        message = showwarning('Attention',"L'entrée ne pointe sur aucun fichier")
    elif (File_name_read[-3:] != 'dsn' and File_name_read[-3:] != 'txt'):
        message = showwarning('Attention',"Le fichier ne se termine pas par '.dsn' ou '.txt'")
    with open(File_name_read) as file_read: 
        content_read = file_read.read()
    read_DSN = Table_DSN(content_read,fen)
    read_DSN.lecture()

#Comparateur
#Fenêtre principale
fen = Tk()
fen.title("Comparateur et lecteur de DSN")

Label(fen,text = 'Comparateur de DSN : ',font= ('calibri',20)).grid(row = 0, sticky= "N", pady = 10,padx = 20)
Label(fen,text = 'Choix du fichier A : ',font= ('calibri',12)).grid(row = 1, sticky= "N", pady = 10)
Button(fen,text = 'Parcourir',command = lambda : cherche_path('A')).grid(row = 2, column = 0, sticky = "N", pady = 10)
EntryA = Entry(fen,state = 'disabled',width=100)
EntryA.grid(row = 2, column = 1, sticky= "N", pady = 10,padx = 20)
Label(fen,text = 'Choix du fichier B : ',font= ('calibri',12)).grid(row = 3, sticky= "N", pady = 10)
Button(fen,text = 'Parcourir',command = lambda : cherche_path('B')).grid(row = 4, column = 0, sticky = "N", pady = 10)
EntryB = Entry(fen,state = 'disabled',width=100)
EntryB.grid(row = 4, column = 1, sticky= "N", pady = 10)
but_base_lecture = Button(fen,text = 'Comparer',command =  lambda : comparer(),width =30)
but_base_lecture.grid(row = 5, column = 1, sticky = "N", pady = 10)


#Lecteur
Label(fen,text = 'Lecteur de DSN : ',font= ('calibri',20)).grid(row = 7, sticky= "N", pady = 10)
Label(fen,text = 'Choix du fichier à lire: ',font= ('calibri',12)).grid(row = 8, sticky= "N", pady = 10)
Button(fen,text = 'Parcourir',command = lambda : cherche_path('read')).grid(row = 9,column = 0,sticky = "N", pady = 10)
Entry_read = Entry(fen,state = 'disabled',width=100)
Entry_read.grid(row = 9, column = 1, sticky= "N", pady = 10)
but_base_comp = Button(fen,text = 'Lire',command = lambda : lire(),width = 30)
but_base_comp.grid(row = 10, column = 1, sticky = "N", pady = 10)
Label(fen,text = 'Si vous avez un problème ou une idée, adressez vos questions/suggestions/insultes à ttale.noblia@soprahr.com',font= ('calibri',8)).grid(row = 11, sticky= "N", pady = 10, columnspan=2)


fen.mainloop()
