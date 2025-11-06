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
police_sous_titre = pygame.font.Font(None, 60)
police_info = pygame.font.Font(None, 30) # Police plus petite pour les infos

# --- Assets (Images) ---
fond_image_menu = None 
fond_image_jeu = None 

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

# ### MODIFIÉ ### : Logique de sélection d'équipe
def ecran_composition_equipe(game_master: GameMaster):
    """Écran pour la composition d'équipe."""
    print("Écran de composition d'équipe !")
    global equipe_combat # On va modifier la liste globale
    
    en_ecran_equipe = True
    horloge = pygame.time.Clock()

    texte_equipe = police_sous_titre.render("Composition d'équipe", True, VIOLET_SECONDAIRE)
    texte_equipe_rect = texte_equipe.get_rect(center=(LARGEUR // 2, HAUTEUR // 6)) # Plus haut

    bouton_retour_rect = pygame.Rect(0, 0, 200, 60)
    bouton_retour_rect.center = (LARGEUR // 2, HAUTEUR - 60) # Bouton "Retour" en bas

    # Créer les rectangles cliquables pour les personnages
    options_cliquables = []
    y_offset = HAUTEUR // 2 - 100
    for perso in equipe_joueur:
        texte_perso = police_bouton.render(perso.name, True, BLANC)
        rect = texte_perso.get_rect(center=(LARGEUR // 2, y_offset))
        options_cliquables.append({'perso': perso, 'rect': rect})
        y_offset += 50 # Plus d'espace

    message_info = "" # Pour afficher les erreurs (ex: "Équipe pleine")

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
                        
                    # On réinitialise le message d'info à chaque clic
                    message_info = "" 
                    
                    # Vérifier si on a cliqué sur un personnage
                    for option in options_cliquables:
                        if option['rect'].collidepoint(event.pos):
                            perso_clique = option['perso']
                            
                            if perso_clique in equipe_combat:
                                # Le personnage est déjà sélectionné -> on le retire
                                equipe_combat.remove(perso_clique)
                                print(f"Retiré : {perso_clique.name}. Équipe : {[p.name for p in equipe_combat]}")
                            else:
                                # Le personnage n'est pas sélectionné -> on l'ajoute
                                if len(equipe_combat) < 3:
                                    equipe_combat.append(perso_clique)
                                    print(f"Ajouté : {perso_clique.name}. Équipe : {[p.name for p in equipe_combat]}")
                                else:
                                    # L'équipe est pleine
                                    print("Équipe déjà pleine (3 personnages max) !")
                                    message_info = "Équipe pleine (3 max) !"

        # --- Dessin de l'écran Composition d'équipe ---
        if fond_image_jeu:
            FENETRE.blit(fond_image_jeu, (0, 0))
        else:
            dessiner_fond_degrade(NOIR, BLEU_BOUTON) 
        
        FENETRE.blit(texte_equipe, texte_equipe_rect)
        
        # Afficher le message d'info (ex: "Équipe pleine")
        texte_info = police_info.render(message_info, True, ROUGE_BOUTON)
        FENETRE.blit(texte_info, texte_info.get_rect(center=(LARGEUR // 2, HAUTEUR - 120)))
        
        # Afficher le statut de la sélection
        texte_statut = police_bouton.render(f"Équipe : {len(equipe_combat)} / 3", True, BLANC)
        FENETRE.blit(texte_statut, texte_statut.get_rect(center=(LARGEUR // 2, HAUTEUR // 4)))

        if not equipe_joueur:
            texte_placeholder = police_bouton.render("Tu n'as aucun PokIUT !", True, GRIS_CLAIR)
            FENETRE.blit(texte_placeholder, texte_placeholder.get_rect(center=(LARGEUR // 2, HAUTEUR // 2)))
        else:
            # Affiche les noms des personnages, en couleur si sélectionnés
            for option in options_cliquables:
                perso = option['perso']
                rect = option['rect']
                
                # Change la couleur si le personnage est dans l'équipe de combat
                couleur = JAUNE_TITRE if perso in equipe_combat else BLANC
                
                texte_perso = police_bouton.render(perso.name, True, couleur)
                FENETRE.blit(texte_perso, rect)

        dessiner_bouton("Valider et Retour", bouton_retour_rect, ROUGE_BOUTON, BLANC, police_bouton, pos_souris)

        pygame.display.flip()
        horloge.tick(60)

# (Le reste de ton script reste identique)

def main_game_menu(game_master: GameMaster):
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

if __name__ == "__main__":
    mon_game_master = GameMaster(characters=character_list, seed=None)
    menu_principal(mon_game_master)