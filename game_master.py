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
    
