import pygame
import sys

# --- Initialisation de Pygame ---
pygame.init()

# --- Paramètres de la fenêtre ---
LARGEUR, HAUTEUR = 800, 600
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

# --- Polices ---
try:
    police_titre = pygame.font.Font("pokemonsolid.ttf", 80)
except FileNotFoundError:
    police_titre = pygame.font.Font(None, 80)

police_bouton = pygame.font.Font(None, 45)
police_sous_titre = pygame.font.Font(None, 60) # Nouvelle police pour les sous-titres

# --- Assets (Images) ---
# Il est FORTEMENT recommandé d'avoir une image de fond !
fond_image_menu = None 
fond_image_jeu = None # Nouvelle image de fond pour le menu du jeu

#try:
    # Essaie de charger une image de fond pour le menu principal
#    fond_image_menu = pygame.image.load("background_grass.png") 
#    fond_image_menu = pygame.transform.scale(fond_image_menu, (LARGEUR, HAUTEUR))
#except pygame.error:
#    print("Image de fond 'background_grass.png' non trouvée pour le menu principal. Utilisation d'un fond dégradé.")
    
#try:
    # Essaie de charger une image de fond pour le menu du jeu (une autre si possible)
#    fond_image_jeu = pygame.image.load("background_lab.png") # Par exemple, un labo Pokémon
#    fond_image_jeu = pygame.transform.scale(fond_image_jeu, (LARGEUR, HAUTEUR))
#except pygame.error:
 #   print("Image de fond 'background_lab.png' non trouvée pour le menu du jeu. Utilisation d'un fond dégradé.")


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
        # Assombrir ou éclaircir le bouton au survol
        couleur_actuelle = (max(0, couleur_fond[0]-30), max(0, couleur_fond[1]-30), max(0, couleur_fond[2]-30))
        
        # --- CORRECTION ICI ---
        # On s'assure que la couleur de la bordure ne dépasse pas 255
        couleur_bordure = (min(255, couleur_fond[0]+30), 
                           min(255, couleur_fond[1]+30), 
                           min(255, couleur_fond[2]+30))
        pygame.draw.rect(FENETRE, couleur_bordure, rect, 3, border_radius=15) # Bordure plus claire
        # --- FIN DE LA CORRECTION ---
        
    pygame.draw.rect(FENETRE, couleur_actuelle, rect, border_radius=15)
    texte_surface = police.render(texte, True, couleur_texte)
    FENETRE.blit(texte_surface, texte_surface.get_rect(center=rect.center))


# --- Fonctions des différents écrans du jeu ---

