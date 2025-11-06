import pkgutil
if not hasattr(pkgutil, "ImpImporter"):
    import zipimport
    pkgutil.ImpImporter = zipimport.zipimporter
from opfunu.cec_based import cec2014

def F62014_fun(ndim=10):
    """
  Returns a callable wrapper for the CEC2014 F6 test function (Shifted and Rotated Weierstrass Function).
    """
    f = cec2014.F62014

    if callable(f):
        try:
            func = f(ndim=ndim)
        except TypeError:
            func = f()
    else:
        func = f

    class CallableWrapper:
        def __init__(self, base_func):
            self._f = base_func
            self.lb = getattr(base_func, "lb", None)
            self.ub = getattr(base_func, "ub", None)
            self.ndim = getattr(base_func, "ndim", ndim)
            self.name = getattr(base_func, "name", "F62014")

        def evaluate(self, x):
            return self._f.evaluate(x)

        def __call__(self, x):
            return self.evaluate(x)

    return CallableWrapper(func)

