# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/08_callback.core.ipynb.

# %% auto 0
__all__ = ['Callback', 'ConservationCallback']

# %% ../../nbs/08_callback.core.ipynb 4
from ..imports import *

# %% ../../nbs/08_callback.core.ipynb 5
_events = L.split('before_create_unv after_create_unv \
                  before_create_env after_create_env \
                  before_create_cmp after_create_cmp \
                  before_get_prop after_get_prop before_change_prop after_change_prop \
                  before_get_law after_get_law before_change_law after_change_law')

# %% ../../nbs/08_callback.core.ipynb 7
mk_class('event', **_events.map_dict(),
         doc="All possible events as attributes to get tab-completion and typo-proofing")

# %% ../../nbs/08_callback.core.ipynb 10
@docs
@funcs_kwargs(as_method=True)
class Callback(Stateful, GetAttr):
    _methods = _events
    _docs = dict(cls_doc='basic class handling tweaks when interact wih properties, laws, compounds, reactants, environment and the universe')

# %% ../../nbs/08_callback.core.ipynb 11
class ConservationCallback(Callback):
    pass