# combat.py
import pygame
import sys
import random
from typing import List, Tuple
import copy

from character import Character
from attack import Attack

# Dimensions identiques à fenetre.py
SPRITE_TAILLE = (128, 128)

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
GRIS = (200, 200, 200)
BLEU_BOUTON = (70, 130, 180)
ROUGE_BOUTON = (220, 20, 60)
VERT_VIE = (40, 200, 40)
ROUGE_VIE_FOND = (100, 0, 0)

# --------------------------
# 1. Clone pour éviter bug des clones ennemis qui prennent des dégâts des alliés
# --------------------------
def clone_character(original: Character) -> Character:
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
    clone.attacks = copy.deepcopy(original.attacks)
    clone.sprite = original.sprite   # déjà chargée
    clone.hp = clone.max_hp
    clone.is_defending = False
    return clone

# --------------------------
# 2. CombatLog : zone de texte en bas à gauche
# --------------------------
class CombatLog:
    def __init__(self, max_messages=9):
        self.messages = []
        self.max_messages = max_messages

    def add(self, text: str):
        print(text)
        self.messages.append(text)
        if len(self.messages) > self.max_messages:
            self.messages.pop(0)

    def draw(self, surface, font, rect):
        # Affiche les messages à l'intérieur de la zone rect
        x, y = rect.x + 10, rect.y + 10
        line_height = 22
        for i, msg in enumerate(self.messages):
            txt = font.render(msg, True, NOIR)
            surface.blit(txt, (x, y + i * line_height))

# --------------------------
# 3. Utilitaires combat
# --------------------------
def persos_vivants(equipe):
    return [p for p in equipe if p.hp > 0]

def equipe_ko(equipe):
    return all(p.hp <= 0 for p in equipe)

def build_timeline(equipe_j, equipe_e):
    timeline = []
    for p in equipe_j:
        if p.hp > 0:
            timeline.append(("joueur", p))
    for p in equipe_e:
        if p.hp > 0:
            timeline.append(("ennemi", p))
    timeline.sort(key=lambda t: t[1].speed, reverse=True)
    return timeline

def next_turn_index(timeline, cur):
    n = len(timeline)
    for k in range(1, n + 1):
        i = (cur + k) % n
        if timeline[i][1].hp > 0:
            return i
    return -1

def draw_ko_overlay(surface, center):
    rect = pygame.Rect(center[0] - SPRITE_TAILLE[0]//2,
                       center[1] - SPRITE_TAILLE[1]//2,
                       SPRITE_TAILLE[0], SPRITE_TAILLE[1])
    voile = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    voile.fill((60, 60, 60, 180))
    surface.blit(voile, rect)

# ======================
# 4. COMBAT PRINCIPAL
# ======================
def lancer_combat(
    FENETRE: pygame.Surface,
    equipe_joueur: List[Character],
    game_master,
    dessiner_infos_perso,
    police_bouton,
    police_info,
    LARGEUR,
    HAUTEUR,
    VERT_VIE,
    ROUGE_VIE_FOND
):
    # --- Clonage des équipes pour ne pas modifier l’original ---
    try:
        adversaires_source = game_master.draw_characters(n=3)
        equipe_joueur_combat = [clone_character(p) for p in equipe_joueur]
        equipe_adverse = [clone_character(p) for p in adversaires_source]
        for p in equipe_joueur_combat: p.heal_full()
        for p in equipe_adverse: p.heal_full()
    except ValueError:
        return "changer_equipe"

    # --- Journal de combat ---
    log = CombatLog()
    log.add("Combat lancé !")
    log.add("Alliés : " + ", ".join(p.name for p in equipe_joueur_combat))
    log.add("Ennemis : " + ", ".join(p.name for p in equipe_adverse))

    # --- Positions des sprites à l’écran ---
