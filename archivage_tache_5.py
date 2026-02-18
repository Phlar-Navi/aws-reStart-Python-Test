import os
import datetime

chemin1 = "mission_data/"
chemin2 = "archives/"
journal = "journal_bord"
time = datetime.datetime.now()

cheminFichier = "mission_data/rapports/rapport_systeme.txt"
# print(datetime.datetime.now())
#print(os.path.join(chemin1, chemin2))
chemin = os.path.join(chemin1, chemin2)

print(type(os.environ))
print(shutil.disk_usage())

def archiver():
    print("::::: DEBUT DE L'ARCHIVAGE")
    cheminOrigine = os.path.join(chemin1, journal+".txt")
    cheminDest = os.path.join(chemin1, chemin2, journal+"_"+str(time))
    os.system(f"cp {cheminOrigine} {cheminDest}")

def creer_fichier():
    with open(cheminFichier, 'w') as file:
        content = os.getcwd()
        listVar = os.environ()

archiver()
