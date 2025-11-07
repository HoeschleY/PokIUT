# combat.py
import pygame
import sys
import random
import copy # <-- AJOUT NÉCESSAIRE POUR LE CLONAGE
from typing import List, Tuple

from character import Character
from attack import Attack

# Même taille que dans fenetre.py
SPRITE_TAILLE: Tuple[int, int] = (128, 128)

# --- COULEURS (copiées de fenetre.py pour être autonomes) ---
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
BLEU_BOUTON = (70, 130, 180)
ROUGE_BOUTON = (220, 20, 60)
JAUNE_TITRE = (255, 215, 0)
VIOLET_SECONDAIRE = (138, 43, 226)

# --- ### AJOUT : Fonction de clonage ### ---
def clone_character(original: Character) -> Character:
    """ Crée une copie du personnage pour éviter les bugs de référence. """
    clone = object.__new__(Character)
    clone.name = original.name
    clone.max_hp = original.max_hp
    clone.atk = original.atk
    clone.defense = original.defense
    clone.atk_spe = original.atk_spe
    clone.def_spe = original.def_spe
    clone.speed = original.speed
    clone.is_player = original.is_player
    clone.level = original.level
    clone.sprite = original.sprite 
    clone.attacks = copy.deepcopy(original.attacks)
    clone.hp = clone.max_hp
    clone.is_defending = False
    return clone
# ----------------------------------------

# --- ### AJOUT ### : On a besoin de la fonction dessiner_bouton ici aussi ---
def dessiner_bouton(surface, texte, rect, couleur_fond, couleur_texte, police, pos_souris):
    """Dessine un bouton (copié de fenetre.py)"""
    couleur_actuelle = couleur_fond
    if rect.collidepoint(pos_souris):
        couleur_actuelle = (max(0, couleur_fond[0]-30), max(0, couleur_fond[1]-30), max(0, couleur_fond[2]-30))
        couleur_bordure = (min(255, couleur_fond[0]+30), 
                           min(255, couleur_fond[1]+30), 
                           min(255, couleur_fond[2]+30))
        pygame.draw.rect(surface, couleur_bordure, rect, 3, border_radius=15)
    pygame.draw.rect(surface, couleur_actuelle, rect, border_radius=15)
    texte_surface = police.render(texte, True, couleur_texte)
    surface.blit(texte_surface, texte_surface.get_rect(center=rect.center))
# -----------------------------------------------------------------

# ===== Journal de combat =====
class CombatLog:
    def __init__(self, max_messages: int = 9):
        self.messages: List[str] = []
        self.max_messages = max_messages
    def add(self, text: str):
        print(text)
        self.messages.append(text)
        if len(self.messages) > self.max_messages:
            self.messages.pop(0)
    def draw(self, surface: pygame.Surface, font: pygame.font.Font, x: int, y: int, color=(0, 0, 0)):
        dy = 22
        for i, msg in enumerate(self.messages):
            txt = font.render(msg, True, color)
            surface.blit(txt, (x, y + i * dy))

# ===== Utilitaires combat =====
def persos_vivants(equipe: List[Character]) -> List[Character]:
    return [p for p in equipe if p.hp > 0]
def equipe_ko(equipe: List[Character]) -> bool:
    return all(p.hp <= 0 for p in equipe)
def build_timeline(equipe_j: List[Character], equipe_e: List[Character]) -> List[Tuple[str, Character]]:
    L: List[Tuple[str, Character]] = []
    for p in equipe_j:
        if p.hp > 0: L.append(("joueur", p))
    for p in equipe_e:
        if p.hp > 0: L.append(("ennemi", p))
    L.sort(key=lambda t: t[1].speed, reverse=True)
    return L
def next_turn_index(timeline: List[Tuple[str, Character]], cur: int) -> int:
    if not timeline: return -1
    n = len(timeline)
    for k in range(1, n + 1):
        i = (cur + k) % n
        if timeline[i][1].hp > 0: return i
    return -1
def draw_ko_overlay(surface: pygame.Surface, center: Tuple[int, int]):
    rect = pygame.Rect(center[0] - SPRITE_TAILLE[0] // 2,
                       center[1] - SPRITE_TAILLE[1] // 2,
                       SPRITE_TAILLE[0], SPRITE_TAILLE[1])
    voile = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    voile.fill((60, 60, 60, 180))
    surface.blit(voile, rect)


