# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/01_compound.law.ipynb.

# %% auto 0
__all__ = ['MassMoleRatio']

# %% ../../nbs/01_compound.law.ipynb 4
from ..imports import *
from ..core.law import Law
from .property import Mass, Mole, MolarMass

# %% ../../nbs/01_compound.law.ipynb 6
class MassMoleRatio(Law):
    def __init__(self, compound):
        super().__init__()
        self.compound = compound
        # self.properties = [Mass, Mole, MolarMass]
        self.properties = [{"object": Mass}, {"object": Mole}, {"object": MolarMass}]

    def expr(self, t, **kwargs):
        cmp = self.compound
        params = {"t": t, **kwargs}
        lhs = cmp.get_prop("molar_mass", **params) * cmp.get_prop("mole", **params)
        rhs = cmp.get_prop("mass", **params)
        return smp.Eq(lhs, rhs)
