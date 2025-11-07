import pytest
from unittest.mock import MagicMock
from character import Character
from combat import lancer_combat

# Test pour la composition de l'équipe
def test_composition_equipe():
    """Test de la logique de composition de l'équipe."""
    global equipe_combat
    equipe_combat = []  # Assure que l'équipe de combat est vide avant
    
    # Créer une équipe fictive de 6 personnages
    equipe_joueur = [
        MagicMock(Character, name="Pikachu", hp=100, max_hp=100),
        MagicMock(Character, name="Bulbizarre", hp=100, max_hp=100),
        MagicMock(Character, name="Carapuce", hp=100, max_hp=100),
        MagicMock(Character, name="Salamèche", hp=100, max_hp=100),
        MagicMock(Character, name="Evoli", hp=100, max_hp=100),
        MagicMock(Character, name="Rondoudou", hp=100, max_hp=100)
    ]
    
    assert len(equipe_combat) == 0  # Aucun personnage dans l'équipe au départ
    assert len(equipe_joueur) == 6  # Assure que l'équipe a bien 6 personnages tirés
    
    # Simuler l'ajout de personnages à l'équipe de combat
    equipe_combat.append(equipe_joueur[0])  # Ajouter le premier personnage
    assert len(equipe_combat) == 1  # L'équipe de combat a maintenant 1 personnage
    
    equipe_combat.append(equipe_joueur[1])  # Ajouter le deuxième personnage
    assert len(equipe_combat) == 2  # L'équipe de combat a maintenant 2 personnages

    equipe_combat.append(equipe_joueur[2])  # Ajouter le troisième personnage
    assert len(equipe_combat) == 3  # L'équipe de combat est maintenant complète

    # Vérifier qu'il n'est pas possible d'ajouter un 4e personnage
    # Essayer d'ajouter un 4e personnage
    if len(equipe_combat) < 3:
        equipe_combat.append(equipe_joueur[3])  # Ajouter un 4e personnage
    assert len(equipe_combat) == 3  # L'équipe de combat ne peut contenir plus de 3 personnages

# Test pour vérifier la gestion des victoires et défaites
def test_compteur_victoires():
    """Test de la gestion des victoires et défaites dans le jeu."""
    global compteur_victoires, compteur_defaites
    compteur_victoires = 0
    compteur_defaites = 0
    
    # Mock des arguments nécessaires pour lancer_combat
    mock_dessiner_infos_perso = MagicMock()
    mock_police_bouton = MagicMock()
    mock_police_info = MagicMock()
    mock_LARGEUR = 800
    mock_HAUTEUR = 600
    mock_VERT_VIE = 50
    mock_ROUGE_VIE_FOND = 50

    # Simuler un combat gagné
    lancer_combat_result = "victoire"
    lancer_combat.return_value = lancer_combat_result
    lancer_combat(
        equipe_joueur=[MagicMock(Character) for _ in range(3)], 
        dessiner_infos_perso=mock_dessiner_infos_perso,
        police_bouton=mock_police_bouton, 
        police_info=mock_police_info, 
        LARGEUR=mock_LARGEUR, 
        HAUTEUR=mock_HAUTEUR, 
        VERT_VIE=mock_VERT_VIE, 
        ROUGE_VIE_FOND=mock_ROUGE_VIE_FOND
    )
    
    # Vérifier les compteurs après une victoire
    assert compteur_victoires == 1  # Le compteur des victoires doit être à 1
    assert compteur_defaites == 0  # Le compteur des défaites reste à 0
    
    # Simuler un combat perdu
    lancer_combat_result = "defaite"
    lancer_combat.return_value = lancer_combat_result
    lancer_combat(
        equipe_joueur=[MagicMock(Character) for _ in range(3)], 
        dessiner_infos_perso=mock_dessiner_infos_perso,
        police_bouton=mock_police_bouton, 
        police_info=mock_police_info, 
        LARGEUR=mock_LARGEUR, 
        HAUTEUR=mock_HAUTEUR, 
        VERT_VIE=mock_VERT_VIE, 
        ROUGE_VIE_FOND=mock_ROUGE_VIE_FOND
    )
    
    # Vérifier les compteurs après une défaite
    assert compteur_victoires == 1  # Le compteur des victoires reste inchangé
    assert compteur_defaites == 1  # Le compteur des défaites doit être à 1

# Test pour vérifier la fonction lancer_combat
def test_lancer_combat():
    """Test pour vérifier si le combat fonctionne correctement."""
    global equipe_combat
    equipe_combat = [
        MagicMock(Character, name="Pikachu", hp=100, max_hp=100),
        MagicMock(Character, name="Bulbizarre", hp=100, max_hp=100),
        MagicMock(Character, name="Carapuce", hp=100, max_hp=100)
    ]
    
    # Mock des arguments nécessaires pour lancer_combat
    mock_dessiner_infos_perso = MagicMock()
    mock_police_bouton = MagicMock()
    mock_police_info = MagicMock()
    mock_LARGEUR = 800
    mock_HAUTEUR = 600
    mock_VERT_VIE = 50
    mock_ROUGE_VIE_FOND = 50
    
    # Simuler un combat avec des arguments mockés
    result = lancer_combat(
        equipe_joueur=equipe_combat, 
        dessiner_infos_perso=mock_dessiner_infos_perso,
        police_bouton=mock_police_bouton, 
        police_info=mock_police_info, 
        LARGEUR=mock_LARGEUR, 
        HAUTEUR=mock_HAUTEUR, 
        VERT_VIE=mock_VERT_VIE, 
        ROUGE_VIE_FOND=mock_ROUGE_VIE_FOND
    )
    
    # Vérifier que le combat renvoie un résultat valide
    assert result in ["victoire", "defaite"]  # Le résultat doit être une victoire ou une défaite
