import pygame
import sys
import subprocess # <-- AJOUT NÉCESSAIRE
import os # <-- AJOUT NÉCESSAIRE

# --- AJOUT : Imports de la logique du jeu ---
from characters_pool import character_list
from game_master import GameMaster
from character import Character
from combat import lancer_combat # <-- IMPORTANT : On importe ton module de combat
# ------------------------------------------

# --- ### MODIFIÉ ### : Ajout des listes globales & compteurs ---
equipe_joueur = [] # L'équipe obtenue au tirage
equipe_combat = [] # L'équipe sélectionnée pour le combat
compteur_victoires = 0
compteur_defaites = 0
# -----------------------------------------------------------

# --- Initialisation de Pygame ---
pygame.init()

# --- Paramètres de la fenêtre ---
LARGEUR, HAUTEUR = 1200, 800 # Taille mise à jour
FENETRE = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("PokIUT - Le Gacha Ultime !")

# --- Couleurs (R, G, B) ---
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
GRIS_CLAIR = (200, 200, 200)
BLEU_BOUTON = (70, 130, 180) # SteelBlue
ROUGE_BOUTON = (220, 20, 60) # Crimson
VERT_BOUTON = (60, 179, 113) # MediumSeaGreen
JAUNE_TITRE = (255, 215, 0) # Gold
VIOLET_SECONDAIRE = (138, 43, 226) # BlueViolet
# --- NOUVEAU : Couleurs & Constantes de combat ---
VERT_VIE = (40, 200, 40)
ROUGE_VIE_FOND = (100, 0, 0) # Fond de la barre de vie
GRIS_FONCE = (50, 50, 50)
# -----------------------------------------------

# --- Polices ---
try:
    police_titre = pygame.font.Font("pokemonsolid.ttf", 80)
except FileNotFoundError:
    police_titre = pygame.font.Font(None, 80)

police_bouton = pygame.font.Font(None, 45)
police_sous_titre = pygame.font.Font(None, 60)
police_info = pygame.font.Font(None, 30) # Police plus petite pour les infos

# --- Assets (Images) ---
fond_image_menu = None 
fond_image_jeu = None 
fond_image_combat = None # Placeholder pour le fond de combat

# --- NOUVEAU : Constantes de combat ---
SPRITE_TAILLE = (128, 128) # Taille fixe de 128x128 pour les sprites en combat
BARRE_VIE_LARGEUR = 120
BARRE_VIE_HAUTEUR = 15
# ------------------------------------


# --- Fonctions utilitaires de dessin ---
def dessiner_fond_degrade(couleur_haut, couleur_bas):
    """Dessine un fond dégradé entre deux couleurs."""
    for y in range(HAUTEUR):
        r = int(couleur_haut[0] + (couleur_bas[0] - couleur_haut[0]) * (y / HAUTEUR))
        g = int(couleur_haut[1] + (couleur_bas[1] - couleur_haut[1]) * (y / HAUTEUR))
        b = int(couleur_haut[2] + (couleur_bas[2] - couleur_haut[2]) * (y / HAUTEUR))
        pygame.draw.line(FENETRE, (r, g, b), (0, y), (LARGEUR, y))

def dessiner_bouton(texte, rect, couleur_fond, couleur_texte, police, pos_souris):
    """Fonction générique pour dessiner un bouton avec effet de survol."""
    couleur_actuelle = couleur_fond
    
    if rect.collidepoint(pos_souris):
        couleur_actuelle = (max(0, couleur_fond[0]-30), max(0, couleur_fond[1]-30), max(0, couleur_fond[2]-30))
        couleur_bordure = (min(255, couleur_fond[0]+30), 
                           min(255, couleur_fond[1]+30), 
                           min(255, couleur_fond[2]+30))
        pygame.draw.rect(FENETRE, couleur_bordure, rect, 3, border_radius=15)
        
    pygame.draw.rect(FENETRE, couleur_actuelle, rect, border_radius=15)
    texte_surface = police.render(texte, True, couleur_texte)
    FENETRE.blit(texte_surface, texte_surface.get_rect(center=rect.center))

