from dataclasses import dataclass, field
from typing import List
from attack import Attack  # ✅ permet d'ajouter une liste d'attaques à chaque personnage


@dataclass
class Character:
    """
    Classe représentant un personnage du jeu.
    """

    name: str
    max_hp: int
    atk: int
    defense: int
    atk_spe: int
    def_spe: int
    speed: int
    attacks: List[Attack]          # ✅ Liste des attaques disponibles pour ce personnage
    is_player: bool = True
    level: int = 1
    sprite: str = "assets/sprites/placeholder.png"

    # Attribut calculé automatiquement après l'initialisation
    hp: int = field(init=False)

    def __post_init__(self):
        """
        Initialise les PV actuels au maximum au moment de la création.
        """
        self.hp = self.max_hp
        self.is_defending = False  # utile pour la classe Defense ou réduction de dégâts

    # ─────────────────────────────
    #         MÉCANIQUES DE JEU
    # ─────────────────────────────

    def take_damage(self, dmg: int):
        """
        Inflige des dégâts au personnage sans descendre sous 0 HP.
        """
        self.hp = max(0, self.hp - int(dmg))

    def heal_full(self):
        """
        Soigne entièrement le personnage.
        """
        self.hp = self.max_hp

    def is_ko(self) -> bool:
        """
        Retourne True si le personnage n'a plus de HP.
        """
        return self.hp <= 0

    def level_up(self):
        """
        Monte le personnage d'un niveau (+10% statistiques de base).
        """
        self.level += 1
        self.max_hp = int(self.max_hp * 1.1)
        self.atk = int(self.atk * 1.1)
        self.defense = int(self.defense * 1.1)
        self.atk_spe = int(self.atk_spe * 1.1)
        self.def_spe = int(self.def_spe * 1.1)
        self.hp = self.max_hp  # régénération totale après level up

    def sprite_state(self) -> str:
        """
        Retourne un état de sprite :
        - 'ko' si HP = 0 (affichage du sprite en gris)
        - 'normal' sinon
        """
        return "ko" if self.is_ko() else "normal"
