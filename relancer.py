# relancer.py
import pygame
import sys

# --- Constantes (doivent être définies à nouveau) ---
LARGEUR, HAUTEUR = 1200, 800
BLANC = (255, 255, 255)
BLEU_BOUTON = (70, 130, 180)
ROUGE_BOUTON = (220, 20, 60)
JAUNE_TITRE = (255, 215, 0)
VIOLET_SECONDAIRE = (138, 43, 226)

# --- Fonction dessiner_bouton (copiée) ---
def dessiner_bouton(surface, texte, rect, couleur_fond, couleur_texte, police, pos_souris):
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

def ecran_relancer():
    pygame.init()
    FENETRE = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("Fin du combat")
    clock = pygame.time.Clock()

    # --- Polices (définies à nouveau) ---
    try:
        police_titre = pygame.font.Font("pokemonsolid.ttf", 80)
    except FileNotFoundError:
        police_titre = pygame.font.Font(None, 80)
    police_bouton = pygame.font.Font(None, 45)

    # --- Lire le résultat du combat ---
    try:
        with open("resultat.txt", "r") as f:
            resultat = f.read().strip()
    except FileNotFoundError:
        resultat = "defaite" # Sécurité

    if resultat == "victoire":
        texte_titre = police_titre.render("Victoire !", True, JAUNE_TITRE)
        message = "3 nouveaux PokIUTs ont été ajoutés à votre réserve !"
    else:
        texte_titre = police_titre.render("Défaite...", True, ROUGE_BOUTON)
        message = "Vous obtenez 3 PokIUTs de consolation."
        
    texte_titre_rect = texte_titre.get_rect(center=(LARGEUR // 2, HAUTEUR // 2 - 150))
    texte_message = police_bouton.render(message, True, BLANC)
    texte_message_rect = texte_message.get_rect(center=(LARGEUR // 2, HAUTEUR // 2 - 50))

    # --- Boutons ---
    bouton_continuer_rect = pygame.Rect(0, 0, 250, 70)
    bouton_continuer_rect.center = (LARGEUR // 2, HAUTEUR // 2 + 50)
    bouton_changer_equipe_rect = pygame.Rect(0, 0, 300, 70)
    bouton_changer_equipe_rect.center = (LARGEUR // 2, HAUTEUR // 2 + 140)

    while True:
        pos_souris = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    
                    choix = None
                    if bouton_continuer_rect.collidepoint(pos_souris):
                        choix = "continuer"
                    elif bouton_changer_equipe_rect.collidepoint(pos_souris):
                        choix = "changer_equipe"
                        
                    if choix:
                        # Écrire le choix dans un fichier
                        with open("choix.txt", "w") as f:
                            f.write(choix)
                        pygame.quit()
                        sys.exit() # Ferme ce script

        FENETRE.fill((20, 0, 30)) # Fond violet sombre
        FENETRE.blit(texte_titre, texte_titre_rect)
        FENETRE.blit(texte_message, texte_message_rect)
        dessiner_bouton(FENETRE, "Continuer", bouton_continuer_rect, BLEU_BOUTON, BLANC, police_bouton, pos_souris)
        dessiner_bouton(FENETRE, "Changer d'équipe", bouton_changer_equipe_rect, VIOLET_SECONDAIRE, BLANC, police_bouton, pos_souris)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    ecran_relancer()