#!/usr/bin/env python
#

"""
// There is already a basic strategy in place here. You can use it as a
// starting point, or you can throw it out entirely and replace it with your
// own.
"""
import logging, traceback, sys, os, inspect
logging.basicConfig(filename=__file__[:-3] +'.log', filemode='w', level=logging.DEBUG)
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from behavior_tree_bot.behaviors import *
from behavior_tree_bot.checks import *
from behavior_tree_bot.bt_nodes import Selector, Sequence, Action, Check

from planet_wars import PlanetWars, finish_turn

# You have to improve this tree or create an entire new one that is capable
# of winning against all the 5 opponent bots
def setup_behavior_tree():

    # Top-down construction of behavior tree
    root = Selector(name='High Level Ordering of Strategies')
    
    initial_strategy = Selector(name='Initial Strategy Selector')
    
    
    
    #offensive strategy
    offensive_plan = Sequence(name='Offensive Strategy')
    largest_fleet_check = Check(fleet_is_strong)
    largest_fleet_update = Check(update_agressive_fleet_min)
    can_take_check = Check(can_take_weakest_planet)
    attack = Action(attack_weakest_enemy_planet)
    offensive_plan.child_nodes = [largest_fleet_check, largest_fleet_update, can_take_check, attack]


    #defensive strategy.
    defensive_plan=Sequence(name="Defensive Strategy")
    planet_in_trouble_check=Check(planet_in_trouble);
    
    defend=Action(defend_Weakest_Planet);
    update_min = Check(update_planet_in_trouble)
    defensive_plan.child_nodes=[planet_in_trouble_check, defend, update_min];

    
    spread_sequence = Sequence(name='Spread Strategy')
    neutral_planet_check = Check(if_neutral_planet_available)
    spread_action = Action(spread_to_nearest_weakest_neutral_planet)
    spread_update = Action(update_extra_forces)
    spread_sequence.child_nodes = [neutral_planet_check, spread_action, spread_update]

    root.child_nodes = [spread_sequence, offensive_plan, spread_action.copy()]

    
    logging.info('\n' + root.tree_to_string())
    return root

# You don't need to change this function
def do_turn(state):
    behavior_tree.execute(planet_wars)

if __name__ == '__main__':
    logging.basicConfig(filename=__file__[:-3] + '.log', filemode='w', level=logging.DEBUG)

    behavior_tree = setup_behavior_tree()
    try:
        map_data = ''
        while True:
            current_line = input()
            if len(current_line) >= 2 and current_line.startswith("go"):
                planet_wars = PlanetWars(map_data)
                do_turn(planet_wars)
                finish_turn()
                map_data = ''
            else:
                map_data += current_line + '\n'

    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
    except Exception:
        traceback.print_exc(file=sys.stdout)
        logging.exception("Error in bot.")
