import json

def charger_json_securise(chemin):
    try:
        with open(chemin, "r+", encoding="UTF-8") as file:
            print("::::: OUVERTURE EN COURS...")
            try:
                content = json.load(file)
                print("::::: Missions.json charge avec succes (5 missions)")
                return content
            except:
                print("!!!!! JSON invalide dans mission_data/corrompu.json")
                return None
    except FileNotFoundError:
        print("!!!!! Fichier introuvable: mission_data/fantome.json")
        return None
        

# Cas 1 : fichier normal
# data = charger_json_securise("mission_data/missions.json")
# print(data)

# Cas 2 : fichier inexistant
# data = charger_json_securise("mission_data/fantome.json")

# Cas 3 : créez un fichier corrompu pour tester
# with open("mission_data/corrompu.json", "w") as f:
    # f.write("{nom: valeur_sans_guillemets}")
# data = charger_json_securise("mission_data/corrompu.json")