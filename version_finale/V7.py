from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk 
from tkinter import filedialog
import shutil
import csv
import ctypes
 
#
#
# afin d'exécuter le code placez le fichier sur le disque dur C

ctypes.windll.shcore.SetProcessDpiAwareness(1)

def load_data(file_path):
    data = {}
    with open(file_path, "r") as file:
        # Lire la première ligne pour obtenir les noms des étiquettes
        labels = file.readline().strip().split(',')

        # Lire les données pour chaque utilisateur
        for line in file:
            values = line.strip().split(',')
            user_info = {label: value for label, value in zip(labels[0:], values[0:])}
            data[values[0]] = user_info

    return data

def add_student(file_path, data, student_name, student_info):
    
    # Ajouter l'étudiant au dictionnaire
    data[student_name] = student_info

    # Écrire les modifications dans le fichier
    with open(file_path, "a") as file:
        # Ajouter les informations de l'élève séparées par des virgules
        for value in student_info.values():
            file.write(value + ',')

        # Aller à la ligne pour le prochain étudiant
        file.write('\n')

def remove_student(file_path, data, student_name):
    # Supprimer l'étudiant du dictionnaire
    if student_name in data:
        del data[student_name]

    # Écrire les modifications dans le fichier
    with open(file_path, "w") as file:
        # Écrire les noms des étiquettes
        labels = ','.join(data[next(iter(data))].keys())
        file.write(labels + '\n')

        # Écrire les informations de chaque élève
        for info in data.values():
            for value in info.values():
                file.write(value + ',')
            file.write('\n')

def update_student(file_path, data, student_name, new_info):
    # Mettre à jour les informations de l'étudiant dans le dictionnaire
    if student_name in data:
        data[student_name]=new_info

    # Écrire les modifications dans le fichier
    with open(file_path, "w") as file:
        # Écrire les noms des étiquettes
        labels = ','.join(data[next(iter(data))].keys())
        file.write(labels + '\n')

        # Écrire les informations de chaque élève après mise à jour
        for student, info in data.items():
            for value in info.values():
                file.write(value + ',')
            file.write('\n')

class Personne :
    def __init__(self, Id_Personne,Nom, Prenom,Email_Address,Date_de_naissance,mot_de_pass ):
        self.Id_Personne= Id_Personne
        self.Nom = Nom
        self.Prenom = Prenom
        self.Email_Address =Email_Address
        self.Date_de_naissance =Date_de_naissance 
        self.mot_de_pass =mot_de_pass

class Etudiant (Personne) : 
    def __init__(self,Id_Personne,Nom, Prenom,Email_Address,Date_de_naissance,mot_de_pass,Année_Entrée,Notes):
        Personne.__init__(self, Id_Personne,Nom, Prenom,Email_Address,Date_de_naissance,mot_de_pass)
        self.Année_Entrée =Année_Entrée
        self.Notes=Notes 

    def telecharger_cours_pdf(self, professeur):
        if professeur.cours_pdf:
            destination = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("Fichiers PDF", "*.pdf")])
            if destination:
                shutil.copy2(professeur.cours_pdf, destination)
                messagebox.showinfo("Téléchargement", f"Téléchargement du cours PDF de {professeur.Nom} réussi.")
            else:
                messagebox.showwarning("Avertissement", "Annulation du téléchargement.")
        else:
            messagebox.showwarning("Avertissement", "Aucun cours PDF disponible.")
        
def add_absence(file_path,data,Id_Personne, absence):
    data[Id_Personne] = absence

    # Écrire les modifications dans le fichier
    with open(file_path, "a") as file:
        # Ajouter les informations de l'élève séparées par des virgules
        for value in absence.values():
            file.write(value + ',')

        # Aller à la ligne pour le prochain étudiant
        file.write('\n')  

def update_absence(file_path,data,Id_Personne,date,new_info):
    # Mettre à jour les informations de l'étudiant dans le dictionnaire
    if Id_Personne in data and date==data[Id_Personne]['Date'] :
        data[Id_Personne]=new_info

   
    with open(file_path, "w") as file:
        
        labels = ','.join(data[next(iter(data))].keys())
        file.write(labels + '\n')

        
        for info in data.values():
            file.write(','.join(info.values()) + '\n')

def remove_absence(file_path, data, student_name, date):
    # Supprimer l'étudiant du dictionnaire
    if student_name in data and data[student_name]["Date"]==date:
        del data[student_name]

    # Écrire les modifications dans le fichier
    with open(file_path, "w") as file:
        # Écrire les noms des étiquettes
        labels = ','.join(data[next(iter(data))].keys())
        file.write(labels + '\n')

        # Écrire les informations de chaque élève
        for info in data.values():
            for value in info.values():
                file.write(value + ',')
            file.write('\n')        
         
class Professeur (Personne) : 
    def __init__(self,Id_Personne,Nom, Prenom,Email_Address,Date_de_naissance,mot_de_pass,Module):
        Personne.__init__(self, Id_Personne,Nom, Prenom,Email_Address,Date_de_naissance,mot_de_pass)
        self.Module =Module
    def get_module(self):
        self.Module

    def modifier_note(self,file_path,data,Id_Personne,nnote):
        Id=Id_Personne
        L=list(data[Id].keys())
        if self.Module==L[-1]:
            b={"Id_Personne":Id,"Nom":data[Id]["Nom"], "Prenom":data[Id]["Prenom"],"Email_Address":data[Id]["Email_Address"],"Date_de_naissance":data[Id]["Date_de_naissance"],"mot_de_pass":data[Id]["mot_de_pass"],"AnnÃ©e_EntrÃ©e":data[Id]["AnnÃ©e_EntrÃ©e"],"module1":data[Id]["module1"],"module2":data[Id]["module2"],"module3":nnote}
        elif self.Module==L[-2]:
            b={"Id_Personne":Id,"Nom":data[Id]["Nom"], "Prenom":data[Id]["Prenom"],"Email_Address":data[Id]["Email_Address"],"Date_de_naissance":data[Id]["Date_de_naissance"],"mot_de_pass":data[Id]["mot_de_pass"],"AnnÃ©e_EntrÃ©e":data[Id]["AnnÃ©e_EntrÃ©e"],"module1":data[Id]["module1"],"module2":nnote,"module3":data[Id]["module3"]}
        elif self.Module==L[-3]:
            b={"Id_Personne":Id,"Nom":data[Id]["Nom"], "Prenom":data[Id]["Prenom"],"Email_Address":data[Id]["Email_Address"],"Date_de_naissance":data[Id]["Date_de_naissance"],"mot_de_pass":data[Id]["mot_de_pass"],"AnnÃ©e_EntrÃ©e":data[Id]["AnnÃ©e_EntrÃ©e"],"module1":nnote,"module2":data[Id]["module2"],"module3":data[Id]["module3"]}
        update_student(file_path,data,Id_Personne,b)

    def ajouter_note(self,file_path,data,Id_Personne,nnote):
            Id=Id_Personne
            L=list(data[Id].keys())
            if self.Module==L[-1]:
                b={"Id_Personne":Id,"Nom":data[Id]["Nom"], "Prenom":data[Id]["Prenom"],
                   "Email_Address":data[Id]["Email_Address"],"Date_de_naissance":data[Id]["Date_de_naissance"],
                   "mot_de_pass":data[Id]["mot_de_pass"],"AnnÃ©e_EntrÃ©e":data[Id]["AnnÃ©e_EntrÃ©e"],
                   "module1":data[Id]["module1"],"module2":data[Id]["module2"],"module3":nnote}
            elif self.Module==L[-2]:
                b={"Id_Personne":Id,"Nom":data[Id]["Nom"], 
                   "Prenom":data[Id]["Prenom"],"Email_Address":data[Id]["Email_Address"],
                   "Date_de_naissance":data[Id]["Date_de_naissance"],"mot_de_pass":data[Id]["mot_de_pass"],
                   "AnnÃ©e_EntrÃ©e":data[Id]["AnnÃ©e_EntrÃ©e"],
                   "module1":data[Id]["module1"],"module2":nnote,"module3":data[Id]["module3"]}
            elif self.Module==L[-3]:
                b={"Id_Personne":Id,"Nom":data[Id]["Nom"], "Prenom":data[Id]["Prenom"],
                   "Email_Address":data[Id]["Email_Address"],"Date_de_naissance":data[Id]["Date_de_naissance"],
                   "mot_de_pass":data[Id]["mot_de_pass"],"AnnÃ©e_EntrÃ©e":data[Id]["AnnÃ©e_EntrÃ©e"],
                   "module1":nnote,"module2":data[Id]["module2"],"module3":data[Id]["module3"]}
            update_student(file_path,data,Id_Personne,b)

    def supprimer_note(self,file_path,data,Id_Personne):
            Id=Id_Personne
            L=list(data[Id].keys())
            if self.Module==L[-1]:
                b={"Id_Personne":Id,"Nom":data[Id]["Nom"], "Prenom":data[Id]["Prenom"],"Email_Address":data[Id]["Email_Address"],"Date_de_naissance":data[Id]["Date_de_naissance"],"mot_de_pass":data[Id]["mot_de_pass"],"AnnÃ©e_EntrÃ©e":data[Id]["AnnÃ©e_EntrÃ©e"],"module1":data[Id]["module1"],"module2":data[Id]["module2"],"module3":"*"}
            elif self.Module==L[-2]:
                b={"Id_Personne":Id,"Nom":data[Id]["Nom"], "Prenom":data[Id]["Prenom"],"Email_Address":data[Id]["Email_Address"],"Date_de_naissance":data[Id]["Date_de_naissance"],"mot_de_pass":data[Id]["mot_de_pass"],"AnnÃ©e_EntrÃ©e":data[Id]["AnnÃ©e_EntrÃ©e"],"module1":data[Id]["module1"],"module2":"*","module3":data[Id]["module3"]}
            elif self.Module==L[-3]:
                b={"Id_Personne":Id,"Nom":data[Id]["Nom"], "Prenom":data[Id]["Prenom"],"Email_Address":data[Id]["Email_Address"],"Date_de_naissance":data[Id]["Date_de_naissance"],"mot_de_pass":data[Id]["mot_de_pass"],"AnnÃ©e_EntrÃ©e":data[Id]["AnnÃ©e_EntrÃ©e"],"module1":"*","module2":data[Id]["module2"],"module3":data[Id]["module3"]}
            update_student(file_path,data,Id_Personne,b)

    def ajouter_absence(self,file_path,data,Id_Personne,date,justifiee,nb_hr):
        a={"Id_Personne":Id_Personne,"Date":date, "Justifiée":justifiee,"Nombre d'heures":nb_hr}
        add_absence(file_path,data,Id_Personne,a)

    def Modifier_absence(self,file_path,data,Id_Personne,date,justifiee, nb_hr):
        b={"Id_Personne":Id_Personne,"Date":date, "Justifiée":justifiee,"Nombre d'heures":nb_hr}
        update_absence(file_path,data,Id_Personne,date,b)

    def supprimer_absence(self, file_path, data, Id_Personne,date):
        remove_absence(file_path,data,Id_Personne,date)
        
    def ajouter_cours_pdf(self):
        fichier = filedialog.askopenfilename(filetypes=[("Fichiers PDF", "*.pdf")])
        if fichier:
            self.cours_pdf = fichier
            messagebox.showinfo("Succès", "Le cours PDF a été ajouté avec succès.")

    def ajouter_cours_pdf(self):
        fichier = filedialog.askopenfilename(filetypes=[("Fichiers PDF", "*.pdf")])
        if fichier:
            self.cours_pdf = fichier
            messagebox.showinfo("Succès", "Le cours PDF a été ajouté avec succès.")


class Administrateur (Personne) : 
    def __init__(self,Id_Personne,Nom,Prenom,Email_Address,Date_de_naissance,mot_de_pass) :
        Personne.__init__(self, Id_Personne,Nom, Prenom,Email_Address,Date_de_naissance,mot_de_pass)
        
    def ajouter_etudiant(self,file_path,data,Id_Personne,Nom,Prenom,Email_Address,Date_de_naissance,mot_de_pass,Année_Entrée,module1="*",module2="*",module3="*"):
        a={"Id_Personne":Id_Personne,"Nom":Nom, "Prenom":Prenom,"Email_Address":Email_Address,"Date_de_naissance":Date_de_naissance,"mot_de_pass":mot_de_pass,"Année_Entrée":Année_Entrée,"module1":module1,"module2":module2,"module3":module3}
        add_student(file_path,data,Id_Personne,a)
   
    def suprimer_etudiant(self,file_path, data,idd):
            remove_student(file_path, data, idd)
            
    def modifier_student(self,file_path,data,Id_Personne,nid,nnom,nprenom,nmail,ndaten,mdp,nAe,module1="*",module2="*",module3="*"):
        b = {"Id_Personne": nid, "Nom": nnom, "Prenom": nprenom, "Email_Address": nmail, "Date_de_naissance": ndaten,
             "mot_de_pass": mdp, "Année_Entrée": nAe, "module1": module1, "module2": module2, "module3": module3}
        update_student(file_path, data, Id_Personne, b)
    def ajouter_Professeur(self,file_path2,data2,Id_Personne,Nom,Prenom,Email_Address,Date_de_naissance,mot_de_pass,module):
        a={"Id_Personne":Id_Personne,"Nom":Nom, "Prenom":Prenom,"Email_Address":Email_Address,"Date_de_naissance":Date_de_naissance,"mot_de_pass":mot_de_pass,"module":module}
        add_student(file_path2,data2,Id_Personne,a)
    
    def supprimer_Professeur(self,file_path2,data2,Id_Personne):
        if Id_Personne in data2:
            del data2[Id_Personne]

        # Écrire les modifications dans le fichier
        with open(file_path2,"w") as file:
            labels = ','.join(data2[next(iter(data2))].keys())
            file.write(labels +'\n')

            for info in data2.values():
                for value in info.values():
                    file.write(value + ',')
                file.write('\n')
    
    def modifier_Professeur(self,file_path2,data2,Id_Personne,nid,nnom,nprenom,nmail,ndaten,mdp,module):
        b={"Id_Personne":nid,"Nom":nnom, "Prenom":nprenom,"Email_Address":nmail,"Date_de_naissance":ndaten,"mot_de_pass":mdp,"module":module}
        update_student(file_path2,data2,Id_Personne,b)  

