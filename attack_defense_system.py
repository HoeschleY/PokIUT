import random

class Attack:
    """
    Classe représentant une attaque physique dans le jeu.

    Attributs :
    -----------
    name : str
        Nom de l’attaque (ex : "Coup d'épée", "Coup de poing").
    power : int
        Niveau de puissance de l’attaque (0-100).
    accuracy : int
        Taux de précision de l’attaque (0-100).

    Méthodes :
    ----------
    attempt(attacker, defender):
        Tente d'effectuer une attaque sur le défenseur et retourne les dégâts infligés.
    """

    def __init__(self, name: str, power: int, accuracy: int):
        assert 0 <= power <= 100, "La puissance doit être entre 0 et 100."
        assert 0 <= accuracy <= 100, "La précision doit être entre 0 et 100."

        self.name = name
        self.power = power
        self.accuracy = accuracy

    def attempt(self, attacker, defender):
        """
        Simule une tentative d’attaque entre deux personnages.

        Paramètres :
        ------------
        attacker : objet avec attributs 'name', 'attack'
        defender : objet avec attributs 'name', 'defense', 'hp', 'is_defending'

        Retourne :
        -----------
        int : les dégâts infligés (0 si raté)
        """
        print(f"\n{attacker.name} utilise {self.name} contre {defender.name} !")

        # Vérifie si l’attaque touche
        hit_chance = random.randint(1, 100)
        if hit_chance > self.accuracy:
            print("❌ L’attaque échoue !")
            return 0

        # Calcule les dégâts physiques
        damage = (attacker.attack * self.power / 100) - (defender.defense / 2)

        # Si le défenseur est en posture défensive, on réduit les dégâts
        if getattr(defender, "is_defending", False):
            print(f"🛡️ {defender.name} se défend ! Les dégâts sont réduits de moitié.")
            damage /= 2
            defender.is_defending = False  # La défense ne dure qu'un tour

        # Minimum 1 point de dégâts
        damage = max(1, int(damage))
        defender.hp = max(0, defender.hp - damage)

        print(f"✅ L’attaque réussit ! {defender.name} perd {damage} PV (PV restants : {defender.hp})")
        return damage


class Defense:
    """
    Classe représentant une action défensive.
    Permet au personnage de réduire les dégâts reçus lors de la prochaine attaque.

    Méthodes :
    ----------
    activate(character):
        Active la posture défensive du personnage.
    """

    @staticmethod
    def activate(character):
        """
        Active la posture défensive du personnage.
        Réduit les dégâts reçus de moitié lors de la prochaine attaque.
        """
        character.is_defending = True
        print(f"\n{character.name} adopte une posture défensive 🛡️ (dégâts subis réduits au prochain tour).")


def calcul_precision(attaque):
    import random

    precision_reelle = random.randint(0, 100)
    if attaque["accuracy"] >= precision_reelle:
        return(True)
    else:
        return(False)

def calcul_degats(attaquant, defenseur, attaque):

    if calcul_precision(attaque):
        stat_ATK = attaquant["atk"]
        stat_DEF = defenseur["def"]
        puissance_attaque = attaque["power"]

        degats = (stat_ATK/stat_DEF) * puissance_attaque

        return(degats)
    else:
        return("L'ennemi a évité l'attaque")