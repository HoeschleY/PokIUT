from dataclasses import dataclass, field
from typing import List
from attack import Attack  # ✅ permet d'ajouter une liste d'attaques à chaque personnage
import pygame

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
        Charge également le sprite du personnage.
        """
        self.hp = self.max_hp
        self.is_defending = False  # utile pour la classe Defense ou réduction de dégâts

        # --- ### CORRECTION IMPORTANTE ICI ### ---
        # On charge l'image à partir du chemin (self.sprite qui est un string)
        # et on remplace le string par l'objet image chargé.
        try:
            image_path = self.sprite  # Garde le chemin en mémoire au cas où
            self.sprite = pygame.image.load(image_path)
            
            # Optionnel : redimensionner tous les sprites à une taille fixe
            # self.sprite = pygame.transform.scale(self.sprite, (128, 128))

        except FileNotFoundError:
            print(f"Erreur: Image {image_path} non trouvée pour {self.name}")
            # On crée une image de remplacement pour éviter de planter
            self.sprite = pygame.Surface((64, 64))
            self.sprite.fill((255, 0, 255)) # Rose vif pour voir l'erreur
        except pygame.error as e:
            print(f"Erreur Pygame en chargeant {image_path}: {e}")
            self.sprite = pygame.Surface((64, 64))
            self.sprite.fill((255, 100, 100)) # Une autre couleur d'erreur
        # --- ### FIN DE LA CORRECTION ### ---

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