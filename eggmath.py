import numbers
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

# habs
habs = 4

# units: dimensionless
internal_hatchery_calm = 3


### functions
def parse_time(timestr):
    if isinstance(timestr, numbers.Number):
        return timestr
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
    if valstr is None:
        return None
    if isinstance(valstr, numbers.Number):
        return valstr
    if valstr[-1].isnumeric():
        return int(valstr)
    if valstr.endswith('M'):
        exponent = 6
        suffix_len = 1
    elif valstr.endswith('B'):
        exponent = 9
        suffix_len = 1
    elif valstr.endswith('T'):
        exponent = 12
        suffix_len = 1
    elif valstr.endswith('q'):
        exponent = 15
        suffix_len = 1
    elif valstr.endswith('Q'):
        exponent = 18
        suffix_len = 1
    elif valstr.endswith('s'):
        exponent = 21
        suffix_len = 1
    elif valstr.endswith('S'):
        exponent = 24
        suffix_len = 1
    elif valstr.endswith('o'):
        exponent = 27
        suffix_len = 1
    elif valstr.endswith('N'):
        exponent = 30
        suffix_len = 1
    # 'd' is at the end
    elif valstr.endswith('U'):
        exponent = 36
        suffix_len = 1
    elif valstr.endswith('D'):
        exponent = 39
        suffix_len = 1
    elif valstr.endswith('Td'):
        exponent = 42
        suffix_len = 2
    elif valstr.endswith('qd'):
        exponent = 45
        suffix_len = 2
    elif valstr.endswith('Qd'):
        exponent = 48
        suffix_len = 2
    elif valstr.endswith('sd'):
        exponent = 51
        suffix_len = 2
    elif valstr.endswith('Sd'):
        exponent = 54
        suffix_len = 2
    elif valstr.endswith('d'):
        exponent = 33
        suffix_len = 1
    else:
        raise ValueError('unknown value %s' % (valstr))
    mantissa = float(valstr[:-suffix_len])
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
    if oom3 == 7:
        suffix = 's'
    if oom3 == 8:
        suffix = 'S'
    if oom3 == 9:
        suffix = 'o'
    if oom3 == 10:
        suffix = 'N'
    if oom3 == 11:
        suffix = 'd'
    if oom3 == 12:
        suffix = 'U'
    if oom3 == 13:
        suffix = 'D'
    if oom3 == 14:
        suffix = 'Td'
    if oom3 == 15:
        suffix = 'qd'
    if oom3 == 16:
        suffix = 'Qd'
    if oom3 == 17:
        suffix = 'sd'
    if oom3 == 18:
        suffix = 'Sd'
    if suffix is None:
        raise ValueError('result too large: 1000**%d' % oom3)
    return'%.3f%s' % (mantissa, suffix)


