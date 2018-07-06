from __future__ import print_function

import farm

# upgrade requirement
target_farm_value = '6.7Sd'

# farm details
hab_max_capacity = 1461600000
farm_value = '75.978sd'
farm_population = 82435477
int_hatchery_rate = 6440

myfarm = farm.Farm(max_capacity=hab_max_capacity, farm_value=farm_value,
                   farm_population=farm_population,
                   int_hatchery_rate=int_hatchery_rate)
t = myfarm.time_to_value(target_farm_value)
goalfarm = myfarm.future(t)

if goalfarm.farm_population > hab_max_capacity:
    t = myfarm.time_to_max_chickens()
    fullfarm = myfarm.future(t)
    print('full farm reached in', farm.format_time(t))
    fullfarm.report()
    print()

print('target reached in', farm.format_time(t))
goalfarm.report()
print()

