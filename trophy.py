from __future__ import print_function

import farm

# trophy requirement
target_chickens = '1.0B'

# farm details
farm_population = 82435477
int_hatchery_rate = 6440

myfarm = farm.Farm(farm_population=farm_population,
                   int_hatchery_rate=int_hatchery_rate)
t = myfarm.time_to_chickens(target_chickens)
print('target reached in', farm.format_time(t))

goalfarm = myfarm.future(t)
goalfarm.report()
print()

