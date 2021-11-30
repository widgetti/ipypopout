from ipywidgets import Widget
from ipypopout.sync_patch_mixin import SyncPatchMixin

Widget.__bases__ = (SyncPatchMixin, *Widget.__bases__)
