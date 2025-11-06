import random
from dataclasses import dataclass
from character import Character  # importe ta classe Character

@dataclass
class Attack:
    """
    Classe représentant une attaque physique dans le jeu.

    Attributs :
    -----------
    name : str
        Nom de l’attaque (ex : "Coup d'épée", "Coup de poing").
    kind : str
        Type de l’attaque ("ATK" uniquement pour cette version).
    power : int
        Niveau de puissance de l’attaque (0-100).
    accuracy : int
        Taux de précision de l’attaque (0-100).
    """

    name: str
    kind: str  # "ATK"
    power: int
    accuracy: int

    def attempt(self, attacker: Character, defender: Character) -> int:
        """
        Tente d'effectuer une attaque entre deux personnages.

        Paramètres :
        ------------
        attacker : Character
            Le personnage qui attaque.
        defender : Character
            Le personnage qui subit l’attaque.

        Retourne :
        -----------
        int : les dégâts infligés (0 si raté).
        """
        print(f"\n{attacker.name} utilise {self.name} contre {defender.name} !")

        # Vérifie la précision
        hit_chance = random.randint(1, 100)
        if hit_chance > self.accuracy:
            print("❌ L’attaque échoue !")
            return 0

        # Calcule les dégâts physiques
        damage = (attacker.atk * self.power / 100) - (defender.defense / 2)

        # Si le défenseur est en posture défensive, on réduit les dégâts
        if getattr(defender, "is_defending", False):
            print(f"🛡️ {defender.name} se défend ! Les dégâts sont réduits de moitié.")
            damage /= 2
            defender.is_defending = False  # la défense ne dure qu’un tour

        # Dégâts minimum = 1
        damage = max(1, int(damage))
        defender.take_damage(damage)

        print(f"✅ L’attaque réussit ! {defender.name} perd {damage} PV (PV restants : {defender.hp})")
        return damage


class Defense:
    """
    Classe représentant une action défensive.
    Permet au personnage de réduire les dégâts reçus lors de la prochaine attaque.
    """

    @staticmethod
    def activate(character: Character):
        """
        Active la posture défensive du personnage.
        Réduit les dégâts reçus de moitié lors de la prochaine attaque.
        """
        character.is_defending = True
        print(f"\n{character.name} adopte une posture défensive 🛡️ (dégâts subis réduits au prochain tour).")
