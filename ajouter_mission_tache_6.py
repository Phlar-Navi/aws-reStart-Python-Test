import json
chemin = "mission_data/missions.json"
nouvChemin = "mission_data/missions_deux.json"
def ajouter_mission(chemin_json, nouvelle_mission):
    with open(chemin_json, 'r', encoding="UTF-8") as file:
        content = json.load(file)
        
        missions = content["missions"]
        file.close()
        #print(missions)
        existe = False
        for element in missions:
            if (element["id"] == nouvelle_mission["id"]):
                print("L\'IDENTIFIANT\' EXISTE DEJA")
                existe = True
                break

        if (existe==False):
            missions.append(nouvelle_mission)
            
            with open(chemin_json, 'w', encoding="UTF-8") as fileWrite:
                json.dump(content, fileWrite, indent=2, ensure_ascii=False)
                print('::::: NOUVELLE VALEUR AJOUTEE')

def supprimer_mission(chemin_json, id_mission):
    with open(chemin_json, 'r', encoding="UTF-8") as file:
        content = json.load(file)
        
        missions = content["missions"]
        file.close()
        #print(missions)
        mission_trouvee = None

        for element in missions:
            if (element["id"] == id_mission):
                print("MISSION TROUVEE: ", element)
                mission_trouvee = element
                break

        if (mission_trouvee is not None):
            confirmation = input("Voulez-vous vraiment supprimer cette mission? (O/N): ")
            if confirmation.upper() == 'O':
                missions.remove(mission_trouvee)
                with open(chemin_json, 'w', encoding="UTF-8") as fileWrite:
                    json.dump(content, fileWrite, indent=2, ensure_ascii=False)
                    print('::::: MISSION SUPPRIMEE')
            else:
                print("::::: SUPPRESSION ANNULEE")

""" ajouter_mission(chemin, {
      "id": "MSN-006",
      "nom": "Artemis IV",
      "destination": "Lune",
      "date_lancement": "2026-09-15",
      "statut": "planifiée",
      "equipage": ["Cmdt. Elena Vasquez", "Dr. Kenji Tanaka", "Ing. Fatou Diallo"],
      "duree_jours": 21,
      "budget_millions_usd": 4200
    },) """