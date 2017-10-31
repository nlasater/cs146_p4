import sys
import operator
sys.path.insert(0, '../')
from planet_wars import issue_order
from checks import max_send
from math import fabs

#target_planet
max_range = 15
extra_forces = 8
max_send = .7
weakest_queue_size = 7

def attack_weakest_enemy_planet(state):
    target_planets = [planet for planet in state.enemy_planets()
                      if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    
    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    weakest_planet = min(target_planets, key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) send req'd ships from my strongest planet to the weakest enemy planet.
        req_ships = weakest_planet.num_ships + \
                                 state.distance(strongest_planet.ID, weakest_planet.ID) * weakest_planet.growth_rate + extra_forces
        if req_ships > strongest_planet.num_ships*max_send and len(state.my_planets()) > 1:
          return False
          
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, req_ships)

#take strongest enemy planet, using 3 strongest planets in range or strongest planet if in range
def take_strongest_enemy(state):
  print("doing blitz");
  strongest_enemy = max(state.enemy_planets(), key=lambda t: t.num_ships, default=None)
  strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)
    
  distance = state.distance(strongest_planet.ID, strongest_enemy.ID)
  if distance <= max_range:
    return issue_order(state, strongest_planet.ID, strongest_enemy.ID, strongest_planet.num_ships*max_send)
  else:
    return False
    
def spread_to_nearest_weakest_neutral_planet(state):
    target_planets = [planet for planet in state.neutral_planets()
                      if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    
    weakest_set = sorted(target_planets, key=lambda x: x.num_ships, reverse=True)
    new_targets = []
    for x in range (0, 4):
      if len(weakest_set) > 0:
        temp = weakest_set.pop()
        new_targets.append(temp)
    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest neutral planet.
    weakest_planet = max(new_targets, key=lambda p: p.growth_rate, default=None)
    
    

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
      
    elif fabs(state.distance(strongest_planet.ID, weakest_planet.ID)) > max_range:
      for x in range(0, len(target_planets)):
        weakest_planet = target_planets.pop()
        if fabs(state.distance(strongest_planet.ID, weakest_planet.ID)) <= max_range:
          break
        else:
          continue
    
    req_ships = weakest_planet.num_ships + extra_forces
    if req_ships > strongest_planet.num_ships:
        return False
    else:
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, req_ships)

def update_extra_forces(state):
  my_ship_count = sum(planet.num_ships for planet in state.my_planets())
  my_planet_count = len(state.my_planets())
  my_ship_count_average = my_ship_count/my_planet_count
  
  
  extra_forces =  my_ship_count_average/2
  return True

def defend_Weakest_Planet(state):
    target_planets = [planet for planet in state.my_planets()
                      if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    my_ship_count = sum(planet.num_ships for planet in state.my_planets())
    my_planet_count = len(state.my_planets())
    my_ship_count_average = my_ship_count/my_planet_count
    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)
    
    # (3) Find the weakest planet.
    weakest_planet = min(target_planets, key=lambda t: t.num_ships, default=None)
    
    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        
        return False
    if strongest_planet.ID == weakest_planet.ID:
      return False
    
    # if strongest planet is too far away, pick strongest 3 in range
    if state.distance(strongest_planet.ID, weakest_planet.ID) > max_range:
      distance_planets = []
      for planet in state.my_planets():
        if state.distance(planet.ID, weakest_planet.ID) < max_range:
          distance_planets.append([planet.num_ships, planet.ID])
        
      if not distance_planets:
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships/2)
      else:
        if len(distance_planets) < 3:
          for planet in distance_planets:
            issue_order(state, planet[1], weakest_planet.ID, planet[0]/2)
        else:
          distance_planets.sort()
          for x in range(0,3):
            
            issue_order(state, distance_planets[x][1], weakest_planet.ID, distance_planets[x][0]/2)
    else:
        #Send half my ships from my strongest planet to my weakest planet.
        
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships/2);
      

      