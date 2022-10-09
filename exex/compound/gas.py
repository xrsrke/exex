# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/01_compound.gas.ipynb.

# %% auto 0
__all__ = ['IsIdealGas', 'BoyleLaw', 'CharlesLaw', 'AvogadroLaw', 'IdealGasLaw', 'State', 'Gas']

# %% ../../nbs/01_compound.gas.ipynb 2
import sympy as smp
from fastcore.test import *

from ..core import *
from .core import *

# %% ../../nbs/01_compound.gas.ipynb 6
class IsIdealGas(PropertyObservable):
    def __init__(self, compound):
        self.abbreviate = 'is_ideal_gas'
        self.unit = None
        super().__init__(compound)
    
    def __bool__(self):
        return False

# %% ../../nbs/01_compound.gas.ipynb 10
class BoyleLaw(Law):
    def __init__(self, compound: Compound):
        super().__init__()
        self.compound = compound
        self.properties = [Pressure, Volume]
        self.x_properties = [
            {"object": Pressure},
            {"object": Volume}
        ]

# %% ../../nbs/01_compound.gas.ipynb 11
class CharlesLaw(Law):
    def __init__(self, compound: Compound) -> None:
        super().__init__()
        self.compound = compound
        self.properties = [Volume, Temperature]
        self.x_properties = [
            {"object": Volume},
            {"object": Temperature}
        ]

# %% ../../nbs/01_compound.gas.ipynb 12
class AvogadroLaw(Law):
    def __init__(self, compound: Compound) -> None:
        super().__init__()
        self.compound = compound
        self.properties = [Volume, Mole]
        self.x_properties = [
            {"object": Volume},
            {"object": Mole}
        ]

# %% ../../nbs/01_compound.gas.ipynb 15
class IdealGasLaw(Law):
    def __init__(self, compound: Compound) -> None:
        #super().__init__()
        self.compound = compound
        self.properties = [Pressure, Volume, Mole, Temperature, IsIdealGas]
        self.x_properties = [
            {"object": Pressure, "unit": "atm"},
            {"object": Volume},
            {"object": Mole},
            {"object": Temperature},
            {"object": IsIdealGas}
        ]
    
    @property
    def expression(self):
        compound = self.compound
        left_side = compound.properties['pressure'].symbol * compound.properties['volume'].symbol
        right_side = compound.properties['mole'].symbol * compound.properties['temperature'].symbol
        return smp.Eq(left_side, right_side)
    
    def solve(self, time, unknown):
        pass

# %% ../../nbs/01_compound.gas.ipynb 19
from abc import ABC, abstractmethod

# %% ../../nbs/01_compound.gas.ipynb 20
class State(ABC):
    def __init__(self, context):
        self.context = context
    
    @abstractmethod
    def __bool__(self, timestep):
        pass

# %% ../../nbs/01_compound.gas.ipynb 23
class Gas(Compound):
    def __init__(self, formula):
        super().__init__(formula)
        
        self._config_laws([BoyleLaw, CharlesLaw, AvogadroLaw, IdealGasLaw])
