# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_core.ipynb.

# %% auto 0
__all__ = ['ureg', 'Q', 'Event', 'Unit', 'unit2expr', 'Object', 'PropertyData', 'BaseProperty', 'Property', 'ConstantProperty',
           'PropertyObservable', 'Mass', 'MolarMass', 'Mole', 'Pressure', 'Volume', 'Temperature', 'BaseLaw', 'Law']

# %% ../nbs/00_core.ipynb 4
from dataclasses import dataclass
from abc import ABC, abstractmethod

from .imports import *
from .utils import *

# %% ../nbs/00_core.ipynb 5
class Event(list):
    def __call__(self, *args, **kwargs):
        for item in self:
            item(*args, **kwargs)

# %% ../nbs/00_core.ipynb 9
class Unit:
    """
    Default SI Units
    """

    LENGTH = u.meter
    MASS = u.kilogram
    TIME = u.second
    TEMPERATURE = u.kelvin

    """
    Derived from SI Units
    """
    MOLAR_MASS = u.gram / u.mole
    MOLE = u.mole
    SPECIFIC_HEAT = u.joule / (u.kilogram * u.kelvin)
    PRESSURE = u.pascal
    VOLUME = u.liter

# %% ../nbs/00_core.ipynb 10
def unit2expr(unit):
    pass

# %% ../nbs/00_core.ipynb 14
ureg = pint.UnitRegistry(system="SI")
Q = ureg.Quantity  # quantity

# %% ../nbs/00_core.ipynb 36
class Object:
    pass

# %% ../nbs/00_core.ipynb 37
class PropertyData(dict):
    pass

# %% ../nbs/00_core.ipynb 42
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

# %% ../nbs/00_core.ipynb 43
@patch
def symbol(self: BaseProperty, t):  # symbolic expression of the property
    """Rewrite this method if you want to modify"""
    return smp.symbols(f"{self.abbrv}_{self.cmp.snake_name}-{t}", real=True)

# %% ../nbs/00_core.ipynb 44
@patch
def set_val(self: BaseProperty, val: str, t: int):
    self._data[t] = {"val": val}

# %% ../nbs/00_core.ipynb 45
@patch
def get_val(self: BaseProperty, t: int):  # time
    if self.is_constant is True:
        return self.compute()
    else:
        return self._data[t]["val"] if t in self._data else self.symbol(t)

# %% ../nbs/00_core.ipynb 46
@patch
def eval(self: BaseProperty, expr, t: int):  # express  # time
    return expr.xreplace({expr: self.get_val(t=t)})

# %% ../nbs/00_core.ipynb 47
@patch
def is_empty(self: BaseProperty, t):
    return type(self.get_val(t))
    # return True if isinstance(type(self.get_val(t)), sympy.core.symbol.Symbol) else False

# %% ../nbs/00_core.ipynb 48
@docs
class Property(BaseProperty):
    _docs = dict(cls_doc="Property that varies in time")

# %% ../nbs/00_core.ipynb 50
@docs
class ConstantProperty(BaseProperty):
    @abstractmethod
    def compute(self):
        pass

    _docs = dict(
        cls_doc="Property that invariant in time", compute="Calculate the value"
    )

# %% ../nbs/00_core.ipynb 52
class Property(BaseProperty):
    pass

# %% ../nbs/00_core.ipynb 53
class PropertyObservable(Property):
    pass

# %% ../nbs/00_core.ipynb 56
class Mass(Property):
    def __init__(self, compound):
        super().__init__(compound)
        self.abbrv = "m"
        self.unit = Unit.MASS

# %% ../nbs/00_core.ipynb 57
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

# %% ../nbs/00_core.ipynb 58
class Mole(Property):
    def __init__(self, compound):
        super().__init__(compound)
        self.abbrv = "n"
        self.unit = Unit.MOLE

# %% ../nbs/00_core.ipynb 59
class Pressure(Property):
    def __init__(self, compound):
        super().__init__(compound)
        self.abbrv = "P"
        self.unit = Unit.PRESSURE

# %% ../nbs/00_core.ipynb 60
class Volume(Property):
    def __init__(self, compound):
        super().__init__(compound)
        self.abbrv = "V"
        self.unit = Unit.VOLUME

# %% ../nbs/00_core.ipynb 61
class Temperature(Property):
    def __init__(self, compound):
        super().__init__(compound)
        self.abbrv = "T"
        self.unit = Unit.TEMPERATURE

# %% ../nbs/00_core.ipynb 63
class BaseLaw(ABC):
    @property
    def name(self) -> str:
        return camel_to_snake(self.__class__.__name__)

    @classmethod
    @property
    def snake_name(cls) -> str:  # return the snake style name
        return camel_to_snake(cls.__name__)

    def n_known_variables(self, timestep: int) -> int:  # the number of known variables
        n_knowns = 0
        for p in self.properties:
            name = camel_to_snake(p["object"].__name__)
            if timestep in self.compound.properties[name]._data:
                n_knowns += 1
        return n_knowns

    def is_solveable(self, timestep: int) -> bool:  # the timestep
        n_unknowns = len(self.properties)
        n_knowns = self.n_known_variables(timestep)
        print(f"n_unknowns={n_unknowns} and n_knowns={n_knowns}")
        return n_unknowns - n_knowns <= 1

    def _run_config(self) -> None:  # run all configuration
        self._config_properties()

    def _config_properties(self) -> None:  # add law's properties to compound

        for p in self.properties:
            # name = camel_to_snake(p['object'].__name__)
            name = p["object"].snake_name

            if not name in self.compound.properties:
                self.compound.properties[name] = p["object"](compound=self.compound)

            self.compound.properties[name].add_law(self)

    def solve(
        self,
        timestep: int,  # the time step of the unknown variable
        unknown: str,  # the unknown variable that you want to solve
    ):
        unknown_symbol = self.compound.properties[unknown].symbol
        return smp.solve(self.expression, unknown_symbol)

    def __call__(self, *args, **kwargs):
        return self.expr(*args, **kwargs)

    @abstractmethod
    def expr(self):
        """The symbolic expression of the law"""
        pass

    def __repr__(self):
        return f"Law({self.name})"

# %% ../nbs/00_core.ipynb 64
class Law(BaseLaw):
    pass
