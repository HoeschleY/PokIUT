from dataclasses import dataclass
import random
# Importation de 'Character'
# On utilise 'if TYPE_CHECKING:' pour éviter une boucle d'importation
# tout en gardant l'autocomplétion pour l'éditeur de code.
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from character import Character

@dataclass
class Attack:
    name: str
    kind: str      # "ATK" ou "ATK_SPE"
    power: int     # puissance (0-100)
    accuracy: int  # % de chance de toucher

    def attempt(self, attacker: "Character", defender: "Character") -> int:
        print(f"\n{attacker.name} utilise {self.name} contre {defender.name} !")
        
        # 1. Précision
        if random.randint(1, 100) > self.accuracy:
            print(f"❌ {attacker.name} rate son attaque {self.name}")
            return 0

        # 2. Calcul des dégâts
        if self.kind == "ATK":
            damage = (attacker.atk * self.power / 100) - (defender.defense / 2)
        else: # "ATK_SPE"
            damage = (attacker.atk_spe * self.power / 100) - (defender.def_spe / 2)

        # 3. Prise en compte de la défense (logique de attack_defense_system.py)
        if getattr(defender, "is_defending", False):
            print(f"🛡️ {defender.name} se défend ! Les dégâts sont réduits de moitié.")
            damage /= 2
            defender.is_defending = False  # La défense ne dure qu'un tour

        # 4. Appliquer les dégâts
        damage = max(1, int(damage))
        defender.take_damage(damage)
        
        print(f"✅ L’attaque réussit ! {defender.name} perd {damage} PV (PV restants : {defender.hp})")
        return damage


class Defense:
    """
    Action défensive.
    Permet au personnage de réduire les dégâts reçus lors de la prochaine attaque.
    """
    name: str = "Se défendre"
    
    @staticmethod
    def activate(character: "Character"):
        """
        Active la posture défensive du personnage.
        """
        character.is_defending = True
        print(f"\n{character.name} adopte une posture défensive 🛡️ (dégâts subis réduits au prochain tour).")