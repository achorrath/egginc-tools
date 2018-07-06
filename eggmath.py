from __future__ import print_function

import farm
import math

### Goals
# units: embedded
time_to_complete = '24hr'

# units: eggs
target_eggs = '5.0q'

# units: chickens
target_chickens = '1.0B'

# units: dollars
target_farm_value = '6.7Sd'

### Stats
# units: eggs
eggs = '3.3q'

# units: chickens
hab_max_capacity = 1461600000

# units: dollars
farm_value = '75.978sd'

# units: chickens
farm_population = 82435477

# units: eggs / minute
egg_laying_rate = '140.820B'

# units: chickens / minute / hab
int_hatchery_rate = 6440


### Values at completion time
print('Stats at completion time')
myfarm = farm.Farm(eggs=eggs, max_capacity=hab_max_capacity, farm_value=farm_value, farm_population=farm_population, egg_laying_rate=egg_laying_rate, int_hatchery_rate=int_hatchery_rate)
new_farm = myfarm.future(time_to_complete)
new_farm.report()
print()


### Values at egg target
print('Stats at egg target')

# units: eggs
e_final = farm.parse_value(target_eggs)
t = myfarm.time_to_eggs(e_final)
print('target reached in', farm.format_time(t))

new_farm2 = myfarm.future(t)
new_farm2.report()
print()


### Values at chicken target
# solve for t
# c_final = c_current + c_velocity * t
print('Stats at chicken target')

# units: chickens
c_final = farm.parse_value(target_chickens)
c_current = myfarm.farm_population
c_velocity = myfarm.chicken_hatching_rate

# units: minutes
t = (c_final - c_current) / c_velocity
print('target reached in', farm.format_time(t))

new_farm3 = myfarm.future(t)
new_farm3.report()
print()


### Values at farm value target
# https://www.reddit.com/r/EggsInc/comments/63pfye/patashus_egg_inc_guide_xpost_from_regginc/
# Farm value is the sum of the three following terms (Thanks /u/dr_hal for finding the third term):
#
# income/sec * 54000
# income/sec/chicken * chicken hab max size * 6000
# income/sec/chicken * internal hatchery rate/hab/min * 7200000
# Then:
# 
# Multiply by accounting tricks (1.0x if not upgraded, 2.0x if fully upgraded)
# Multiply by (1.0+0.5 for each egg upgrade above edible egg). Examples: Edible egg = 1.0x, superfood egg = 1.5x, medical egg = 2x, rocket fuel egg = 2.5x ... terraform egg = 7.0x)

# My research says:
# farm_value = (hab capacity + 9*farm population + 12000*int hatchery rate) * value_scalar
# farm population is the only part that changes over time
print('Stats at farm value target')

# units: dollars
v_final = farm.parse_value(target_farm_value)

# units: chickens
c_final = (v_final / myfarm.value_scalar - (myfarm.max_capacity + 12000 * myfarm.int_hatchery_rate))/9

# units: minutes
t = (c_final - c_current) / c_velocity
print('target reached in', farm.format_time(t))
new_farm4 = myfarm.future(t)
new_farm4.report()

if c_final > hab_max_capacity:
    # units: dollars
    v_best = (10 * myfarm.max_capacity + 12000 * myfarm.int_hatchery_rate) * myfarm.value_scalar
    print('         best possible farm value:', farm.format_value(v_best))