def apo(x):
    return  Professeur("a","a", "a","a","a","a",prof_database[x]["module"])
def apoetu(x):
    return  Etudiant("a","a", "a","a","a","a",'a','a')
admin= Administrateur("ze","zz","zz","zz","zz","zz")    
prof=Professeur("1234","prof","prof","ob@gmail.com","12-03-2003",'mdp','module1')
 
# importer les données des fichiers 

file_path = r"C:\version_finale/test2.txt" # Etudiants
file_path2=r"C:\version_finale/data prof.txt" # Enseignants
file_path3=r"C:\version_finale/file abs.txt"# Absences
user_database = load_data(file_path)
prof_database = load_data(file_path2)
abs_database=load_data(file_path3)
admin_database = {'admin':{'mot_de_pass':'admin','Nom':'admin'}}
profdata = {'prof':{'mot_de_pass':'prof','Nom':'prof'}}

# Fonction pour visualiser les absences sous forme de tableau

def view_csv1(csv_file):
    root = tk.Tk()
    root.title("CSV Viewer")

    tree = ttk.Treeview(root)
    headers = get_csv_header1(csv_file)
    tree["columns"] = tuple(headers)
    tree["show"] = "headings"

    for col in tree["columns"]:
        tree.heading(col, text=col)

    load_csv_data1(tree, csv_file)
    tree.pack(expand=True, fill="both")

    root.mainloop() 

def get_csv_header1(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)
    return header

