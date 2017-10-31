#set all variables to be checked against
blitz_min_planets = 3
agressive_fleet_min = 100
max_send = .7
being_attacked = None


def if_neutral_planet_available(state):
    return any(state.neutral_planets())


def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())

# returns true if enemy has less than or equal to blitz_min_planets        
def enemy_owns_few_planets(state):
  # check only planets we are not already attacking
  enemy_planets = [planet for planet in state.enemy_planets()
                      if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
  if enemy_planets.length <= blitz_min_planets:
    return True
  else:
    return False
  

  # returns true if our fleet average is over the agressive_fleet_min
  # note this only checks standby fleets, not active ones
def fleet_is_strong(state):
    my_ship_count = sum(planet.num_ships for planet in state.my_planets())
    my_planet_count = len(state.my_planets())
    if my_planet_count == 0:
      return False
    my_ship_count_average = my_ship_count/my_planet_count

    if my_ship_count_average > agressive_fleet_min:
      return True
    else:
      return False
    
def update_agressive_fleet_min(state):
    my_ship_count = sum(planet.num_ships for planet in state.my_planets())
    my_planet_count = len(state.my_planets())
    if my_planet_count == 0:
      return False
    my_ship_count_average = my_ship_count/my_planet_count
    
    agressive_fleet_min = my_ship_count_average + 20
    return True
    
  # returns true if we can take largest enemy planet with our one/two strongest planets
def can_take_largest_enemy_planet(state):
    largest_enemy_planet_count = max(planet.num_ships for planet in state.enemy_planets())
    my_largest_planet_count = max(planet.num_ships for planet in state.my_planets())
    second_strongest=-999;

    #Get second strongest planet.
    for planet in state.my_planets():
       if(planet.num_ships!=my_largest_planet_count and planet.num_ships>second_strongest): second_strongest=planet.num_ships;

    if my_largest_planet_count*max_send > largest_enemy_planet_count:
      return True

    else:
      # take this and the next strongest planet
      my_largest_planet_count = my_largest_planet_count + second_strongest;
      if my_largest_planet_count*max_send > largest_enemy_planet_count:
        return True
      else:
        return False
def can_take_weakest_planet(state):
    weakest_enemy = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None);
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None);
    
    if not weakest_enemy or not strongest_planet:
      return False
    
    if strongest_planet.num_ships*max_send > weakest_enemy.num_ships:
      return True
    else:
      return False
    
def planet_in_trouble(state):
    weakest_planet = min(state.my_planets(), key=lambda t: t.num_ships, default=None);
    if not weakest_planet:
      return False
    my_ship_count = sum(planet.num_ships for planet in state.my_planets())
    my_planet_count = len(state.my_planets())
    if my_planet_count == 0:
      return False
    my_ship_average = my_ship_count/my_planet_count
    
    planet_in_trouble_at = (my_ship_average*0.1)
    if(weakest_planet.num_ships < planet_in_trouble_at):
      return True;
    else: return False
    

# returns true if planet under attack, and sets being_attacked to [planet, attacking force]
def planet_under_attack(state):
  for fleet in state.enemy_fleets():
    if(fleet.destination_planet in state.my_planets().ID):
      being_attacked = fleet.destination_planet
      return True
    else:
      return False
    
    