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


black = soya.Material()
black.diffuse = (0.0, 0.0, 0.0, 1.0)

red = soya.Material()
red.diffuse = (1.0, 0.0, 0.0, 1.0)

blue = soya.Material()
blue.diffuse = (0.0, 0.0, 1.0, 1.0)


def widget_demo():
  window = soya.gui.Window(root)
  table = soya.gui.VTable(window, 2)
  table.row_pad = 20
  soya.gui.Label(table, "Fullscreen")
  soya.gui.CheckBox(table, "bla bla", 1)
  soya.gui.Label(table, "Quality")
  soya.gui.HScrollBar(table, 0, 9, 1, 1, 1)
  soya.gui.CancelButton(table)
  soya.gui.ValidateButton(table)

def text_demo():
  window = soya.gui.Window(root)
  table = soya.gui.VTable(window)
  table.row_pad = 30
  soya.gui.Label(table, "Simple label")
  scroll_pane  = soya.gui.ScrollPane(table)
  soya.gui.Text(scroll_pane, """Multiline text with automatic breaklines, included inside a scroll pane.

All texts are Unicode, notice the support for accentuated characters: éêëè.

This text is deliberately long and boring, but it is mandatory in order to have a text long enought to get the scroll bar.

I apologize for the lack of interest of this text.

Sorry, Jiba""")
  soya.gui.Input(table, "A simple one-line text input")
  
def list_demo():
  window = soya.gui.Window(root, "List demo")
  table = soya.gui.VTable(window, 2)
  table.row_pad = table.col_pad = 20
  
  soya.gui.Label(table, "vertical list\nin a scroll pane")
  l = soya.gui.VList(soya.gui.ScrollPane(table))
  soya.gui.Label(l, "Baby").extra_width = 1.0
  soya.gui.Label(l, "Beginner")
  soya.gui.Label(l, "Very easy")
  soya.gui.Label(l, "Easy")
  soya.gui.Label(l, "Hard gamer")
  soya.gui.Label(l, "Nighmare")
  soya.gui.Label(l, "Impossible")
  soya.gui.Label(l, "God")
  soya.gui.Label(l, "Jiba :-)")
  
  soya.gui.Label(table, "vertical list\nwith 2 columns")
  l = soya.gui.VList(table, 2)
  soya.gui.ProgressBar(l, 0.2)
  soya.gui.Label(l, "Beginner")
  soya.gui.ProgressBar(l, 0.5)
  soya.gui.Label(l, "Hard gamer")
  soya.gui.ProgressBar(l, 0.8)
  soya.gui.Label(l, "Nighmare")
  
  soya.gui.Label(table, "horizontal list")
  l = soya.gui.HList(table)
  soya.gui.Label(l, "Beginner")
  soya.gui.Label(l, "Hard gamer")
  soya.gui.Label(l, "Nighmare")
  
def camera_demo(transparent = 0, fps = 0):
  window = soya.gui.Window(root, "Camera demo")
  layer = soya.gui.Layer(window)
  scene = soya.World()
  if transparent: scene.atmosphere = soya.NoBackgroundAtmosphere()
  light = soya.Light(scene)
  light.set_xyz(0.5, 0.0, 2.0)
  camera = soya.Camera(scene)
  camera.z = 2.0
  camera.partial = 1
  body = soya.Body(scene, soya.Model.get("sword"))
  body.advance_time = lambda proportion: body.rotate_lateral(proportion)
  soya.gui.CameraViewport(layer, camera)
  if fps: soya.gui.FPSLabel(layer)
  soya.MAIN_LOOP.scenes.append(scene)
  
def resize_demo():
  window = soya.gui.Window(root, "Resize demo")
  table = soya.gui.VTable(window)
  label = soya.gui.Label(table, "???")
  soya.gui.Input(table, "")
  def set_random_text():
    label.text = "".join([chr(random.randint(65, 90)) for i in range(random.randint(3, 30))])
  soya.gui.Button(table, "Random text", set_random_text)
  
def tree_demo():
  import soya3.gui.tree
  
  window = soya.gui.Window(root, "Tree demo")
  tree = soya.gui.tree.Tree(soya.gui.ScrollPane(window))
  soya_coders = soya.gui.tree.SimpleNode(tree, "Soya coders")
  lamy        = soya.gui.tree.SimpleNode(soya_coders, "Lamy brothers", soya.Material.get("little-dunk"))
  jiba        = soya.gui.tree.SimpleNode(lamy, "Jiba", soya.Material.get("little-dunk"))
  blam        = soya.gui.tree.SimpleNode(lamy, "Blam", soya.Material.get("little-dunk"))
  marmoute    = soya.gui.tree.SimpleNode(soya_coders, "Marmoute", soya.Material.get("little-dunk"))
  souvarine   = soya.gui.tree.SimpleNode(soya_coders, "Souvarine", soya.Material.get("little-dunk"))
  dunk        = soya.gui.tree.SimpleNode(soya_coders, "Dunk", soya.Material.get("little-dunk"))
  dunk        = soya.gui.tree.SimpleNode(soya_coders, "...", soya.Material.get("little-dunk"))
  
root  = soya.gui.RootLayer(None)
backg = soya.gui.Image(root, black)

window = soya.gui.Window(root, "Soya GUI demo", closable = 0)
table = soya.gui.VTable(window)
soya.gui.Button(table, "Widget demo", on_clicked = widget_demo)
soya.gui.Button(table, "Text demo", on_clicked = text_demo)
soya.gui.Button(table, "List demo", on_clicked = list_demo)
soya.gui.Button(table, "Camera demo", on_clicked = lambda: camera_demo(0, 0))
soya.gui.Button(table, "Transparent camera demo", on_clicked = lambda: camera_demo(1, 0))
soya.gui.Button(table, "FPS camera demo", on_clicked = lambda: camera_demo(0, 1))
soya.gui.Button(table, "Resize demo", on_clicked = resize_demo)
soya.gui.Button(table, "Tree demo", on_clicked = tree_demo)
soya.gui.CancelButton(table, "Quit", on_clicked = sys.exit)

#soya.gui.Button(root, "Tree demo", on_clicked = tree_demo).calc_size()

soya.set_root_widget(root)
soya.MainLoop().main_loop()

