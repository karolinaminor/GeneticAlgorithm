import math

def sample_function(x, y, z):
    """Sample 3-variable objective function: f(x, y, z) = sin(x) + cos(y) + exp(-z^2)"""
    return math.sin(x) + math.cos(y) + math.exp(-z ** 2)
