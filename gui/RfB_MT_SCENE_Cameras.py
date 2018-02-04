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
# Blender Imports
#
import bpy

#
# RenderManForBlender Imports
#
from . import icons


class RfB_MT_SCENE_Cameras(bpy.types.Menu):
    bl_idname = "rfb_mt_scene_cameras"
    bl_label = "Switch Active Camera"
    bl_description = "Select and switch active (render) camera."
    opr = "rfb.object_select_camera"
    iida = icons.iconid('cameraactive')
    iide = icons.iconid('empty')

    def draw(self, context):
        menu = self.layout
        cams = [
            obj for obj in bpy.context.scene.objects if obj.type == "CAMERA"
        ]
        if cams:
            cams.sort(key=lambda cam: cam.name)
            for cam in cams:
                name = cam.name
                try:
                    active = bpy.data.scenes[context.scene.name].camera.name
                    iid = self.iida if active == name else self.iide
                except AttributeError:
                    iid = self.iide
                # menu.enabled = not cam.hide
                op = menu.operator(self.opr, text=name, icon_value=iid)
                op.cam_name = name
        else:
            menu.label("No camera in scene!")
