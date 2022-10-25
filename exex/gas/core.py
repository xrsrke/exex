# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/07_gas.core.ipynb.

# %% auto 0
__all__ = ['IdealGasConstant', 'IsIdealGas', 'BoyleLaw', 'CharlesLaw', 'AvogadroLaw', 'IdealGasLaw', 'State', 'Gas']

# %% ../../nbs/07_gas.core.ipynb 4
from ..basics import *

# %% ../../nbs/07_gas.core.ipynb 6
class IdealGasConstant(PropertyObservable):
    def __init__(self, compound):
        self.abbreviate = 'R'
        super().__init__(compound)

# %% ../../nbs/07_gas.core.ipynb 7
class IsIdealGas(PropertyObservable):
    def __init__(self, compound):
        self.abbreviate = 'is_ideal_gas'
        self.unit = None
        super().__init__(compound)
    
    def __bool__(self):
        return False

# %% ../../nbs/07_gas.core.ipynb 11
class BoyleLaw(Law):
    def __init__(self, compound: Compound):
        super().__init__()
        self.compound = compound
        #self.properties = [Pressure, Volume]
        self.properties = [
            {"object": Pressure},
            {"object": Volume}
        ]
    
    def expr(self): pass

# %% ../../nbs/07_gas.core.ipynb 12
class CharlesLaw(Law):
    def __init__(self, compound: Compound) -> None:
        super().__init__()
        self.compound = compound
        #self.properties = [Volume, Temperature]
        self.properties = [
            {"object": Volume},
            {"object": Temperature}
        ]
    
    def expr(self): pass

# %% ../../nbs/07_gas.core.ipynb 13
class AvogadroLaw(Law):
    def __init__(self, compound: Compound) -> None:
        super().__init__()
        self.compound = compound
        #self.properties = [Volume, Mole]
        self.properties = [
            {"object": Volume},
            {"object": Mole}
        ]
    
    def expr(self): pass

# %% ../../nbs/07_gas.core.ipynb 16
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
    
    def expr(self, t, **kwargs):
        
        cmp = self.compound
        params = {'t': t}
        
        left_side = cmp.get_prop('pressure', *params) * cmp.get_prop('volume', *params)
        right_side = cmp.get_prop('mole', *params) * cmp.get_prop('ideal_gas_constant', *params) * cmp.get_prop('temperature', *params)
        
        return smp.Eq(left_side, right_side)

# %% ../../nbs/07_gas.core.ipynb 20
from abc import ABC, abstractmethod

# %% ../../nbs/07_gas.core.ipynb 21
class State(ABC):
    def __init__(self, context):
        self.context = context
    
    @abstractmethod
    def __bool__(self, timestep):
        pass

# %% ../../nbs/07_gas.core.ipynb 24
class Gas(Compound):
    def __init__(
        self,
        formula: str # the chemical formula
    ) -> None:
        super().__init__(formula)
        
        #self._laws = [BoyleLaw, CharlesLaw, AvogadroLaw, IdealGasLaw]
        #self._config_laws()

        self.add_laws = [BoyleLaw, CharlesLaw, AvogadroLaw, IdealGasLaw, MassMoleRatio]
