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
    
    """ BLITZ - not working
    initial_strategy = Selector(name='Initial Strategy Selector')
    
    blitz_plan = Sequence(name='Blitz Strategy')
    #colonize_plan = Sequence(name='Colonize Strategy')
    
    initial_strategy.child_nodes = [blitz_plan]
    
    enemy_owns_few_check = Check(enemy_owns_few_planets)
    
    take_target_seq = Sequence(name='Take Enemys largest planet (usually home)')
    can_we_take_target_selector = Selector(name='Can Fleet Take Planet')
    is_fleet_well_off_check = Check(fleet_is_strong)
    can_we_take_home_planet = Check(can_take_largest_enemy_planet)
    take_enemy_planet = Action(take_strongest_enemy)
    can_we_take_target_selector.child_nodes = [is_fleet_well_off_check, can_we_take_home_planet]
    take_target_seq.child_nodes = [can_we_take_target_selector, take_enemy_planet]
    blitz_plan.child_nodes = [take_target_seq]
     """
    
    offensive_plan = Sequence(name='Offensive Strategy')
    largest_fleet_check = Check(have_largest_fleet)
    attack = Action(attack_weakest_enemy_planet)
    offensive_plan.child_nodes = [largest_fleet_check, attack]

    spread_sequence = Sequence(name='Spread Strategy')
    neutral_planet_check = Check(if_neutral_planet_available)
    spread_action = Action(spread_to_weakest_neutral_planet)
    spread_sequence.child_nodes = [neutral_planet_check, spread_action]
   
    
    
    root.child_nodes = [offensive_plan, spread_sequence, attack.copy()]
    
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
