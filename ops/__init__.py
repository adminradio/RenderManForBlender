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
__ALL__ = [
    "RfB_OT_AOVsAddRenderman",
    "RfB_OT_CollectionTogglePath",
    "RfB_OT_FileOpenLastRIB",
    "RfB_OT_FileSpoolRender",
    "RfB_OT_FileViewStats",
    "RfB_OT_ItemMovetoGroup",
    "RfB_OT_ItemRemoveGroup",
    "RfB_OT_ItemToggleLightlink",
    "RfB_OT_ListAddMultilayer",
    "RfB_OT_MaterialAddBXDF",
    "RfB_OT_MaterialNewBXDF",
    "RfB_OT_NodeAddNodetree",
    "RfB_OT_NodeBakePatterns",
    "RfB_OT_NodeCyclesConvertall",
    "RfB_OT_NodeRefreshOSL",
    "RfB_OT_ObjectAddArealight",
    "RfB_OT_ObjectAddCamera",
    "RfB_OT_ObjectAddDaylight",
    "RfB_OT_ObjectAddHemilight",
    "RfB_OT_ObjectAddLightfilter",
    "RfB_OT_ObjectDeleteCamera",
    "RfB_OT_ObjectDeleteLight",
    "RfB_OT_ObjectEnableSubdiv",
    "RfB_OT_ObjectExportRIB",
    "RfB_OT_ObjectMakeEmissive",
    "RfB_OT_ObjectSelectCamera",
    "RfB_OT_ObjectSelectLight",
    "RfB_OT_OutputToggleChannel",
    "RfB_OT_RenderAddPreset",
    "RfB_OT_ToolStartIPR",
    "RfB_OT_ToolStartIT",
    "RfB_OT_ToolStartLQ",
    "Rfb_OT_ToolReloadRfB",
    "register",
    "unregister"
]

import os
import bpy

from . utils import quick_add_presets
from . utils import compile_shader_menu_func
from . utils.RenderPresets import RenderPresets


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
    bpy.types.TEXT_MT_text.remove(utils.compile_shader_menu_func)
    bpy.types.TEXT_MT_toolbox.remove(utils.compile_shader_menu_func)
    #
    # It should be fine to leave presets registered as they are not in memory.
    #
