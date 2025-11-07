# combat.py
import pygame
import sys
import random
from typing import List, Tuple

from character import Character
from attack import Attack

# Même taille que dans fenetre.py
SPRITE_TAILLE: Tuple[int, int] = (128, 128)

# ===== Journal de combat =====
class CombatLog:
    def __init__(self, max_messages: int = 9):
        self.messages: List[str] = []
        self.max_messages = max_messages

    def add(self, text: str):
        # Affiche aussi en console pour debug
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
    """Retourne [(camp, perso), ...] trié par speed décroissant."""
    L: List[Tuple[str, Character]] = []
    for p in equipe_j:
        if p.hp > 0:
            L.append(("joueur", p))
    for p in equipe_e:
        if p.hp > 0:
            L.append(("ennemi", p))
    L.sort(key=lambda t: t[1].speed, reverse=True)
    return L

def next_turn_index(timeline: List[Tuple[str, Character]], cur: int) -> int:
    """Index du prochain perso vivant, sinon -1 si plus personne."""
    if not timeline:
        return -1
    n = len(timeline)
    for k in range(1, n + 1):
        i = (cur + k) % n
        if timeline[i][1].hp > 0:
            return i
    return -1

def draw_ko_overlay(surface: pygame.Surface, center: Tuple[int, int]):
    """Grise un sprite (si KO) en posant un voile semi-transparent sur sa zone."""
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
    dessiner_infos_perso,         # fonction fournie par fenetre.py
    police_bouton: pygame.font.Font,
    police_info: pygame.font.Font,
    LARGEUR: int,
    HAUTEUR: int,
    VERT_VIE, ROUGE_VIE_FOND
):
    """Lance un combat en conservant la disposition originale, avec log séparé et tours par vitesse."""

    # --- Tirer l'équipe adverse ---
    try:
        equipe_adverse: List[Character] = game_master.draw_characters(n=3)
    except ValueError:
        print("Pas assez de personnages pour l'équipe adverse.")
        return

    # --- Journal ---
    log = CombatLog()
    log.add("🔥 Combat lancé !")
    log.add("Alliés : " + ", ".join(p.name for p in equipe_joueur))
    log.add("Ennemis : " + ", ".join(p.name for p in equipe_adverse))

    # --- Positions (identiques à ton code) ---
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

    # --- Bouton quitter (comme avant) ---
    bouton_retour_rect = pygame.Rect(0, 0, 250, 60)
    bouton_retour_rect.center = (LARGEUR // 2, HAUTEUR - 40)

    # --- Zones log & actions (séparées pour ne jamais se recouvrir) ---
    # Log discret juste au-dessus du bouton quitter
    zone_log = pygame.Rect(50, HAUTEUR - 230, LARGEUR - 100, 140)
    # Boutons d'attaque : ligne de boutons au-dessus du log
    # (On laisse ~60px de marge entre sprites et cette zone)
    zone_actions_y = HAUTEUR - 300
    bouton_atk_rects = [pygame.Rect(50 + i * 220, zone_actions_y, 200, 50) for i in range(3)]  # 3 boutons visibles max

    # --- Timeline par vitesse ---
    timeline = build_timeline(equipe_joueur, equipe_adverse)
    turn_idx = 0 if timeline else -1

    # --- État du tour ---
    etat = "choisir_attaque"   # ou "choisir_cible"
    attaque_choisie: Attack | None = None
    cible_highlight = None

    # --- Anti-spam : petite temporisation après action (ms) ---
    action_cooldown_ms = 250
    next_action_ready_at = 0

    # --- Boucle de combat ---
    clock = pygame.time.Clock()
    en_combat = True

    while en_combat:
        now = pygame.time.get_ticks()
        pos_souris = pygame.mouse.get_pos()

        # Fin de combat ?
        if equipe_ko(equipe_joueur) or equipe_ko(equipe_adverse):
            if equipe_ko(equipe_joueur):
                log.add("❌ Défaite ! Tous vos PokIUTs sont KO.")
            else:
                log.add("🏆 Victoire ! Tous les ennemis sont KO.")
            # On affiche 1.2s le message puis on sort
            pygame.display.flip()
            pygame.time.delay(1200)
            return

        # Rebuild timeline si nécessaire
        timeline = build_timeline(equipe_joueur, equipe_adverse)
        if not timeline:
            log.add("Combat terminé.")
            pygame.display.flip()
            pygame.time.delay(800)
            return

        # S'assurer que l'index pointe vers un vivant
        if turn_idx == -1 or timeline[turn_idx][1].hp <= 0:
            turn_idx = next_turn_index(timeline, turn_idx if turn_idx != -1 else 0)
            if turn_idx == -1:
                continue  # boucle suivante (cas limite)

        camp, acteur = timeline[turn_idx]

        # ======= Events =======
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Quitter le combat
                if bouton_retour_rect.collidepoint(event.pos):
                    en_combat = False
                    break

                # Tour JOUEUR
                if camp == "joueur" and acteur.hp > 0 and now >= next_action_ready_at:
                    # Choix attaque
                    if etat == "choisir_attaque":
                        for i, atk in enumerate(acteur.attacks[:3]):  # 3 boutons max
                            if bouton_atk_rects[i].collidepoint(event.pos):
                                attaque_choisie = atk
                                etat = "choisir_cible"
                                log.add(f"➡ {acteur.name} prépare {atk.name}…")
                                next_action_ready_at = now + action_cooldown_ms
                                break

                    # Choix cible : clic sur sprite adverse vivant
                    elif etat == "choisir_cible" and attaque_choisie is not None:
                        for i, ennemi in enumerate(equipe_adverse):
                            if ennemi.hp <= 0:
                                continue
                            cx, cy = pos_adverse[i]
                            rect_sprite = pygame.Rect(cx - SPRITE_TAILLE[0] // 2,
                                                      cy - SPRITE_TAILLE[1] // 2,
                                                      SPRITE_TAILLE[0], SPRITE_TAILLE[1])
                            if rect_sprite.collidepoint(event.pos):
                                # Effectuer l'attaque
                                dmg = attaque_choisie.attempt(acteur, ennemi)
                                if dmg <= 0:
                                    log.add(f"❌ {acteur.name} rate {attaque_choisie.name} sur {ennemi.name}.")
                                else:
                                    log.add(f"🗡️ {acteur.name} inflige {dmg} à {ennemi.name}.")
                                    if ennemi.hp <= 0:
                                        log.add(f"💀 {ennemi.name} est KO.")
                                # Reset & tour suivant
                                attaque_choisie = None
                                etat = "choisir_attaque"
                                next_action_ready_at = now + action_cooldown_ms
                                # avancer le tour
                                turn_idx = next_turn_index(timeline, turn_idx)
                                break

        # ====== Tour IA (automatique) ======
        if camp == "ennemi" and acteur.hp > 0 and now >= next_action_ready_at:
            cibles = persos_vivants(equipe_joueur)
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
            # Avancer le tour
            next_action_ready_at = now + action_cooldown_ms
            turn_idx = next_turn_index(timeline, turn_idx)

        # ======= Dessin =======
        # Fond simple (identique à ton écran combat)
        FENETRE.fill((200, 200, 200))

        # Titres
        FENETRE.blit(police_bouton.render("Votre Équipe", True, (255, 255, 255)),
                     (int(LARGEUR * 1/4) - 100, 40))
        FENETRE.blit(police_bouton.render("Adversaires", True, (220, 20, 60)),
                     (int(LARGEUR * 3/4) - 100, 40))

        # Sprites + infos (on grisera manuellement si KO)
        for i, perso in enumerate(equipe_joueur):
            dessiner_infos_perso(FENETRE, perso, pos_joueur[i])
            if perso.hp <= 0:
                draw_ko_overlay(FENETRE, pos_joueur[i])

        for i, perso in enumerate(equipe_adverse):
            dessiner_infos_perso(FENETRE, perso, pos_adverse[i])
            if perso.hp <= 0:
                draw_ko_overlay(FENETRE, pos_adverse[i])

        # Bandeau d'aide (tour courant)
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

        # Boutons d'attaque (uniquement quand c'est au joueur)
        if camp == "joueur" and acteur.hp > 0:
            for i in range(3):
                # fond bouton (grisé si pas d'attaque correspondante)
                has_atk = i < len(acteur.attacks)
                rect = bouton_atk_rects[i]
                col = (70, 130, 180) if has_atk and etat == "choisir_attaque" else (170, 170, 170)
                pygame.draw.rect(FENETRE, col, rect, border_radius=10)
                label = acteur.attacks[i].name if has_atk else "-"
                txt = police_info.render(label, True, (255, 255, 255))
                FENETRE.blit(txt, txt.get_rect(center=rect.center))

            # Indice visuel lors du choix de la cible
            if etat == "choisir_cible":
                hint = police_info.render("(Clique sur un ennemi vivant)", True, (255, 140, 0))
                FENETRE.blit(hint, (50, zone_actions_y + 60))

        # Journal (en bas, séparé)
        pygame.draw.rect(FENETRE, (240, 240, 240), zone_log, border_radius=10)
        log.draw(FENETRE, police_info, zone_log.x + 10, zone_log.y + 10)

        # Bouton quitter
        pygame.draw.rect(FENETRE, (220, 20, 60), bouton_retour_rect, border_radius=10)
        lbl = police_bouton.render("Quitter le combat", True, (255, 255, 255))
        FENETRE.blit(lbl, lbl.get_rect(center=bouton_retour_rect.center))

        pygame.display.flip()
        clock.tick(60)
