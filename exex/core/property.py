# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/00c_core.property.ipynb.

# %% auto 0
__all__ = ['Object', 'PropertyData', 'BaseProperty', 'Property', 'ConstantProperty', 'PropertyObservable', 'Mass', 'MolarMass',
           'Mole', 'Pressure', 'Volume', 'Temperature']

# %% ../../nbs/00c_core.property.ipynb 4
from dataclasses import dataclass
from abc import ABC, abstractmethod

from ..imports import *
from .event import *
from .unit import *
from ..utils import camel_to_snake

# %% ../../nbs/00c_core.property.ipynb 6
class Object:
    pass

# %% ../../nbs/00c_core.property.ipynb 7
class PropertyData(dict):
    pass

# %% ../../nbs/00c_core.property.ipynb 12
@docs
class BaseProperty:
    def __init__(self, cmp):  # chemical substance
        self.is_constant: bool = False
        self.compound = cmp
        self.cmp = cmp
        self._data = PropertyData()

        self._connections = []
        self.laws = dict()
        self.func_changed = Event()

    @property
    def name(self) -> str:
        return camel_to_snake(self.__class__.__name__)

    @classmethod
    @property
    def snake_name(cls) -> str:  # return the snake style name
        return camel_to_snake(cls.__name__)

    def expr(self, t: int):  # time
        return self.symbol(t)

    def __call__(self, t: int, eval: bool = False, **kwargs):  # time
        self.t = t
        self.kwargs = {**kwargs, "eval": eval}

        expr = self.expr(t)

        if eval == True:
            return self.eval(expr, t)
        else:
            return expr

    def add_law(self, law):
        if not law in self.laws:
            self.laws[camel_to_snake(law.__class__.__name__)] = law

    _docs = dict(cls_doc="Property", add_law="", expr="Symbolic expression")

# %% ../../nbs/00c_core.property.ipynb 13
@patch
def symbol(self: BaseProperty, t):  # symbolic expression of the property
    """Rewrite this method if you want to modify"""
    return smp.symbols(f"{self.abbrv}_{self.cmp.snake_name}-{t}", real=True)

# %% ../../nbs/00c_core.property.ipynb 14
@patch
def set_val(self: BaseProperty, val: str, t: int):
    self._data[t] = {"val": val}

# %% ../../nbs/00c_core.property.ipynb 15
@patch
def get_val(self: BaseProperty, t: int):  # time
    if self.is_constant is True:
        return self.compute()
    else:
        return self._data[t]["val"] if t in self._data else self.symbol(t)

# %% ../../nbs/00c_core.property.ipynb 16
@patch
def eval(self: BaseProperty, expr, t: int):  # express  # time
    return expr.xreplace({expr: self.get_val(t=t)})

# %% ../../nbs/00c_core.property.ipynb 17
@patch
def is_empty(self: BaseProperty, t):
    return type(self.get_val(t))
    # return True if isinstance(type(self.get_val(t)), sympy.core.symbol.Symbol) else False

# %% ../../nbs/00c_core.property.ipynb 18
@docs
class Property(BaseProperty):
    _docs = dict(cls_doc="Property that varies in time")

# %% ../../nbs/00c_core.property.ipynb 20
@docs
class ConstantProperty(BaseProperty):
    @abstractmethod
    def compute(self):
        pass

    _docs = dict(
        cls_doc="Property that invariant in time", compute="Calculate the value"
    )

# %% ../../nbs/00c_core.property.ipynb 22
class Property(BaseProperty):
    pass

# %% ../../nbs/00c_core.property.ipynb 23
class PropertyObservable(Property):
    pass

# %% ../../nbs/00c_core.property.ipynb 26
class Mass(Property):
    def __init__(self, compound):
        super().__init__(compound)
        self.abbrv = "m"
        self.unit = Unit.MASS

# %% ../../nbs/00c_core.property.ipynb 27
class MolarMass(ConstantProperty):
    def __init__(self, compound):
        self.abbrv = "M"
        self.unit = Unit.MOLAR_MASS
        super().__init__(compound)
        self.is_constant = True

    def compute(self):
        mass = 0
        for element in self.compound.elements:
            mass += element.AtomicMass

        return mass * self.unit

# %% ../../nbs/00c_core.property.ipynb 28
class Mole(Property):
    def __init__(self, compound):
        super().__init__(compound)
        self.abbrv = "n"
        self.unit = Unit.MOLE

# %% ../../nbs/00c_core.property.ipynb 29
class Pressure(Property):
    def __init__(self, compound):
        super().__init__(compound)
        self.abbrv = "P"
        self.unit = Unit.PRESSURE

# %% ../../nbs/00c_core.property.ipynb 30
class Volume(Property):
    def __init__(self, compound):
        super().__init__(compound)
        self.abbrv = "V"
        self.unit = Unit.VOLUME

# %% ../../nbs/00c_core.property.ipynb 31
class Temperature(Property):
    def __init__(self, compound):
        super().__init__(compound)
        self.abbrv = "T"
        self.unit = Unit.TEMPERATURE
