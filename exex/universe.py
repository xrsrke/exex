# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_universe.ipynb.

# %% auto 0
__all__ = ['Universe', 'OurUniverse', 'ConservationOfMass', 'ConservationOfEnergy', 'ConservationOfElectricCharge']

# %% ../nbs/00_universe.ipynb 4
from abc import ABC, abstractmethod

from .imports import *
from .core import *

# %% ../nbs/00_universe.ipynb 5
@docs
class Universe(ABC):
    def __init__(self):
        self._laws: list[Law] = L([])
    
    _docs = dict(cls_doc='An abstract base class for create a new universe')

# %% ../nbs/00_universe.ipynb 6
@docs
class OurUniverse(Universe):
    _docs = dict(cls_doc='The universe that has the law of physics from our universe (yeah you and me)')

# %% ../nbs/00_universe.ipynb 9
@docs
class ConservationOfMass:
    _docs = dict(cls_doc='The sum of all masses in the universe')

# %% ../nbs/00_universe.ipynb 10
@docs
class ConservationOfEnergy:
    _docs = dict(cls_doc='The sum of all energies in the universe')

# %% ../nbs/00_universe.ipynb 11
@docs
class ConservationOfElectricCharge:
    _docs = dict(cls_doc='The sum of all electric charges in the universe')
