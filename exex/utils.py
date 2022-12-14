# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/0_utils.ipynb.

# %% auto 0
__all__ = ['camel_to_snake', 'snake_name']

# %% ../nbs/0_utils.ipynb 4
import re

from fastcore.test import test_eq

# %% ../nbs/0_utils.ipynb 6
def camel_to_snake(
    name: str # the string that you want to convert
    ) -> str: # converted string
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

# %% ../nbs/0_utils.ipynb 11
def snake_name(x) -> str: # return the snake name style
    "Get the snake style name of an instance"
    
    if type(x) == type: return camel_to_snake(x.__name__)
    return camel_to_snake(x.__class__.__name__)
