# -*- coding: utf-8 -*-

# Soya 3D
# Copyright (C) 2001-2014 Jean-Baptiste LAMY
# http://www.lesfleursdunormal.fr/static/informatique/soya3d/index_en.html

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys, os, os.path, random
import soya3 as soya, soya3.gui

soya.path.append(os.path.join(os.path.dirname(sys.argv[0]), "data"))

soya.init(width = 640, height = 480)


red = soya.Material()
red.diffuse = (1.0, 0.0, 0.0, 1.0)

root  = soya.gui.RootLayer(None)
scene = soya.World()
light = soya.Light(scene)
light.set_xyz(0.5, 0.0, 2.0)
camera = soya.Camera(scene)
camera.z = 4.0
camera.partial = 1
body = soya.Body(scene, soya.Model.get("caterpillar_head"))
body.advance_time = lambda proportion: body.rotate_lateral(proportion)
soya.gui.CameraViewport(root, camera)

window = soya.gui.Window(root, "Soya GUI demo: window over camera", closable = 0)
table = soya.gui.VTable(window)
soya.gui.CancelButton(table, "Quit", on_clicked = sys.exit)

soya.set_root_widget(root)
soya.MainLoop(scene).main_loop()

