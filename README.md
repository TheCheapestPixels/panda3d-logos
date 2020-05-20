panda3d-logos
=============

The Panda3D logo in various formats, a 3d animated splash screen and code to show it off.


Wait, code?
-----------

Yup. You're already using Panda3D, after all, right? Here's the
pertinent bits of `examples/panda3d_logo.py`

```python
from panda3d_logos.splashes import RainbowSplash

splash = RainbowSplash()
interval = splash.setup()  # This'll change the scene graph, in
                           # particular reparent the cam!
# interval is a Panda3D interval you can .start() it now
splash.teardown()          # To de-litter your state.
```
