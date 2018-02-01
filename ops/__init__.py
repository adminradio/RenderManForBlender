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

# <pep8-80 compliant>

#
# Python Imports
#
import os
import bpy

#
# Blender Imports
#

#
# RenderManForBlender Imports
#
from .. rfb.lib.file import fixname


#
# TODO:   Implement a JSON laoader/saver and store customised preset
# DATE:   2018-01-12
# AUTHOR: Timm Wimmers
# STATUS: -unassigned-
#
# Utility class to contain all default presets
# this has the added bonus of not using operators for each preset
#
class RenderPresets():
    FinalDenoisePreset = [
        "rm = bpy.context.scene.renderman",
        "rm.pixel_variance = 0.01",
        "rm.min_samples = 32",
        "rm.max_samples = 256",
        "rm.max_specular_depth = 6",
        "rm.max_diffuse_depth = 2",
        "rm.motion_blur = True",
        "rm.do_denoise = True",
        "rm.PxrPathTracer_settings.maxPathLength = 10", ]
    FinalHighPreset = [
        "rm = bpy.context.scene.renderman",
        "rm.pixel_variance = 0.0025",
        "rm.min_samples = 64",
        "rm.max_samples = 1024",
        "rm.max_specular_depth = 6",
        "rm.max_diffuse_depth = 3",
        "rm.motion_blur = True",
        "rm.do_denoise = False",
        "rm.PxrPathTracer_settings.maxPathLength = 10", ]
    FinalPreset = [
        "rm = bpy.context.scene.renderman",
        "rm.pixel_variance = 0.005",
        "rm.min_samples = 32",
        "rm.max_samples = 512",
        "rm.max_specular_depth = 6",
        "rm.max_diffuse_depth = 2",
        "rm.motion_blur = True",
        "rm.do_denoise = False",
        "rm.PxrPathTracer_settings.maxPathLength = 10", ]
    MidPreset = [
        "rm = bpy.context.scene.renderman",
        "rm.pixel_variance = 0.05",
        "rm.min_samples = 0",
        "rm.max_samples = 64",
        "rm.max_specular_depth = 6",
        "rm.max_diffuse_depth = 2",
        "rm.motion_blur = True",
        "rm.do_denoise = False",
        "rm.PxrPathTracer_settings.maxPathLength = 10", ]
    PreviewPreset = [
        "rm = bpy.context.scene.renderman",
        "rm.pixel_variance = 0.1",
        "rm.min_samples = 0",
        "rm.max_samples = 16",
        "rm.max_specular_depth = 2",
        "rm.max_diffuse_depth = 1",
        "rm.motion_blur = False",
        "rm.do_denoise = False",
        "rm.PxrPathTracer_settings.maxPathLength = 5", ]
    TractorLocalQueuePreset = [
        "rm = bpy.context.scene.renderman",
        "rm.pixel_variance = 0.01",
        "rm.min_samples = 24",
        "rm.max_samples = 124",
        "rm.max_specular_depth = 6",
        "rm.max_diffuse_depth = 2",
        "rm.motion_blur = True",
        "rm.PxrPathTracer_settings.maxPathLength = 10",
        "rm.enable_external_rendering = True",
        "rm.external_action = \'spool\'", ]


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
        self.report({'WARNING'}, "Failed to create presets path")
        return {'CANCELLED'}

    filepath = os.path.join(target_path, filename) + ".py"
    file_preset = open(filepath, 'w')
    file_preset.write("import bpy\n")

    for item in presetList:
        file_preset.write(str(item) + "\n")
    file_preset.close()


def register():
    bpy.types.TEXT_MT_text.append(compile_shader_menu_func)
    bpy.types.TEXT_MT_toolbox.append(compile_shader_menu_func)

    # Register any default presets here.
    # This includes render based and Material based
    quick_add_presets(
        RenderPresets.FinalDenoisePreset,
        os.path.join("renderman", "render"),
        "FinalDenoise")

    quick_add_presets(
        RenderPresets.FinalHighPreset,
        os.path.join("renderman", "render"),
        "FinalHigh")

    quick_add_presets(
        RenderPresets.FinalPreset,
        os.path.join("renderman", "render"),
        "Final")

    quick_add_presets(
        RenderPresets.MidPreset,
        os.path.join("renderman", "render"),
        "Mid")

    quick_add_presets(
        RenderPresets.PreviewPreset,
        os.path.join("renderman", "render"),
        "Preview")

    quick_add_presets(
        RenderPresets.TractorLocalQueuePreset,
        os.path.join("renderman", "render"),
        "TractorLocalQueue")


def unregister():
    bpy.types.TEXT_MT_text.remove(compile_shader_menu_func)
    bpy.types.TEXT_MT_toolbox.remove(compile_shader_menu_func)
    #
    # It should be fine to leave presets registered as they are not in memory.
    #
