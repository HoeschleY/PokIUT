import pytest
from character import Character

def test_character_starts_with_full_hp():
    c = Character("Hero", 100, 30, 20, 15, 15, 10, [])
    assert c.hp == 100

def test_take_damage_reduces_hp():
    c = Character("Hero", 100, 30, 20, 15, 15, 10, [])
    c.take_damage(30)
    assert c.hp == 70

def test_hp_cannot_go_below_zero():
    c = Character("Hero", 100, 30, 20, 15, 15, 10, [])
    c.take_damage(999)
    assert c.hp == 0

def test_is_ko_returns_true_when_hp_zero():
    c = Character("Hero", 100, 30, 20, 15, 15, 10, [])
    c.take_damage(100)
    assert c.is_ko() is True

def test_level_up_increases_level_and_stats():
    c = Character("Hero", 100, 30, 20, 15, 15, 10, [])
    c.level_up()
    assert c.level == 2
    assert c.max_hp > 100   # HP augmente
    assert c.hp == c.max_hp # HP régénéré
    assert c.atk > 30       # attaque augmente

def test_sprite_state_changes_when_ko():
    c = Character("Hero", 100, 30, 20, 15, 15, 10, [], sprite="hero.png")
    c.take_damage(100)
    assert c.sprite_state() == "ko"
