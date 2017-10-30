import sys
sys.path.insert(0, '../')
from planet_wars import issue_order

#target_planet
max_range = 1000

def attack_weakest_enemy_planet(state):
    # (1) If we currently have a fleet in flight, abort plan.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)

#take strongest enemy planet, using 3 strongest planets in range or strongest planet if in range
def take_strongest_enemy(state):
  print("doing blitz");
  strongest_enemy = max(state.enemy_planets(), key=lambda t: t.num_ships, default=None)
  strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)
    
  distance = state.distance(strongest_planet, strongest_enemy)
  if distance <= max_range:
    return issue_order(state, strongest_planet.ID, strongest_enemy.ID, strongest_planet.num_ships*max_allowable_send_percentage)
  else:
    return False
    
def spread_to_weakest_neutral_planet(state):
    # (1) If we currently have a fleet in flight, just do nothing.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest neutral planet.
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)

def defend_Weakest_Planet(state):
    my_ship_count = sum(planet.num_ships for planet in state.my_planets())
    my_planet_count = len(state.my_planets())
    my_ship_count_average = my_ship_count/my_planet_count
    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)
    # (3) Find the weakest planet.
    weakest_planet = min(state.my_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        #Send half my ships from my strongest planet to my weakest planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, (strongest_planet.num_ships +weakest_planet.num_ships)/2);