import os
import json
from datetime import datetime
from exceptions import *
from validation_tache_9 import valider_mission, verifier_carburant
from navigation_tache_8 import (
    charger_corps_celestes,
    distance_interplanetaire,
    temps_trajet,
    delta_v,
    poids_sur_corps
)
from evaluate_missions_tache_3 import charger, afficher, budget_total
from ajouter_mission_tache_6 import ajouter_mission
from analyse_tache_7 import analyser_telemetrie
from rapport_tache_2 import listContent


MISSIONS_PATH = "mission_data/missions.json"
TELEMETRIE_PATH = "mission_data/telemetries.json"
CORPS_PATH = "mission_data/corps_celestes.json"
JOURNAL_PATH = "mission_data/journal_bord.txt"
RAPPORTS_PATH = "mission_data/rapports"
LOG_PATH = os.path.join(RAPPORTS_PATH, "log_controle.txt")


def log_action(message):
    os.makedirs(RAPPORTS_PATH, exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] {message}\n")

def details_mission():
    try:
        mission_id = input("ID mission : ").strip()
        missions = charger(MISSIONS_PATH)
        corps = charger_corps_celestes()

        mission = next((m for m in missions if m["id"] == mission_id), None)
        if not mission:
            print("Mission introuvable.")
            return

        print(json.dumps(mission, indent=2))

        dest = mission["destination"]
        if dest in corps:
            gravite = corps[dest]["gravite_m_s2"]
            poids = poids_sur_corps(80, gravite)
            print(f"Poids d'un astronaute (80kg) sur {dest} : {poids:.1f} N")

        log_action(f"Détails mission {mission_id}")

    except Exception as e:
        print(e)

def telemetrie_realtime():
    try:
        data = charger(TELEMETRIE_PATH)
        if not data:
            print("Aucune donnée télémétrique disponible.")
            return

        if isinstance(data, list):
            releves = data
        elif isinstance(data, dict) and "releves" in data:
            releves = data["releves"]
        else:
            print("Format télémétrie invalide.")
            return

        if not releves:
            print("Aucun relevé disponible.")
            return

        dernier = releves[-1]

        carburant = dernier.get("carburant_pct")
        phase = dernier.get("phase", "inconnue")
        altitude = dernier.get("altitude_km", "?")
        vitesse = dernier.get("vitesse_km_s", "?")

        if carburant is None:
            raise CarburantError("Champ carburant_pct manquant.")

        if carburant > 50:
            indicateur = "🟢"
        elif 20 <= carburant <= 50:
            indicateur = "🟡"
        else:
            indicateur = "🔴"

        print("\n=== TÉLÉMÉTRIE EN TEMPS RÉEL ===")
        print(f"{indicateur} Phase      : {phase}")
        print(f"   Altitude   : {altitude} km")
        print(f"   Vitesse    : {vitesse} km/s")
        print(f"   Carburant  : {carburant}%")

        verifier_carburant(dernier)

        log_action("Consultation télémétrie temps réel")

    except CarburantError as e:
        print(f"🔴 ALERTE CARBURANT : {e}")
        log_action("Alerte carburant critique")
    except Exception as e:
        print("Erreur télémétrie :", e)

def calcul_navigation():
    try:
        corps = charger_corps_celestes()
        depart = input("Départ : ")
        arrivee = input("Arrivée : ")

        distance = distance_interplanetaire(depart, arrivee, corps)
        temps = temps_trajet(distance, 11)

        dv = delta_v(
            corps[depart]["gravite_m_s2"],
            corps[arrivee]["gravite_m_s2"],
            400
        )

        print(f"Distance : {distance} Mkm")
        print(f"Temps estimé : {temps:.0f} jours")
        print(f"Delta-v estimé : {dv:.2f} km/s")

        log_action(f"Calcul navigation {depart} → {arrivee}")

    except Exception as e:
        print(e)

def recherche_journal():
    try:
        mot = input("Mot-clé : ").lower()
        with open(JOURNAL_PATH, "r", encoding="utf-8") as f:
            lignes = f.readlines()

        resultats = [l for l in lignes if mot in l.lower()]

        print(f"{len(resultats)} résultat(s)")
        for r in resultats:
            print(r.strip())

        log_action(f"Recherche journal : {mot}")

    except Exception as e:
        print(e)

def generer_rapport():
    missions = charger(MISSIONS_PATH)
    telem = charger(TELEMETRIE_PATH)

    rapport = {
        "date_generation": str(datetime.now()),
        "nb_missions": len(missions),
        "nb_releves": len(telem)
    }

    path = os.path.join(RAPPORTS_PATH, "rapport_complet.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(rapport, f, indent=2)

    print("✅ Rapport généré.")
    log_action("Génération rapport complet")

def afficher_menu():
    print("""
╔══════════════════════════════════════════════════╗
║       🚀 CENTRE DE CONTRÔLE DE MISSION 🚀       ║
╠══════════════════════════════════════════════════╣
║  1. Afficher toutes les missions                 ║
║  2. Détails d'une mission (par ID)               ║
║  3. Ajouter une nouvelle mission                 ║
║  4. Télémétrie en temps réel                     ║
║  5. Calculateur de navigation                    ║
║  6. Diagnostic système                           ║
║  7. Recherche dans le journal de bord            ║
║  8. Générer un rapport complet (JSON)            ║
║  9. Arborescence des fichiers mission            ║
║  0. Quitter                                      ║
╚══════════════════════════════════════════════════╝
""")
    
def main():
    while True:
        afficher_menu()
        choix = input("Choix : ")

        try:
            if choix == "1":
                missions = charger(MISSIONS_PATH)
                tab_missions = missions["missions"]
                afficher(tab_missions)
            elif choix == "2":
                missions = charger(MISSIONS_PATH)
                tab_missions = missions["missions"]
                details_mission()
            elif choix == "3":
                nouvelle = {
                    "id": input("ID : "),
                    "nom": input("Nom : "),
                    "destination": input("Destination : "),
                    "date_lancement": input("Date (YYYY-MM-DD) : "),
                    "statut": input("Statut : "),
                    "equipage": [],
                    "duree_jours": int(input("Durée (jours) : ")),
                    "budget_millions_usd": float(input("Budget (M$) : "))
                }
                ajouter_mission(MISSIONS_PATH, nouvelle)
            elif choix == "4":
                telemetrie_realtime()
            elif choix == "5":
                calcul_navigation()
            elif choix == "6":
                analyser_telemetrie(TELEMETRIE_PATH)
            elif choix == "7":
                recherche_journal()
            elif choix == "8":
                generer_rapport()
            elif choix == "9":
                listContent("mission_data/")
            elif choix == "0":
                print("Fin du programme.")
                break
            else:
                print("Choix invalide.")
        except Exception as e:
            print("Erreur :", e)


main()