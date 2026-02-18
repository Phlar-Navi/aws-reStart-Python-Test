import json
import math


def distance_interplanetaire(corps1, corps2, donnees_corps):
    """
    Calcule la distance approximative entre deux corps célestes
    basée sur leur distance au Soleil (en millions de km).
    Retourne la valeur absolue de la différence.
    """
    try:
        d1 = donnees_corps[corps1]["distance_soleil_mkm"]
        d2 = donnees_corps[corps2]["distance_soleil_mkm"]
        return abs(d1 - d2)
    except KeyError:
        raise ValueError(f"Corps céleste introuvable : {corps1} ou {corps2}")


def temps_trajet(distance_mkm, vitesse_km_s):
    """
    Calcule le temps de trajet en jours.
    distance en millions de km, vitesse en km/s.
    """
    if vitesse_km_s <= 0:
        raise ValueError("La vitesse doit être supérieure à 0.")

    distance_km = distance_mkm * 1_000_000
    temps_secondes = distance_km / vitesse_km_s
    temps_jours = temps_secondes / 86400

    return temps_jours


def delta_v(gravite_depart, gravite_arrivee, altitude_orbite_km):
    """
    Estimation simplifiée du delta-v nécessaire (en km/s).
    """
    if altitude_orbite_km <= 0:
        raise ValueError("Altitude invalide.")

    altitude_m = altitude_orbite_km * 1000

    dv_depart = math.sqrt(2 * gravite_depart * altitude_m)
    dv_arrivee = math.sqrt(2 * gravite_arrivee * altitude_m)

    return (dv_depart + dv_arrivee) / 1000  # conversion m/s → km/s


def poids_sur_corps(masse_kg, gravite_m_s2):
    """Calcule le poids (en Newtons) sur un corps céleste."""
    if masse_kg < 0:
        raise ValueError("La masse doit être positive.")
    return masse_kg * gravite_m_s2


def charger_corps_celestes(chemin="mission_data/corps_celestes.json"):
    """
    Charge le fichier des corps célestes.
    Transforme la liste JSON en dictionnaire indexé par nom.
    """
    try:
        with open(chemin, "r", encoding="utf-8") as file:
            data = json.load(file)

            if "corps_celestes" not in data:
                raise ValueError("Clé 'corps_celestes' manquante.")

            # 🔹 Transformation liste → dict indexé par nom
            corps_dict = {
                corps["nom"]: corps
                for corps in data["corps_celestes"]
            }

            return corps_dict

    except FileNotFoundError:
        raise FileNotFoundError(f"Fichier introuvable : {chemin}")
    except json.JSONDecodeError:
        raise ValueError("Erreur de décodage JSON.")
    except KeyError:
        raise ValueError("Format JSON invalide (clé 'nom' manquante).")

if __name__ == "__main__":
    corps = charger_corps_celestes()

    d = distance_interplanetaire("Terre", "Mars", corps)
    print(f"Distance Terre-Mars : {d} millions km")

    t = temps_trajet(d, 11.0)
    print(f"Temps de trajet à 11 km/s : {t:.0f} jours")

    gravite_mars = corps["Mars"]["gravite_m_s2"]
    print(f"Poids d'un astronaute (80 kg) sur Mars : {poids_sur_corps(80, gravite_mars):.1f} N")

    dv = delta_v(corps["Terre"]["gravite_m_s2"],
                 corps["Mars"]["gravite_m_s2"],
                 400)
    print(f"Delta-v estimé : {dv:.2f} km/s")
