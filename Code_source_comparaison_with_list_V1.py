import os
from tkinter.filedialog import asksaveasfilename
from createur_tableau_DSN import df_DSN
from tkinter import Tk, Label,Button,Entry,Toplevel
import pandas as pd
from tkinter.ttk import Progressbar

class Ligne_DSN():

    def __init__(self, ligne, position = 0):
        self.texte = ligne
        self.bloc = self.texte[0:10]
        self.num_rub = self.texte[11:14]
        self.rubrique = self.texte[0:14]
        self.valeur = self.texte[15:][1:-1]
        self.entreprise = ''
        self.etablissement = ''
        self.individu = ''
        self.contrat = ''
        
    def __str__(self):
        return self.texte
    
    def __print__(self):
        print(str(self))
        
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)
    
    def show_attributs(self):
        print(self.__dict__)
        
    def attribue_caracteristiques(self, entreprise, etablissement,individu, contrat):
        self.entreprise = entreprise
        self.etablissement = etablissement
        self.individu = individu
        self.contrat = contrat

class Table_DSN():
    
    def __init__(self, texte, fenetre):
        self.fenetre = fenetre
        self.texte = texte
        self.liste_lignes = []
        entreprise = ''
        etablissement = ''
        individu = ''
        contrat = ''
        #On attribue les caractéristiques entreprise, individu etc... de la manière suivante:
        #On trouve la rubrique identifiante dans les lignes, puis on attribue cette caractéristique à toutes les 
        #rubriques suivantes jusqu'à ce que la caractéristique change
        for ligne in texte.split('\n'):
            a = Ligne_DSN(ligne)
            if a.rubrique == 'S21.G00.06.001':
                entreprise = a.valeur
            elif a.rubrique == 'S21.G00.11.001':
                etablissement = a.valeur
            elif a.rubrique == 'S21.G00.30.019':
                individu = a.valeur
            elif a.rubrique == 'S21.G00.40.009':
                contrat = a.valeur
            a.attribue_caracteristiques(entreprise, etablissement,individu, contrat)
            #Ajout de la ligne dans la liste des lignes
            self.liste_lignes.append(a)
            #Certaines rubriques des blocs contrats et individus n'ont pas leur attribut "contrat" ou "individu"
            #à jour du fait qu'ils arrivent avant la rubrique identifiante (par exemple, la rubrique identifiante de
            #l'individu arrive en 19ème position => 'S21.G00.30.019'. Cela veut dire qu'il y a 18 rubriques du bloc
            #individu non identifiées avant).
            # Il faut donc identifier ces rubriques en "retournant" la liste et en mettant à jour
            #les attributs "contrat" et "individu" comme on l'a fait précédemment. Puis on reretourne la liste
            
        #Retournement de la liste
        self.liste_lignes.reverse()
        for ligne in self.liste_lignes:
            #On récupère l'attribut
            if ligne.rubrique == 'S21.G00.40.009':
                contrat = ligne.valeur
            elif ligne.rubrique == 'S21.G00.30.019':
                individu = ligne.valeur
            #On l'attribue auX rubriqueS du même bloc qui on un num_rub inférieur (c'est à dire toutes les rubriques d'avant)
            if ligne.bloc == 'S21.G00.40' and int(ligne.num_rub)<9:
                ligne.contrat = contrat
            elif ligne.bloc == 'S21.G00.30' and int(ligne.num_rub)<19:
                ligne.individu = individu 
            #On enlève les attributs contrat, individu etc... au bloc 90
            if ligne.bloc == 'S90.G00.90':
                ligne.attribue_caracteristiques('','','','')
        #On reretourne la liste
        self.liste_lignes.reverse()
                
            
    def __getitem__(self,key):
        return self.liste_lignes[key]
    
    def __iter__(self):
        return iter(self.liste_lignes)
    
    def __str__(self):
        return  self.texte
    
    def __print__(self):
        print(str(self))
        
    def copy(self):
        copy = self.liste_lignes.copy()
        return copy
        
    def delete_ligne(self, ligneDSN):
        self.liste_lignes.remove(ligneDSN)
        
    def cherche_position(self, valeur_cherchee):
        n = 0
        for ligne in self.liste_lignes:
            if ligne.valeur == valeur_cherchee:
                print(n)
            n+=1
    
    def creer_dic_rubriques(self):
        dic_rubrique = {}
        for ligne in self.liste_lignes:
            try:
                dic_rubrique[ligne.rubrique].append(ligne)
            except:
                dic_rubrique[ligne.rubrique] = [ligne]
        return dic_rubrique
    
    def differences(self, other):
        fen_prog_c= Toplevel(self.fenetre)
        fen_prog_c.title('progression')
        Label(fen_prog_c,text = 'Comparaison A <=> B',font= ('calibri',12)).grid(row = 0, sticky= "N", pady = 10)
        progress_diff1 =  Progressbar(fen_prog_c,orient ="horizontal",length = 200, mode ="determinate")
        progress_diff1.grid(row = 1, sticky= "N", pady = 10,padx = 20)

        #Pour chaque ligne dans le fichier
        def bar_c():
            but_comp.config(state = 'disabled')
            n1= 0
            max_n1 = len(self.liste_lignes)
            progress_diff1["maximum"] = max_n1
            progress_diff1["value"]  = n1
            dicoB = other.creer_dic_rubriques()
            list_diff1 = []
            list_diff2 = []

            for ligneDSN in self:
                try:
                    dicoB[ligneDSN.rubrique].remove(ligneDSN)
                except:
                    lib_bloc = df_DSN['Libellé bloc'][df_DSN['id bloc'] == ligneDSN.bloc].values[0]
                    lib_rub = df_DSN['Libellé rubrique'][df_DSN['Id rubrique'] == ligneDSN.rubrique].values[0]
                    list_diff1.append({"SIREN Entreprise" : ligneDSN.entreprise,"NIC Etablissement": ligneDSN.etablissement,
                                            "Matcle Individu":ligneDSN.individu, "Contrat":ligneDSN.contrat,
                                            'libellé Bloc':lib_bloc,'Libellé rubrique':lib_rub,
                                            'Code rubrique':ligneDSN.rubrique,'Valeur':ligneDSN.valeur})
                n1 += 1
                if n1%2000 == 0:
                    progress_diff1["value"] = n1
                    progress_diff1.update()
                if n1 == progress_diff1["maximum"]:
                    progress_diff1["value"] = progress_diff1["maximum"]
            for key in dicoB.keys():
                for ligneDSN in dicoB[key]:
                    lib_bloc = df_DSN['Libellé bloc'][df_DSN['id bloc'] == ligneDSN.bloc].values[0]
                    lib_rub = df_DSN['Libellé rubrique'][df_DSN['Id rubrique'] == ligneDSN.rubrique].values[0]
                    list_diff2.append({"SIREN Entreprise" : ligneDSN.entreprise,"NIC Etablissement": ligneDSN.etablissement,
                                            "Matcle Individu":ligneDSN.individu, "Contrat":ligneDSN.contrat,
                                            'libellé Bloc':lib_bloc,'Libellé rubrique':lib_rub,
                                            'Code rubrique':ligneDSN.rubrique,'Valeur':ligneDSN.valeur})
                    fen_prog_c.destroy()
            df_diff = pd.DataFrame(list_diff1)
            df_diff2 = pd.DataFrame(list_diff2)
            saved_file = asksaveasfilename(defaultextension = '.xlsx',initialfile = 'Comparaison_DSN')
            writer = pd.ExcelWriter(saved_file, engine='xlsxwriter')
            df_diff.to_excel(writer,'Diff A-B')
            df_diff2.to_excel(writer,'Diff B-A')
            writer.save()
        but_comp = Button(fen_prog_c, text = 'Lancer la comparaison', command = bar_c)
        but_comp.grid(row = 5, sticky= "N", pady = 10)
        
    def lecture(self):
        fen_prog= Toplevel(self.fenetre)
        fen_prog.title('progression')
        progress =  Progressbar(fen_prog,orient ="horizontal",length = 200, mode ="determinate")
        progress.grid(row = 0, sticky= "N", pady = 10,padx = 20)

        def bar():
            but_lecture.config(state = 'disabled')
            n= 0
            max_n = len(self.liste_lignes) -1
            progress["maximum"] = max_n
            progress["value"]  = n
            list_lines = []
            for ligneDSN in self:
                if ligneDSN.texte != "":
                    lib_bloc = df_DSN['Libellé bloc'][df_DSN['id bloc'] == ligneDSN.bloc].values[0]
                    lib_rub = df_DSN['Libellé rubrique'][df_DSN['Id rubrique'] == ligneDSN.rubrique].values[0]
                    list_lines.append({"SIREN Entreprise" : ligneDSN.entreprise,"NIC Etablissement": ligneDSN.etablissement,
                                                "Matcle Individu":ligneDSN.individu, "Contrat":ligneDSN.contrat,
                                                'libellé Bloc':lib_bloc,'Libellé rubrique':lib_rub,
                                                'Code rubrique':ligneDSN.rubrique,'Valeur':ligneDSN.valeur})
                    n+=1
                    #Voir commentaire pour prog_diff1
                    if n%2000 == 0:
                        progress["value"] = n
                        progress.update()
                    if n == progress["maximum"]:
                        fen_prog.destroy()
            df_read = pd.DataFrame(list_lines)
            saved_file = asksaveasfilename(defaultextension = '.xlsx',initialfile = 'Lecture_DSN')
            writer = pd.ExcelWriter(saved_file, engine='xlsxwriter')
            df_read.to_excel(writer,'Lecture')
            writer.save()
    
        but_lecture = Button(fen_prog, text = 'Lancer la lecture', command = lambda : bar())
        but_lecture.grid(row = 1, pady = 10)
