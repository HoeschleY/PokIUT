import pygame
import sys

# --- AJOUT : Imports de la logique du jeu ---
from characters_pool import character_list
from game_master import GameMaster
from character import Character
# ------------------------------------------

# --- ### MODIFIÉ ### : Ajout des listes globales ---
equipe_joueur = [] # L'équipe obtenue au tirage
equipe_combat = [] # L'équipe sélectionnée pour le combat
# -----------------------------------------------------------

# --- Initialisation de Pygame ---
pygame.init()

# --- Paramètres de la fenêtre ---
LARGEUR, HAUTEUR = 1200, 800
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
    
    # 1. Dessiner le Sprite (redimensionné à SPRITE_TAILLE)
    try:
        # On redimensionne le sprite chargé (perso.sprite) à notre taille fixe
        sprite_scaled = pygame.transform.scale(perso.sprite, SPRITE_TAILLE)
    except Exception as e:
        # Au cas où le sprite n'a pas pu être chargé (ex: placeholder)
        print(f"Erreur scaling sprite {perso.name}: {e}")
        sprite_scaled = pygame.Surface(SPRITE_TAILLE)
        sprite_scaled.fill((255, 0, 255)) # Sprite d'erreur
        
    rect_img = sprite_scaled.get_rect(center=centre_img_pos)
    surface.blit(sprite_scaled, rect_img)
    
    # 2. Dessiner le Nom (sous l'image)
    nom_texte = police_info.render(perso.name, True, BLANC)
    nom_rect = nom_texte.get_rect(center=(rect_img.centerx, rect_img.bottom + 15))
    surface.blit(nom_texte, nom_rect)
    
    # --- Barre de vie et HP (sous le nom) ---
    
    # 3. Position Y de la barre (sous le nom)
    y_barre = nom_rect.bottom + 8
    
    # 4. Préparer le texte HP
    hp_texte_surface = police_info.render(f"{perso.hp}/{perso.max_hp}", True, BLANC)
    hp_texte_rect = hp_texte_surface.get_rect()
    
    # 5. Calculer le point de départ pour centrer le bloc [BARRE] + [TEXTE]
    largeur_totale_bloc = BARRE_VIE_LARGEUR + 5 + hp_texte_rect.width # 5px de padding
    x_barre_fond = rect_img.centerx - (largeur_totale_bloc / 2)
    
    # 6. Dessiner la barre (Fond)
    rect_barre_fond = pygame.Rect(x_barre_fond, y_barre, BARRE_VIE_LARGEUR, BARRE_VIE_HAUTEUR)
    pygame.draw.rect(surface, ROUGE_VIE_FOND, rect_barre_fond, border_radius=4)
    
    # 7. Dessiner la barre (Vie)
    ratio_hp = 0
    if perso.max_hp > 0: # Évite la division par zéro
        ratio_hp = max(0, perso.hp / perso.max_hp)
        
    rect_barre_vie = pygame.Rect(x_barre_fond, y_barre, BARRE_VIE_LARGEUR * ratio_hp, BARRE_VIE_HAUTEUR)
    pygame.draw.rect(surface, VERT_VIE, rect_barre_vie, border_radius=4)
    
    # 8. Dessiner le texte HP (à droite de la barre)
    hp_texte_rect.midleft = (rect_barre_fond.right + 5, rect_barre_fond.centery)
    surface.blit(hp_texte_surface, hp_texte_rect)
# --- ### FIN NOUVELLE FONCTION ### ---


# --- Fonctions des différents écrans du jeu ---

