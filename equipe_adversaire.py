import random
from characters_pool import character_list
from character import Character

class GameMaster:
    # AJOUTE "self" ICI
    def build_random_team(self, character_list: list) -> list:
        # random.sample choisit 3 éléments uniques dans la liste
        return random.sample(character_list, k=3)


# 1. Tu dois d'abord créer un "GameMaster"
gm = GameMaster()

# 2. Maintenant, cet appel fonctionne
equipe_aleatoire = gm.build_random_team(character_list)

print(f"Équipe choisie : {[p.name for p in equipe_aleatoire]}")