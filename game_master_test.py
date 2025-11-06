import pytest
from game_master import GameMaster
from character import Character

def create_fake_characters():
    return [
        Character(f"Hero{i}", 100, 30, 20, 15, 15, 10, [])
        for i in range(10)
    ]

def test_draw_six_characters_returns_exactly_6_unique():
    chars = create_fake_characters()
    gm = GameMaster(chars, seed=42)
    draw = gm.draw_characters(6)
    assert len(draw) == 6
    assert len(set(c.name for c in draw)) == 6  # aucun doublon

def test_cannot_draw_more_than_available():
    chars = create_fake_characters()
    gm = GameMaster(chars)
    with pytest.raises(ValueError):
        gm.draw_characters(20)
