# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/01_compound.core.ipynb.

# %% auto 0
__all__ = ['Compound']

# %% ../../nbs/01_compound.core.ipynb 4
from dataclasses import dataclass
import chemlib

from ..imports import *
from ..core.all import *
from ..system import *
from ..utils import *
from .law import *

# %% ../../nbs/01_compound.core.ipynb 6
class Compound(Matter):

    LAWS = [MassMoleRatio]

    def __init__(self, formula: str) -> None:  # the chemical formula
        super().__init__()

        compound = chemlib.Compound(formula)
        # self._laws = [MassMoleRatio]
        self.add_laws = [MassMoleRatio]

        self.elements = compound.elements
        self.formula = compound.formula
        self._formula = formula
        self.coefficient = compound.coefficient
        self.occurences = compound.occurences

        self._setup_laws([MassMoleRatio])

    @property
    def snake_name(self) -> str:  # return the snake name style
        return self._formula

    def info(self, **kwargs):
        dta = {}

        for k, v in self.properties.items():
            # data_point = {}
            # print(v._data)
            key = k
            # if v.unit:
            #     key += f' ({v.unit})'

            dta[key] = v._data

        df = pd.DataFrame(data=dta, **kwargs)
        df.index.name = "Time"
        return df.sort_index()

    def get_data(self, time: int, name: str):  # the time  # the property name
        if not name in self.properties:
            return "The property don't exist"
        pass

    def __repr__(self):
        return f"Compound({self.formula})"
