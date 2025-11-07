from character import Character
from attack import Attack

# Définir quelques attaques de base
slash = Attack(name="Slash", kind="ATK", power=40, accuracy=95)
punch = Attack(name="Punch", kind="ATK", power=35, accuracy=100)
mega_punch = Attack(name="MegaPunch", kind="ATK", power=75, accuracy=85)
run = Attack(name="Run", kind="ATK", power=60, accuracy=100)
blague = Attack(name="Blague", kind="ATK", power=60, accuracy=70)
kick  = Attack(name="Kick",  kind="ATK", power=50, accuracy=90)
andrew = Attack(name="Andrew Special", kind="ATK", power=75, accuracy=85)
Vdecramer = Attack(name="Vdecramer", kind="ATK", power=65, accuracy=90)
dessine = Attack(name="Dessine", kind="ATK", power=70, accuracy=95)
ce_message_ne_vient_PAS_de_moi = Attack(name="Ce message ne vient PAS de moi", kind="ATK", power=80, accuracy=90)
dormir = Attack(name="Dormir", kind="DEF", power=45, accuracy=100)
valo = Attack(name="Valo", kind="ATK", power=50, accuracy=80)
roblox = Attack(name="Roblox", kind="ATK", power=50, accuracy=90)
enter_the_void = Attack(name="Enter the Void", kind="ATK", power=65, accuracy=70)
magic_the_gathering = Attack(name="Magic The Gathering", kind="ATK", power=60, accuracy=75)
mail = Attack(name="Mail", kind="ATK", power=50, accuracy=100)
do_brazil =  Attack(name="Do Brazil", kind="ATK", power=60, accuracy=100)

character_list = [
    Character(name="Jade", max_hp=70, atk=80, defense=40, speed=100, atk_spe=0, def_spe=0, attacks=[slash, punch, dormir], sprite="assets/sprites/jade.png"),
    Character(name="Yannick", max_hp=150, atk=50, defense=40, speed=15, atk_spe=0, def_spe=0, attacks=[slash, roblox, kick], sprite="assets/sprites/yannick.png"),
    Character(name="Lucas MichMich", max_hp=100, atk=40, defense=60, speed=40, atk_spe=0, def_spe=0, attacks=[kick, punch, enter_the_void], sprite="assets/sprites/lucas_michmich.png"),
    Character(name="Corentin", max_hp=100, atk=60, defense=40, speed=40, atk_spe=0, def_spe=0, attacks=[slash, kick, blague], sprite="assets/sprites/corentin.png"),
    Character(name="Philippe", max_hp=85, atk=60, defense=70, speed=60, atk_spe=0, def_spe=0, attacks=[punch, dormir, blague], sprite="assets/sprites/philippe.png"),
    Character(name="Martimoule", max_hp=70, atk=85, defense=70, speed=100, atk_spe=0, def_spe=0, attacks=[enter_the_void, dessine, dormir], sprite="assets/sprites/martimoule.png"),
    Character(name="Ugo", max_hp=85, atk=80, defense=50, speed=95, atk_spe=0, def_spe=0, attacks=[punch, mega_punch, kick], sprite="assets/sprites/ugo.png"),
    Character(name="Ibrahim", max_hp=150, atk=35, defense=20, speed=15, atk_spe=0, def_spe=0, attacks=[valo, dormir, roblox], sprite="assets/sprites/ibrahim.png"),
    Character(name="Igor", max_hp=100, atk=50, defense=20, speed=60, atk_spe=0, def_spe=0, attacks=[kick, mail, ce_message_ne_vient_PAS_de_moi], sprite="assets/sprites/igor.png"),
    Character(name="Claire La Femme", max_hp=100, atk=100, defense=20, speed=60, atk_spe=0, def_spe=0, attacks=[punch, mega_punch, andrew], sprite="assets/sprites/clairelafemme.png"),
    Character(name="Hervé SilverFarb", max_hp=100, atk=100, defense=20, speed=60, atk_spe=0, def_spe=0, attacks=[Vdecramer, punch, kick], sprite="assets/sprites/herve.png"),
    Character(name="Alexy Rassoul", max_hp=100, atk=50, defense=100, speed=40,atk_spe=0, def_spe=0, attacks=[magic_the_gathering, punch, kick], sprite="assets/sprites/rassoul.png"),
    Character(name="Lavalanche", max_hp=90, atk=90, defense=30, speed=20, atk_spe=0, def_spe=0, attacks=[slash, punch, kick], sprite="assets/sprites/laval.png"),
    Character(name="Leon", max_hp=50, atk=110, defense=60, speed=90, atk_spe=0, def_spe=0, attacks=[blague, punch, kick], sprite="assets/sprites/leon.png"),
    Character(name="Champ Billard", max_hp=150, atk=20, defense=40, speed=60, atk_spe=0, def_spe=0, attacks=[slash, punch, kick], sprite="assets/sprites/chanvillard.png"),
    Character(name="Adri Anguille", max_hp=100, atk=100, defense=10, speed=100, atk_spe=0, def_spe=0, attacks=[slash, Vdecramer, punch], sprite="assets/sprites/guille.png"),
    Character(name="Nolan", max_hp=70, atk=70, defense=70, speed=70, atk_spe=0, def_spe=0, attacks=[slash, run, kick], sprite="assets/sprites/nolan.png"),
    Character(name="Agouno", max_hp=100, atk=100, defense=20, speed=60, atk_spe=0, def_spe=0, attacks=[slash, punch, kick], sprite="assets/sprites/agoun.png"),
    Character(name="Boubou", max_hp=150, atk=50, defense=50, speed=50, atk_spe=0, def_spe=0, attacks=[slash, mega_punch, run], sprite="assets/sprites/boubou.png"),
    Character(name="Ouz Route", max_hp=100, atk=100, defense=100, speed=10, atk_spe=0, def_spe=0, attacks=[mega_punch, punch, slash], sprite="assets/sprites/ouzrout.png"),
    Character(name="Fan dy Rassoul", max_hp=10, atk=10, defense=10, speed=50, atk_spe=0, def_spe=0, attacks=[slash, punch, kick], sprite="assets/sprites/fan.png"),
    Character(name="Charo line", max_hp=90, atk=80, defense=60, speed=60, atk_spe=0, def_spe=0, attacks=[punch, kick, do_brazil], sprite="assets/sprites/charoline.png"),
    Character(name="Yanis", max_hp=90, atk=80, defense=70, speed=60, atk_spe=0, def_spe=0, attacks=[dormir, run, blague], sprite="assets/sprites/yanis.png"),
    Character(name="Muller", max_hp=90, atk=90, defense=90, speed=90, atk_spe=0, def_spe=0, attacks=[run, punch, kick], sprite="assets/sprites/muller.png")
]












