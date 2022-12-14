# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/01_compound.gas.ipynb.

# %% auto 0
__all__ = ['IdealGasConstant', 'IsIdealGas', 'BoyleLaw', 'CharlesLaw', 'AvogadroLaw', 'IdealGasLaw', 'State', 'Gas']

# %% ../../nbs/01_compound.gas.ipynb 2
import sympy as smp
from fastcore.test import *

from ..core import *
from .core import *

# %% ../../nbs/01_compound.gas.ipynb 6
class IdealGasConstant(PropertyObservable):
    def __init__(self, compound):
        self.abbreviate = 'R'
        super().__init__(compound)

# %% ../../nbs/01_compound.gas.ipynb 7
class IsIdealGas(PropertyObservable):
    def __init__(self, compound):
        self.abbreviate = 'is_ideal_gas'
        self.unit = None
        super().__init__(compound)
    
    def __bool__(self):
        return False

# %% ../../nbs/01_compound.gas.ipynb 11
class BoyleLaw(Law):
    def __init__(self, compound: Compound):
        super().__init__()
        self.compound = compound
        #self.properties = [Pressure, Volume]
        self.properties = [
            {"object": Pressure},
            {"object": Volume}
        ]

# %% ../../nbs/01_compound.gas.ipynb 12
class CharlesLaw(Law):
    def __init__(self, compound: Compound) -> None:
        super().__init__()
        self.compound = compound
        #self.properties = [Volume, Temperature]
        self.properties = [
            {"object": Volume},
            {"object": Temperature}
        ]

# %% ../../nbs/01_compound.gas.ipynb 13
class AvogadroLaw(Law):
    def __init__(self, compound: Compound) -> None:
        super().__init__()
        self.compound = compound
        #self.properties = [Volume, Mole]
        self.properties = [
            {"object": Volume},
            {"object": Mole}
        ]

# %% ../../nbs/01_compound.gas.ipynb 16
class IdealGasLaw(Law):
    def __init__(self, compound: Compound) -> None:
        #super().__init__()
        self.compound = compound
        #self.properties = [Pressure, Volume, Mole, Temperature, IsIdealGas]
        self.properties = [
            {"object": Pressure, "unit": "atm"},
            {"object": Volume},
            {"object": Mole},
            {"object": Temperature},
            {"object": IdealGasConstant},
            {"object": IsIdealGas}
        ]
    
    @property
    def expression(self):
        p = self.compound.properties
        left_side = p['pressure'].symbol * p['volume'].symbol
        right_side = p['mole'].symbol * p['ideal_gas_constant'].symbol * p['temperature'].symbol
        return smp.Eq(left_side, right_side)

# %% ../../nbs/01_compound.gas.ipynb 20
from abc import ABC, abstractmethod

# %% ../../nbs/01_compound.gas.ipynb 21
class State(ABC):
    def __init__(self, context):
        self.context = context
    
    @abstractmethod
    def __bool__(self, timestep):
        pass

# %% ../../nbs/01_compound.gas.ipynb 24
class Gas(Compound):
    def __init__(self, formula):
        super().__init__(formula)
        
        self._config_laws([BoyleLaw, CharlesLaw, AvogadroLaw, IdealGasLaw])
