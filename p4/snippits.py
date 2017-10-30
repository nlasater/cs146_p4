#take strongest enemy planet, using 3 strongest planets in range or strongest planet if in range
def take_strongest_enemy(state):
  
    strongest_enemy = max(state.enemy_planets(), key=lambda t: t.num_ships, default=None)
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)
    
    distance = state.distance(strongest_planet, strongest_enemy)
    if distance <= max_range:
      return issue_order(state, strongest_planet.ID, strongest_enemy.ID, strongest_planet.num_ships*max_allowable_send_percentage)
    else:
      return False
      
      
      
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
    my_planet_count = sum(planet for planet in state.my_planets())
    my_ship_count_average = my_ship_count/my_planet_count
    
    if my_ship_count_average > agressive_fleet_min:
      return True
    else:
      return False
    
  # returns true if we can take largest enemy planet with our one/two strongest planets
def can_take_largest_enemy_planet(state):
    largest_enemy_planet_count = max(planet.num_ships for planet in state.enemy_planets())
    my_largest_planet_count = max(planet.num_ships for planet in state.my_planets())
    
    if my_largest_planet_count*max_allowable_send_percentage > largest_enemy_planet_count:
      return True
    else:
      # take this and the next strongest planet
      my_largest_planet_count = my_largest_planet_count + max(planet.num_ships != my_largest_planet_count for planet in state.my_planets(), 0)
      if my_largest_planet_count*max_allowable_send_percentage > largest_enemy_planet_count:
        return True
      else:
        return False