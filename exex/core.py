# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_core.ipynb.

# %% auto 0
__all__ = ['Event', 'Unit', 'Object', 'PropertyData', 'PropertyObservable', 'Mass', 'Mole', 'Pressure', 'Volume', 'Temperature',
           'Law', 'System']

# %% ../nbs/00_core.ipynb 4
from dataclasses import dataclass

import sympy as smp
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
class Object:
    pass

# %% ../nbs/00_core.ipynb 10
class PropertyData(dict):
    pass

# %% ../nbs/00_core.ipynb 18
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
    
    def add_data(self, time, value):
        self._data[time] = {'value': value}
    
    def add_law(self, law):
        if not law in self.laws:
            self.laws[camel_to_snake(law.__class__.__name__)] = law

# %% ../nbs/00_core.ipynb 19
class Mass(PropertyObservable):
    def __init__(self, compound):
        self.abbreviate = 'm'
        self.unit = Unit.MASS
        super().__init__(compound)

# %% ../nbs/00_core.ipynb 20
class Mole(PropertyObservable):
    def __init__(self, compound):
        self.abbreviate = 'n'
        self.unit = Unit.MOLE
        super().__init__(compound)

# %% ../nbs/00_core.ipynb 21
class Pressure(PropertyObservable):
    def __init__(self, compound):
        self.abbreviate = 'P'
        self.unit = Unit.PRESSURE
        super().__init__(compound)

# %% ../nbs/00_core.ipynb 22
class Volume(PropertyObservable):
    def __init__(self, compound):
        self.abbreviate = 'V'
        self.unit = Unit.VOLUME
        super().__init__(compound)

# %% ../nbs/00_core.ipynb 23
class Temperature(PropertyObservable):
    def __init__(self, compound):
        self.abbreviate = 'T'
        self.unit = Unit.TEMPERATURE
        super().__init__(compound)

# %% ../nbs/00_core.ipynb 25
class Law:
    def _run_config(self):
        self._config_properties()
    
    def _config_properties(self):
#         for p in self.properties:
#             name = camel_to_snake(p.__name__)
            
#             if not name in self.compound.properties:
#                 self.compound.properties[name] = p(compound=self.compound)
            
#             self.compound.properties[name].add_law(self)
        
        for p in self.x_properties:
            name = camel_to_snake(p['object'].__name__)
            
            if not name in self.compound.properties:
                self.compound.properties[name] = p['object'](compound=self.compound)
            
            self.compound.properties[name].add_law(self)

# %% ../nbs/00_core.ipynb 27
class System:
    def __init__(self):
        self.reactions = dict()
