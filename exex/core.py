# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_core.ipynb.

# %% auto 0
__all__ = ['ureg', 'Q', 'Event', 'Unit', 'Object', 'PropertyData', 'PropertyObservable', 'Mass', 'Mole', 'Pressure', 'Volume',
           'Temperature', 'Law', 'System']

# %% ../nbs/00_core.ipynb 4
from dataclasses import dataclass

from .imports import *
from .utils import *

# %% ../nbs/00_core.ipynb 5
class Event(list):
    def __call__(self, *args, **kwargs):
        for item in self:
            item(*args, **kwargs)

# %% ../nbs/00_core.ipynb 7
@dataclass
class Unit:
    """
    Default Units
    """
    
    # SI Unit
    LENGTH = 'meter'
    MASS = 'kilogram'
    TIME = 'second'
    TEMPERATURE = 'kelvin'
    
    # Derived from SI Unit
    MOLE = 'mole'
    SPECIFIC_HEAT = 'joule / (kilogram kelvin)'
    PRESSURE = 'pascal'
    VOLUME = 'liter'

# %% ../nbs/00_core.ipynb 9
ureg = pint.UnitRegistry(system='SI')
Q = ureg.Quantity # quantity

# %% ../nbs/00_core.ipynb 17
class Object:
    pass

# %% ../nbs/00_core.ipynb 18
class PropertyData(dict):
    pass

# %% ../nbs/00_core.ipynb 23
class PropertyObservable:
    def __init__(self, compound):
        self._data = PropertyData()
        self.compound = compound
        self._connections = []
        self.laws = dict()
        self.func_changed = Event()
        
        # print(f'self.compound={self.compound}')
        # print(self.compound.__dict__)
        # print(f'formula={self.compound.formula}')
        
        self.symbol = smp.symbols(f'{self.abbreviate}', real=True)
    
    @property
    def name(self) -> str:
        return camel_to_snake(self.__class__.__name__)
    
    @classmethod
    @property
    def snake_name(cls) -> str: # return the snake style name
        return camel_to_snake(cls.__name__)
    
    def add_data(self, time, value):
        self._data[time] = {'value': value}
    
    def get_value(
        self,
        time: int # time
    ):
        if not time in self._data:
            return f"Don't have data for time={time}"
        return self._data[time]['value']
    
    def add_law(self, law):
        if not law in self.laws:
            self.laws[camel_to_snake(law.__class__.__name__)] = law

# %% ../nbs/00_core.ipynb 24
class Mass(PropertyObservable):
    def __init__(self, compound):
        self.abbreviate = 'm'
        self.unit = Unit.MASS
        super().__init__(compound)

# %% ../nbs/00_core.ipynb 25
class Mole(PropertyObservable):
    def __init__(self, compound):
        self.abbreviate = 'n'
        self.unit = Unit.MOLE
        super().__init__(compound)

# %% ../nbs/00_core.ipynb 26
class Pressure(PropertyObservable):
    def __init__(self, compound):
        self.abbreviate = 'P'
        self.unit = Unit.PRESSURE
        super().__init__(compound)

# %% ../nbs/00_core.ipynb 27
class Volume(PropertyObservable):
    def __init__(self, compound):
        self.abbreviate = 'V'
        self.unit = Unit.VOLUME
        super().__init__(compound)

# %% ../nbs/00_core.ipynb 28
class Temperature(PropertyObservable):
    def __init__(self, compound):
        self.abbreviate = 'T'
        self.unit = Unit.TEMPERATURE
        super().__init__(compound)

# %% ../nbs/00_core.ipynb 30
class Law:
    @property
    def name(self) -> str:
        return camel_to_snake(self.__class__.__name__)
    
    @classmethod
    @property
    def snake_name(cls) -> str: # return the snake style name
        return camel_to_snake(cls.__name__)
    
    def n_known_variables(
        self,
        timestep: int
    ) -> int: # the number of known variables
        n_knowns = 0
        for p in self.properties:
            name = camel_to_snake(p['object'].__name__)
            if timestep in self.compound.properties[name]._data:
                n_knowns += 1
        return n_knowns

    def is_solveable(
        self,
        timestep: int # the timestep
    ) -> bool:
        n_unknowns = len(self.properties)
        n_knowns = self.n_known_variables(timestep)
        print(f'n_unknowns={n_unknowns} and n_knowns={n_knowns}')
        return n_unknowns - n_knowns <= 1

    def _run_config(self) -> None: # run all configuration
        self._config_properties()
    
    def _config_properties(self) -> None: # add law's properties to compound
        
        for p in self.properties:
            # name = camel_to_snake(p['object'].__name__)
            name = p['object'].snake_name
            
            if not name in self.compound.properties:
                self.compound.properties[name] = p['object'](compound=self.compound)
            
            self.compound.properties[name].add_law(self)
    
    def solve(
        self,
        timestep: int, # the time step of the unknown variable
        unknown: str # the unknown variable that you want to solve
    ):
        unknown_symbol = self.compound.properties[unknown].symbol
        return smp.solve(self.expression, unknown_symbol)

# %% ../nbs/00_core.ipynb 34
class System:
    def __init__(self):
        self.reactions = dict()
        self.universe = None
        self.subscribers: dict[str, Callable] = dict()
        self.current_time: int = None
        self.highest_time: int = None
