# test_combat.py
import pytest
from character import Character
from attack import Attack
from combat import clone_character, build_timeline, persos_vivants

# --- 1. Attaque basique ---
def test_attack_reduces_hp():
    attaquant = Character("TestA", 100, 50, 10, 10, 10, 20, [])
    defenseur = Character("TestB", 100, 30, 5, 10, 10, 15, [])
    attaque = Attack("Basic", "ATK", 40, 100)
    dmg = attaque.attempt(attaquant, defenseur)

    assert dmg > 0, "Le dégât doit être > 0"
    assert defenseur.hp == 100 - dmg, "HP doit avoir diminué"

# --- 2. KO ---
def test_character_gets_ko():
    c1 = Character("A", 50, 40, 10, 5, 5, 10, [])
    c2 = Character("B", 30, 40, 10, 5, 5, 10, [])
    atk = Attack("Strong", "ATK", 100, 100)

    dmg = atk.attempt(c1, c2)
    assert c2.hp == 0, "HP doit être 0 après KO"
    assert c2.is_ko() == True, "Personnage doit être KO"

# --- 3. Clonage propre ---
def test_clone_does_not_share_hp_or_sprite():
    orig = Character("Cloneable", 120, 40, 30, 5, 5, 10, [])
    clone = clone_character(orig)

    assert clone is not orig
    assert clone.name == orig.name
    assert clone.hp == orig.max_hp
    clone.hp -= 50
    assert orig.hp != clone.hp, "Les HP ne doivent pas être partagés"

# --- 4. Timeline (ordre par speed) ---
def test_timeline_sorted_by_speed():
    c1 = Character("Slow", 100, 20, 20, 5, 5, 5, [])
    c2 = Character("Fast", 100, 20, 20, 5, 5, 50, [])
    c3 = Character("Medium", 100, 20, 20, 5, 5, 30, [])

    timeline = build_timeline([c1, c2], [c3])
    names = [perso.name for _, perso in timeline]

    assert names == ["Fast", "Medium", "Slow"], "L'ordre de jeu doit suivre la vitesse"

# --- 5. Une attaque sur soi-même NE doit PAS arriver ---
def test_same_name_enemy_does_not_hurt_self():
    c1 = Character("Yannick", 100, 30, 20, 5, 5, 20, [])
    c2 = Character("Yannick", 100, 30, 20, 5, 5, 10, [])
    atk = Attack("Punch", "ATK", 50, 100)

    dmg = atk.attempt(c1, c2)  # Ce sont bien deux objets différents
    assert c1.hp == 100, "L'attaquant ne doit pas perdre sa propre vie"
    assert c2.hp < 100, "La cible doit bien perdre des HP"