class Farm(object):
    def __init__(self, eggs=None, max_capacity=None, farm_value=None,
                 farm_population=None, egg_laying_rate=None,
                 int_hatchery_rate=None):
        # From contract info screen
        self.eggs = parse_value(eggs)  # units: eggs
        
        # From hen housing screen
        self.max_capacity = parse_value(max_capacity)  # units: chickens
        self.habs = 4  # units: habs

        # From stats screen
        self.farm_value = parse_value(farm_value)  # units: dollars
        self.farm_population = parse_value(farm_population)  # units: chickens
        self.egg_laying_rate = parse_value(egg_laying_rate)  # units: eggs / minute
        self.int_hatchery_rate = parse_value(int_hatchery_rate)  # units: chickens / hab / minute
        
        # From epic research screen
        self.internal_hatchery_calm = 3  # units: dimensionless
        
        # Intermediate values
        self.chicken_hatching_rate = None
        if self.int_hatchery_rate is not None:
            self.chicken_hatching_rate = self.int_hatchery_rate * self.habs * self.internal_hatchery_calm
        self.egg_laying_rate_per_chicken = None
        if self.egg_laying_rate is not None and self.farm_population is not None:
            self.egg_laying_rate_per_chicken = self.egg_laying_rate / self.farm_population
        self.egg_laying_acceleration = None
        if self.chicken_hatching_rate is not None and self.egg_laying_rate_per_chicken is not None:
            self.egg_laying_acceleration = self.chicken_hatching_rate * self.egg_laying_rate_per_chicken
        self.value_scalar = None
        if self.farm_value is not None and self.max_capacity is not None and self.farm_population is not None and self.int_hatchery_rate is not None:
            self.value_scalar = self.farm_value / (self.max_capacity + 9 * self.farm_population + 12000 * self.int_hatchery_rate)

    def future(self, t):
        minutes = parse_time(t)
        kwargs = {}
        if self.eggs is not None and self.egg_laying_rate is not None and self.egg_laying_acceleration is not None:
            kwargs['eggs'] = self.eggs + self.egg_laying_rate * minutes + 0.5 * self.egg_laying_acceleration * minutes * minutes
        if self.max_capacity is not None:
            kwargs['max_capacity'] = self.max_capacity
        if self.farm_population is not None and self.chicken_hatching_rate is not None:
            kwargs['farm_population'] = self.farm_population + self.chicken_hatching_rate * minutes
        if self.farm_population is not None and self.chicken_hatching_rate is not None:
            kwargs['int_hatchery_rate'] = self.int_hatchery_rate
        if 'farm_population' in kwargs and self.egg_laying_rate_per_chicken is not None:
            kwargs['egg_laying_rate'] = kwargs['farm_population'] * self.egg_laying_rate_per_chicken
        if 'max_capacity' in kwargs and 'farm_population' in kwargs and 'int_hatchery_rate' in kwargs:
            kwargs['farm_value'] = self.value_scalar * (kwargs['max_capacity'] + 9 * kwargs['farm_population'] + 12000 * kwargs['int_hatchery_rate'])
        return Farm(**kwargs)

    def report(self):
        if self.eggs is not None:
            print('eggs:', format_value(self.eggs))
        if self.farm_population is not None:
            print('farm population:', format_value(self.farm_population))
            if self.max_capacity and self.farm_population > self.max_capacity:
                print('WARNING: farm population limited to %s by hab capacity' % format_value(self.max_capacity))
        if self.egg_laying_rate is not None:
            print('egg laying rate:', format_value(self.egg_laying_rate))
        if self.farm_value is not None:
            print('farm value:', format_value(self.farm_value))


### Values at completion time
print('Stats at completion time')
myfarm = Farm(eggs=eggs, max_capacity=hab_max_capacity, farm_value=farm_value, farm_population=farm_population, egg_laying_rate=egg_laying_rate, int_hatchery_rate=int_hatchery_rate)
new_farm = myfarm.future(time_to_complete)
new_farm.report()
print()


### Values at egg target
# solve for t
# e_final = e_current + e_velocity * t + 0.5 * e_acceleration * t * t
# 0.5 * e_acceleration * t * t + e_velocity * t + e_current - e_final = 0
print('Stats at egg target')

# units: eggs
e_final = parse_value(target_eggs)
e_current = myfarm.eggs
e_velocity = myfarm.egg_laying_rate
e_acceleration = myfarm.egg_laying_acceleration

# quadratic equation
a = 0.5 * e_acceleration
b = e_velocity
c = e_current - e_final
d = b**2 - 4*a*c

# units: minutes
t = (-b + math.sqrt(d)) / (2 * a)
print('target reached in', format_time(t))

new_farm2 = myfarm.future(t)
new_farm2.report()
print()


### Values at chicken target
# solve for t
# c_final = c_current + c_velocity * t
print('Stats at chicken target')

# units: chickens
c_final = parse_value(target_chickens)
c_current = myfarm.farm_population
c_velocity = myfarm.chicken_hatching_rate

# units: minutes
t = (c_final - c_current) / c_velocity
print('target reached in', format_time(t))

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
v_final = parse_value(target_farm_value)

# units: chickens
c_final = (v_final / myfarm.value_scalar - (myfarm.max_capacity + 12000 * myfarm.int_hatchery_rate))/9

# units: minutes
t = (c_final - c_current) / c_velocity
print('target reached in', format_time(t))
new_farm4 = myfarm.future(t)
new_farm4.report()

if c_final > hab_max_capacity:
    # units: dollars
    v_best = (10 * myfarm.max_capacity + 12000 * myfarm.int_hatchery_rate) * myfarm.value_scalar
    print('         best possible farm value:', format_value(v_best))
    