def load_csv_data1(tree, file):
    identifiant=entry_username.get()
    tree.delete(*tree.get_children())  # Clear previous data
    with open(file, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            if row[0] == identifiant:
                tree.insert("", "end", values=row)



def etudiant_abs():
    view_csv1(file_path3)

# Espaces de l'etudiant de la plateforme

def etudiant_cours():
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\version_finale\assets\frame11")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    window = tk.Toplevel(window_login)
    window.geometry("1000x550")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(window, bg="#FFFFFF", height=550, width=1000, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)
    canvas.create_rectangle(1.0, 3.0, 1002.0, 59.0, fill="#D5F0C1", outline="")

    canvas.create_text(905.0, 20.0, anchor="nw", text="Etudiant", fill="#000000", font=("Inter", 20 * -1))

    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(96.59716796875, 25.8587646484375, image=image_image_1)

    image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(43.0, 78.0, image=image_image_2)

    canvas.create_text(63.0, 66.0, anchor="nw", text="Mes cours", fill="#116A7B", font=("Inter", 20 * -1))
    def on_deconnexion_click():
        window.destroy()
        espace_etudiant()
    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    button_1 = Button(canvas,image=button_image_1, borderwidth=0, highlightthickness=0, command=lambda: on_deconnexion_click(), relief="flat", bg="#FFFFFF")
    button_1.place(x=950.0, y=62.0, width=34.0, height=33.0)

    apoetu(entry_username.get()).telecharger_cours_pdf(prof)
    def on_deconnexion_click():
        window.destroy()
        espace_etudiant()

    window.resizable(False, False)
    window.mainloop()

def calculer_moyenne():
    if user_database[entry_username.get()]['module1']=='*' or user_database[entry_username.get()]['module2']=='*' or user_database[entry_username.get()]['module3']=='*':
        print('les notes ne sont pas complètes')
    else:
        return (int(user_database[entry_username.get()]['module1'])*2+int(user_database[entry_username.get()]['module2'])*5+int(user_database[entry_username.get()]['module3'])*3)/10
def etudiant_notes():
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\version_finale\assets\frame10")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    window = tk.Toplevel(window_login)
    window.geometry("1000x550")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(window, bg="#FFFFFF", height=550, width=1000, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)
    canvas.create_rectangle(1.0, 3.0, 1002.0, 59.0, fill="#D5F0C1", outline="")

    canvas.create_text(905.0, 20.0, anchor="nw", text="Etudiant", fill="#000000", font=("Inter", 20 * -1))

    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(96.5972900390625, 25.8587646484375, image=image_image_1)

    image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(43.0, 78.0, image=image_image_2)

    canvas.create_text(63.0, 66.0, anchor="nw", text="Mes notes", fill="#116A7B", font=("Inter", 20 * -1))

    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    button_1 = Button(canvas,image=button_image_1, borderwidth=0, highlightthickness=0, command=lambda: on_deconnexion_click(), relief="flat", bg="#FFFFFF")
    button_1.place(x=950.0, y=62.0, width=34.0, height=33.0)

    info_frame = tk.Frame(window)
    info_frame.pack(pady=(150, 10), padx=(50, 10))
    
    id_label = tk.Label(info_frame, text="module1 :" + user_database[entry_username.get()]['module1'], font=("Arial", 14))
    id_label.grid(row=1, column=0, pady=10)
    
    id_label = tk.Label(info_frame, text="module2 :" + user_database[entry_username.get()]['module2'], font=("Arial", 14))
    id_label.grid(row=2, column=0, pady=10)
    
    id_label = tk.Label(info_frame, text="module3 :" + user_database[entry_username.get()]['module3'], font=("Arial", 14))
    id_label.grid(row=3, column=0,pady=10)

    id_label = tk.Label(info_frame, text="moyenne générale :" + str(calculer_moyenne()), font=("Arial", 14))
    id_label.grid(row=4, column=0,pady=10)
                                
    def on_deconnexion_click():
        window.destroy()
        espace_etudiant()

    window.resizable(False, False)
    window.mainloop()

def espace_etudiant():
    window_login.withdraw()

    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\version_finale\assets\frame2")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    window = tk.Toplevel(window_login)
    window.geometry("1000x550")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(window, bg="#FFFFFF", height=550, width=1000, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)
    canvas.create_rectangle(1.0, 3.0, 1002.0, 59.0, fill="#D5F0C1", outline="")

    canvas.create_text(905.0, 20.0, anchor="nw", text="Etudiant", fill="#000000", font=("Inter", 20 * -1))

    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(96.5972900390625, 25.8587646484375, image=image_image_1)

    image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(43.0, 78.0, image=image_image_2)

    canvas.create_text(63.0, 66.0, anchor="nw", text="Page d’accueil", fill="#116A7B", font=("Inter", 20 * -1))

    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    button_1 = Button(canvas,image=button_image_1, borderwidth=0, highlightthickness=0, command=lambda: notes(), relief="flat", bg="#FFFFFF")
    button_1.place(x=347.0, y=104.0, width=306.0, height=85.0)

    button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
    button_2 = Button(canvas,image=button_image_2, borderwidth=0, highlightthickness=0, command=lambda: etudiant_abs(), relief="flat", bg="#FFFFFF")
    button_2.place(x=347.0, y=238.0, width=306.0, height=85.0)

    button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
    button_3 = Button(canvas,image=button_image_3, borderwidth=0, highlightthickness=0, command=lambda: cours(), relief="flat", bg="#FFFFFF")
    button_3.place(x=347.0, y=362.0, width=306.0, height=85.0)

    button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
    button_4 = Button(canvas,image=button_image_4, borderwidth=0, highlightthickness=0, command=lambda: on_deconnexion_click(), relief="flat", bg="#FFFFFF")
    button_4.place(x=940.0, y=66.0, width=34.0, height=33.0)

    def cours():
        window.withdraw()
        etudiant_cours()
    
    def notes():
        window.withdraw()
        etudiant_notes()
    
    def absences():
        window.withdraw()
        etudiant_abs()
    
    def on_deconnexion_click():
        window.destroy()
        window_login.deiconify()


    window.resizable(False, False)
    window.mainloop()
# Fonction pour visualiser les donnees dans un tableau
def view_csv(csv_file):
    root = tk.Toplevel()
    root.title("CSV Viewer")

    tree = ttk.Treeview(root)
    headers = get_csv_header(csv_file)
    tree["columns"] = tuple(headers)
    tree["show"] = "headings"

    for col in tree["columns"]:
        tree.heading(col, text=col)

    load_csv_data(tree, csv_file)
    tree.pack(expand=True, fill="both")

    root.mainloop() 

def get_csv_header(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)
    return header
def admin__absence():
    view_csv(file_path3)
def load_csv_data(tree, file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            tree.insert("", "end",values=row)

# Espaces de l'administrateur de la plateforme
def admin_cours():
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\version_finale\assets\frame15")


    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    window = tk.Toplevel(window_login)
    window.geometry("1000x550")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(window, bg="#FFFFFF", height=550, width=1000, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)

    canvas.create_rectangle(1.0, 3.0, 1002.0, 59.0, fill="#C4DFDF", outline="")
    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(915.0, 26.0, image=image_image_1)

    canvas.create_rectangle(0.0, 56.0, 285.0, 549.0, fill="#F0F0F0", outline="")

    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    button_1 = Button(canvas,image=button_image_1, borderwidth=0, highlightthickness=0, command=lambda: absence(), relief="flat")
    button_1.place(x=38.0, y=367.0, width=169.0, height=37.0)

    button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
    button_2 = Button(canvas,image=button_image_2, borderwidth=0, highlightthickness=0, command=lambda: print('button clicked'), relief="flat")
    button_2.place(x=38.0, y=307.0, width=150.0, height=37.0)

    button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
    button_3 = Button(canvas,image=button_image_3, borderwidth=0, highlightthickness=0, command=lambda: cours(), relief="flat")
    button_3.place(x=35.0, y=251.0, width=179.0, height=33.0)

    button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
    button_4 = Button(canvas,image=button_image_4, borderwidth=0, highlightthickness=0, command=lambda: etudiant(), relief="flat")
    button_4.place(x=33.0, y=190.0, width=163.0, height=38.0)

    button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
    button_5 = Button(canvas,image=button_image_5, borderwidth=0, highlightthickness=0, command=lambda: enseignant(), relief="flat")
    button_5.place(x=31.0, y=136.0, width=170.0, height=37.0)

    image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(96.59716796875, 25.8587646484375, image=image_image_2)

    button_image_6 = PhotoImage(file=relative_to_assets("button_6.png"))
    button_6 = Button(canvas,image=button_image_6, borderwidth=0, highlightthickness=0, command=lambda: admin(), relief="flat")
    button_6.place(x=33.0, y=76.0, width=190.0, height=37.0)

    image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(321.0, 78.0, image=image_image_3)

    canvas.create_text(341.0, 66.0, anchor="nw", text="Cours", fill="#116A7B", font=("Inter", 20 * -1))

    button_image_7 = PhotoImage(file=relative_to_assets("button_7.png"))
    button_7 = Button(canvas,image=button_image_7, borderwidth=0, highlightthickness=0, command=lambda: on_deconnexion_click(), relief="flat", bg="#FFFFFF")
    button_7.place(x=949.0, y=69.0, width=34.0, height=33.0)

    def admin():
        window.withdraw()
        espace_admin()
    
    def enseignant():
        window.withdraw()
        admin_enseignant()
    
    def etudiant():
        window.withdraw()
        admin_etudiant()

    def cours():
        window.withdraw()
        admin_cours()
    
    def absence():
        window.withdraw()
        admin__absence()
    
    
    def on_deconnexion_click():
        window.destroy()
        window_login.deiconify()
    window.resizable(False, False)
    window.mainloop()

def enregistrer_ajout(Id_entry,nom_entry,Prenom_entry,Adresse_entry,Date_de_naissance_entry,mdp_entry,Année_Entrée_entry):
    #Id_entry,nom_entry,Prenom_entry,Adresse_entry,Date_de_naissance_entry,mdp_entry,Année_Entrée_entry
        idd = Id_entry.get()
        nom = nom_entry.get()
        prenom = Prenom_entry.get()
        adress = Adresse_entry.get()
        date = Date_de_naissance_entry.get()
        mdp = mdp_entry.get()
        ae = Année_Entrée_entry.get()
        if not idd or not nom or not prenom or not adress  or not date or not mdp or not ae:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
            return
    
        admin.ajouter_etudiant(file_path,user_database,idd,nom,prenom,adress,date,mdp,ae)
    
        messagebox.showinfo("Succès", "Étudiant ajouté avec succès.")
def admin_aj_etudiant():
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\version_finale\assets\frame17")
    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    window = tk.Toplevel(window_login)
    window.geometry("1000x550")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(window, bg="#FFFFFF", height=550, width=1000, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)

    canvas.create_rectangle(1.0, 3.0, 1002.0, 59.0, fill="#C4DFDF", outline="")
    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(915.0, 26.0, image=image_image_1)

    canvas.create_rectangle(0.0, 56.0, 285.0, 549.0, fill="#F0F0F0", outline="")

    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    button_1 = Button(canvas,image=button_image_1, borderwidth=0, highlightthickness=0, command=lambda: absence(), relief="flat")
    button_1.place(x=38.0, y=367.0, width=169.0, height=37.0)

    button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
    button_2 = Button(canvas,image=button_image_2, borderwidth=0, highlightthickness=0, command=lambda: print('button 7 is clicked'), relief="flat")
    button_2.place(x=38.0, y=307.0, width=150.0, height=37.0)

    button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
    button_3 = Button(canvas,image=button_image_3, borderwidth=0, highlightthickness=0, command=lambda: cours(), relief="flat")
    button_3.place(x=35.0, y=251.0, width=179.0, height=33.0)

    button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
    button_4 = Button(canvas,image=button_image_4, borderwidth=0, highlightthickness=0, command=lambda: etudiant(), relief="flat")
    button_4.place(x=33.0, y=190.0, width=163.0, height=38.0)

    button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
    button_5 = Button(canvas,image=button_image_5, borderwidth=0, highlightthickness=0, command=lambda: enseignant(), relief="flat")
    button_5.place(x=31.0, y=136.0, width=170.0, height=37.0)

    image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(96.59716796875, 25.8587646484375, image=image_image_2)

    button_image_6 = PhotoImage(file=relative_to_assets("button_6.png"))
    button_6 = Button(canvas,image=button_image_6, borderwidth=0, highlightthickness=0, command=lambda: admin(), relief="flat")
    button_6.place(x=33.0, y=76.0, width=190.0, height=37.0)

    image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(321.0, 78.0, image=image_image_3)

    canvas.create_text(341.0, 66.0, anchor="nw", text="Ajouter étudiant", fill="#116A7B", font=("Inter", 20 * -1))

    button_image_7 = PhotoImage(file=relative_to_assets("button_7.png"))
    button_7 = Button(canvas,image=button_image_7, borderwidth=0, highlightthickness=0, command=lambda: on_deconnexion_click(), relief="flat", bg="#FFFFFF")
    button_7.place(x=949.0, y=69.0, width=34.0, height=33.0)

    entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(611.0, 142.5, image=entry_image_1)
    entry_1 = Entry(canvas,bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0)
    entry_1.place(x=440.5, y=131.0, width=341.0, height=21.0)

    canvas.create_text(444.0, 107.0, anchor="nw", text="Id étudiant", fill="#000000", font=("Inter", 15 * -1))

    entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(611.0, 466.5, image=entry_image_2)
    entry_2 = Entry(canvas,bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0)
    entry_2.place(x=440.5, y=455.0, width=341.0, height=21.0)

    canvas.create_text(444.0, 431.0, anchor="nw", text="Année entrée", fill="#000000", font=("Inter", 15 * -1))

    entry_image_3 = PhotoImage(file=relative_to_assets("entry_3.png"))
    entry_bg_3 = canvas.create_image(611.0, 198.5, image=entry_image_3)
    entry_3 = Entry(canvas,bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0)
    entry_3.place(x=440.5, y=187.0, width=341.0, height=21.0)

    canvas.create_text(444.0, 163.0, anchor="nw", text="Nom", fill="#000000", font=("Inter", 15 * -1))

    entry_image_4 = PhotoImage(file=relative_to_assets("entry_4.png"))
    entry_bg_4 = canvas.create_image(611.0, 254.5, image=entry_image_4)
    entry_4 = Entry(canvas,bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0)
    entry_4.place(x=440.5, y=243.0, width=341.0, height=21.0)

    canvas.create_text(444.0, 219.0, anchor="nw", text="Prénom", fill="#000000", font=("Inter", 15 * -1))

    entry_image_5 = PhotoImage(file=relative_to_assets("entry_5.png"))
    entry_bg_5 = canvas.create_image(611.0, 310.5, image=entry_image_5)
    entry_5 = Entry(canvas,bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0)
    entry_5.place(x=440.5, y=299.0, width=341.0, height=21.0)

    canvas.create_text(444.0, 275.0, anchor="nw", text="Email", fill="#000000", font=("Inter", 15 * -1))

    entry_image_6 = PhotoImage(file=relative_to_assets("entry_6.png"))
    entry_bg_6 = canvas.create_image(611.0, 360.5, image=entry_image_6)
    entry_6 = Entry(canvas,bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0)
    entry_6.place(x=440.5, y=349.0, width=341.0, height=21.0)

    canvas.create_text(444.0, 325.0, anchor="nw", text="Date de naissance", fill="#000000", font=("Inter", 15 * -1))

    entry_image_7 = PhotoImage(file=relative_to_assets("entry_7.png"))
    entry_bg_7 = canvas.create_image(611.0, 416.5, image=entry_image_7)
    entry_7 = Entry(canvas,bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0)
    entry_7.place(x=440.5, y=405.0, width=341.0, height=21.0)

    canvas.create_text(444.0, 381.0, anchor="nw", text="Mot de passe", fill="#000000", font=("Inter", 15 * -1))

    button_image_8 = PhotoImage(file=relative_to_assets("button_8.png"))
    button_8 = Button(canvas,image=button_image_8, borderwidth=0, highlightthickness=0, command=lambda: enregistrer_ajout(entry_1,entry_3,entry_4,entry_5,entry_6,entry_7,entry_2), relief="flat", bg="#FFFFFF")
    button_8.place(x=816.0, y=500.70587158203125, width=170.99990844726562, height=24.29412841796875)

    def admin():
        window.withdraw()
        espace_admin()
    
    def enseignant():
        window.withdraw()
        admin_enseignant()
    
    def etudiant():
        window.withdraw()
        admin_etudiant()

    def cours():
        window.withdraw()
        admin_cours()
    
    def absence():
        window.withdraw()
        admin__absence()
    
    
    def on_deconnexion_click():
        window.destroy()
        admin_etudiant()

    window.resizable(False, False)
    window.mainloop()
def enregistrer_modification(Id_entry,nom_entry,Prenom_entry,Adresse_entry,Date_de_naissance_entry,mdp_entry,Année_Entrée_entry):
        idd = Id_entry.get()
        nom = nom_entry.get()
        prenom = Prenom_entry.get()
        adress = Adresse_entry.get()
        date = Date_de_naissance_entry.get()
        mdp = mdp_entry.get()
        ae = Année_Entrée_entry.get()
        if not idd or not nom or not prenom or not adress  or not date or not mdp or not ae:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
            return
    
        admin.modifier_student(file_path,user_database,idd,idd,nom,prenom,adress,date,mdp,ae)
   
        messagebox.showinfo("Succès", "Étudiant modifié avec succès.")
def admin_mod_etudiant():
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\version_finale\assets\frame18")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    window = tk.Toplevel(window_login)

    window.geometry("1000x550")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(window, bg="#FFFFFF", height=550, width=1000, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)
    canvas.create_rectangle(1.0, 3.0, 1002.0, 59.0, fill="#C4DFDF", outline="")

    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(915.0, 26.0, image=image_image_1)

    canvas.create_rectangle(0.0, 56.0, 285.0, 549.0, fill="#F0F0F0", outline="")

    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    button_1 = Button(canvas,image=button_image_1, borderwidth=0, highlightthickness=0, command=lambda: absence(), relief="flat")
    button_1.place(x=38.0, y=367.0, width=169.0, height=37.0)

    button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
    button_2 = Button(canvas,image=button_image_2, borderwidth=0, highlightthickness=0, command=lambda: print("button_5 clicked"), relief="flat")
    button_2.place(x=38.0, y=307.0, width=150.0, height=37.0)

    button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
    button_3 = Button(canvas,image=button_image_3, borderwidth=0, highlightthickness=0, command=lambda: cours(), relief="flat")
    button_3.place(x=35.0, y=251.0, width=179.0, height=33.0)

    button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
    button_4 = Button(canvas,image=button_image_4, borderwidth=0, highlightthickness=0, command=lambda: etudiant(), relief="flat")
    button_4.place(x=33.0, y=190.0, width=163.0, height=38.0)

    button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
    button_5 = Button(canvas,image=button_image_5, borderwidth=0, highlightthickness=0, command=lambda: enseignant(), relief="flat")
    button_5.place(x=31.0, y=136.0, width=170.0, height=37.0)

    image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(96.59716796875, 25.8587646484375, image=image_image_2)

    button_image_6 = PhotoImage(file=relative_to_assets("button_6.png"))
    button_6 = Button(canvas,image=button_image_6, borderwidth=0, highlightthickness=0, command=lambda: admin(), relief="flat")
    button_6.place(x=33.0, y=76.0, width=190.0, height=37.0)

    image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(321.0, 78.0, image=image_image_3)

    canvas.create_text(341.0, 66.0, anchor="nw", text="Modifier étudiant", fill="#116A7B", font=("Inter", 20 * -1))

    button_image_7 = PhotoImage(file=relative_to_assets("button_7.png"))
    button_7 = Button(canvas,image=button_image_7, borderwidth=0, highlightthickness=0, command=lambda: on_deconnexion_click(), relief="flat", bg="#FFFFFF")
    button_7.place(x=949.0, y=69.0, width=34.0, height=33.0)

    entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(611.0, 142.5, image=entry_image_1)
    entry_1 = Entry(canvas,bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0)
    entry_1.place(x=440.5, y=131.0, width=341.0, height=21.0)

    canvas.create_text(444.0, 107.0, anchor="nw", text="Id étudiant", fill="#000000", font=("Inter", 15 * -1))

    entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(611.0, 466.5, image=entry_image_2)
    entry_2 = Entry(canvas,bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0)
    entry_2.place(x=440.5, y=455.0, width=341.0, height=21.0)

    canvas.create_text(444.0, 431.0, anchor="nw", text="Année entrée", fill="#000000", font=("Inter", 15 * -1))

    entry_image_3 = PhotoImage(file=relative_to_assets("entry_3.png"))
    entry_bg_3 = canvas.create_image(611.0, 198.5, image=entry_image_3)
    entry_3 = Entry(canvas,bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0)
    entry_3.place(x=440.5, y=187.0, width=341.0, height=21.0)

    canvas.create_text(444.0, 163.0, anchor="nw", text="Nom", fill="#000000", font=("Inter", 15 * -1))

    entry_image_4 = PhotoImage(file=relative_to_assets("entry_4.png"))
    entry_bg_4 = canvas.create_image(611.0, 254.5, image=entry_image_4)
    entry_4 = Entry(canvas,bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0)
    entry_4.place(x=440.5, y=243.0, width=341.0, height=21.0)

    canvas.create_text(444.0, 219.0, anchor="nw", text="Prénom", fill="#000000", font=("Inter", 15 * -1))

    entry_image_5 = PhotoImage(file=relative_to_assets("entry_5.png"))
    entry_bg_5 = canvas.create_image(611.0, 310.5, image=entry_image_5)
    entry_5 = Entry(canvas,bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0)
    entry_5.place(x=440.5, y=299.0, width=341.0, height=21.0)

    canvas.create_text(444.0, 275.0, anchor="nw", text="Email", fill="#000000", font=("Inter", 15 * -1))

    entry_image_6 = PhotoImage(file=relative_to_assets("entry_6.png"))
    entry_bg_6 = canvas.create_image(611.0, 360.5, image=entry_image_6)
    entry_6 = Entry(canvas,bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0)
    entry_6.place(x=440.5, y=349.0, width=341.0, height=21.0)

    canvas.create_text(444.0, 325.0, anchor="nw", text="Date de naissance", fill="#000000", font=("Inter", 15 * -1))

    entry_image_7 = PhotoImage(file=relative_to_assets("entry_7.png"))
    entry_bg_7 = canvas.create_image(611.0, 416.5, image=entry_image_7)
    entry_7 = Entry(canvas,bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0)
    entry_7.place(x=440.5, y=405.0, width=341.0, height=21.0)

    canvas.create_text(444.0, 381.0, anchor="nw", text="Mot de passe", fill="#000000", font=("Inter", 15 * -1))

    button_image_8 = PhotoImage(file=relative_to_assets("button_8.png"))
    button_8 = Button(canvas,image=button_image_8, borderwidth=0, highlightthickness=0, command=lambda: enregistrer_modification(entry_1,entry_3,entry_4,entry_5,entry_6,entry_7,entry_2), relief="flat", bg="#FFFFFF")
    button_8.place(x=816.0, y=500.70587158203125, width=170.99990844726562, height=24.29412841796875)

    def admin():
        window.withdraw()
        espace_admin()
    
    def enseignant():
        window.withdraw()
        admin_enseignant()
    
    def etudiant():
        window.withdraw()
        admin_etudiant()

    def cours():
        window.withdraw()
        admin_cours()
    
    def absence():
        window.withdraw()
        admin__absence()
    
    
    def on_deconnexion_click():
        window.destroy()
        admin_etudiant()

    window.resizable(False, False)
    window.mainloop()
def enregistrer_suppression(nom_entry):
        nom = nom_entry.get()
        if not nom :
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
            return
    
        admin.suprimer_etudiant(file_path,user_database, nom)  
        messagebox.showinfo("Succès", "Étudiant supprimé avec succès.")
def admin_supp_etudiant():
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\version_finale\assets\frame19")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    window = tk.Toplevel(window_login)

    window.geometry("1000x550")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(window, bg="#FFFFFF", height=550, width=1000, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)
    canvas.create_rectangle(1.0, 3.0, 1002.0, 59.0, fill="#C4DFDF", outline="")

    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(915.0, 26.0, image=image_image_1)

    canvas.create_rectangle(0.0, 56.0, 285.0, 549.0, fill="#F0F0F0", outline="")

    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    button_1 = Button(canvas,image=button_image_1, borderwidth=0, highlightthickness=0, command=lambda: absence(), relief="flat")
    button_1.place(x=38.0, y=367.0, width=169.0, height=37.0)

    button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
    button_2 = Button(canvas,image=button_image_2, borderwidth=0, highlightthickness=0, command=lambda: print("button_5 clicked"), relief="flat")
    button_2.place(x=38.0, y=307.0, width=150.0, height=37.0)

    button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
    button_3 = Button(canvas,image=button_image_3, borderwidth=0, highlightthickness=0, command=lambda: cours(), relief="flat")
    button_3.place(x=35.0, y=251.0, width=179.0, height=33.0)

    button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
    button_4 = Button(canvas,image=button_image_4, borderwidth=0, highlightthickness=0, command=lambda: etudiant(), relief="flat")
    button_4.place(x=33.0, y=190.0, width=163.0, height=38.0)

    button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
    button_5 = Button(canvas,image=button_image_5, borderwidth=0, highlightthickness=0, command=lambda: enseignant(), relief="flat")
    button_5.place(x=31.0, y=136.0, width=170.0, height=37.0)

    image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(96.59716796875, 25.8587646484375, image=image_image_2)

    button_image_6 = PhotoImage(file=relative_to_assets("button_6.png"))
    button_6 = Button(canvas,image=button_image_6, borderwidth=0, highlightthickness=0, command=lambda: admin(), relief="flat")
    button_6.place(x=33.0, y=76.0, width=190.0, height=37.0)

    image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(321.0, 78.0, image=image_image_3)

    canvas.create_text(341.0, 66.0, anchor="nw", text="Supprimer étudiant", fill="#116A7B", font=("Inter", 20 * -1))

    button_image_7 = PhotoImage(file=relative_to_assets("button_7.png"))
    button_7 = Button(canvas,image=button_image_7, borderwidth=0, highlightthickness=0, command=lambda: on_deconnexion_click(), relief="flat",bg="#FFFFFF")
    button_7.place(x=949.0, y=69.0, width=34.0, height=33.0)

    entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(611.0, 223.5, image=entry_image_1)
    entry_1 = Entry(canvas,bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0)
    entry_1.place(x=440.5, y=212.0, width=341.0, height=21.0)

    canvas.create_text(444.0, 188.0, anchor="nw", text="Id étudiant", fill="#000000", font=("Inter", 15 * -1))

    button_image_8 = PhotoImage(file=relative_to_assets("button_8.png"))
    button_8 = Button(canvas,image=button_image_8, borderwidth=0, highlightthickness=0, command=lambda: enregistrer_suppression(entry_1), relief="flat",bg="#FFFFFF")
    button_8.place(x=526.0, y=291.0, width=170.99990844726562, height=24.29412841796875)

    def admin():
        window.withdraw()
        espace_admin()
    
    def enseignant():
        window.withdraw()
        admin_enseignant()
    
    def etudiant():
        window.withdraw()
        admin_etudiant()

    def cours():
        window.withdraw()
        admin_cours()
    
    def absence():
        window.withdraw()
        admin__absence()
    
    
    def on_deconnexion_click():
        window.destroy()
        admin_etudiant()

    window.resizable(False, False)
    window.mainloop()

def admin_etudiant():

    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\version_finale\assets\frame13")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    window = tk.Toplevel(window_login)

    window.geometry("1000x550")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(window, bg="#FFFFFF", height=550, width=1000, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)

    canvas.create_rectangle(1.0, 3.0, 1002.0, 59.0, fill="#C4DFDF", outline="")
    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(915.0, 26.0, image=image_image_1)

    canvas.create_rectangle(0.0, 56.0, 285.0, 549.0, fill="#F0F0F0", outline="")

    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    button_1 = Button(canvas,image=button_image_1, borderwidth=0, highlightthickness=0, command=lambda: absence(), relief="flat")
    button_1.place(x=38.0, y=367.0, width=169.0, height=37.0)

    button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
    button_2 = Button(canvas,image=button_image_2, borderwidth=0, highlightthickness=0, command=lambda: print("button_5 clicked"), relief="flat")
    button_2.place(x=38.0, y=307.0, width=150.0, height=37.0)

    button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
    button_3 = Button(canvas,image=button_image_3, borderwidth=0, highlightthickness=0, command=lambda: cours(), relief="flat")
    button_3.place(x=35.0, y=251.0, width=179.0, height=33.0)

    button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
    button_4 = Button(canvas,image=button_image_4, borderwidth=0, highlightthickness=0, command=lambda:etudiant(), relief="flat")
    button_4.place(x=33.0, y=190.0, width=163.0, height=38.0)

    button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
    button_5 = Button(canvas,image=button_image_5, borderwidth=0, highlightthickness=0, command=lambda: enseignant(), relief="flat")
    button_5.place(x=31.0, y=136.0, width=170.0, height=37.0)

    image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(96.5972900390625, 25.8587646484375, image=image_image_2)

    button_image_6 = PhotoImage(file=relative_to_assets("button_6.png"))
    button_6 = Button(canvas,image=button_image_6, borderwidth=0, highlightthickness=0, command=lambda: admin(), relief="flat")
    button_6.place(x=33.0, y=76.0, width=190.0, height=37.0)

    image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(321.0, 78.0, image=image_image_3)

    canvas.create_text(341.0, 66.0, anchor="nw", text="Etudiants", fill="#116A7B", font=("Inter", 20 * -1))

    button_image_7 = PhotoImage(file=relative_to_assets("button_7.png"))
    button_7 = Button(canvas,image=button_image_7, borderwidth=0, highlightthickness=0, command=lambda: sup_etudiant(), relief="flat", bg="#FFFFFF")
    button_7.place(x=504.80322265625, y=417.6153564453125, width=306.1968994140625, height=71.38461303710938)

    button_image_8 = PhotoImage(file=relative_to_assets("button_8.png"))
    button_8 = Button(canvas,image=button_image_8, borderwidth=0, highlightthickness=0, command=lambda: aj_etudiant(), relief="flat", bg="#FFFFFF")
    button_8.place(x=500.0, y=199.0, width=306.1968994140625, height=71.38461303710938)

    button_image_9 = PhotoImage(file=relative_to_assets("button_9.png"))
    button_9 = Button(canvas,image=button_image_9, borderwidth=0, highlightthickness=0, command=lambda: mod_etudiant(), relief="flat", bg="#FFFFFF")
    button_9.place(x=500.0, y=306.96923828125, width=306.1968994140625, height=71.38461303710938)

    button_image_10 = PhotoImage(file=relative_to_assets("button_10.png"))
    button_10 = Button(canvas,image=button_image_10, borderwidth=0, highlightthickness=0, command=lambda: on_deconnexion_click(), relief="flat", bg="#FFFFFF")
    button_10.place(x=949.0, y=69.0, width=34.0, height=33.0)

    button_image_11 = PhotoImage(file=relative_to_assets("button_11.png"))
    button_11 = Button(canvas,image=button_image_11, borderwidth=0, highlightthickness=0, command=lambda: view_csv(file_path), relief="flat", bg="#FFFFFF")
    button_11.place(x=499.0, y=102.0, width=307.0, height=71.0)

    def admin():
        window.withdraw()
        espace_admin()
    
    def enseignant():
        window.withdraw()
        admin_enseignant()
    
    def etudiant():
        window.withdraw()
        admin_etudiant()

    def cours():
        window.withdraw()
        admin_cours()
    
    def absence():
        window.withdraw()
        admin__absence()

    def aj_etudiant():
        window.withdraw()
        admin_aj_etudiant()
    
    def mod_etudiant():
        window.withdraw()
        admin_mod_etudiant()

    def sup_etudiant():
        window.withdraw()
        admin_supp_etudiant()

    def on_deconnexion_click():
        window.withdraw()
        espace_admin()

    window.resizable(False, False)
    window.mainloop()

def enregistrer_ajout_ens(Id_entry,nom_entry,Prenom_entry,Adresse_entry,Date_de_naissance_entry,mdp_entry,Année_Entrée_entry):
    #Id_entry,nom_entry,Prenom_entry,Adresse_entry,Date_de_naissance_entry,mdp_entry,Année_Entrée_entry
        idd = Id_entry.get()
        nom = nom_entry.get()
        prenom = Prenom_entry.get()
        adress = Adresse_entry.get()
        date = Date_de_naissance_entry.get()
        mdp = mdp_entry.get()
        ae = Année_Entrée_entry.get()
        if not idd or not nom or not prenom or not adress  or not date or not mdp or not ae:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
            return
    
        admin.ajouter_Professeur(file_path2,prof_database,idd,nom,prenom,adress,date,mdp,ae)
    
        messagebox.showinfo("Succès", "Professeur ajouté avec succès.")
def admin_aj_enseignant():
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\version_finale\assets\frame22")
    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    window = tk.Toplevel(window_login)
    window.geometry("1000x550")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(window, bg="#FFFFFF", height=550, width=1000, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)

    canvas.create_rectangle(1.0, 3.0, 1002.0, 59.0, fill="#C4DFDF", outline="")
    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(915.0, 26.0, image=image_image_1)

    canvas.create_rectangle(0.0, 56.0, 285.0, 549.0, fill="#F0F0F0", outline="")

    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    button_1 = Button(canvas,image=button_image_1, borderwidth=0, highlightthickness=0, command=lambda: absence(), relief="flat")
    button_1.place(x=38.0, y=367.0, width=169.0, height=37.0)

    button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
    button_2 = Button(canvas,image=button_image_2, borderwidth=0, highlightthickness=0, command=lambda: print("button_5 clicked"), relief="flat")
    button_2.place(x=38.0, y=307.0, width=150.0, height=37.0)

    button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
    button_3 = Button(canvas,image=button_image_3, borderwidth=0, highlightthickness=0, command=lambda: cours(), relief="flat")
    button_3.place(x=35.0, y=251.0, width=179.0, height=33.0)

    button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
    button_4 = Button(canvas,image=button_image_4, borderwidth=0, highlightthickness=0, command=lambda: etudiant(), relief="flat")
    button_4.place(x=33.0, y=190.0, width=163.0, height=38.0)

    button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
    button_5 = Button(canvas,image=button_image_5, borderwidth=0, highlightthickness=0, command=lambda: enseignant(), relief="flat")
    button_5.place(x=31.0, y=136.0, width=170.0, height=37.0)

    image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(96.59716796875, 25.8587646484375, image=image_image_2)

    button_image_6 = PhotoImage(file=relative_to_assets("button_6.png"))
    button_6 = Button(canvas,image=button_image_6, borderwidth=0, highlightthickness=0, command=lambda: admin(), relief="flat")
    button_6.place(x=33.0, y=76.0, width=190.0, height=37.0)

    image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(321.0, 78.0, image=image_image_3)

    canvas.create_text(341.0, 66.0, anchor="nw", text="Ajouter enseignant", fill="#116A7B", font=("Inter", 20 * -1))

    button_image_7 = PhotoImage(file=relative_to_assets("button_7.png"))
    button_7 = Button(canvas,image=button_image_7, borderwidth=0, highlightthickness=0, command=lambda: on_deconnexion_click(), relief="flat", bg="#FFFFFF")
    button_7.place(x=949.0, y=69.0, width=34.0, height=33.0)

    entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(611.0, 149.5, image=entry_image_1)
    entry_1 = Entry(canvas,bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0)
    entry_1.place(x=440.5, y=138.0, width=341.0, height=21.0)

    canvas.create_text(444.0, 114.0, anchor="nw", text="Id enseignant", fill="#000000", font=("Inter", 15 * -1))

    entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(611.0, 473.5, image=entry_image_2)
    entry_2 = Entry(canvas,bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0)
    entry_2.place(x=440.5, y=462.0, width=341.0, height=21.0)

    canvas.create_text(444.0, 438.0, anchor="nw", text="Module enseigné", fill="#000000", font=("Inter", 15 * -1))

    entry_image_3 = PhotoImage(file=relative_to_assets("entry_3.png"))
    entry_bg_3 = canvas.create_image(611.0, 205.5, image=entry_image_3)
    entry_3 = Entry(canvas,bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0)
    entry_3.place(x=440.5, y=194.0, width=341.0, height=21.0)

    canvas.create_text(444.0, 170.0, anchor="nw", text="Nom", fill="#000000", font=("Inter", 15 * -1))

    entry_image_4 = PhotoImage(file=relative_to_assets("entry_4.png"))
    entry_bg_4 = canvas.create_image(611.0, 261.5, image=entry_image_4)
    entry_4 = Entry(canvas,bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0)
    entry_4.place(x=440.5, y=250.0, width=341.0, height=21.0)

    canvas.create_text(444.0, 226.0, anchor="nw", text="Prénom", fill="#000000", font=("Inter", 15 * -1))

    entry_image_5 = PhotoImage(file=relative_to_assets("entry_5.png"))
    entry_bg_5 = canvas.create_image(611.0, 317.5, image=entry_image_5)
    entry_5 = Entry(canvas,bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0)
    entry_5.place(x=440.5, y=306.0, width=341.0, height=21.0)

    canvas.create_text(444.0, 282.0, anchor="nw", text="Email", fill="#000000", font=("Inter", 15 * -1))

    entry_image_6 = PhotoImage(file=relative_to_assets("entry_6.png"))
    entry_bg_6 = canvas.create_image(611.0, 367.5, image=entry_image_6)
    entry_6 = Entry(canvas,bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0)
    entry_6.place(x=440.5, y=356.0, width=341.0, height=21.0)

    canvas.create_text(444.0, 332.0, anchor="nw", text="Date de naissance", fill="#000000", font=("Inter", 15 * -1))

    entry_image_7 = PhotoImage(file=relative_to_assets("entry_7.png"))
    entry_bg_7 = canvas.create_image(611.0, 423.5, image=entry_image_7)
    entry_7 = Entry(canvas,bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0)
    entry_7.place(x=440.5, y=412.0, width=341.0, height=21.0)

    canvas.create_text(444.0, 388.0, anchor="nw", text="Mot de passe", fill="#000000", font=("Inter", 15 * -1))

    button_image_8 = PhotoImage(file=relative_to_assets("button_8.png"))
    button_8 = Button(canvas,image=button_image_8, borderwidth=0, highlightthickness=0, command=lambda: enregistrer_ajout_ens(entry_1,entry_3,entry_4,entry_5,entry_6,entry_7,entry_2), relief="flat", bg="#FFFFFF")
    button_8.place(x=816.0, y=500.70587158203125, width=170.99990844726562, height=24.29412841796875)

    def admin():
        window.withdraw()
        espace_admin()
    
    def enseignant():
        window.withdraw()
        admin_enseignant()
    
    def etudiant():
        window.withdraw()
        admin_etudiant()

    def cours():
        window.withdraw()
        admin_cours()
    
    def absence():
        window.withdraw()
        admin__absence()
    
    
    def on_deconnexion_click():
        window.destroy()
        admin_enseignant()

    window.resizable(False, False)
    window.mainloop()
def enregistrer_modification_ens(Id_entry,nom_entry,Prenom_entry,Adresse_entry,Date_de_naissance_entry,mdp_entry,Année_Entrée_entry):
        idd = Id_entry.get()
        nom = nom_entry.get()
        prenom = Prenom_entry.get()
        adress = Adresse_entry.get()
        date = Date_de_naissance_entry.get()
        mdp = mdp_entry.get()
        ae = Année_Entrée_entry.get()
        if not idd or not nom or not prenom or not adress  or not date or not mdp or not ae:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
            return
    
        admin.modifier_Professeur(file_path2,prof_database,idd,idd,nom,prenom,adress,date,mdp,ae)
   
        messagebox.showinfo("Succès", "Professeur modifié avec succès.")
def admin_mod_enseignant():
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\version_finale\assets\frame21")
    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    window = tk.Toplevel(window_login)

    window.geometry("1000x550")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(window, bg="#FFFFFF", height=550, width=1000, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)

    canvas.create_rectangle(1.0, 3.0, 1002.0, 59.0, fill="#C4DFDF", outline="")
    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(915.0, 26.0, image=image_image_1)

    canvas.create_rectangle(0.0, 56.0, 285.0, 549.0, fill="#F0F0F0", outline="")

    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    button_1 = Button(canvas,image=button_image_1, borderwidth=0, highlightthickness=0, command=lambda: absence(), relief="flat")
    button_1.place(x=38.0, y=367.0, width=169.0, height=37.0)

    button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
    button_2 = Button(canvas,image=button_image_2, borderwidth=0, highlightthickness=0, command=lambda: print("button_5 clicked"), relief="flat")
    button_2.place(x=38.0, y=307.0, width=150.0, height=37.0)

    button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
    button_3 = Button(canvas,image=button_image_3, borderwidth=0, highlightthickness=0, command=lambda: cours(), relief="flat")
    button_3.place(x=35.0, y=251.0, width=179.0, height=33.0)

    button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
    button_4 = Button(canvas,image=button_image_4, borderwidth=0, highlightthickness=0, command=lambda: etudiant(), relief="flat")
    button_4.place(x=33.0, y=190.0, width=163.0, height=38.0)

    button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
    button_5 = Button(canvas,image=button_image_5, borderwidth=0, highlightthickness=0, command=lambda: enseignant(), relief="flat")
    button_5.place(x=31.0, y=136.0, width=170.0, height=37.0)

    image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(96.59716796875, 25.8587646484375, image=image_image_2)

    button_image_6 = PhotoImage(file=relative_to_assets("button_6.png"))
    button_6 = Button(canvas,image=button_image_6, borderwidth=0, highlightthickness=0, command=lambda: admin(), relief="flat")
    button_6.place(x=33.0, y=76.0, width=190.0, height=37.0)

    image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(321.0, 78.0, image=image_image_3)

    canvas.create_text(341.0, 66.0, anchor="nw", text="Modifier enseignant", fill="#116A7B", font=("Inter", 20 * -1))

    button_image_7 = PhotoImage(file=relative_to_assets("button_7.png"))
    button_7 = Button(canvas,image=button_image_7, borderwidth=0, highlightthickness=0, command=lambda: on_deconnexion_click(), relief="flat", bg="#FFFFFF")
    button_7.place(x=949.0, y=69.0, width=34.0, height=33.0)

    entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(611.0, 142.5, image=entry_image_1)
    entry_1 = Entry(canvas,bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0)
    entry_1.place(x=440.5, y=131.0, width=341.0, height=21.0)

    canvas.create_text(444.0, 107.0, anchor="nw", text="Id enseignant", fill="#000000", font=("Inter", 15 * -1))

    entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(611.0, 466.5, image=entry_image_2)
    entry_2 = Entry(canvas,bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0)
    entry_2.place(x=440.5, y=455.0, width=341.0, height=21.0)

    canvas.create_text(444.0, 431.0, anchor="nw", text=" Module enseigné", fill="#000000", font=("Inter", 15 * -1))

    entry_image_3 = PhotoImage(file=relative_to_assets("entry_3.png"))
    entry_bg_3 = canvas.create_image(611.0, 198.5, image=entry_image_3)
    entry_3 = Entry(canvas,bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0)
    entry_3.place(x=440.5, y=187.0, width=341.0, height=21.0)

    canvas.create_text(444.0, 163.0, anchor="nw", text="Nom", fill="#000000", font=("Inter", 15 * -1))

    entry_image_4 = PhotoImage(file=relative_to_assets("entry_4.png"))
    entry_bg_4 = canvas.create_image(611.0, 254.5, image=entry_image_4)
    entry_4 = Entry(canvas,bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0)
    entry_4.place(x=440.5, y=243.0, width=341.0, height=21.0)

    canvas.create_text(444.0, 219.0, anchor="nw", text="Prénom", fill="#000000", font=("Inter", 15 * -1))

    entry_image_5 = PhotoImage(file=relative_to_assets("entry_5.png"))
    entry_bg_5 = canvas.create_image(611.0, 310.5, image=entry_image_5)
    entry_5 = Entry(canvas,bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0)
    entry_5.place(x=440.5, y=299.0, width=341.0, height=21.0)

    canvas.create_text(444.0, 275.0, anchor="nw", text="Email", fill="#000000", font=("Inter", 15 * -1))

    entry_image_6 = PhotoImage(file=relative_to_assets("entry_6.png"))
    entry_bg_6 = canvas.create_image(611.0, 360.5, image=entry_image_6)
    entry_6 = Entry(canvas,bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0)
    entry_6.place(x=440.5, y=349.0, width=341.0, height=21.0)

    canvas.create_text(444.0, 325.0, anchor="nw", text="Date de naissance", fill="#000000", font=("Inter", 15 * -1))

    entry_image_7 = PhotoImage(file=relative_to_assets("entry_7.png"))
    entry_bg_7 = canvas.create_image(611.0, 416.5, image=entry_image_7)
    entry_7 = Entry(canvas,bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0)
    entry_7.place(x=440.5, y=405.0, width=341.0, height=21.0)

    canvas.create_text(444.0, 381.0, anchor="nw", text="Mot de passe", fill="#000000", font=("Inter", 15 * -1))

    button_image_8 = PhotoImage(file=relative_to_assets("button_8.png"))
    button_8 = Button(canvas,image=button_image_8, borderwidth=0, highlightthickness=0, command=lambda: enregistrer_modification_ens(entry_1,entry_3,entry_4,entry_5,entry_6,entry_7,entry_2), relief="flat", bg="#FFFFFF")
    button_8.place(x=816.0, y=500.70587158203125, width=170.99990844726562, height=24.29412841796875)

    def admin():
        window.withdraw()
        espace_admin()
    
    def enseignant():
        window.withdraw()
        admin_enseignant()
    
    def etudiant():
        window.withdraw()
        admin_etudiant()

    def cours():
        window.withdraw()
        admin_cours()
    
    def absence():
        window.withdraw()
        admin__absence()
    
    
    def on_deconnexion_click():
        window.destroy()
        admin_enseignant()

    window.resizable(False, False)
    window.mainloop()
def enregistrer_suppression_ens(nom_entry):
        nom = nom_entry.get()
        if not nom :
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
            return
    
        admin.suprimer_Professeur(file_path2,prof_database, nom)  
        messagebox.showinfo("Succès", "Professeur supprimé avec succès.")
def admin_supp_enseignant():

    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\version_finale\assets\frame20")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    window = tk.Toplevel(window_login)

    window.geometry("1000x550")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(window, bg="#FFFFFF", height=550, width=1000, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)
    canvas.create_rectangle(1.0, 3.0, 1002.0, 59.0, fill="#C4DFDF", outline="")

    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(915.0, 26.0, image=image_image_1)

    canvas.create_rectangle(0.0, 56.0, 285.0, 549.0, fill="#F0F0F0", outline="")

    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    button_1 = Button(canvas,image=button_image_1, borderwidth=0, highlightthickness=0, command=lambda: absence(), relief="flat")
    button_1.place(x=38.0, y=367.0, width=169.0, height=37.0)

    button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
    button_2 = Button(canvas,image=button_image_2, borderwidth=0, highlightthickness=0, command=lambda: print("button_5 clicked"), relief="flat")
    button_2.place(x=38.0, y=307.0, width=150.0, height=37.0)

    button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
    button_3 = Button(canvas,image=button_image_3, borderwidth=0, highlightthickness=0, command=lambda: cours(), relief="flat")
    button_3.place(x=35.0, y=251.0, width=179.0, height=33.0)

    button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
    button_4 = Button(canvas,image=button_image_4, borderwidth=0, highlightthickness=0, command=lambda: etudiant(), relief="flat")
    button_4.place(x=33.0, y=190.0, width=163.0, height=38.0)

    button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
    button_5 = Button(canvas,image=button_image_5, borderwidth=0, highlightthickness=0, command=lambda: enseignant(), relief="flat")
    button_5.place(x=31.0, y=136.0, width=170.0, height=37.0)

    image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(96.59716796875, 25.8587646484375, image=image_image_2)

    button_image_6 = PhotoImage(file=relative_to_assets("button_6.png"))
    button_6 = Button(canvas,image=button_image_6, borderwidth=0, highlightthickness=0, command=lambda: admin(), relief="flat")
    button_6.place(x=33.0, y=76.0, width=190.0, height=37.0)

    image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(321.0, 78.0, image=image_image_3)

    canvas.create_text(341.0, 66.0, anchor="nw", text="Supprimer enseignant", fill="#116A7B", font=("Inter", 20 * -1))

    button_image_7 = PhotoImage(file=relative_to_assets("button_7.png"))
    button_7 = Button(canvas,image=button_image_7, borderwidth=0, highlightthickness=0, command=lambda: on_deconnexion_click(), relief="flat", bg='#FFFFFF')
    button_7.place(x=949.0, y=69.0, width=34.0, height=33.0)

    entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(611.0, 223.5, image=entry_image_1)
    entry_1 = Entry(canvas,bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0)
    entry_1.place(x=440.5, y=212.0, width=341.0, height=21.0)

    canvas.create_text(444.0, 188.0, anchor="nw", text="Id enseignant", fill="#000000", font=("Inter", 15 * -1))

    button_image_8 = PhotoImage(file=relative_to_assets("button_8.png"))
    button_8 = Button(canvas,image=button_image_8, borderwidth=0, highlightthickness=0, command=lambda: enregistrer_suppression_ens(entry_1), relief="flat", bg="#FFFFFF")
    button_8.place(x=526.0, y=291.0, width=170.99990844726562, height=24.29412841796875)

    def admin():
        window.withdraw()
        espace_admin()
    
    def enseignant():
        window.withdraw()
        admin_enseignant()
    
    def etudiant():
        window.withdraw()
        admin_etudiant()

    def cours():
        window.withdraw()
        admin_cours()
    
    def absence():
        window.withdraw()
        admin__absence()
    
    
    def on_deconnexion_click():
        window.destroy()
        admin_enseignant()

    window.resizable(False, False)
    window.mainloop()

def admin_enseignant():

    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\version_finale\assets\frame14")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    window = tk.Toplevel(window_login)
    window.geometry("1000x550")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(window, bg="#FFFFFF", height=550, width=1000, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)

    canvas.create_rectangle(1.0, 3.0, 1002.0, 59.0, fill="#C4DFDF", outline="")
    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(915.0, 26.0, image=image_image_1)

    canvas.create_rectangle(0.0, 56.0, 285.0, 549.0, fill="#F0F0F0", outline="")

    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    button_1 = Button(canvas,image=button_image_1, borderwidth=0, highlightthickness=0, command=lambda: absence(), relief="flat")
    button_1.place(x=38.0, y=367.0, width=169.0, height=37.0)

    button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
    button_2 = Button(canvas,image=button_image_2, borderwidth=0, highlightthickness=0, command=lambda: print("button_5 clicked"), relief="flat")
    button_2.place(x=38.0, y=307.0, width=150.0, height=37.0)

    button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
    button_3 = Button(canvas,image=button_image_3, borderwidth=0, highlightthickness=0, command=lambda: cours(), relief="flat")
    button_3.place(x=35.0, y=251.0, width=179.0, height=33.0)

    button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
    button_4 = Button(canvas,image=button_image_4, borderwidth=0, highlightthickness=0, command=lambda: etudiant(), relief="flat")
    button_4.place(x=33.0, y=190.0, width=163.0, height=38.0)

    button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
    button_5 = Button(canvas,image=button_image_5, borderwidth=0, highlightthickness=0, command=lambda: enseignant(), relief="flat")
    button_5.place(x=31.0, y=136.0, width=170.0, height=37.0)

    image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(96.59716796875, 25.8587646484375, image=image_image_2)

    button_image_6 = PhotoImage(file=relative_to_assets("button_6.png"))
    button_6 = Button(canvas,image=button_image_6, borderwidth=0, highlightthickness=0, command=lambda: admin(), relief="flat")
    button_6.place(x=33.0, y=76.0, width=190.0, height=37.0)

    image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(321.0, 78.0, image=image_image_3)

    canvas.create_text(341.0, 66.0, anchor="nw", text="Enseignants", fill="#116A7B", font=("Inter", 20 * -1))

    button_image_7 = PhotoImage(file=relative_to_assets("button_7.png"))
    button_7 = Button(canvas,image=button_image_7, borderwidth=0, highlightthickness=0, command=lambda: on_deconnexion_click(), relief="flat", bg="#FFFFFF")
    button_7.place(x=949.0, y=69.0, width=34.0, height=33.0)

    button_image_8 = PhotoImage(file=relative_to_assets("button_8.png"))
    button_8 = Button(canvas,image=button_image_8, borderwidth=0, highlightthickness=0, command=lambda: sup_ens(), relief="flat", bg="#FFFFFF")
    button_8.place(x=521.80322265625, y=418.6153564453125, width=306.1968994140625, height=71.38461303710938)

    button_image_9 = PhotoImage(file=relative_to_assets("button_9.png"))
    button_9 = Button(canvas,image=button_image_9, borderwidth=0, highlightthickness=0, command=lambda: aj_ens(), relief="flat", bg="#FFFFFF")
    button_9.place(x=517.0, y=200.0, width=306.1968994140625, height=71.38461303710938)

    button_image_10 = PhotoImage(file=relative_to_assets("button_10.png"))
    button_10 = Button(canvas,image=button_image_10, borderwidth=0, highlightthickness=0, command=lambda: mod_ens(), relief="flat", bg="#FFFFFF")
    button_10.place(x=517.0, y=307.96923828125, width=306.1968994140625, height=71.38461303710938)

    button_image_11 = PhotoImage(file=relative_to_assets("button_11.png"))
    button_11 = Button(canvas,image=button_image_11, borderwidth=0, highlightthickness=0, command=lambda: view_csv(file_path2), relief="flat", bg="#FFFFFF")
    button_11.place(x=516.0, y=103.0, width=307.0, height=71.0)

    def admin():
        window.withdraw()
        espace_admin()
    
    def enseignant():
        window.withdraw()
        admin_enseignant()
    
    def etudiant():
        window.withdraw()
        admin_etudiant()

    def cours():
        window.withdraw()
        admin_cours()
    
    def absence():
        window.withdraw()
        admin__absence()

    def aj_ens():
        window.withdraw()
        admin_aj_enseignant()
    
    def mod_ens():
        window.withdraw()
        admin_mod_enseignant()

    def sup_ens():
        window.withdraw()
        admin_supp_enseignant()

    def on_deconnexion_click():
        window.withdraw()
        espace_admin()
        
    window.resizable(False, False)
    window.mainloop()
def count_lines(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return sum(1 for line in file)-1
def espace_admin():
    window_login.withdraw()

    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\version_finale\assets\frame1")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    window = tk.Toplevel(window_login)
    window.geometry("1000x550")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(window, bg="#FFFFFF", height=550, width=1000, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)

    canvas.create_rectangle(1.0, 3.0, 1002.0, 59.0, fill="#C4DFDF", outline="")
    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(915.0, 26.0, image=image_image_1)

    canvas.create_rectangle(0.0, 56.0, 285.0, 549.0, fill="#F0F0F0", outline="")

    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    button_1 = Button(canvas, image=button_image_1, borderwidth=0, highlightthickness=0, command=lambda: absence(), relief="flat")
    button_1.place(x=20.0, y=367.0, width=169.0, height=37.0)

    button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
    button_2 = Button(canvas,image=button_image_2, borderwidth=0, highlightthickness=0, command=lambda: print("button_6 clicked"), relief="flat")
    button_2.place(x=20.0, y=307.0, width=150.0, height=37.0)

    button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
    button_3 = Button(canvas,image=button_image_3, borderwidth=0, highlightthickness=0, command=lambda: cours(), relief="flat")
    button_3.place(x=3.0, y=251.0, width=179.0, height=33.0)

    button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
    button_4 = Button(canvas,image=button_image_4, borderwidth=0, highlightthickness=0, command=lambda: etudiant(), relief="flat")
    button_4.place(x=25.0, y=190.0, width=163.0, height=38.0)

    button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
    button_5 = Button(canvas,image=button_image_5, borderwidth=0, highlightthickness=0, command=lambda: enseignant() , relief="flat")
    button_5.place(x=31.0, y=136.0, width=170.0, height=37.0)

    image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(96.5972900390625, 25.8587646484375, image=image_image_2)

    button_image_6 = PhotoImage(file=relative_to_assets("button_6.png"))
    button_6 = Button(canvas,image=button_image_6, borderwidth=0, highlightthickness=0, command=lambda: admin(), relief="flat")
    button_6.place(x=33.0, y=76.0, width=190.0, height=37.0)

    image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(321.0, 78.0, image=image_image_3)

    canvas.create_text(341.0, 66.0, anchor="nw", text="Page d’accueil", fill="#116A7B", font=("Inter", 20 * -1))

    button_image_7 = PhotoImage(file=relative_to_assets("button_7.png"))
    button_7 = Button(canvas,image=button_image_7, borderwidth=0, highlightthickness=0, command=lambda: etudiant(), relief="flat", bg="#FFFFFF")
    button_7.place(x=332.0, y=120.0, width=56.0, height=57.0)

    canvas.create_text(405.0, 125.0, anchor="nw", text=str(count_lines(file_path))+' Etudiants', fill="#116A7B", font=("Inter SemiBold", 24 * -1))

    button_image_8 = PhotoImage(file=relative_to_assets("button_8.png"))
    button_8 = Button(canvas,image=button_image_8, borderwidth=0, highlightthickness=0, command=lambda: enseignant(), relief="flat", bg="#FFFFFF")
    button_8.place(x=332.0, y=224.0, width=56.0, height=63.0)

    canvas.create_text(405.0, 232.0, anchor="nw", text=str(count_lines(file_path2))+" Enseignants", fill="#116A7B", font=("Inter SemiBold", 24 * -1))
    canvas.create_text(405.0, 343.0, anchor="nw", text="2 Cours", fill="#116A7B", font=("Inter SemiBold", 24 * -1))

    button_image_9 = PhotoImage(file=relative_to_assets("button_9.png"))
    button_9 = Button(canvas,image=button_image_9, borderwidth=0, highlightthickness=0, command=lambda: cours(), relief="flat", bg="#FFFFFF")
    button_9.place(x=332.0, y=338.0, width=56.0, height=57.0)

    def admin():
        window.withdraw()
        espace_admin()
    
    def enseignant():
        window.withdraw()
        admin_enseignant()
    
    def etudiant():
        window.withdraw()
        admin_etudiant()

    def cours():
        window.withdraw()
        admin_cours()
    
    def absence():
        admin__absence()
    
    
    def on_deconnexion_click():
        # Fermer la fenêtre d'accueil
        window.destroy()
        # Ouvrir la fenêtre de connexion
        window_login.deiconify()

  

    window.resizable(False, False)
    window.mainloop()

# Espaces des enseignants

def ajout_ens_note(Id_entry,nom_entry):
    #Id_entry,nom_entry,Prenom_entry,Adresse_entry,Date_de_naissance_entry,mdp_entry,Année_Entrée_entry
        idd = Id_entry.get()
        nom = nom_entry.get()

        
        if not idd or not nom   :
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
            return
    
        apo(entry_username.get()).ajouter_note(file_path,user_database,idd,nom)
    
        messagebox.showinfo("Succès", "Note ajoutée avec succès.")
def ens_aj_notes():
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\version_finale\assets\frame23")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)
    
    def on_deconnexion_click():
        window.withdraw()
        ens_notes()

    window = tk.Toplevel()

    window.geometry("1000x550")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(window, bg="#FFFFFF", height=550, width=1000, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)
    canvas.create_rectangle(1.0, 3.0, 1002.0, 59.0, fill="#C8BCC2", outline="")

    canvas.create_text(871.0, 20.0, anchor="nw", text="Enseignant", fill="#000000", font=("Inter", 20 * -1))

    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(96.59716796875, 25.8587646484375, image=image_image_1)

    image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(43.0, 78.0, image=image_image_2)

    canvas.create_text(63.0, 66.0, anchor="nw", text="Ajouter Note", fill="#3F2E3E", font=("Inter", 20 * -1))

    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    button_1 = Button(canvas,image=button_image_1, borderwidth=0, highlightthickness=0, command=lambda: on_deconnexion_click(), relief="flat", bg="#FFFFFF")
    button_1.place(x=940.0, y=66.0, width=34.0, height=33.0)

    entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(500.0, 166.5, image=entry_image_1)
    entry_1 = Entry(canvas,bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0)
    entry_1.place(x=329.5, y=155.0, width=341.0, height=21.0)

    canvas.create_text(333.0, 131.0, anchor="nw", text="Id étudiant", fill="#000000", font=("Inter", 15 * -1))

    entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(500.0, 222.5, image=entry_image_2)
    entry_2 = Entry(canvas,bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0)
    entry_2.place(x=329.5, y=211.0, width=341.0, height=21.0)

    canvas.create_text(333.0, 187.0, anchor="nw", text="Note", fill="#000000", font=("Inter", 15 * -1))

    button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
    button_2 = Button(canvas,image=button_image_2, borderwidth=0, highlightthickness=0, command=lambda: ajout_ens_note(entry_1,entry_2), relief="flat")
    button_2.place(x=415.0, y=267.0, width=170.99990844726562, height=24.29412841796875)
    

    window.resizable(False, False)
    window.mainloop()
def supp_ens_note(Id_entry):
    #Id_entry,nom_entry,Prenom_entry,Adresse_entry,Date_de_naissance_entry,mdp_entry,Année_Entrée_entry
        idd = Id_entry.get()

        
        if not idd   :
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
            return
    
        apo(entry_username.get()).ajouter_note(file_path,user_database,idd,"*")
    
        messagebox.showinfo("Succès", "Note modifiée avec succès.")
def ens_supp_notes():
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\version_finale\assets\frame25")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    window = tk.Toplevel(window_login)
    window.geometry("1000x550")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(window, bg="#FFFFFF", height=550, width=1000, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)
    canvas.create_rectangle(1.0, 3.0, 1002.0, 59.0, fill="#C8BCC2", outline="")

    canvas.create_text(871.0, 20.0, anchor="nw", text="Enseignant", fill="#000000", font=("Inter", 20 * -1))

    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(96.59716796875, 25.8587646484375, image=image_image_1)

    image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(43.0, 78.0, image=image_image_2)

    canvas.create_text(63.0, 66.0, anchor="nw", text="Supprimer Note", fill="#3F2E3E", font=("Inter", 20 * -1))

    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    button_1 = Button(canvas,image=button_image_1, borderwidth=0, highlightthickness=0, command=lambda: on_deconnexion_click(), relief="flat", bg="#FFFFFF")
    button_1.place(x=940.0, y=66.0, width=34.0, height=33.0)

    entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(496.0, 212.5, image=entry_image_1)
    entry_1 = Entry(canvas,bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0)
    entry_1.place(x=325.5, y=201.0, width=341.0, height=21.0)

    canvas.create_text(329.0, 177.0, anchor="nw", text="Id étudiant", fill="#000000", font=("Inter", 15 * -1))

    button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
    button_2 = Button(canvas,image=button_image_2, borderwidth=0, highlightthickness=0, command=lambda: supp_ens_note(entry_1), relief="flat", bg="#FFFFFF")
    button_2.place(x=415.0, y=267.0, width=170.99990844726562, height=24.29412841796875)

    def on_deconnexion_click():
        window.withdraw()
        ens_notes()

    window.resizable(False, False)
    window.mainloop()
def modif_ens_note(Id_entry,nom_entry):
    #Id_entry,nom_entry,Prenom_entry,Adresse_entry,Date_de_naissance_entry,mdp_entry,Année_Entrée_entry
        idd = Id_entry.get()
        nom = nom_entry.get()

        
        if not idd or not nom   :
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
            return
    
        apo(entry_username.get()).ajouter_note(file_path,user_database,idd,nom)
    
        messagebox.showinfo("Succès", "Note modifiée avec succès.")
def ens_mod_notes():
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\version_finale\assets\frame24")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    window = tk.Toplevel(window_login)

    window.geometry("1000x550")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(window, bg="#FFFFFF", height=550, width=1000, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)
    canvas.create_rectangle(1.0, 3.0, 1002.0, 59.0, fill="#C8BCC2", outline="")

    canvas.create_text(871.0, 20.0, anchor="nw", text="Enseignant", fill="#000000", font=("Inter", 20 * -1))

    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(96.59716796875, 25.8587646484375, image=image_image_1)

    image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(43.0, 78.0, image=image_image_2)

    canvas.create_text(63.0, 66.0, anchor="nw", text="Modifier Note", fill="#3F2E3E", font=("Inter", 20 * -1))

    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    button_1 = Button(canvas,image=button_image_1, borderwidth=0, highlightthickness=0, command=lambda: on_deconnexion_click(), relief="flat", bg="#FFFFFF")
    button_1.place(x=940.0, y=66.0, width=34.0, height=33.0)

    entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(500.0, 166.5, image=entry_image_1)
    entry_1 = Entry(canvas,bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0)
    entry_1.place(x=329.5, y=155.0, width=341.0, height=21.0)

    canvas.create_text(333.0, 131.0, anchor="nw", text="Id étudiant", fill="#000000", font=("Inter", 15 * -1))

    entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(500.0, 222.5, image=entry_image_2)
    entry_2 = Entry(canvas,bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0)
    entry_2.place(x=329.5, y=211.0, width=341.0, height=21.0)

    canvas.create_text(333.0, 187.0, anchor="nw", text="Note", fill="#000000", font=("Inter", 15 * -1))

    button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
    button_2 = Button(canvas,image=button_image_2, borderwidth=0, highlightthickness=0, command=lambda: modif_ens_note(entry_1,entry_2), relief="flat", bg="#FFFFFF")
    button_2.place(x=415.0, y=267.0, width=170.99990844726562, height=24.29412841796875)

    def on_deconnexion_click():
        window.withdraw()
        ens_notes()

    window.resizable(False, False)
    window.mainloop()

def ens_notes():
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\version_finale\assets\frame9")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    window = tk.Toplevel(window_login)

    window.geometry("1000x550")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(window, bg="#FFFFFF", height=550, width=1000, bd=0, highlightthickness=0, relief="ridge")

    canvas.place(x=0, y=0)
    canvas.create_rectangle(1.0, 3.0, 1002.0, 59.0, fill="#C8BCC2", outline="")
    canvas.create_text(871.0, 20.0, anchor="nw", text="Enseignant", fill="#000000", font=("Inter", 20 * -1))

    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(96.59716796875, 25.8587646484375, image=image_image_1)

    image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(43.0, 78.0, image=image_image_2)

    canvas.create_text(63.0, 66.0, anchor="nw", text="Notes", fill="#3F2E3E", font=("Inter", 20 * -1))

    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    button_1 = Button(canvas,image=button_image_1, borderwidth=0, highlightthickness=0,command=lambda: on_deconnexion_click(), relief="flat", bg="#FFFFFF")
    button_1.place(x=940.0, y=66.0, width=34.0, height=33.0)

    button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
    button_2 = Button(canvas, image=button_image_2, borderwidth=0, highlightthickness=0, command=lambda: aj_notes(), relief="flat", bg="#FFFFFF")
    button_2.place(x=355.0, y=117.0, width=341.0, height=84.0)

    button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
    button_3 = Button(canvas,image=button_image_3, borderwidth=0, highlightthickness=0, command=lambda: mod_notes(), relief="flat", bg="#FFFFFF")
    button_3.place(x=355.0, y=252.0, width=341.0, height=84.0)

    button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
    button_4 = Button(canvas,image=button_image_4, borderwidth=0, highlightthickness=0, command=lambda: sup_notes(), relief="flat", bg="#FFFFFF")
    button_4.place(x=345.0, y=383.0, width=370.0, height=90.0)

    def aj_notes():
        window.withdraw()
        ens_aj_notes()
    
    def mod_notes():
        window.withdraw()
        ens_mod_notes()
    
    def sup_notes():
        window.withdraw()
        ens_supp_notes()

    def on_deconnexion_click():
        window.withdraw()
        espace_professeur()

    window.resizable(False, False)
    window.mainloop()

def enregistrer_ajout_ens_abs(Id_entry,nom_entry,Prenom_entry,Adresse_entry):
    #Id_entry,nom_entry,Prenom_entry,Adresse_entry,Date_de_naissance_entry,mdp_entry,Année_Entrée_entry
        idd = Id_entry.get()
        nom = nom_entry.get()
        prenom = Prenom_entry.get()
        adress = Adresse_entry.get()
        
        if not idd or not nom or not prenom or not adress  :
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
            return
    
        apo(entry_username.get()).ajouter_absence(file_path3,abs_database,idd,nom,prenom,adress)
    
        messagebox.showinfo("Succès", "Absence ajouté avec succès.")
def ens_aj_abs():
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\version_finale\assets\frame6")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    window = tk.Toplevel(window_login)

    window.geometry("1000x550")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(window, bg="#FFFFFF", height=550, width=1000, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)
    canvas.create_rectangle(1.0, 3.0, 1002.0, 59.0, fill="#C8BCC2", outline="")

    canvas.create_text(871.0, 20.0, anchor="nw", text="Enseignant", fill="#000000", font=("Inter", 20 * -1))

    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(96.5972900390625, 25.8587646484375, image=image_image_1)

    image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(43.0, 78.0, image=image_image_2)

    canvas.create_text(63.0, 66.0, anchor="nw", text="Ajouter absence", fill="#3F2E3E", font=("Inter", 20 * -1))

    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    button_1 = Button(canvas,image=button_image_1, borderwidth=0, highlightthickness=0, command=lambda: on_deconnexion_click(), relief="flat", bg="#FFFFFF")
    button_1.place(x=940.0, y=66.0, width=34.0, height=33.0)

    entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(500.0, 166.5, image=entry_image_1)
    entry_1 = Entry(canvas,bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0)
    entry_1.place(x=329.5, y=155.0, width=341.0, height=21.0)

    canvas.create_text(333.0, 131.0, anchor="nw", text="Id étudiant", fill="#000000", font=("Inter", 15 * -1))

    entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(500.0, 222.5, image=entry_image_2)
    entry_2 = Entry(canvas,bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0)
    entry_2.place(x=329.5, y=211.0, width=341.0, height=21.0)

    canvas.create_text(333.0, 187.0, anchor="nw", text="Date d’absence", fill="#000000", font=("Inter", 15 * -1))

    entry_image_3 = PhotoImage(file=relative_to_assets("entry_3.png"))
    entry_bg_3 = canvas.create_image(500.0, 278.5, image=entry_image_3)
    entry_3 = Entry(canvas,bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0)
    entry_3.place(x=329.5, y=267.0, width=341.0, height=21.0)

    canvas.create_text(333.0, 243.0, anchor="nw", text="Justifiée (oui/non)", fill="#000000", font=("Inter", 15 * -1))

    entry_image_4 = PhotoImage(file=relative_to_assets("entry_4.png"))
    entry_bg_4 = canvas.create_image(500.0, 334.5, image=entry_image_4)
    entry_4 = Entry(canvas,bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0)
    entry_4.place(x=329.5, y=323.0, width=341.0, height=21.0)

    canvas.create_text(333.0, 299.0, anchor="nw", text="Nombre d’heures", fill="#000000", font=("Inter", 15 * -1))

    button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
    button_2 = Button(canvas,image=button_image_2, borderwidth=0, highlightthickness=0, command=lambda: enregistrer_ajout_ens_abs(entry_1,entry_2,entry_3,entry_4), relief="flat", bg="#FFFFFF")
    button_2.place(x=415.0, y=379.0, width=170.99990844726562, height=24.29412841796875)
    
    def on_deconnexion_click():
        window.withdraw()
        ens_absences()
    window.resizable(False, False)
    window.mainloop()
def enregistrer_modif_ens_abs(Id_entry,nom_entry,Prenom_entry,Adresse_entry):
    #Id_entry,nom_entry,Prenom_entry,Adresse_entry,Date_de_naissance_entry,mdp_entry,Année_Entrée_entry
        idd = Id_entry.get()
        nom = nom_entry.get()
        prenom = Prenom_entry.get()
        adress = Adresse_entry.get()
        
        if not idd or not nom or not prenom or not adress  :
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
            return
    
        apo(entry_username.get()).Modifier_absence(file_path3,abs_database,idd,nom,prenom,adress)
    
        messagebox.showinfo("Succès", "Absence modifié avec succès.")
def ens_mod_abs():
    
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\version_finale\assets\frame7")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    window = tk.Toplevel(window_login)

    window.geometry("1000x550")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(window, bg="#FFFFFF", height=550, width=1000, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)
    canvas.create_rectangle(1.0, 3.0, 1002.0, 59.0, fill="#C8BCC2", outline="")

    canvas.create_text(871.0, 20.0, anchor="nw", text="Enseignant", fill="#000000", font=("Inter", 20 * -1))

    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(96.5972900390625, 25.8587646484375, image=image_image_1)

    image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(43.0, 78.0, image=image_image_2)

    canvas.create_text(63.0, 66.0, anchor="nw", text="Modifier absence", fill="#3F2E3E", font=("Inter", 20 * -1))

    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    button_1 = Button(canvas,image=button_image_1, borderwidth=0, highlightthickness=0, command=lambda: on_deconnexion_click(), relief="flat",bg="#FFFFFF")
    button_1.place(x=940.0, y=66.0, width=34.0, height=33.0)

    entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(500.0, 166.5, image=entry_image_1)
    entry_1 = Entry(canvas,bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0)
    entry_1.place(x=329.5, y=155.0, width=341.0, height=21.0)

    canvas.create_text(333.0, 131.0, anchor="nw", text="Id étudiant", fill="#000000", font=("Inter", 15 * -1))

    entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(500.0, 222.5, image=entry_image_2)
    entry_2 = Entry(canvas,bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0)
    entry_2.place(x=329.5, y=211.0, width=341.0, height=21.0)

    canvas.create_text(333.0, 187.0, anchor="nw", text="Date d’absence", fill="#000000", font=("Inter", 15 * -1))

    entry_image_3 = PhotoImage(file=relative_to_assets("entry_3.png"))
    entry_bg_3 = canvas.create_image(500.0, 278.5, image=entry_image_3)
    entry_3 = Entry(canvas,bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0)
    entry_3.place(x=329.5, y=267.0, width=341.0, height=21.0)

    canvas.create_text(333.0, 243.0, anchor="nw", text="Justifiée (oui/non)", fill="#000000", font=("Inter", 15 * -1))

    entry_image_4 = PhotoImage(file=relative_to_assets("entry_4.png"))
    entry_bg_4 = canvas.create_image(500.0, 334.5, image=entry_image_4)
    entry_4 = Entry(canvas,bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0)
    entry_4.place(x=329.5, y=323.0, width=341.0, height=21.0)

    canvas.create_text(333.0, 299.0, anchor="nw", text="Nombre d’heures", fill="#000000", font=("Inter", 15 * -1))

    button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
    button_2 = Button(canvas,image=button_image_2, borderwidth=0, highlightthickness=0, command=lambda: enregistrer_modif_ens_abs(entry_1,entry_2,entry_3,entry_4), relief="flat", bg="#FFFFFF")
    button_2.place(x=415.0, y=379.0, width=170.99990844726562, height=24.29412841796875)

    def on_deconnexion_click():
        window.withdraw()
        ens_absences()

    window.resizable(False, False)
    window.mainloop()
def enregistrer_sup_ens_abs(Id_entry,nom_entry):
    #Id_entry,nom_entry,Prenom_entry,Adresse_entry,Date_de_naissance_entry,mdp_entry,Année_Entrée_entry
        idd = Id_entry.get()
        nom = nom_entry.get()
        
        if not idd or not nom   :
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
            return
    
        apo(entry_username.get()).supprimer_absence(file_path3,abs_database,idd,nom)
    
        messagebox.showinfo("Succès", "absence suprimée avec succès.")
def ens_supp_abs():
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\version_finale\assets\frame8")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    window = tk.Toplevel(window_login)
    window.geometry("1000x550")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(window, bg="#FFFFFF", height=550, width=1000, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)
    canvas.create_rectangle(1.0, 3.0, 1002.0, 59.0, fill="#C8BCC2", outline="")

    canvas.create_text(871.0, 20.0, anchor="nw", text="Enseignant", fill="#000000", font=("Inter", 20 * -1))

    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(96.5972900390625, 25.8587646484375, image=image_image_1)

    image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(43.0, 78.0, image=image_image_2)

    canvas.create_text(63.0, 66.0, anchor="nw", text="Supprimer absence", fill="#3F2E3E", font=("Inter", 20 * -1))

    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    button_1 = Button(canvas,image=button_image_1, borderwidth=0, highlightthickness=0, command=lambda: on_deconnexion_click(), relief="flat", bg="#FFFFFF")
    button_1.place(x=940.0, y=66.0, width=34.0, height=33.0)

    entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(500.0, 166.5, image=entry_image_1)
    entry_1 = Entry(canvas,bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0)
    entry_1.place(x=329.5, y=155.0, width=341.0, height=21.0)

    canvas.create_text(333.0, 131.0, anchor="nw", text="Id étudiant", fill="#000000", font=("Inter", 15 * -1))

    entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(500.0, 222.5, image=entry_image_2)
    entry_2 = Entry(canvas,bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0)
    entry_2.place(x=329.5, y=211.0, width=341.0, height=21.0)

    canvas.create_text(333.0, 187.0, anchor="nw", text="Date d’absence", fill="#000000", font=("Inter", 15 * -1))

    button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
    button_2 = Button(canvas,image=button_image_2, borderwidth=0, highlightthickness=0, command=lambda: enregistrer_sup_ens_abs(entry_1,entry_2), relief="flat", bg="#FFFFFF")
    button_2.place(x=415.0, y=267.0, width=170.99990844726562, height=24.29412841796875)

    def on_deconnexion_click():
        window.withdraw()
        ens_absences()

    window.resizable(False, False)
    window.mainloop()

def ens_absences():
    
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\version_finale\assets\frame5")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    window = tk.Toplevel(window_login)
    window.geometry("1000x550")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(window, bg="#FFFFFF", height=550, width=1000, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)
    canvas.create_rectangle(1.0, 3.0, 1002.0, 59.0, fill="#C8BCC2", outline="")

    canvas.create_text(871.0, 20.0, anchor="nw", text="Enseignant", fill="#000000", font=("Inter", 20 * -1))

    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(96.5972900390625, 25.8587646484375, image=image_image_1)

    image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(43.0, 78.0, image=image_image_2)

    canvas.create_text(63.0, 66.0, anchor="nw", text="Absences", fill="#3F2E3E", font=("Inter", 20 * -1))

    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    button_1 = Button(canvas,image=button_image_1, borderwidth=0, highlightthickness=0, command=lambda: on_deconnexion_click(), relief="flat", bg="#FFFFFF")
    button_1.place(x=940.0, y=66.0, width=34.0, height=33.0)

    button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
    button_2 = Button(canvas,image=button_image_2, borderwidth=0, highlightthickness=0, command=lambda: aj_abs(), relief="flat", bg="#FFFFFF")
    button_2.place(x=355.0, y=117.0, width=341.0, height=84.0)

    button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
    button_3 = Button(canvas,image=button_image_3, borderwidth=0, highlightthickness=0, command=lambda: mod_abs(), relief="flat", bg="#FFFFFF")
    button_3.place(x=355.0, y=252.0, width=341.0, height=84.0)

    button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
    button_4 = Button(canvas,image=button_image_4, borderwidth=0, highlightthickness=0, command=lambda: sup_abs(), relief="flat", bg="#FFFFFF")
    button_4.place(x=345.0, y=383.0, width=370.0, height=90.0)

    def aj_abs():
        window.withdraw()
        ens_aj_abs()
    
    def mod_abs():
        window.withdraw()
        ens_mod_abs()
    
    def sup_abs():
        window.withdraw()
        ens_supp_abs()

    def on_deconnexion_click():
        window.withdraw()
        espace_professeur()

    window.resizable(False, False)
    window.mainloop()

def ens_cours():
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r"C:\version_finale\assets\frame4")

    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    window = tk.Toplevel(window_login)
    window.geometry("1000x550")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(window, bg="#FFFFFF", height=550, width=1000, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)
    canvas.create_rectangle(1.0, 3.0, 1002.0, 59.0, fill="#C8BCC2", outline="")

    canvas.create_text(871.0, 20.0, anchor="nw", text="Enseignant", fill="#000000", font=("Inter", 20 * -1))

    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(96.5972900390625, 25.8587646484375, image=image_image_1)

    image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(43.0, 78.0, image=image_image_2)

    canvas.create_text(63.0, 66.0, anchor="nw", text="Cours", fill="#3F2E3E", font=("Inter", 20 * -1))

    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    button_1 = Button(canvas,image=button_image_1, borderwidth=0, highlightthickness=0, command=lambda: on_deconnexion_click(), relief="flat", bg="#FFFFFF")
    button_1.place(x=940.0, y=66.0, width=34.0, height=33.0)

    button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
    button_2 = Button(canvas,image=button_image_2, borderwidth=0, highlightthickness=0, command=lambda: prof.ajouter_cours_pdf(), relief="flat", bg="#FFFFFF")
    button_2.place(x=355.0, y=117.0, width=290.0, height=83.0)

    button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
    button_3 = Button(canvas,image=button_image_3, borderwidth=0, highlightthickness=0, command=lambda: prof.ajouter_cours_pdf(), relief="flat", bg="#FFFFFF")
    button_3.place(x=355.0, y=250.0, width=290.0, height=83.0)

    button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
    button_4 = Button(canvas,image=button_image_4, borderwidth=0, highlightthickness=0, command=lambda: print("button_4 clicked"), relief="flat", bg="#FFFFFF")
    button_4.place(x=350.0, y=383.0, width=290.0, height=83.0)


    def on_deconnexion_click():
        window.destroy()
        espace_professeur()

    window.resizable(False, False)
    window.mainloop()

def espace_professeur():
    window_login.withdraw()

    OUTPUT_PATH3 = Path(__file__).parent
    ASSETS_PATH3 = OUTPUT_PATH3 / Path(r"C:\version_finale\assets\frame3")

    def relative_to_assets3(path: str) -> Path:
        return ASSETS_PATH3 / Path(path)

    window = tk.Toplevel(window_login)
    window.geometry("1000x550")
    window.configure(bg="#FFFFFF")
    window.title("Page d'accueil")

    canvas = Canvas(window, bg="#FFFFFF", height=550, width=1000, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)
    canvas.create_rectangle(1.0, 3.0, 1002.0, 59.0, fill="#C8BCC2", outline="")

    canvas.create_text(871.0, 20.0, anchor="nw", text="Enseignant", fill="#000000", font=("Inter", 20 * -1))

    image_image_1 = PhotoImage(file=relative_to_assets3("image_1.png"))
    image_1 = canvas.create_image(96.5972900390625, 25.8587646484375, image=image_image_1)

    image_image_2 = PhotoImage(file=relative_to_assets3("image_2.png"))
    image_2 = canvas.create_image(43.0, 78.0, image=image_image_2)

    canvas.create_text(63.0, 66.0, anchor="nw", text="Page d’accueil", fill="#3F2E3E", font=("Inter", 20 * -1))

    button_image_1 = PhotoImage(file=relative_to_assets3("button_1.png"))
    button_1 = Button(canvas,image=button_image_1, borderwidth=0, highlightthickness=0, command=lambda: on_deconnexion_click(), relief="flat", bg="#FFFFFF")
    button_1.place(x=940.0, y=66.0, width=34.0, height=33.0)

    button_image_2 = PhotoImage(file=relative_to_assets3("button_2.png"))
    button_2 = Button(canvas,image=button_image_2, borderwidth=0, highlightthickness=0, command=lambda: cours(), relief="flat", bg="#FFFFFF")
    button_2.place(x=347.0, y=108.0, width=286.0, height=83.0)

    button_image_3 = PhotoImage(file=relative_to_assets3("button_3.png"))
    button_3 = Button(canvas,image=button_image_3, borderwidth=0, highlightthickness=0, command=lambda: notes(), relief="flat", bg="#FFFFFF")
    button_3.place(x=347.0, y=228.0, width=301.0, height=83.0)

    button_image_4 = PhotoImage(file=relative_to_assets3("button_4.png"))
    button_4 = Button(canvas,image=button_image_4, borderwidth=0, highlightthickness=0, command=lambda: absences(), relief="flat", bg="#FFFFFF")
    button_4.place(x=347.0, y=359.0, width=301.0, height=83.0)

    def cours():
        window.withdraw()
        ens_cours()
    
    def notes():
        window.withdraw()
        ens_notes()
    
    def absences():
        window.withdraw()
        ens_absences()
    
    def on_deconnexion_click():
        window.destroy()
        window_login.deiconify()

  

    window.resizable(False, False)
    window.mainloop()

# Fonction de vérification des informations d'authentification
def authenticate(username, password):
    return username in user_database and user_database[username]['mot_de_pass'] == password

def authenticate_admin(username, password):
    return username in admin_database and admin_database[username]['mot_de_pass'] == password

def authenticate_prof1(username, password):
    return username in prof_database and prof_database[username]['mot_de_pass'] == password

# Fonction d'authentification
def on_login():
    username = entry_username.get()
    password = entry_password.get()

    if authenticate(username, password):
        messagebox.showinfo("Authentification réussie", "Bienvenue, " + user_database[username]['Nom'] + "!")
        espace_etudiant()
        # Fermer la fenêtre de connexion
        window_login.withdraw()
    elif authenticate_admin(username, password):
        messagebox.showinfo("Authentification réussie", "Bienvenue, " + admin_database[username]['Nom'] + "!")
        espace_admin()
        # Fermer la fenêtre de connexion
        window_login.withdraw()
    elif authenticate_prof1(username, password):
        messagebox.showinfo("Authentification réussie", "Bienvenue, " + prof_database[username]['Nom'] + "!")
        espace_professeur()
        # Fermer la fenêtre de connexion
        window_login.withdraw()        
    else:
        messagebox.showerror("Erreur d'authentification", "Nom d'utilisateur ou mot de passe incorrect.")

# Fenêtre d'authentification
OUTPUT_PATH0 = Path(__file__).parent
ASSETS_PATH0 = OUTPUT_PATH0 / Path(r"C:\version_finale\assets\frame0")

def relative_to_assets0(path: str) -> Path:
    return ASSETS_PATH0 / Path(path)

window_login = Tk()
window_login.geometry("1000x550")
window_login.configure(bg="#FFFFFF")
window_login.title('Bienvenue !')

canvas = Canvas(window_login, bg="#FFFFFF", height=550, width=1000, bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)

entry_image_1 = PhotoImage(file=relative_to_assets0("entry_1.png"))
entry_bg_1 = canvas.create_image(688.5, 244.0, image=entry_image_1)
entry_username = Entry(bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0)
entry_username.place(x=496.0, y=227.0, width=385.0, height=32.0)



entry_image_2 = PhotoImage(file=relative_to_assets0("entry_2.png"))
entry_bg_2 = canvas.create_image(688.5, 369.0, image=entry_image_2)
entry_password = Entry(bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0, show="*")
entry_password.place(x=496.0, y=352.0, width=385.0, height=32.0)

canvas.create_text(480.0, 64.0, anchor="nw", text="Bienvenue !", fill="#116A7B", font=("Inter Bold", 50 * -1))
canvas.create_text(480.0, 133.0, anchor="nw", text="Connectez-vous à votre Eduportal", fill="#000000", font=("Inter", 15 * -1))
canvas.create_text(538.0, 187.0, anchor="nw", text="Username", fill="#116A7B", font=("Inter SemiBold", 20 * -1))
canvas.create_text(538.0, 310.0, anchor="nw", text="Password", fill="#116A7B", font=("Inter SemiBold", 20 * -1))

image_image_1 = PhotoImage(file=relative_to_assets0("image_1.png"))
image_1 = canvas.create_image(514.0, 200.0, image=image_image_1)

image_image_2 = PhotoImage(file=relative_to_assets0("image_2.png"))
image_2 = canvas.create_image(234.0, 271.0, image=image_image_2)

button_image_1 = PhotoImage(file=relative_to_assets0("button_1.png"))
button_1 = Button(image=button_image_1, borderwidth=0, highlightthickness=0, command=on_login, relief="flat", bg="#FFFFFF")
button_1.place(x=605.0, y=435.0, width=150.0, height=34.0)

image_image_3 = PhotoImage(file=relative_to_assets0("image_3.png"))
image_3 = canvas.create_image(515.0, 315.0, image=image_image_3)

window_login.resizable(False, False)
window_login.mainloop()
