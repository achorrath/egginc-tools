import math


### Goals
# units: embedded
time_to_complete = '23hr15min'

# units: eggs
target_eggs = '5.0q'

# units: chickens
target_chickens = '1.0B'


### Stats
# units: eggs
eggs = '3.3q'

# units: chickens
farm_population = 690676309

# units: eggs / minute
egg_laying_rate = '694.026B'

# units: chickens / minute / hab
int_hatchery_rate = 5940

# habs
habs = 4

# units: dimensionless
internal_hatchery_calm = 3


### functions
def parse_time(timestr):
    orig = timestr
    days = 0
    hours = 0
    minutes = 0
    if 'd' in timestr:
        daystr, timestr = timestr.split('d')
        days = int(daystr)
    if 'hr' in timestr:
        hourstr, timestr = timestr.split('hr')
        hours = int(hourstr)
    if 'min' in timestr:
        minutestr, timestr = timestr.split('min')
        minutes = int(minutestr)
    if timestr:
        raise ValueError('unknown time value %s (from %s)' % (timestr, orig))
    # units: minutes
    return days * 24 * 60 + hours * 60 + minutes


def format_time(num):
    days, remainder = divmod(num, 24 * 60)
    hours, remainder = divmod(remainder, 60)
    if days:
        return '%dd%dhr' % (days, hours)
    minutes, remainder = divmod(remainder, 1)
    if hours:
        return '%dhr%dmin' % (hours, minutes)
    return '%dmin' % minutes


def parse_value(valstr):
    suffix = valstr[-1]
    if suffix in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
        return int(valstr)
    mantissa = float(valstr[:-1])
    if suffix == 'B':
        exponent = 9
    elif suffix == 'T':
        exponent = 12
    elif suffix == 'q':
        exponent = 15
    else:
        raise ValueError('unknown suffix %s (from %s)' % (suffix, valstr))
    return mantissa * 10 ** exponent


def format_value(value):
    oom3 = int(math.log(value, 1000))
    if oom3 < 3:
        return str(int(value))
    mantissa = value / 1000**oom3
    suffix = None
    if oom3 == 3:
        suffix = 'B'
    if oom3 == 4:
        suffix = 'T'
    if oom3 == 5:
        suffix = 'q'
    if oom3 == 6:
        suffix = 'Q'
    if suffix is None:
        raise ValueError('result too large: 1000**%d' % oom3)
    return'%.3f%s' % (mantissa, suffix)


### Intermediate values

# units: eggs / minute / chicken = (eggs / minute) / chickens
egg_laying_rate_per_chicken = parse_value(egg_laying_rate) / farm_population

# units: chickens / minute = (chickens / minute / hab) * habs * dimensionless
chicken_hatching_rate = int_hatchery_rate * habs * internal_hatchery_calm


### Values at completion time
print('Stats at completion time')
# units: eggs
e_current = parse_value(eggs)

# units: eggs / minute
e_velocity = parse_value(egg_laying_rate)

# units: eggs / minute / minute = (chickens / minute) * (eggs / minute / chicken)
e_acceleration = chicken_hatching_rate * egg_laying_rate_per_chicken

# units: minutes
t = parse_time(time_to_complete)

# units: eggs
e_final = e_current + e_velocity * t + 0.5 * e_acceleration * t * t
print('eggs:', format_value(e_final))

# units: chickens
c_current = farm_population

# units: chickens / minute
c_velocity = chicken_hatching_rate

# units: chickens
c_final = c_current + c_velocity * t
print('farm population:', format_value(c_final))

# units: chickens / minute
e_velocity_final = e_velocity + e_acceleration * t
print('egg laying rate', format_value(e_velocity_final))
print()


### Values at egg target
# solve for t
# e_final = e_current + e_velocity * t + 0.5 * e_acceleration * t * t
# 0.5 * e_acceleration * t * t + e_velocity * t + e_current - e_final = 0
print('Stats at egg target')

# units: eggs
e_final = parse_value(target_eggs)

# quadratic equation
a = 0.5 * e_acceleration
b = e_velocity
c = e_current - e_final
d = b**2 - 4*a*c

# units: minutes
t = (-b + math.sqrt(d)) / (2 * a)
print('target reached in', format_time(t))
print('eggs:', format_value(e_final))

# units: chickens
c_final = c_current + c_velocity * t
print('farm population:', format_value(c_final))

# units: chickens / minute
e_velocity_final = e_velocity + e_acceleration * t
print('egg laying rate', format_value(e_velocity_final))
print()


### Values at chicken target
# solve for t
# c_final = c_current + c_velocity * t
print('Stats at chicken target')

# units: chickens
c_final = parse_value(target_chickens)

# units: minutes
t = (c_final - c_current) / c_velocity
print('target reached in', format_time(t))

# units: eggs
e_final = e_current + e_velocity * t + 0.5 * e_acceleration * t * t
print('eggs:', format_value(e_final))
print('farm population:', format_value(c_final))

# units: chickens / minute
e_velocity_final = e_velocity + e_acceleration * t
print('egg laying rate', format_value(e_velocity_final))
print()

