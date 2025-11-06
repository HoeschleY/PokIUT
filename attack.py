from dataclasses import dataclass
from character import Character
import random

@dataclass
class Attack:
    name: str
    kind: str      # "ATK" ou "ATK_SPE"
    power: int     # puissance (0-100)
    accuracy: int  # % de chance de toucher

    def attempt(self, attacker: Character, defender: Character) -> int:
        # Précision
        if random.randint(1, 100) > self.accuracy:
            print(f"{attacker.name} rate son attaque {self.name} ❌")
            return 0

        if self.kind == "ATK":
            damage = (attacker.atk * self.power / 100) - (defender.defense / 2)
        else:
            damage = (attacker.atk_spe * self.power / 100) - (defender.def_spe / 2)

        damage = max(1, int(damage))
        defender.take_damage(damage)
        print(f"{attacker.name} inflige {damage} à {defender.name} avec {self.name} ✅")
        return damage
