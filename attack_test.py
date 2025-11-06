# test_attack.py
import pytest
from attack import Attack
from character import Character

def test_attack_hits_and_deals_damage(monkeypatch):
    attacker = Character("Hero", 100, 50, 20, 0, 0, 10, [])
    defender = Character("Enemy", 100, 30, 20, 0, 0, 10, [])
    attack = Attack("Slash", "ATK", 40, 100)

    # Force accuracy = success
    monkeypatch.setattr("random.randint", lambda a, b: 1)

    damage = attack.attempt(attacker, defender)
    assert damage > 0
    assert defender.hp < 100

def test_attack_misses(monkeypatch):
    attacker = Character("Hero", 100, 50, 20, 0, 0, 10, [])
    defender = Character("Enemy", 100, 30, 20, 0, 0, 10, [])
    attack = Attack("Slash", "ATK", 40, 100)

    # Force accuracy = miss
    monkeypatch.setattr("random.randint", lambda a, b: 101)

    damage = attack.attempt(attacker, defender)
    assert damage == 0
    assert defender.hp == 100

def test_attack_reduced_when_defending(monkeypatch):
    attacker = Character("Hero", 100, 50, 20, 0, 0, 10, [])
    defender = Character("Enemy", 100, 30, 20, 0, 0, 10, [])
    defender.is_defending = True
    attack = Attack("Slash", "ATK", 40, 100)

    monkeypatch.setattr("random.randint", lambda a, b: 1)

    damage = attack.attempt(attacker, defender)
    assert defender.hp == 100 - damage
    assert damage < 20  # should be reduced by half
    assert defender.is_defending is False  # defense only for 1 turn
