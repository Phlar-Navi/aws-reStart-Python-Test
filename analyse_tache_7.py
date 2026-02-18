import json
from datetime import datetime
from pathlib import Path

chemin = "mission_data/telemetries.json"

def analyser_telemetrie(chemin_json):
    with open(chemin_json, 'r', encoding="UTF-8") as file:
        content = json.load(file)
        telemetries = content["releves"]
        file.close()

        print("\nPhase          | Altitude          | Vitesse          | Carburant")
        print("-----------------|-------------------|------------------|----------")

        alertes_detectees = []

        premier_releve = telemetries[0]
        dernier_releve = telemetries[-1]

        for telemetrie in telemetries:
            phase = telemetrie["phase"]
            altitude = f"{telemetrie['altitude_km']:,}".replace(",", " ") + " km"
            vitesse = f"{telemetrie['vitesse_km_s']} km/s"
            carburant = f"{telemetrie['carburant_pct']}%"

        alertes = []
        for systeme, statut in telemetrie["systemes"].items():
            if statut != "nominal":
                alertes.append(systeme)

        if alertes:
            alertes_str = ", ".join(alertes)
            alertes_detectees.append({
                "timestamp": telemetrie["timestamp"],
                "phase": phase,
                "systemes_en_alerte": alertes
            })
        else:
            alertes_str = "-"

        print(f"{phase:<20}| {altitude:<15}| {vitesse:<9}| {carburant:<9}| {alertes_str}")

    date_debut = datetime.fromisoformat(premier_releve["timestamp"])
    date_fin = datetime.fromisoformat(dernier_releve["timestamp"])

    duree_jours = (date_fin - date_debut).total_seconds() / 86400

    carburant_debut = premier_releve["carburant_pct"]
    carburant_fin = dernier_releve["carburant_pct"]

    consommation_totale = carburant_debut - carburant_fin
    consommation_moyenne = consommation_totale / duree_jours if duree_jours > 0 else 0

    print("\nConsommation moyenne de carburant : "
          f"{consommation_moyenne:.2f}% par jour")

    dossier_rapport = Path("mission_data/rapports")
    dossier_rapport.mkdir(parents=True, exist_ok=True)

    chemin_sortie = dossier_rapport / "alertes_systemes.json"

    with open(chemin_sortie, "w", encoding="utf-8") as file:
        json.dump(alertes_detectees, file, indent=2, ensure_ascii=False)

    print(f"\n {len(alertes_detectees)} relevé(s) avec alerte sauvegardé(s) dans {chemin_sortie}")

#analyser_telemetrie(chemin)


            