# --- ### NOUVELLE FONCTION HELPER ### ---
def dessiner_infos_perso(surface, perso, centre_img_pos):
    """
    Dessine le sprite (redimensionné), le nom, la barre de vie 
    et les HP d'un personnage.
    """
    
    try:
        sprite_scaled = pygame.transform.scale(perso.sprite, SPRITE_TAILLE)
    except Exception as e:
        print(f"Erreur scaling sprite {perso.name}: {e}")
        sprite_scaled = pygame.Surface(SPRITE_TAILLE)
        sprite_scaled.fill((255, 0, 255))
        
    rect_img = sprite_scaled.get_rect(center=centre_img_pos)
    
    if perso.is_ko():
        sprite_scaled.set_alpha(100)
        
    surface.blit(sprite_scaled, rect_img)
    
    nom_texte = police_info.render(perso.name, True, BLANC)
    nom_rect = nom_texte.get_rect(center=(rect_img.centerx, rect_img.bottom + 15))
    surface.blit(nom_texte, nom_rect)
    
    y_barre = nom_rect.bottom + 8
    hp_texte_surface = police_info.render(f"{perso.hp}/{perso.max_hp}", True, BLANC)
    hp_texte_rect = hp_texte_surface.get_rect()
    largeur_totale_bloc = BARRE_VIE_LARGEUR + 5 + hp_texte_rect.width
    x_barre_fond = rect_img.centerx - (largeur_totale_bloc / 2)
    rect_barre_fond = pygame.Rect(x_barre_fond, y_barre, BARRE_VIE_LARGEUR, BARRE_VIE_HAUTEUR)
    pygame.draw.rect(surface, ROUGE_VIE_FOND, rect_barre_fond, border_radius=4)
    ratio_hp = 0
    if perso.max_hp > 0:
        ratio_hp = max(0, perso.hp / perso.max_hp)
    rect_barre_vie = pygame.Rect(x_barre_fond, y_barre, BARRE_VIE_LARGEUR * ratio_hp, BARRE_VIE_HAUTEUR)
    pygame.draw.rect(surface, VERT_VIE, rect_barre_vie, border_radius=4)
    hp_texte_rect.midleft = (rect_barre_fond.right + 5, rect_barre_fond.centery)
    surface.blit(hp_texte_surface, hp_texte_rect)
# --- ### FIN NOUVELLE FONCTION ### ---


# --- Fonctions des différents écrans du jeu ---

