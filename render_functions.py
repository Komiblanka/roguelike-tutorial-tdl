from enum import Enum
from game_states import GameStates
from menus import inventory_menu

class RenderOrder(Enum):
    CORPSE = 1
    ITEM = 2
    ACTOR = 3

def get_names_under_mouse(mouse_coordinates, entities, game_map):
    x, y = mouse_coordinates

    names = [entity.name for entity in entities
            if entity.x == x and entity.y == y and game_map.fov[entity.x, entity.y]]
                
    names = ", ".join(names)
    
    return names.capitalize()    

def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color, string_color):
    # Render a bar (HP, exp, etc..). First calculate the width of the bar
    bar_width = int(float(value) / maximum * total_width)

    # Render background first
    panel.draw_rect(x, y, total_width, 1, None, bg=back_color)

    # Now render bar on top
    if bar_width > 0:
        panel.draw_rect(x, y, bar_width, 1, None, bg=bar_color)

    # Finally, some centered text with values
    text = name + ": " + str(value) + "/" + str(maximum)
    x_centered = x + int((total_width-len(text))/2)

    panel.draw_str(x_centered, y, text, fg=string_color, bg=None)

def render_all(con, panel, entities, player, game_map, fov_recompute,  root_console, message_log, screen_width, screen_height, bar_width, panel_height, panel_y, mouse_coordinates, colors, game_state):
    # Draw map

    if fov_recompute:
        for x, y in game_map:
            wall = not game_map.transparent[x, y]

            if game_map.fov[x, y]:
                if wall:
                    con.draw_char(x, y, None, fg=None, bg=colors.get("light_wall"))
                else:
                    con.draw_char(x, y, None, fg=None, bg=colors.get("light_ground"))
                game_map.explored[x][y] = True

            elif game_map.explored[x][y]:
                if wall:
                    con.draw_char(x, y, None, fg=None, bg=colors.get("dark_wall"))
                else:
                    con.draw_char(x, y, None, fg=None, bg=colors.get("dark_ground"))

    # Draw all entities in the list
    entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)

    for entity in entities_in_render_order:
        draw_entity(con, entity, game_map.fov)

    root_console.blit(con, 0, 0, screen_width, screen_height, 0, 0)

    panel.clear(fg=colors.get("white"), bg=colors.get("black"))

    # Print the game messages, one at a time
    y = 1
    for message in message_log.messages:
        panel.draw_str(message_log.x, y, message.text, bg=None, fg=message.color)
        y += 1

    render_bar(panel, 1, 1, bar_width, "HP", player.fighter.hp, player.fighter.max_hp, colors.get("light_red"), colors.get("darker_red"), colors.get("white"))

    panel.draw_str(1, 0, get_names_under_mouse(mouse_coordinates, entities, game_map))

    root_console.blit(panel, 0, panel_y, screen_width, panel_height, 0, 0)

    if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        if game_state == GameStates.SHOW_INVENTORY:
            inventory_title = "Press the key next to an item to use it, or ESC to cancel.\n"
        else:
            inventory_title = "Press the key next to an item to drop it, or ESC to cancel.\n"

        inventory_menu(con, root_console, inventory_title, player.inventory, 50, screen_width, screen_height)

def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)

def draw_entity(con, entity, fov):
    # Draw the character
    if fov[entity.x, entity.y]:
        con.draw_char(entity.x, entity.y, entity.char, entity.color, bg=None)

def clear_entity(con, entity):
    # Erase character by printing something empty
    con.draw_char(entity.x, entity.y, " ", entity.color, bg=None)
