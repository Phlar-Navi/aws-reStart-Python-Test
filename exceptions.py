class NavigationError(Exception):
    """Classe de base pour les erreurs de navigation spatiale."""
    pass


class MissionDataError(NavigationError):
    """Données de mission invalides ou incomplètes."""
    pass


class TrajectoireError(NavigationError):
    """Paramètres de trajectoire invalides."""
    pass


class CarburantError(NavigationError):
    """Niveau de carburant critique ou invalide."""
    pass