# ### MODIFIÉ ### : Logique de tirage mise à jour pour afficher les 6 persos
def ecran_gacha(game_master: GameMaster):
    """Écran pour le tirage au sort de personnages."""
    print("Écran de tirage Gacha !")
    en_ecran_gacha = True
    horloge = pygame.time.Clock()

    resultat_affiche = False 
    
    texte_gacha = police_sous_titre.render("Tirage au sort PokIUT", True, VIOLET_SECONDAIRE)
    texte_gacha_rect = texte_gacha.get_rect(center=(LARGEUR // 2, HAUTEUR // 4))
    
    texte_resultat = police_sous_titre.render("Félicitations !", True, JAUNE_TITRE)
    texte_resultat_rect = texte_resultat.get_rect(center=(LARGEUR // 2, 50))

    bouton_tirer_rect = pygame.Rect(0, 0, 250, 70)
    bouton_tirer_rect.center = (LARGEUR // 2, HAUTEUR // 2)

    bouton_retour_rect = pygame.Rect(0, 0, 200, 60)
    bouton_retour_rect.center = (LARGEUR // 2, HAUTEUR // 2 + 150)
    
    bouton_continuer_rect = pygame.Rect(0, 0, 200, 60)
    bouton_continuer_rect.center = (LARGEUR // 2, HAUTEUR - 60)
    
    positions_tirage = [
        (LARGEUR * 1/4, HAUTEUR // 2 - 120),
        (LARGEUR * 2/4, HAUTEUR // 2 - 120),
        (LARGEUR * 3/4, HAUTEUR // 2 - 120),
        (LARGEUR * 1/4, HAUTEUR // 2 + 180),
        (LARGEUR * 2/4, HAUTEUR // 2 + 180),
        (LARGEUR * 3/4, HAUTEUR // 2 + 180),
    ]

    while en_ecran_gacha:
        pos_souris = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    
                    if resultat_affiche:
                        if bouton_continuer_rect.collidepoint(event.pos):
                            resultat_affiche = False 
                    
                    else:
                        if bouton_tirer_rect.collidepoint(event.pos):
                            print("Faire un tirage de 6 personnages !")
                            
                            global equipe_joueur 
                            global equipe_combat 
                            equipe_combat = []   
                            
                            try:
                                equipe_joueur = game_master.draw_characters(n=6)
                                for perso in equipe_joueur:
                                    perso.heal_full()
                                print(f"Équipe obtenue : {[p.name for p in equipe_joueur]}") 
                                resultat_affiche = True 
                            except ValueError:
                                print("Erreur: Plus de personnages à tirer !")
                            
                        elif bouton_retour_rect.collidepoint(event.pos):
                            en_ecran_gacha = False
        
        if resultat_affiche:
            if fond_image_jeu: 
                FENETRE.blit(fond_image_jeu, (0, 0))
            else:
                dessiner_fond_degrade(NOIR, VIOLET_SECONDAIRE) 

            FENETRE.blit(texte_resultat, texte_resultat_rect)
            
            for i in range(len(equipe_joueur)):
                if i < len(positions_tirage):
                    dessiner_infos_perso(FENETRE, equipe_joueur[i], positions_tirage[i])
            
            dessiner_bouton("Continuer", bouton_continuer_rect, BLEU_BOUTON, BLANC, police_bouton, pos_souris)
            
        else:
            if fond_image_jeu: 
                FENETRE.blit(fond_image_jeu, (0, 0))
            else:
                dessiner_fond_degrade(NOIR, VIOLET_SECONDAIRE) 

            FENETRE.blit(texte_gacha, texte_gacha_rect)
            dessiner_bouton("Tirer un PokIUT", bouton_tirer_rect, VERT_BOUTON, BLANC, police_bouton, pos_souris)
            dessiner_bouton("Retour", bouton_retour_rect, ROUGE_BOUTON, BLANC, police_bouton, pos_souris)

        pygame.display.flip()
        horloge.tick(60)

# --- ### MODIFIÉ ### : Logique de fin de partie déplacée ici ---
# --- ### MODIFIÉ ### : Pas de récompense en cas de défaite ---
def ecran_combat(game_master: GameMaster):
    """
    Gère la boucle de combat, appelle combat.py,
    puis gère l'écran de fin de partie.
    """
    print(f"Lancement du module de combat avec : {[p.name for p in equipe_combat]}")
    
    global compteur_victoires, compteur_defaites, equipe_joueur

    en_combat_global = True
    horloge = pygame.time.Clock()
    
    # Textes de fin de partie (définis une seule fois)
    texte_victoire = police_titre.render("Victoire !", True, JAUNE_TITRE)
    texte_defaite = police_titre.render("Défaite...", True, ROUGE_BOUTON)
    
    # Boutons de fin de partie (définis une seule fois)
    bouton_continuer_rect = pygame.Rect(0, 0, 250, 70)
    bouton_continuer_rect.center = (LARGEUR // 2, HAUTEUR // 2 + 50)
    bouton_changer_equipe_rect = pygame.Rect(0, 0, 300, 70)
    bouton_changer_equipe_rect.center = (LARGEUR // 2, HAUTEUR // 2 + 140)
    
    # Positions pour les récompenses
    positions_recompense = [
        (LARGEUR * 1/4, HAUTEUR // 2),
        (LARGEUR * 2/4, HAUTEUR // 2),
        (LARGEUR * 3/4, HAUTEUR // 2),
    ]

    while en_combat_global:
        
        # Soigne l'équipe avant le combat
        for perso in equipe_joueur:
            perso.heal_full()
            
        # 1. Lancer le combat (combat.py prend le contrôle)
        resultat = lancer_combat(
            FENETRE, 
            equipe_combat, 
            game_master, 
            dessiner_infos_perso,
            police_bouton,  
            police_info,    
            LARGEUR,        
            HAUTEUR,        
            VERT_VIE,       
            ROUGE_VIE_FOND  
        )
        
        # 2. Combat terminé, fenetre.py reprend le contrôle
        nouveaux_persos = []
        message_recompense = ""
        
        if resultat == "victoire":
            compteur_victoires += 1
            print(f"Combat gagné ! (Total: {compteur_victoires}).")
            texte_titre_fin = texte_victoire
            try:
                nouveaux_persos = game_master.draw_characters(n=3)
                equipe_joueur.extend(nouveaux_persos)
                message_recompense = "Vous obtenez 3 nouveaux PokIUTs !"
                print(f"3 nouveaux PokIUTs obtenus ! (Total: {len(equipe_joueur)})")
            except ValueError:
                message_recompense = "Pool de personnages épuisée !"

        elif resultat == "defaite":
            compteur_defaites += 1
            print(f"Combat perdu. (Total: {compteur_defaites}).")
            texte_titre_fin = texte_defaite
            # --- ### MODIFIÉ ICI ### ---
            message_recompense = "Vous n'obtenez pas de récompense."
            nouveaux_persos = [] # Assure qu'on n'affiche rien
            # (Le tirage de 3 persos a été supprimé)
            # --- ### FIN MODIFICATION ### ---

        else: # "changer_equipe" ou autre
            print("Retour à la sélection de l'équipe.")
            en_combat_global = False
            continue # Saute l'écran de relance

        # 3. Boucle de l'écran "Relancer" (géré par fenetre.py)
        ecran_relance_actif = True
        while ecran_relance_actif:
            pos_souris = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if bouton_continuer_rect.collidepoint(pos_souris):
                            ecran_relance_actif = False # Sortir de l'écran relance
                            # en_combat_global reste True, on relance un combat
                        elif bouton_changer_equipe_rect.collidepoint(pos_souris):
                            ecran_relance_actif = False # Sortir de l'écran relance
                            en_combat_global = False # Sortir de la boucle de combat

            # Dessin de l'écran de relance
            FENETRE.fill((20, 0, 30)) # Fond violet sombre
            
            # Afficher "Victoire" ou "Défaite"
            FENETRE.blit(texte_titre_fin, texte_titre_fin.get_rect(center=(LARGEUR // 2, HAUTEUR // 2 - 200)))
            
            # Afficher le message de récompense
            msg_surf = police_bouton.render(message_recompense, True, BLANC)
            FENETRE.blit(msg_surf, msg_surf.get_rect(center=(LARGEUR // 2, HAUTEUR // 2 - 100)))

            # Afficher les 3 nouveaux persos (sera une liste vide si défaite)
            for i in range(len(nouveaux_persos)):
                dessiner_infos_perso(FENETRE, nouveaux_persos[i], positions_recompense[i])

            # Dessiner les boutons
            dessiner_bouton("Continuer", bouton_continuer_rect, BLEU_BOUTON, BLANC, police_bouton, pos_souris)
            dessiner_bouton("Changer d'équipe", bouton_changer_equipe_rect, VIOLET_SECONDAIRE, BLANC, police_bouton, pos_souris)
            
            pygame.display.flip()
            horloge.tick(60)

    # --- Fin de la boucle 'en_combat_global' ---
    for perso in equipe_joueur:
        perso.heal_full()
    print("Sortie de l'écran de combat.")
# --- ### FIN DE LA MODIFICATION ### ---

# --- ### MODIFIÉ ### : Logique de sélection d'équipe et bouton "Jouer" ---
def ecran_composition_equipe(game_master: GameMaster):
    """Écran pour la composition d'équipe."""
    print("Écran de composition d'équipe !")
    global equipe_combat 
    
    en_ecran_equipe = True
    horloge = pygame.time.Clock()

    texte_equipe = police_sous_titre.render("Composition d'équipe", True, VIOLET_SECONDAIRE)
    texte_equipe_rect = texte_equipe.get_rect(center=(LARGEUR // 2, HAUTEUR // 6)) 

    bouton_retour_rect = pygame.Rect(0, 0, 200, 60)
    bouton_retour_rect.center = (LARGEUR // 2, HAUTEUR - 60) 

    bouton_jouer_rect = pygame.Rect(0, 0, 250, 70)
    bouton_jouer_rect.center = (LARGEUR // 2, HAUTEUR - 140) 

    options_cliquables = []
    y_offset = HAUTEUR // 2 - 150 # Remonté un peu
    for perso in equipe_joueur:
        texte_perso = police_bouton.render(perso.name, True, BLANC)
        rect = texte_perso.get_rect(center=(LARGEUR // 2, y_offset))
        options_cliquables.append({'perso': perso, 'rect': rect})
        y_offset += 50 # Plus d'espace

    message_info = "" 

    while en_ecran_equipe:
        pos_souris = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    message_info = "" 
                    
                    if bouton_retour_rect.collidepoint(event.pos):
                        en_ecran_equipe = False
                        
                    if len(equipe_combat) == 3:
                        if bouton_jouer_rect.collidepoint(event.pos):
                            print("Validation de l'équipe et lancement du combat !")
                            ecran_combat(game_master) 
                            
                    for option in options_cliquables:
                        if option['rect'].collidepoint(event.pos):
                            perso_clique = option['perso']
                            
                            if perso_clique in equipe_combat:
                                equipe_combat.remove(perso_clique)
                                print(f"Retiré : {perso_clique.name}. Équipe : {[p.name for p in equipe_combat]}")
                            else:
                                if len(equipe_combat) < 3:
                                    equipe_combat.append(perso_clique)
                                    print(f"Ajouté : {perso_clique.name}. Équipe : {[p.name for p in equipe_combat]}")
                                else:
                                    print("Équipe déjà pleine (3 personnages max) !")
                                    message_info = "Équipe pleine (3 max) !"

        if fond_image_jeu:
            FENETRE.blit(fond_image_jeu, (0, 0))
        else:
            dessiner_fond_degrade(NOIR, BLEU_BOUTON) 
        
        FENETRE.blit(texte_equipe, texte_equipe_rect)
        
        texte_info = police_info.render(message_info, True, ROUGE_BOUTON)
        texte_info_rect = texte_info.get_rect(center=(LARGEUR // 2, HAUTEUR - 200)) 
        FENETRE.blit(texte_info, texte_info_rect)
        
        texte_statut = police_bouton.render(f"Équipe : {len(equipe_combat)} / 3", True, BLANC)
        FENETRE.blit(texte_statut, texte_statut.get_rect(center=(LARGEUR // 2, HAUTEUR // 4)))

        if not equipe_joueur:
            texte_placeholder = police_bouton.render("Tu n'as aucun PokIUT !", True, GRIS_CLAIR)
            FENETRE.blit(texte_placeholder, texte_placeholder.get_rect(center=(LARGEUR // 2, HAUTEUR // 2)))
        else:
            for option in options_cliquables:
                perso = option['perso']
                rect = option['rect']
                couleur = JAUNE_TITRE if perso in equipe_combat else BLANC
                texte_perso = police_bouton.render(perso.name, True, couleur)
                FENETRE.blit(texte_perso, rect)

        dessiner_bouton("Retour", bouton_retour_rect, ROUGE_BOUTON, BLANC, police_bouton, pos_souris)
        
        if len(equipe_combat) == 3:
            dessiner_bouton("Valider et Jouer", bouton_jouer_rect, VERT_BOUTON, BLANC, police_bouton, pos_souris)

        pygame.display.flip()
        horloge.tick(60)

# --- ### MODIFIÉ ### : Taille des boutons et affichage score ---
def main_game_menu(game_master: GameMaster):
    """
    Menu principal du jeu après avoir cliqué sur "Jouer".
    """
    print("Affichage du menu principal du jeu.")
    en_main_game_menu = True
    horloge = pygame.time.Clock()

    texte_titre_jeu = police_sous_titre.render("Aventure PokIUT", True, JAUNE_TITRE)
    ombre_titre_jeu = police_sous_titre.render("Aventure PokIUT", True, NOIR)
    titre_jeu_rect = texte_titre_jeu.get_rect(center=(LARGEUR // 2, HAUTEUR // 5))
    ombre_titre_jeu_rect = ombre_titre_jeu.get_rect(center=(LARGEUR // 2 + 3, HAUTEUR // 5 + 3))

    # --- ### MODIFIÉ ICI ### ---
    bouton_gacha_rect = pygame.Rect(0, 0, 400, 70)
    bouton_gacha_rect.center = (LARGEUR // 2, HAUTEUR // 2 - 80)

    bouton_equipe_rect = pygame.Rect(0, 0, 400, 70)
    bouton_equipe_rect.center = (LARGEUR // 2, HAUTEUR // 2 + 20)
    # --- ### FIN MODIFICATION ### ---

    bouton_retour_rect = pygame.Rect(0, 0, 200, 60)
    bouton_retour_rect.center = (LARGEUR // 2, HAUTEUR // 2 + 150)

    while en_main_game_menu:
        pos_souris = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if bouton_gacha_rect.collidepoint(event.pos):
                        print("Accès à l'écran de Tirage Gacha.")
                        ecran_gacha(game_master)
                    elif bouton_equipe_rect.collidepoint(event.pos):
                        print("Accès à l'écran de Composition d'équipe.")
                        ecran_composition_equipe(game_master)
                    elif bouton_retour_rect.collidepoint(event.pos):
                        print("Retour au menu principal.")
                        en_main_game_menu = False 

        if fond_image_jeu:
            FENETRE.blit(fond_image_jeu, (0, 0))
        else:
            dessiner_fond_degrade(GRIS_CLAIR, BLEU_BOUTON) 

        FENETRE.blit(ombre_titre_jeu, ombre_titre_jeu_rect)
        FENETRE.blit(texte_titre_jeu, titre_jeu_rect)

        dessiner_bouton("Tirage de PokIUTs", bouton_gacha_rect, BLEU_BOUTON, BLANC, police_bouton, pos_souris)
        dessiner_bouton("Composition d'équipe", bouton_equipe_rect, VIOLET_SECONDAIRE, BLANC, police_bouton, pos_souris)
        dessiner_bouton("Retour", bouton_retour_rect, ROUGE_BOUTON, BLANC, police_bouton, pos_souris)

        # --- ### AJOUT : Affichage du score ### ---
        texte_score = police_info.render(f"Victoires : {compteur_victoires} | Défaites : {compteur_defaites}", True, BLANC)
        score_rect = texte_score.get_rect(center=(LARGEUR // 2, HAUTEUR - 30))
        FENETRE.blit(texte_score, score_rect)
        # ------------------------------------

        pygame.display.flip()
        horloge.tick(60)

def menu_principal(game_master: GameMaster):
    """
    Menu de démarrage initial avec les boutons "Jouer" et "Quitter".
    """
    en_train_de_jouer = True
    
    texte_titre = police_titre.render("PokIUT", True, JAUNE_TITRE)
    ombre_titre = police_titre.render("PokIUT", True, NOIR)
    
    titre_rect = texte_titre.get_rect(center=(LARGEUR // 2, HAUTEUR // 4))
    ombre_rect = ombre_titre.get_rect(center=(LARGEUR // 2 + 5, HAUTEUR // 4 + 5))

    bouton_jouer_rect = pygame.Rect(0, 0, 200, 60)
    bouton_jouer_rect.center = (LARGEUR // 2, HAUTEUR // 2)

    bouton_quitter_rect = pygame.Rect(0, 0, 200, 60)
    bouton_quitter_rect.center = (LARGEUR // 2, HAUTEUR // 2 + 100)

    while en_train_de_jouer:
        pos_souris = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_train_de_jouer = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if bouton_jouer_rect.collidepoint(event.pos):
                        print("Bouton Jouer cliqué ! Lancement du menu de jeu...")
                        main_game_menu(game_master)
                    elif bouton_quitter_rect.collidepoint(event.pos):
                        print("Bouton Quitter cliqué !")
                        en_train_de_jouer = False

        if fond_image_menu: 
            FENETRE.blit(fond_image_menu, (0, 0))
        else:
            dessiner_fond_degrade(NOIR, BLEU_BOUTON)

        FENETRE.blit(ombre_titre, ombre_rect)
        FENETRE.blit(texte_titre, titre_rect)
        dessiner_bouton("Jouer", bouton_jouer_rect, BLEU_BOUTON, BLANC, police_bouton, pos_souris)
        dessiner_bouton("Quitter", bouton_quitter_rect, ROUGE_BOUTON, BLANC, police_bouton, pos_souris)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

# --- Lancer le menu principal au démarrage du script ---
if __name__ == "__main__":
    # On crée le GameMaster ici
    mon_game_master = GameMaster(characters=character_list, seed=None)
    
    # On lance le menu principal en lui donnant accès au game_master
    menu_principal(mon_game_master)