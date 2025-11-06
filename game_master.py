import random
from character import Character

class GameMaster:
    def __init__(self, characters: list[Character], seed=None):
        self.characters = characters
        self.random = random.Random(seed)  # utile pour les tests (résultats reproductibles)

    def draw_characters(self, n=6):
        """Tire aléatoirement `n` personnages sans doublon."""
        if n > len(self.characters):
            raise ValueError("Pas assez de personnages dans la base.")
        return self.random.sample(self.characters, n)

from character import Character, Attack

# 1) Création d’attaques
fireball = Attack(name="Fireball", kind="ATK_SPE", power=50, accuracy=90)
slash = Attack(name="Slash", kind="ATK", power=40, accuracy=95)

# 2) Création d’un personnage
mage = Character(
    name="Aeris",
    max_hp=120,
    atk=20,
    defense=15,
    atk_spe=40,
    def_spe=30,
    speed=25,
    attacks=[fireball, slash],  # liste d’attaques disponibles
    is_player=True,
    level=1,
    sprite="assets/sprites/placeholder.png"
)

print(mage)
print("HP :", mage.hp)
print("Attaque 1 :", mage.attacks[0].name)