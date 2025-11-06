from character import Character
from attack import Attack

# Définir quelques attaques de base
slash = Attack(name="Slash", kind="ATK", power=40, accuracy=95)
punch = Attack(name="Punch", kind="ATK", power=30, accuracy=100)
kick  = Attack(name="Kick",  kind="ATK", power=50, accuracy=90)

character_list = [
    Character(name="Jade", max_hp=70, atk=80, defense=80, speed=100, atk_spe=0, def_spe=0, attacks=[slash, punch], sprite="assets/sprites/jade.png"),
    Character(name="Yannick", max_hp=150, atk=50, defense=40, speed=15, atk_spe=0, def_spe=0, attacks=[slash], sprite="assets/sprites/yannick.png"),
    Character(name="Lucas MichMich", max_hp=100, atk=40, defense=60, speed=40, atk_spe=0, def_spe=0, attacks=[kick], sprite="assets/sprites/lucas_michmich.png"),
    Character(name="Corentin", max_hp=100, atk=60, defense=40, speed=40, atk_spe=0, def_spe=0, attacks=[slash, kick], sprite="assets/sprites/corentin.png"),
    Character(name="Philippe", max_hp=85, atk=60, defense=70, speed=60, atk_spe=0, def_spe=0, attacks=[punch], sprite="assets/sprites/philippe.png"),
    Character(name="Martimoule", max_hp=70, atk=85, defense=90, speed=100, atk_spe=0, def_spe=0, attacks=[slash, kick], sprite="assets/sprites/martimoule.png"),
    Character(name="Ugo", max_hp=85, atk=80, defense=50, speed=95, atk_spe=0, def_spe=0, attacks=[punch], sprite="assets/sprites/ugo.png"),
    Character(name="Ibrahim", max_hp=150, atk=35, defense=20, speed=15, atk_spe=0, def_spe=0, attacks=[slash], sprite="assets/sprites/ibrahim.png"),
    Character(name="Igor", max_hp=100, atk=50, defense=20, speed=60, atk_spe=0, def_spe=0, attacks=[kick], sprite="assets/sprites/igor.png"),
    Character(name="Claire La Femme", max_hp=100, atk=100, defense=20, speed=60, atk_spe=0, def_spe=0, attacks=[slash, punch, kick], sprite="aassets/sprites/claire_la_femme.png"),
    Character(name="Hervé SilverFarb", max_hp=100, atk=100, defense=20, speed=60, atk_spe=0, def_spe=0, attacks=[slash, punch, kick], sprite="assets/sprites/herve.png"),
    Character(name="Alexy Rassoul", max_hp=100, atk=50, defense=100, speed=40,atk_spe=0, def_spe=0, attacks=[slash, punch, kick], sprite="assets/sprites/rassoul.png")
]