def ecran_gacha():
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
                        print("Faire un tirage !")
                        # TODO: Intégrer la logique de tirage Gacha ici
                        # Pour l'instant, un simple message et attendre un peu
                        message_tirage = police_bouton.render("Tu as obtenu un nouveau PokIUT !", True, BLANC)
                        message_tirage_rect = message_tirage.get_rect(center=(LARGEUR // 2, HAUTEUR // 2 - 80))
                        FENETRE.fill(NOIR)
                        FENETRE.blit(message_tirage, message_tirage_rect)
                        pygame.display.flip()
                        pygame.time.wait(2000) # Attendre 2 secondes
                    elif bouton_retour_rect.collidepoint(event.pos):
                        en_ecran_gacha = False # Quitte l'écran Gacha pour revenir au menu du jeu

        # --- Dessin de l'écran Gacha ---
        if fond_image_jeu: # Utilise le fond_image_jeu
            FENETRE.blit(fond_image_jeu, (0, 0))
        else:
            dessiner_fond_degrade(NOIR, VIOLET_SECONDAIRE) # Dégradé spécifique pour cet écran

        FENETRE.blit(texte_gacha, texte_gacha_rect)
        
        dessiner_bouton("Tirer un PokIUT", bouton_tirer_rect, VERT_BOUTON, BLANC, police_bouton, pos_souris)
        dessiner_bouton("Retour", bouton_retour_rect, ROUGE_BOUTON, BLANC, police_bouton, pos_souris)

        pygame.display.flip()
        horloge.tick(60)

def ecran_composition_equipe():
    """Écran pour la composition d'équipe."""
    print("Écran de composition d'équipe !")
    en_ecran_equipe = True
    horloge = pygame.time.Clock()

    texte_equipe = police_sous_titre.render("Composition d'équipe PokIUT", True, VIOLET_SECONDAIRE)
    texte_equipe_rect = texte_equipe.get_rect(center=(LARGEUR // 2, HAUTEUR // 4))

    bouton_retour_rect = pygame.Rect(0, 0, 200, 60)
    bouton_retour_rect.center = (LARGEUR // 2, HAUTEUR // 2 + 150)

    while en_ecran_equipe:
        pos_souris = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if bouton_retour_rect.collidepoint(event.pos):
                        en_ecran_equipe = False

        # --- Dessin de l'écran Composition d'équipe ---
        if fond_image_jeu:
            FENETRE.blit(fond_image_jeu, (0, 0))
        else:
            dessiner_fond_degrade(NOIR, BLEU_BOUTON) # Dégradé spécifique
        
        FENETRE.blit(texte_equipe, texte_equipe_rect)
        
        # TODO: Afficher les PokIUT possédés et permettre de les arranger
        texte_placeholder = police_bouton.render("Tes PokIUTs seront ici !", True, GRIS_CLAIR)
        FENETRE.blit(texte_placeholder, texte_placeholder.get_rect(center=(LARGEUR // 2, HAUTEUR // 2)))

        dessiner_bouton("Retour", bouton_retour_rect, ROUGE_BOUTON, BLANC, police_bouton, pos_souris)

        pygame.display.flip()
        horloge.tick(60)

def main_game_menu():
    """
    Menu principal du jeu après avoir cliqué sur "Jouer" depuis le menu de démarrage.
    Contient les options "Tirage au sort", "Composition d'équipe" et "Retour".
    """
    print("Affichage du menu principal du jeu.")
    en_main_game_menu = True
    horloge = pygame.time.Clock()

    # --- Titre du Menu du Jeu ---
    texte_titre_jeu = police_sous_titre.render("Aventure PokIUT", True, JAUNE_TITRE)
    ombre_titre_jeu = police_sous_titre.render("Aventure PokIUT", True, NOIR)
    titre_jeu_rect = texte_titre_jeu.get_rect(center=(LARGEUR // 2, HAUTEUR // 5))
    ombre_titre_jeu_rect = ombre_titre_jeu.get_rect(center=(LARGEUR // 2 + 3, HAUTEUR // 5 + 3))

    # --- Boutons ---
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
                        ecran_gacha()
                    elif bouton_equipe_rect.collidepoint(event.pos):
                        print("Accès à l'écran de Composition d'équipe.")
                        ecran_composition_equipe()
                    elif bouton_retour_rect.collidepoint(event.pos):
                        print("Retour au menu principal.")
                        en_main_game_menu = False # Quitte cette boucle pour revenir au menu principal

        # --- Affichage / Dessin ---
        if fond_image_jeu:
            FENETRE.blit(fond_image_jeu, (0, 0))
        else:
            dessiner_fond_degrade(GRIS_CLAIR, BLEU_BOUTON) # Dégradé pour le menu de jeu

        FENETRE.blit(ombre_titre_jeu, ombre_titre_jeu_rect)
        FENETRE.blit(texte_titre_jeu, titre_jeu_rect)

        dessiner_bouton("Tirage de PokIUTs", bouton_gacha_rect, BLEU_BOUTON, BLANC, police_bouton, pos_souris)
        dessiner_bouton("Composition d'équipe", bouton_equipe_rect, VIOLET_SECONDAIRE, BLANC, police_bouton, pos_souris)
        dessiner_bouton("Retour", bouton_retour_rect, ROUGE_BOUTON, BLANC, police_bouton, pos_souris)

        pygame.display.flip()
        horloge.tick(60)

def menu_principal():
    """
    Menu de démarrage initial avec les boutons "Jouer" et "Quitter".
    """
    en_train_de_jouer = True
    
    # --- Titre du Jeu ---
    texte_titre = police_titre.render("PokIUT", True, JAUNE_TITRE)
    ombre_titre = police_titre.render("PokIUT", True, NOIR)
    
    titre_rect = texte_titre.get_rect(center=(LARGEUR // 2, HAUTEUR // 4))
    ombre_rect = ombre_titre.get_rect(center=(LARGEUR // 2 + 5, HAUTEUR // 4 + 5))

    # --- Boutons ---
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
                        main_game_menu() # Lance le nouveau menu du jeu
                        # Si main_game_menu() se termine (en cliquant sur "Retour"),
                        # on revient ici dans la boucle du menu_principal
                    elif bouton_quitter_rect.collidepoint(event.pos):
                        print("Bouton Quitter cliqué !")
                        en_train_de_jouer = False

        # --- Affichage / Dessin ---
        if fond_image_menu: # Utilise le fond_image_menu
            FENETRE.blit(fond_image_menu, (0, 0))
        else:
            dessiner_fond_degrade(NOIR, BLEU_BOUTON)

        FENETRE.blit(ombre_titre, ombre_rect)
        FENETRE.blit(texte_titre, titre_rect)

        dessiner_bouton("Jouer", bouton_jouer_rect, BLEU_BOUTON, BLANC, police_bouton, pos_souris)
        dessiner_bouton("Quitter", bouton_quitter_rect, ROUGE_BOUTON, BLANC, police_bouton, pos_souris)
        
        pygame.display.flip()

    # --- Quitter Pygame ---
    pygame.quit()
    sys.exit()

# --- Lancer le menu principal au démarrage du script ---
if __name__ == "__main__":
    menu_principal()