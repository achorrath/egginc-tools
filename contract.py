from __future__ import print_function

import farm
import math

# contract details
time_to_complete = '3d'
egg_goal_1 = '50T'
egg_goal_2 = '500T'
egg_goal_3 = '4.0q'

# farm details
eggs = '437T'
farm_population = 337283248
egg_laying_rate = '338.919B'
int_hatchery_rate = 5840

myfarm = farm.Farm(eggs=eggs, farm_population=farm_population,
                   egg_laying_rate=egg_laying_rate,
                   int_hatchery_rate=int_hatchery_rate)
ttc = farm.parse_time(time_to_complete)
bestfarm = myfarm.future(ttc)

best_reported = False
for n, egg_goal in enumerate([egg_goal_1, egg_goal_2, egg_goal_3]):
    if egg_goal is None:
        break

    goal = farm.parse_value(egg_goal)
    t = myfarm.time_to_eggs(goal)
    if t > ttc:
        if not best_reported:
            print('contract complete in', time_to_complete)
            bestfarm.report()
            print()
            best_reported = True

    print('goal', n+1)
    if myfarm.eggs >= goal:
        print('completed')
    else:
        if t > ttc:
            print('completed after contract ends, in', farm.format_time(t))
        else:
            print('completed in', farm.format_time(t))
        goalfarm = myfarm.future(t)
        goalfarm.report()
    print()

if not best_reported:
    print('contract complete in', time_to_complete)
    bestfarm.report()
    print()
    best_reported = True

