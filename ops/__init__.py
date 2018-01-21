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
    "RfB_OT_RPASS_AddRenderman",
    "RfB_OT_COLL_TogglePath",
    "RfB_OT_FILE_OpenLastRIB",
    "RfB_OT_FILE_SpoolRender",
    "RfB_OT_FILE_ViewStats",
    "RfB_OT_ITEM_MovetoGroup",
    "RfB_OT_ITEM_RemoveGroup",
    "RfB_OT_ITEM_ToggleLightlink",
    "RfB_OT_LIST_AddMultilayer",
    "RfB_OT_MATERIAL_AddBXDF",
    "RfB_OT_MATERIAL_NewBXDF",
    "RfB_OT_NODE_AddNodetree",
    "RfB_OT_NODE_BakePatterns",
    "RfB_OT_NODE_CyclesConvertall",
    "RfB_OT_NODE_RefreshOSL",
    "RfB_OT_OBJECT_AddLightArea",
    "RfB_OT_OBJECT_AddCamera",
    "RfB_OT_OBJECT_AddLightDay",
    "RfB_OT_OBJECT_AddLightHemi",
    "RfB_OT_OBJECT_AddFilterLight",
    "RfB_OT_OBJECT_DeleteCamera",
    "RfB_OT_OBJECT_DeleteLight",
    "RfB_OT_OBJECT_EnableSubdiv",
    "RfB_OT_OBJECT_ExportRIB",
    "RfB_OT_OBJECT_MakeEmissive",
    "RfB_OT_OBJECT_SelectCamera",
    "RfB_OT_OBJECT_SelectLight",
    "RfB_OT_OUTPUT_ToggleChannel",
    "RfB_OT_RENDER_AddPreset",
    "RfB_OT_TOOL_StartIPR",
    "RfB_OT_TOOL_StartIT",
    "RfB_OT_TOOL_StartLQ",
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
