# test_defense.py
from attack import Defense
from character import Character

def test_defense_activates():
    c = Character("Hero", 100, 30, 20, 15, 15, 10, [])
    assert c.is_defending is False
    Defense.activate(c)
    assert c.is_defending is True