def ecran_gacha(game_master: GameMaster):
    """Écran pour le tirage au sort de personnages."""
    print("Écran de tirage Gacha !")
    en_ecran_gacha = True
    horloge = pygame.time.Clock()

    texte_gacha = police_sous_titre.render("Tirage au sort PokIUT", True, VIOLET_SECONDAIRE)
    texte_gacha_rect = texte_gacha.get_rect(center=(LARGEUR // 2, HAUTEUR // 4))

    bouton_tirer_rect = pygame.Rect(0, 0, 250, 70)
    bouton_tirer_rect.center = (LARGEUR // 2, HAUTEUR // 2)

    bouton_retour_rect = pygame.Rect(0, 0, 200, 60)
    bouton_retour_rect.center = (LARGEUR // 2, HAUTEUR // 2 + 150)

    while en_ecran_gacha:
        pos_souris = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if bouton_tirer_rect.collidepoint(event.pos):
                        print("Faire un tirage de 6 personnages !")
                        
                        global equipe_joueur 
                        global equipe_combat # On réinitialise l'équipe de combat
                        equipe_combat = []   # car on a tiré une nouvelle équipe
                        
                        try:
                            equipe_joueur = game_master.draw_characters(n=6)
                            print(f"Équipe obtenue : {[p.name for p in equipe_joueur]}") 
                            message_tirage = police_bouton.render("Tu as obtenu 6 PokIUTs !", True, BLANC)
                        except ValueError:
                            message_tirage = police_bouton.render("Plus de personnages !", True, ROUGE_BOUTON)
                        
                        message_tirage_rect = message_tirage.get_rect(center=(LARGEUR // 2, HAUTEUR // 2 - 80))
                        
                        if fond_image_jeu: FENETRE.blit(fond_image_jeu, (0, 0))
                        else: dessiner_fond_degrade(NOIR, VIOLET_SECONDAIRE)
                        
                        FENETRE.blit(texte_gacha, texte_gacha_rect)
                        FENETRE.blit(message_tirage, message_tirage_rect)
                        
                        dessiner_bouton("Tirer un PokIUT", bouton_tirer_rect, VERT_BOUTON, BLANC, police_bouton, pos_souris)
                        dessiner_bouton("Retour", bouton_retour_rect, ROUGE_BOUTON, BLANC, police_bouton, pos_souris)
                        
                        pygame.display.flip()
                        pygame.time.wait(2000)
                        
                    elif bouton_retour_rect.collidepoint(event.pos):
                        en_ecran_gacha = False 

        if fond_image_jeu: 
            FENETRE.blit(fond_image_jeu, (0, 0))
        else:
            dessiner_fond_degrade(NOIR, VIOLET_SECONDAIRE) 

        FENETRE.blit(texte_gacha, texte_gacha_rect)
        dessiner_bouton("Tirer un PokIUT", bouton_tirer_rect, VERT_BOUTON, BLANC, police_bouton, pos_souris)
        dessiner_bouton("Retour", bouton_retour_rect, ROUGE_BOUTON, BLANC, police_bouton, pos_souris)

        pygame.display.flip()
        horloge.tick(60)

# --- ### MODIFIÉ ### : Écran de combat avec affichage ---
def ecran_combat(game_master: GameMaster):
    """
    Écran de combat principal, affichant l'équipe du joueur contre 
    une équipe adverse générée aléatoirement.
    """
    print(f"Combat lancé avec : {[p.name for p in equipe_combat]}")
    
    # --- 1. Générer l'équipe adverse ---
    try:
        # On utilise le game_master pour tirer 3 nouveaux persos pour l'IA
        equipe_adversaire = game_master.draw_characters(n=3)
        print(f"Adversaires : {[p.name for p in equipe_adversaire]}")
    except ValueError:
        print("Erreur : Pas assez de personnages restants pour l'équipe adverse !")
        return # On quitte le combat si on ne peut pas créer d'ennemis

    en_combat = True
    horloge = pygame.time.Clock()

    # --- 2. Définir les positions d'affichage (Ajustées pour plus d'espace) ---
    pos_joueur = [
        (LARGEUR * 1/4, HAUTEUR // 2 - 200), # Haut-gauche
        (LARGEUR * 1/4, HAUTEUR // 2),       # Milieu-gauche
        (LARGEUR * 1/4, HAUTEUR // 2 + 200)  # Bas-gauche
    ]
    
    pos_adverse = [
        (LARGEUR * 3/4, HAUTEUR // 2 - 200), # Haut-droite
        (LARGEUR * 3/4, HAUTEUR // 2),       # Milieu-droite
        (LARGEUR * 3/4, HAUTEUR // 2 + 200)  # Bas-droite
    ]

    # Titres pour les équipes
    texte_joueur_titre = police_bouton.render("Votre Équipe", True, BLANC)
    texte_adverse_titre = police_bouton.render("Adversaires", True, ROUGE_BOUTON)

    bouton_retour_rect = pygame.Rect(0, 0, 250, 60)
    bouton_retour_rect.center = (LARGEUR // 2, HAUTEUR - 40) # Un peu plus haut

    while en_combat:
        pos_souris = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if bouton_retour_rect.collidepoint(event.pos):
                        # TODO: Réinitialiser la vie des persos ?
                        en_combat = False 

        # --- 3. Dessin de l'interface ---
        FENETRE.fill(GRIS_CLAIR) 
        
        # Dessiner les titres
        FENETRE.blit(texte_joueur_titre, texte_joueur_titre.get_rect(center=(LARGEUR * 1/4, 40)))
        FENETRE.blit(texte_adverse_titre, texte_adverse_titre.get_rect(center=(LARGEUR * 3/4, 40)))
        
        # Dessiner les 3 personnages du joueur (equipe_combat)
        for i in range(len(equipe_combat)):
            dessiner_infos_perso(FENETRE, equipe_combat[i], pos_joueur[i])

        # Dessiner les 3 personnages adverses (equipe_adversaire)
        for i in range(len(equipe_adversaire)):
            dessiner_infos_perso(FENETRE, equipe_adversaire[i], pos_adverse[i])

        dessiner_bouton("Quitter le combat", bouton_retour_rect, ROUGE_BOUTON, BLANC, police_bouton, pos_souris)
        
        pygame.display.flip()
        horloge.tick(60)

# --- ### MODIFIÉ ### : Logique de sélection d'équipe et bouton "Jouer" ---
def ecran_composition_equipe(game_master: GameMaster):
    """Écran pour la composition d'équipe."""
    print("Écran de composition d'équipe !")
    global equipe_combat # On va modifier la liste globale
    
    en_ecran_equipe = True
    horloge = pygame.time.Clock()

    texte_equipe = police_sous_titre.render("Composition d'équipe", True, VIOLET_SECONDAIRE)
    texte_equipe_rect = texte_equipe.get_rect(center=(LARGEUR // 2, HAUTEUR // 6)) # Plus haut

    # --- Définition des boutons ---
    bouton_retour_rect = pygame.Rect(0, 0, 200, 60)
    bouton_retour_rect.center = (LARGEUR // 2, HAUTEUR - 60) # Toujours en bas

    bouton_jouer_rect = pygame.Rect(0, 0, 250, 70)
    bouton_jouer_rect.center = (LARGEUR // 2, HAUTEUR - 140) # Au-dessus du bouton retour
    # -----------------------------

    options_cliquables = []
    y_offset = HAUTEUR // 2 - 100
    for perso in equipe_joueur:
        texte_perso = police_bouton.render(perso.name, True, BLANC)
        rect = texte_perso.get_rect(center=(LARGEUR // 2, y_offset))
        options_cliquables.append({'perso': perso, 'rect': rect})
        y_offset += 50 

    message_info = "" 

    while en_ecran_equipe:
        pos_souris = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    message_info = "" # Réinitialise le message
                    
                    # --- 1. Clic sur le bouton "Retour" (Toujours actif) ---
                    if bouton_retour_rect.collidepoint(event.pos):
                        en_ecran_equipe = False
                        
                    # --- 2. Clic sur "Valider et Jouer" (Actif seulement si 3 persos) ---
                    if len(equipe_combat) == 3:
                        if bouton_jouer_rect.collidepoint(event.pos):
                            print("Validation de l'équipe et lancement du combat !")
                            ecran_combat(game_master) # Lance l'écran de combat
                            
                    # --- 3. Clic sur un personnage ---
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

        # --- Dessin de l'écran ---
        if fond_image_jeu:
            FENETRE.blit(fond_image_jeu, (0, 0))
        else:
            dessiner_fond_degrade(NOIR, BLEU_BOUTON) 
        
        FENETRE.blit(texte_equipe, texte_equipe_rect)
        
        texte_info = police_info.render(message_info, True, ROUGE_BOUTON)
        texte_info_rect = texte_info.get_rect(center=(LARGEUR // 2, HAUTEUR - 200)) # Espace pour les boutons
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

        # --- Dessin des boutons ---
        # 1. Toujours dessiner le bouton "Retour"
        dessiner_bouton("Retour", bouton_retour_rect, ROUGE_BOUTON, BLANC, police_bouton, pos_souris)
        
        # 2. Dessiner "Valider" seulement si l'équipe est pleine
        if len(equipe_combat) == 3:
            dessiner_bouton("Valider et Jouer", bouton_jouer_rect, VERT_BOUTON, BLANC, police_bouton, pos_souris)

        pygame.display.flip()
        horloge.tick(60)

# --- (Le reste du script est identique) ---

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

    bouton_gacha_rect = pygame.Rect(0, 0, 300, 70)
    bouton_gacha_rect.center = (LARGEUR // 2, HAUTEUR // 2 - 80)

    bouton_equipe_rect = pygame.Rect(0, 0, 300, 70)
    bouton_equipe_rect.center = (LARGEUR // 2, HAUTEUR // 2 + 20)

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
    # On lui donne la liste de tous les personnages possibles
    mon_game_master = GameMaster(characters=character_list, seed=None)
    
    # On lance le menu principal en lui donnant accès au game_master
    menu_principal(mon_game_master)