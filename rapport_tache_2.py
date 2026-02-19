import os

repertoire = "mission_data/"
# Cette fonction se charge de lister le contenu d'un repertoire
# avec la taille de ses elements
def listContent(nomRepertoire):
    contenu = os.listdir(nomRepertoire)
    print("::::: CONTENU DU REPERTOIRE")
    for file in contenu:
        print(f"- {file}      ({os.path.getsize(repertoire+file)/1000}) ")

# Cette fonction se contente de verifier le contenu d'un repertoire
# en l'occurence, celui de mission_data
def verify_and_list():
    if (os.path.exists(repertoire)):
        print("::::: LE REPERTOIRE \'mission_data\' EXISTE! ")
        #print("::::: VOICI DONC LES FICHIERS CONTENUS DANS LE DOSSIER: \n")
        #listContent(repertoire)
        create_directories(repertoire)
    else:
        print("!!!!! ERREUR! LE REPERTOIRE N'EXISTE PAS !")

def create_directories(chemin):
    if(os.path.exists(chemin)):
        if(os.path.exists(chemin+"rapports")):
            print("::::: LE REPERTOIRE \'rapports\' EXISTE DEJA -> PAS DE CFREATION")
        else:
            print("REPERTOIRE NON EXISTANT -> CREATION")
            os.mkdir("mission_data/rapports")
    if(os.path.exists(chemin)):
        if(os.path.exists(chemin+"archives")):
            print("::::: LE REPERTOIRE \'rapports\' EXISTE DEJA -> PAS DE CFREATION")
        else:
            print("REPERTOIRE NON EXISTANT -> CREATION")
            os.mkdir("mission_data/archives")
    listContent(chemin)

#verify_and_list()