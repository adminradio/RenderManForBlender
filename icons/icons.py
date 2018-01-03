# ##### BEGIN MIT LICENSE BLOCK #####
#
# Copyright (c) 2015 - 2017 Pixar
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
#
# ##### END MIT LICENSE BLOCK #####

# see ./README.md

import os
import re
import bpy
import bpy.utils.previews

# being chatty
from ..common_utils import echo

renderman_icon_collections = {}
renderman_icons_loaded = False


def get_iconid(ident):
    """Return an 'icon_id' which can be used as 'icon_value'"""
    icn = load_icons().get(ident)
    iid = None
    if icn:
        iid = icn.icon_id
    else:
        echo("Error loading icon id: '" + ident + "' :: using 'dev_error'!")
        iid = load_icons().get("dev_error").icon_id
    return iid


def load_icons():
    global renderman_icon_collections
    global renderman_icons_loaded

    if renderman_icons_loaded:
        return renderman_icon_collections["main"]

    # being chatty
    echo("Loading icons into session.")

    # Previews collection. Used local in short scope,
    # abbreviation should be ok.
    prv = bpy.utils.previews.new()

    # Ressource path. Used local in short scope,
    # abbreviation should be ok.
    rsc = os.path.join(os.path.dirname(__file__))

    for file in os.listdir(rsc):
        if file.endswith(".png"):
            ident = os.path.splitext(file)[0].lower()
            prv.load(ident, os.path.join(rsc, file), 'IMAGE')

    # Add/Atach Coordsys
    # Create Holdout
    # Open Linking Panel
    # Dynamic Binding Editor
    # Create PxrLM Material
    # Create Spot Light
    # custom_icons.load("spotlight", os.path.join(icons_dir, "rman_RMSPointLight.png"), 'IMAGE')
    # Create Geo LightBlocker
    # Make Selected Geo Emissive
    # Create Archive node
    # Update Archive
    # Inspect RIB Selection
    # Shared Geometry Attribute
    # Open Tmake Window
    # Create OpenVDB Visualizer

    renderman_icon_collections["main"] = prv
    renderman_icons_loaded = True

    echo("Done.")
    return renderman_icon_collections["main"]


def clear_icons():
    global renderman_icons_loaded
    for icon in renderman_icon_collections.values():
        bpy.utils.previews.remove(icon)
    renderman_icon_collections.clear()
    renderman_icons_loaded = False
