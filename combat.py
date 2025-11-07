# combat.py
import pygame
import sys
import random
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
# ====== Combat principal (UI conservée) ======
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

    # --- ### AJOUTE CE BLOC ICI ### ---
    # On recrée police_titre localement car ce fichier ne la connaît pas
    try:
        police_titre = pygame.font.Font("pokemonsolid.ttf", 80)
    except FileNotFoundError:
        police_titre = pygame.font.Font(None, 80)
    # --- ### FIN DE L'AJOUT ### ---

    # --- ### MODIFIÉ : Utilisation du CLONAGE ### ---
    try:
        # 1. On tire 3 persos "source"
        adversaires_source: List[Character] = game_master.draw_characters(n=3)
        
        # 2. On clone l'équipe du joueur pour ce combat
        equipe_joueur_combat = [clone_character(p) for p in equipe_joueur]
        
        # 3. On clone l'équipe adverse pour ce combat
        equipe_adverse = [clone_character(p) for p in adversaires_source]

        # On soigne les clones au cas où
        for p in equipe_adverse: p.heal_full()
        for p in equipe_joueur_combat: p.heal_full() 

    except ValueError:
        print("Pas assez de personnages pour l'équipe adverse.")
        return "changer_equipe"
    # ------------------------------------------------

    # --- Journal ---
    log = CombatLog()
    # ... (le reste de ta fonction) ...
    log.add("🔥 Combat lancé !")
    log.add("Alliés : " + ", ".join(p.name for p in equipe_joueur_combat)) # Utilise les clones
    log.add("Ennemis : " + ", ".join(p.name for p in equipe_adverse))

    # ... (le reste de ton code) ...

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
    
    # --- ### AJOUT : Boutons de fin de partie ### ---
    bouton_continuer_rect = pygame.Rect(0, 0, 250, 70)
    bouton_continuer_rect.center = (LARGEUR // 2, HAUTEUR // 2 + 50)
    bouton_changer_equipe_rect = pygame.Rect(0, 0, 300, 70)
    bouton_changer_equipe_rect.center = (LARGEUR // 2, HAUTEUR // 2 + 140)
    
    # Textes de fin de partie
    texte_victoire = police_titre.render("Victoire !", True, JAUNE_TITRE)
    texte_defaite = police_titre.render("Défaite...", True, ROUGE_BOUTON)
    # ------------------------------------------

    # --- Zones log & actions (séparées pour ne jamais se recouvrir) ---
    zone_log = pygame.Rect(50, HAUTEUR - 230, LARGEUR - 100, 140)
    zone_actions_y = HAUTEUR - 300
    bouton_atk_rects = [pygame.Rect(50 + i * 220, zone_actions_y, 200, 50) for i in range(3)] 

    # --- Timeline par vitesse ---
    timeline = build_timeline(equipe_joueur, equipe_adverse)
    turn_idx = 0 if timeline else -1

    # --- État du tour ---
    etat = "choisir_attaque"  
    attaque_choisie: Attack | None = None
    
    # --- Anti-spam : petite temporisation après action (ms) ---
    action_cooldown_ms = 250
    next_action_ready_at = 0
    
    # --- ### AJOUT : État de fin de combat ### ---
    etat_combat = "en_cours" # "en_cours", "victoire", "defaite"
    # ---------------------------------------------

    # --- Boucle de combat ---
    clock = pygame.time.Clock()
    en_combat = True

    while en_combat:
        now = pygame.time.get_ticks()
        pos_souris = pygame.mouse.get_pos()

        # --- ### MODIFIÉ : Gestion de la fin de combat ### ---
        if etat_combat == "en_cours":
            if equipe_ko(equipe_joueur):
                log.add("❌ Défaite ! Tous vos PokIUTs sont KO.")
                etat_combat = "defaite"
                next_action_ready_at = now + 1200 # Délai avant affichage boutons
            elif equipe_ko(equipe_adverse):
                log.add("🏆 Victoire ! Tous les ennemis sont KO.")
                etat_combat = "victoire"
                next_action_ready_at = now + 1200
        # -----------------------------------------------------

        # Rebuild timeline si nécessaire (sauf si combat fini)
        if etat_combat == "en_cours":
            timeline = build_timeline(equipe_joueur, equipe_adverse)
            if not timeline:
                log.add("Combat terminé (erreur timeline).")
                pygame.time.delay(800)
                return "changer_equipe" # Sécurité

            # --- ### CORRECTION DU BUG INDEXERROR ### ---
            # 1. Vérifier si turn_idx est hors limites (trop grand) pour la NOUVELLE timeline
            if turn_idx >= len(timeline):
                turn_idx = 0 # Simplement réinitialiser à 0
                
            # 2. S'assurer que le personnage actuel (ou -1) est valide
            if turn_idx == -1 or timeline[turn_idx][1].hp <= 0:
                turn_idx = next_turn_index(timeline, turn_idx if turn_idx != -1 else 0)
                if turn_idx == -1:
                    continue # Plus personne de vivant, la boucle va re-checker
            # --- ### FIN CORRECTION ### ---

            camp, acteur = timeline[turn_idx]

        # ======= Events =======
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                
                # --- ### MODIFIÉ : Logique de clic selon l'état ### ---
                
                if etat_combat == "en_cours":
                    # Clic sur "Quitter" PENDANT le combat
                    if bouton_retour_rect.collidepoint(event.pos):
                        return "changer_equipe" # Retourne "changer_equipe"

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
                
                elif etat_combat in ("victoire", "defaite") and now >= next_action_ready_at:
                    # Clic sur les boutons de FIN de partie
                    if bouton_continuer_rect.collidepoint(event.pos):
                        return etat_combat # Retourne "victoire" ou "defaite"
                        
                    if bouton_changer_equipe_rect.collidepoint(event.pos):
                        return "changer_equipe"
                # -----------------------------------------------------

        # ====== Tour IA (automatique) ======
        if etat_combat == "en_cours" and camp == "ennemi" and acteur.hp > 0 and now >= next_action_ready_at:
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
            next_action_ready_at = now + action_cooldown_ms
            turn_idx = next_turn_index(timeline, turn_idx)

        # ======= Dessin =======
        FENETRE.fill((200, 200, 200)) # Fond gris clair

        # Titres
        FENETRE.blit(police_bouton.render("Votre Équipe", True, (0,0,0)),
                       (int(LARGEUR * 1/4) - 100, 40))
        FENETRE.blit(police_bouton.render("Adversaires", True, (220, 20, 60)),
                       (int(LARGEUR * 3/4) - 100, 40))

        # Sprites + infos
        for i, perso in enumerate(equipe_joueur):
            dessiner_infos_perso(FENETRE, perso, pos_joueur[i])
            if perso.hp <= 0:
                draw_ko_overlay(FENETRE, pos_joueur[i])

        for i, perso in enumerate(equipe_adverse):
            dessiner_infos_perso(FENETRE, perso, pos_adverse[i])
            if perso.hp <= 0:
                draw_ko_overlay(FENETRE, pos_adverse[i])

        # --- ### MODIFIÉ : Dessin selon l'état ### ---
        if etat_combat == "en_cours":
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

            # Boutons d'attaque
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
            
            # Bouton quitter
            dessiner_bouton(FENETRE, "Quitter le combat", bouton_retour_rect, ROUGE_BOUTON, BLANC, police_bouton, pos_souris)

        elif now >= next_action_ready_at: # Attente avant d'afficher les boutons
            if etat_combat == "victoire":
                FENETRE.blit(texte_victoire, texte_victoire.get_rect(center=(LARGEUR // 2, HAUTEUR // 2 - 100)))
                dessiner_bouton(FENETRE, "Continuer", bouton_continuer_rect, BLEU_BOUTON, BLANC, police_bouton, pos_souris)
                dessiner_bouton(FENETRE, "Changer d'équipe", bouton_changer_equipe_rect, VIOLET_SECONDAIRE, BLANC, police_bouton, pos_souris)
            
            elif etat_combat == "defaite":
                FENETRE.blit(texte_defaite, texte_defaite.get_rect(center=(LARGEUR // 2, HAUTEUR // 2 - 100)))
                dessiner_bouton(FENETRE, "Continuer", bouton_continuer_rect, BLEU_BOUTON, BLANC, police_bouton, pos_souris)
                dessiner_bouton(FENETRE, "Changer d'équipe", bouton_changer_equipe_rect, VIOLET_SECONDAIRE, BLANC, police_bouton, pos_souris)
        # --------------------------------------------------

        # Journal (toujours en bas)
        pygame.draw.rect(FENETRE, (240, 240, 240), zone_log, border_radius=10)
        log.draw(FENETRE, police_info, zone_log.x + 10, zone_log.y + 10)

        pygame.display.flip()
        clock.tick(60)

def clone_character(original: Character) -> Character:
    """
    Crée une copie indépendante du personnage sans relire d’image.
    Évite les problèmes de TypeError: not a file object.
    """
    # 1. On recrée un personnage AVEC LE MÊME NOM → post_init charge son vrai sprite à partir du chemin.
    clone = Character(
        name=original.name,
        max_hp=original.max_hp,
        atk=original.atk,
        defense=original.defense,
        speed=original.speed,
        atk_spe=original.atk_spe,
        def_spe=original.def_spe,
        attacks=list(original.attacks)  # on copie la liste des attaques pour éviter toute référence partagée
    )
    # 2. On remplace directement le sprite par celui déjà chargé (surface pygame.Surface)
    clone.sprite = original.sprite

    # 3. On réinitialise les HP
    clone.hp = clone.max_hp

    return clone