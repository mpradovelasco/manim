import numpy as np
from utils.simple_functions import sigmoid
from utils.bezier import bezier

def smooth(t, inflection = 10.0):
    error = sigmoid(-inflection / 2)
    return (sigmoid(inflection*(t - 0.5)) - error) / (1 - 2*error)

def rush_into(t):
    return 2*smooth(t/2.0)

def rush_from(t):
    return 2*smooth(t/2.0+0.5) - 1

def slow_into(t):
    return np.sqrt(1-(1-t)*(1-t))

def double_smooth(t):
    if t < 0.5:
        return 0.5*smooth(2*t)
    else:
        return 0.5*(1 + smooth(2*t - 1))

def there_and_back(t, inflection = 10.0):
    new_t = 2*t if t < 0.5 else 2*(1 - t)
    return smooth(new_t, inflection)

def there_and_back_with_pause(t):
    if t < 1./3:
        return smooth(3*t)
    elif t < 2./3:
        return 1
    else:
        return smooth(3 - 3*t)

def running_start(t, pull_factor = -0.5):
    return bezier([0, 0, pull_factor, pull_factor, 1, 1, 1])(t)

def not_quite_there(func = smooth, proportion = 0.7):
    def result(t):
        return proportion*func(t)
    return result

def wiggle(t, wiggles = 2):
    return there_and_back(t) * np.sin(wiggles*np.pi*t)

def squish_rate_func(func, a = 0.4, b = 0.6):
    def result(t):
        if a == b:
            return a

        if t < a:
            return func(0)
        elif t > b:
            return func(1)
        else:
            return func((t-a)/(b-a))
            
    return result

# Stylistically, should this take parameters (with default values)?
# Ultimately, the functionality is entirely subsumed by squish_rate_func,
# but it may be useful to have a nice name for with nice default params for 
# "lingering", different from squish_rate_func's default params
def lingering(t):
    return squish_rate_func(lambda t: t, 0, 0.8)(t)