# ✅ Nouvelles positions, plus espacées et plus hautes pour éviter le log
# Sprites alliés à gauche (plus haut qu’avant)
# Hauteur d’un bloc perso = sprite (128px) + nom + barre + marge ≈ 200px
# On définit une hauteur de bloc pour chaque personnage
    Y_DEPART = 80       # ← remonte tous les sprites de 40px
    HAUT_BLOC = 170     # ← resserre un peu l’espacement vertical


    pos_joueur = [
        (LARGEUR * 0.25, Y_DEPART),
        (LARGEUR * 0.25, Y_DEPART + HAUT_BLOC),
        (LARGEUR * 0.25, Y_DEPART + 2 * HAUT_BLOC),
    ]

    pos_adverse = [
        (LARGEUR * 0.75, Y_DEPART),
        (LARGEUR * 0.75, Y_DEPART + HAUT_BLOC),
        (LARGEUR * 0.75, Y_DEPART + 2 * HAUT_BLOC),
    ]




    # --- Bouton quitter en bas ---
    bouton_retour_rect = pygame.Rect(0, 0, 250, 50)
    bouton_retour_rect.center = (LARGEUR // 2, HAUTEUR - 25)

    # --- Zone de log en bas à gauche ---
    zone_log = pygame.Rect(40, HAUTEUR - 220, LARGEUR * 0.45, 180)

    # --- Zone des attaques en bas à droite ---
    zone_actions = pygame.Rect(LARGEUR * 0.55, HAUTEUR - 220, LARGEUR * 0.40, 180)

    # Trois boutons d'attaque
    bouton_atk_rects = [
        pygame.Rect(zone_actions.x + 20, zone_actions.y + 20 + i*55, 250, 45)
        for i in range(3)
    ]

    # --- Timeline combat ---
    timeline = build_timeline(equipe_joueur_combat, equipe_adverse)
    turn_idx = 0
    etat = "choisir_attaque"
    attaque_choisie = None
    next_action_ready_at = 0
    cooldown = 250
    clock = pygame.time.Clock()

    # ============ BOUCLE DE COMBAT ============
    while True:
        now = pygame.time.get_ticks()
        pos_souris = pygame.mouse.get_pos()

        # --- Vérification fin combat ---
        if equipe_ko(equipe_joueur_combat):
            log.add("Défaite ! Tous vos PokIUT sont KO.")
            pygame.display.flip()
            pygame.time.delay(1200)
            return "defaite"
        if equipe_ko(equipe_adverse):
            log.add("Victoire ! Tous les ennemis sont KO.")
            pygame.display.flip()
            pygame.time.delay(1200)
            return "victoire"

        timeline = build_timeline(equipe_joueur_combat, equipe_adverse)
        if not timeline:
            return "changer_equipe"
        if turn_idx >= len(timeline):
            turn_idx = 0

        if timeline[turn_idx][1].hp <= 0:
            turn_idx = next_turn_index(timeline, turn_idx)
            if turn_idx == -1:
                continue

        camp, acteur = timeline[turn_idx]

        # --- Gestion des events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if bouton_retour_rect.collidepoint(event.pos):
                    return "changer_equipe"

                if camp == "joueur" and acteur.hp > 0 and now >= next_action_ready_at:
                    if etat == "choisir_attaque":
                        for i, atk in enumerate(acteur.attacks[:3]):
                            if bouton_atk_rects[i].collidepoint(event.pos):
                                attaque_choisie = atk
                                etat = "choisir_cible"
                                log.add(f"{acteur.name} prépare {atk.name}...")
                                next_action_ready_at = now + cooldown
                                break
                    elif etat == "choisir_cible" and attaque_choisie:
                        for i, ennemi in enumerate(equipe_adverse):
                            if ennemi.hp <= 0: continue
                            cx, cy = pos_adverse[i]
                            rect_sprite = pygame.Rect(cx - 64, cy - 64, 128, 128)
                            if rect_sprite.collidepoint(event.pos):
                                dmg = attaque_choisie.attempt(acteur, ennemi)
                                if dmg > 0:
                                    log.add(f"{acteur.name} inflige {dmg} à {ennemi.name}.")
                                    if ennemi.hp <= 0:
                                        log.add(f"{ennemi.name} est KO.")
                                else:
                                    log.add(f"{acteur.name} rate {attaque_choisie.name}.")
                                etat = "choisir_attaque"
                                attaque_choisie = None
                                next_action_ready_at = now + cooldown
                                turn_idx = next_turn_index(timeline, turn_idx)
                                break

        # --- Tour de l'ennemi ---
        if camp == "ennemi" and now >= next_action_ready_at:
            vivants = persos_vivants(equipe_joueur_combat)
            if vivants:
                cible = random.choice(vivants)
                atk = random.choice(acteur.attacks)
                log.add(f"{acteur.name} utilise {atk.name} sur {cible.name}.")
                dmg = atk.attempt(acteur, cible)
                if dmg > 0:
                    log.add(f"{cible.name} subit {dmg}.")
                    if cible.hp <= 0:
                        log.add(f"{cible.name} est KO.")
            next_action_ready_at = now + cooldown
            turn_idx = next_turn_index(timeline, turn_idx)

        # ========== DESSIN ==========

        FENETRE.fill((220, 220, 220))

        # Titre en haut
        if camp == "joueur":
            if etat == "choisir_attaque":
                aide = f"Tour de {acteur.name} — choisis une attaque."
            else:
                aide = f"{acteur.name} — choisis une cible."
        else:
            aide = f"Tour de l'ennemi ({acteur.name})..."
        titre_surf = police_info.render(aide, True, NOIR)
        FENETRE.blit(titre_surf, titre_surf.get_rect(center=(LARGEUR // 2, 30)))

        # Dessin sprites
        for i, p in enumerate(equipe_joueur_combat):
            dessiner_infos_perso(FENETRE, p, pos_joueur[i])
            if p.hp <= 0: draw_ko_overlay(FENETRE, pos_joueur[i])
        for i, p in enumerate(equipe_adverse):
            dessiner_infos_perso(FENETRE, p, pos_adverse[i])
            if p.hp <= 0: draw_ko_overlay(FENETRE, pos_adverse[i])

        # --- Zone log blanc ---
        pygame.draw.rect(FENETRE, (245, 245, 245), zone_log, border_radius=10)
        log.draw(FENETRE, police_info, zone_log)

        # --- Zone actions (attaques) ---
        pygame.draw.rect(FENETRE, (240,240,240), zone_actions, border_radius=10)

        if camp == "joueur" and acteur.hp > 0:
            for i, rect in enumerate(bouton_atk_rects):
                if i < len(acteur.attacks):
                    col = BLEU_BOUTON if etat == "choisir_attaque" else (150,150,150)
                    pygame.draw.rect(FENETRE, col, rect, border_radius=10)
                    txt = police_info.render(acteur.attacks[i].name, True, BLANC)
                else:
                    pygame.draw.rect(FENETRE, (180,180,180), rect, border_radius=10)
                    txt = police_info.render("-", True, BLANC)
                FENETRE.blit(txt, txt.get_rect(center=rect.center))

        # -- Bouton quitter --
        pygame.draw.rect(FENETRE, ROUGE_BOUTON, bouton_retour_rect, border_radius=15)
        quit_txt = police_info.render("Quitter le combat", True, BLANC)
        FENETRE.blit(quit_txt, quit_txt.get_rect(center=bouton_retour_rect.center))

        pygame.display.flip()
        clock.tick(60)


