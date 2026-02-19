import json

fichier = "mission_data//missions.json"

def identifie_duree(missions):
    max = 0
    maxId = ""
    min = 100000
    minId = ""
    for element in missions:
        if (max < element['duree_jours']):
            max = element['duree_jours']
            maxId = element['id']
        if (min > element['duree_jours']):
            min = element['duree_jours']
            minId = element['id']   
    print("::::: Mission la plus longue: ", maxId)
    print("::::: Mission la plus courte: ", minId)

    """ for element in missions:
        if (element['id'] == maxId) | (element['id'] == minId):
            print(element) """

def charger(fileName):
    contenu={}
    with open(fileName, 'r', encoding="UTF-8") as file:
        contenu = json.load(file)
    return contenu

def afficher(missions):
    for element in missions:
        print(f"[{element['id']}] {element['nom']} -> {element['destination']} | {element['duree_jours']} jours | Equipage : {len(element['equipage'])} | Budget : {element['budget_millions_usd']} M$")

def budget_total(missions):
    sum = 0
    for element in missions:
        sum += element['budget_millions_usd']
    return sum

#missions = charger(fichier)
#tab_missions = missions["missions"]
#afficher(tab_missions)
#print("\n::::: Budget total de toutes les missions: ", budget_total(tab_missions), "M$")
#identifie_duree(tab_missions)
#print(missions["missions"]) # Apparament, ceci est un tableau d'objets....
