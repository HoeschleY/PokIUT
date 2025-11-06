from dataclasses import dataclass, field
from typing import List

@dataclass
class Attack:
    name: str
    kind: str     # "ATK" ou "ATK_SPE"
    power: int
    accuracy: int

@dataclass
class Character:
    name: str
    max_hp: int
    atk: int
    defense: int
    atk_spe: int
    def_spe: int
    speed: int
    attacks: List[Attack]
    is_player: bool = True
    level: int = 1
    sprite: str = "assets/sprites/placeholder.png"

    hp: int = field(init=False)

    def __post_init__(self):
        self.hp = self.max_hp

    # --- MÉTHODES MÉCANIQUES ---

    def take_damage(self, dmg: int):
        """Enlève des HP sans descendre sous 0."""
        self.hp = max(0, self.hp - int(dmg))

    def is_ko(self) -> bool:
        """Retourne True si le personnage est à 0 HP."""
        return self.hp <= 0

    def heal_full(self):
        """Soigne entièrement le personnage."""
        self.hp = self.max_hp

    def level_up(self):
        """Passe au niveau suivant (+stats, +HP)."""
        self.level += 1
        self.max_hp = int(self.max_hp * 1.1)
        self.atk = int(self.atk * 1.1)
        self.defense = int(self.defense * 1.1)
        # On remet au max HP après montée de niveau
        self.hp = self.max_hp

    def sprite_state(self) -> str:
        """Retourne 'ko' si K.O sinon 'normal' (utilisé par Pygame)."""
        return "ko" if self.is_ko() else "normal"
