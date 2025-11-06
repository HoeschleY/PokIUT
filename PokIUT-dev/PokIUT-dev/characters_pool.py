from character import Character
from attack import Attack

# Définir quelques attaques de base
slash = Attack(name="Slash", kind="ATK", power=40, accuracy=95)
punch = Attack(name="Punch", kind="ATK", power=30, accuracy=100)
kick  = Attack(name="Kick",  kind="ATK", power=50, accuracy=90)

character_list = [
    Character(name="Jade", max_hp=70, atk=80, defense=80, speed=100, atk_spe=0, def_spe=0, attacks=[slash, punch]),
    Character(name="Yannick", max_hp=150, atk=50, defense=40, speed=15, atk_spe=0, def_spe=0, attacks=[slash]),
    Character(name="Lucas MichMich", max_hp=100, atk=40, defense=60, speed=40, atk_spe=0, def_spe=0, attacks=[kick]),
    Character(name="Corentin", max_hp=100, atk=60, defense=40, speed=40, atk_spe=0, def_spe=0, attacks=[slash, kick]),
    Character(name="Philippe", max_hp=85, atk=60, defense=70, speed=60, atk_spe=0, def_spe=0, attacks=[punch]),
    Character(name="Martimoule", max_hp=70, atk=85, defense=90, speed=100, atk_spe=0, def_spe=0, attacks=[slash, kick]),
    Character(name="Ugo", max_hp=85, atk=80, defense=50, speed=95, atk_spe=0, def_spe=0, attacks=[punch]),
    Character(name="Ibrahim", max_hp=150, atk=35, defense=20, speed=15, atk_spe=0, def_spe=0, attacks=[slash]),
    Character(name="Igor", max_hp=100, atk=50, defense=20, speed=60, atk_spe=0, def_spe=0, attacks=[kick]),
    Character(name="Claire La Femme", max_hp=100, atk=100, defense=20, speed=60, atk_spe=0, def_spe=0, attacks=[slash, punch, kick])
]
