from game_messages import Message
from game_states import GameStates
from render_functions import RenderOrder

def kill_player(player, colors):
    player.char = "%"
    player.color = colors.get("dark_red")

    return Message("You died!", colors.get("red")), GameStates.PLAYER_DEAD

def kill_monster(monster, colors):
    death_message = Message(monster.name.capitalize() + " is dead!", colors.get("orange"))

    monster.char = "%"
    monster.color = colors.get("dark_red")
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = "Remains of " + monster.name
    monster.render_order = RenderOrder.CORPSE

    return death_message

