# ##### BEGIN MIT LICENSE BLOCK #####
#
# Copyright (c) 2015 - 2018 Pixar
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

#
# Python Imports
#
import os

#
# Blender Imports
#
import bpy

#
# RenderMan for Blender Imports
#
from . RenderPresets import RenderPresets
from ... rfb.lib.file import fixname

#
# Menus
#
compile_shader_menu_func = (
    lambda self,
    context: self.layout.operator(TEXT_OT_compile_shader.bl_idname)
)


def quick_add_presets(presetList, pathFromPresetDir, name):
    filename = fixname(name)
    target_path = os.path.join("presets", pathFromPresetDir)
    target_path = bpy.utils.user_resource('SCRIPTS',
                                          target_path,
                                          create=True)
    if not target_path:
        self.report(
            {'WARNING'},
            "Failed to create presets path")
        return {'CANCELLED'}

    filepath = os.path.join(target_path, filename) + ".py"
    file_preset = open(filepath, 'w')
    file_preset.write("import bpy\n")

    for item in presetList:
        file_preset.write(str(item) + "\n")
    file_preset.close()
