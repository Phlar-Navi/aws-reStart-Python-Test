# Script de recensement des lignes contenant alertes,
# et de journalisation de ces dernieres

 # Le fichier a evaluer est fileName et 
 # le fichier a recevoir en sortie est fileDestName
def recense_alertes(fileName, fileDestName):
    print("~~~~~ DEBUT DE LA JOURNALISATION DES LIGNES CONTENANT \'Alerte\' ~~~~~\n")
    with open(fileName, 'r', encoding='UTF-8') as file:
        content = file.readlines()
        #print(list(content))
        print("::::: NOMBRE TOTAL DE LIGNES: ", len(content), "\n")
        journal = []
        for line in content:
            if ("Alerte" in line) | ("alerte" in line):
                print("::::: LIGNE CONTENANT ALERTE: ", line)
                journal.append(line)
        #print("CONTENU DU JOURNAL: ", journal)
        with open(fileDestName, 'w') as fileOut:
            fileOut.write("".join(journal))
            fileOut.close()
        file.close()
    print("\n~~~~~ JOURNALISATION DES ALERTES TERMINEE ~~~~~")
        


recense_alertes("mission_data/journal_bord.txt", "journal_bord_alertes.txt")