# ====== Combat principal (UI conservée) ======
def lancer_combat(
    FENETRE: pygame.Surface,
    equipe_joueur: List[Character],
    game_master,
    dessiner_infos_perso, 
    police_bouton: pygame.font.Font,
    police_info: pygame.font.Font,
    LARGEUR: int,
    HAUTEUR: int,
    VERT_VIE, ROUGE_VIE_FOND
): # 10 arguments
    """Lance un combat et retourne 'victoire', 'defaite' ou 'changer_equipe'."""
    
    # --- Clonage des équipes ---
    try:
        adversaires_source: List[Character] = game_master.draw_characters(n=3)
        equipe_joueur_combat = [clone_character(p) for p in equipe_joueur]
        equipe_adverse = [clone_character(p) for p in adversaires_source]
        for p in equipe_adverse: p.heal_full()
        for p in equipe_joueur_combat: p.heal_full() 
    except ValueError:
        print("Pas assez de personnages pour l'équipe adverse.")
        return "changer_equipe" 

    log = CombatLog()
    log.add("🔥 Combat lancé !")
    log.add("Alliés : " + ", ".join(p.name for p in equipe_joueur_combat))
    log.add("Ennemis : " + ", ".join(p.name for p in equipe_adverse))

    pos_joueur = [
        (LARGEUR * 1/4, HAUTEUR // 2 - 200),
        (LARGEUR * 1/4, HAUTEUR // 2),
        (LARGEUR * 1/4, HAUTEUR // 2 + 200),
    ]
    pos_adverse = [
        (LARGEUR * 3/4, HAUTEUR // 2 - 200),
        (LARGEUR * 3/4, HAUTEUR // 2),
        (LARGEUR * 3/4, HAUTEUR // 2 + 200),
    ]

    bouton_retour_rect = pygame.Rect(0, 0, 300, 60) # Élargi
    bouton_retour_rect.center = (LARGEUR // 2, HAUTEUR - 40)
    
    zone_log = pygame.Rect(50, HAUTEUR - 230, LARGEUR - 100, 140)
    zone_actions_y = HAUTEUR - 300
    bouton_atk_rects = [pygame.Rect(50 + i * 220, zone_actions_y, 200, 50) for i in range(3)] 

    timeline = build_timeline(equipe_joueur_combat, equipe_adverse)
    turn_idx = 0 if timeline else -1

    etat = "choisir_attaque"  
    attaque_choisie: Attack | None = None
    
    action_cooldown_ms = 250
    next_action_ready_at = 0
    
    clock = pygame.time.Clock()
    en_combat = True

    while en_combat:
        now = pygame.time.get_ticks()
        pos_souris = pygame.mouse.get_pos()

        # --- ### MODIFIÉ : Gestion de la fin de combat ### ---
        if equipe_ko(equipe_joueur_combat):
            log.add("❌ Défaite ! Tous vos PokIUTs sont KO.")
            pygame.display.flip()
            pygame.time.delay(1200) # Délai pour lire le message
            return "defaite" # On retourne le résultat
        elif equipe_ko(equipe_adverse):
            log.add("🏆 Victoire ! Tous les ennemis sont KO.")
            pygame.display.flip()
            pygame.time.delay(1200)
            return "victoire" # On retourne le résultat
        # -----------------------------------------------------

        timeline = build_timeline(equipe_joueur_combat, equipe_adverse)
        if not timeline:
            return "changer_equipe" 

        if turn_idx >= len(timeline):
            turn_idx = 0 
            
        if turn_idx == -1 or timeline[turn_idx][1].hp <= 0:
            turn_idx = next_turn_index(timeline, turn_idx if turn_idx != -1 else 0)
            if turn_idx == -1:
                continue 

        camp, acteur = timeline[turn_idx]

        # ======= Events =======
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                
                if bouton_retour_rect.collidepoint(event.pos):
                    return "changer_equipe" # Quitte et signale de changer

                # Tour JOUEUR
                if camp == "joueur" and acteur.hp > 0 and now >= next_action_ready_at:
                    if etat == "choisir_attaque":
                        for i, atk in enumerate(acteur.attacks[:3]):
                            if bouton_atk_rects[i].collidepoint(event.pos):
                                attaque_choisie = atk
                                etat = "choisir_cible"
                                log.add(f"➡ {acteur.name} prépare {atk.name}…")
                                next_action_ready_at = now + action_cooldown_ms
                                break
                    elif etat == "choisir_cible" and attaque_choisie is not None:
                        for i, ennemi in enumerate(equipe_adverse):
                            if ennemi.hp <= 0: continue
                            cx, cy = pos_adverse[i]
                            rect_sprite = pygame.Rect(cx - SPRITE_TAILLE[0] // 2,
                                                      cy - SPRITE_TAILLE[1] // 2,
                                                      SPRITE_TAILLE[0], SPRITE_TAILLE[1])
                            if rect_sprite.collidepoint(event.pos):
                                dmg = attaque_choisie.attempt(acteur, ennemi)
                                if dmg <= 0:
                                    log.add(f"❌ {acteur.name} rate {attaque_choisie.name} sur {ennemi.name}.")
                                else:
                                    log.add(f"🗡️ {acteur.name} inflige {dmg} à {ennemi.name}.")
                                    if ennemi.hp <= 0:
                                        log.add(f"💀 {ennemi.name} est KO.")
                                
                                attaque_choisie = None
                                etat = "choisir_attaque"
                                next_action_ready_at = now + action_cooldown_ms
                                turn_idx = next_turn_index(timeline, turn_idx)
                                break

        # ====== Tour IA (automatique) ======
        if camp == "ennemi" and acteur.hp > 0 and now >= next_action_ready_at:
            cibles = persos_vivants(equipe_joueur_combat)
            if cibles and acteur.attacks:
                cible = random.choice(cibles)
                atk = random.choice(acteur.attacks)
                log.add(f"🤖 {acteur.name} utilise {atk.name} sur {cible.name}.")
                dmg = atk.attempt(acteur, cible)
                if dmg <= 0:
                    log.add(f"❌ {acteur.name} rate {atk.name}.")
                else:
                    log.add(f"🩸 {cible.name} subit {dmg}.")
                    if cible.hp <= 0:
                        log.add(f"💀 {cible.name} est KO.")
            next_action_ready_at = now + action_cooldown_ms
            turn_idx = next_turn_index(timeline, turn_idx)

        # ======= Dessin =======
        FENETRE.fill((200, 200, 200)) 

        FENETRE.blit(police_bouton.render("Votre Équipe", True, (0,0,0)),
                       (int(LARGEUR * 1/4) - 100, 40))
        FENETRE.blit(police_bouton.render("Adversaires", True, (220, 20, 60)),
                       (int(LARGEUR * 3/4) - 100, 40))

        for i, perso in enumerate(equipe_joueur_combat):
            dessiner_infos_perso(FENETRE, perso, pos_joueur[i])
            if perso.hp <= 0:
                draw_ko_overlay(FENETRE, pos_joueur[i])
        for i, perso in enumerate(equipe_adverse):
            dessiner_infos_perso(FENETRE, perso, pos_adverse[i])
            if perso.hp <= 0:
                draw_ko_overlay(FENETRE, pos_adverse[i])

        aide_txt = ""
        if camp == "joueur":
            if etat == "choisir_attaque":
                aide_txt = f"Tour de {acteur.name} — choisis une attaque."
            elif etat == "choisir_cible":
                aide_txt = f"{acteur.name} — choisis une cible."
        else:
            aide_txt = f"Tour de l'ennemi ({acteur.name})…"
        
        aide_surface = police_info.render(aide_txt, True, (0, 0, 0))
        FENETRE.blit(aide_surface, (50, HAUTEUR - 340))

        if camp == "joueur" and acteur.hp > 0:
            for i in range(3):
                has_atk = i < len(acteur.attacks)
                rect = bouton_atk_rects[i]
                col = (70, 130, 180) if has_atk and etat == "choisir_attaque" else (170, 170, 170)
                pygame.draw.rect(FENETRE, col, rect, border_radius=10)
                label = acteur.attacks[i].name if has_atk else "-"
                txt = police_info.render(label, True, (255, 255, 255))
                FENETRE.blit(txt, txt.get_rect(center=rect.center))
            
            if etat == "choisir_cible":
                hint = police_info.render("(Clique sur un ennemi vivant)", True, (255, 140, 0))
                FENETRE.blit(hint, (50, zone_actions_y + 60))
        
        dessiner_bouton(FENETRE, "Quitter le combat", bouton_retour_rect, ROUGE_BOUTON, BLANC, police_bouton, pos_souris)

        pygame.draw.rect(FENETRE, (240, 240, 240), zone_log, border_radius=10)
        log.draw(FENETRE, police_info, zone_log.x + 10, zone_log.y + 10)

        pygame.display.flip()
        clock.tick(60)