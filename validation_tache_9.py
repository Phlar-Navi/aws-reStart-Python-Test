from datetime import datetime
from exceptions import *
from navigation_tache_8 import distance_interplanetaire, charger_corps_celestes


def valider_mission(mission_dict):
    champs_obligatoires = {
        "id",
        "nom",
        "destination",
        "date_lancement",
        "statut",
        "equipage",
        "duree_jours",
        "budget_millions_usd"
    }

    champs_manquants = champs_obligatoires - mission_dict.keys()
    if champs_manquants:
        raise MissionDataError(
            f"Champs manquants : {', '.join(champs_manquants)}"
        )

    if mission_dict["duree_jours"] <= 0:
        raise MissionDataError("La durée doit être positive.")

    if mission_dict["budget_millions_usd"] <= 0:
        raise MissionDataError("Le budget doit être positif.")

    try:
        datetime.fromisoformat(mission_dict["date_lancement"])
    except ValueError:
        raise MissionDataError("Format de date invalide (attendu YYYY-MM-DD).")

    corps_connus = charger_corps_celestes()

    destination = mission_dict["destination"]

    if destination in corps_connus:
        distance = distance_interplanetaire(
            "Terre",
            destination,
            corps_connus
        )

        distance_km = distance * 1_000_000
        temps_estime_jours = (distance_km / 11) / 86400

        if mission_dict["duree_jours"] > temps_estime_jours * 10:
            raise TrajectoireError(
                "Durée incohérente par rapport à la distance estimée."
            )

    return True


def verifier_carburant(releve):
    if "carburant_pct" not in releve:
        raise CarburantError("Champ carburant_pct manquant.")

    niveau = releve["carburant_pct"]

    if niveau < 10:
        raise CarburantError(
            f"Niveau critique ({niveau}%) en phase {releve.get('phase', '?')}"
        )

    elif niveau < 30:
        print(
            f" Warning : carburant faible ({niveau}%) "
            f"phase {releve.get('phase', '?')}"
        )

    return True

""" # Cas valide
try:
    valider_mission({
        "id": "MSN-001",
        "nom": "Test",
        "destination": "Mars",
        "date_lancement": "2028-01-01",
        "statut": "planifiée",
        "equipage": [],
        "duree_jours": 680,
        "budget_millions_usd": 5000
    })
    print("✅ Mission valide")

except NavigationError as e:
    print(f"❌ {type(e).__name__}: {e}")


# Cas invalide : durée négative
try:
    valider_mission({
        "id": "MSN-999",
        "nom": "Bad",
        "destination": "Lune",
        "date_lancement": "2028-01-01",
        "statut": "test",
        "equipage": [],
        "duree_jours": -5,
        "budget_millions_usd": 100
    })
except NavigationError as e:
    print(f"❌ {type(e).__name__}: {e}")


# Cas carburant critique
try:
    verifier_carburant({
        "carburant_pct": 7.5,
        "phase": "approche_mars"
    })
except CarburantError as e:
    print(f"🔴 {e}")

 """