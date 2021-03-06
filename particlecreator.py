# Author: Shao Zhang, Phil Saltzman
# Last Updated: 4/19/2005
#
# This file contians the minimum code needed to load the particle panel tool
# See readme.txt for more information

from direct.tkpanels.ParticlePanel import ParticlePanel
import sys
try:
    import _tkinter
except Exception:
    sys.exit("Please install python module 'Tkinter'")
try:
    import Pmw
except Exception:
    sys.exit("Please install Python megawidgets")


# Makes sure that Panda is set to open external windows
base.startTk()


pp = ParticlePanel()             # Create the panel
base.disableMouse()              # Disable camera control to place it
camera.setY(-10)                 # Place the camera
base.setBackgroundColor(0, 0, 0)  # Most particle systems show up better on black backgrounds
run()
