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
import platform

#
# Blender Imports
#
import bpy

from bpy.types import AddonPreferences
from bpy.props import IntProperty
from bpy.props import BoolProperty
from bpy.props import EnumProperty
from bpy.props import StringProperty
from bpy.props import PointerProperty
from bpy.props import CollectionProperty

#
# RenderManForBlender Imports
#
from . lib import rman
from . import RfB_PreferencePath
from . import RfB_EnvVarSettings
from .. assets.properties import RendermanAssetGroup


class RfB_Preferences(AddonPreferences):
    bl_idname = __package__

    # find the renderman options installed
    def find_installed_rendermans(self, context):
        options = [('NEWEST', 'Newest Version Installed',
                    'Automatically updates when new version installed.')]

        for vers, path in rman.available().items():
            options.append((path, vers, path))
        return options

    shader_paths = CollectionProperty(
        type=RfB_PreferencePath,
        name="Shader Paths"
    )

    shader_paths_index = IntProperty(
        min=-1,
        default=-1
    )

    texture_paths = CollectionProperty(
        type=RfB_PreferencePath,
        name="Texture Paths"
    )

    texture_paths_index = IntProperty(
        min=-1,
        default=-1
    )

    procedural_paths = CollectionProperty(
        type=RfB_PreferencePath,
        name="Procedural Paths"
    )

    procedural_paths_index = IntProperty(min=-1, default=-1)

    archive_paths = CollectionProperty(type=RfB_PreferencePath,
                                       name="Archive Paths")

    archive_paths_index = IntProperty(min=-1, default=-1)

    use_default_paths = BoolProperty(
        name="Use RenderMan default paths",
        description="Includes paths for default shaders etc. from selected "
                    "RenderMan Pro Server installation.",
        default=True
    )

    use_builtin_paths = BoolProperty(
        name="Use built in paths",
        description="Includes paths for default shaders etc. from selected "
                    "RenderMan exporter",
        default=False
    )

    rmantree_choice = EnumProperty(
        name='RenderMan Version to use',
        description="Leaving as 'Newest' will automatically update when "
                    "you install a new RenderMan version",
        # default='NEWEST',
        items=find_installed_rendermans
    )

    rmantree_method = EnumProperty(
        name='RenderMan Location',
        description="How RenderMan should be detected. "
                    "Most users should leave to 'Detect'",
        items=[
            (
                "DETECT",
                "Choose From Installed",
                "Scan for installed RenderMan locations to choose from."
            ),
            (
                "ENV",
                "Get From RMANTREE Environment Variable",
                "This will use the RMANTREE variable from current uers "
                "environment (falls back to 'NEWEST' if RMANTREE isn't set "
                "or a valid installation was not found at given value."
            ),
            (
                "MANUAL",
                "Set Manually",
                "Manually set the RenderMan installation (for expert users)."
            )
        ]
    )

    path_rmantree = StringProperty(
        name="RMANTREE Path",
        description="Path to RenderMan Pro Server installation folder",
        subtype='DIR_PATH',
        default='')

    path_renderer = StringProperty(
        name="Renderer Path",
        description="Path to renderer executable",
        subtype='FILE_PATH',
        default="prman")

    path_shader_compiler = StringProperty(
        name="Shader Compiler Path",
        description="Path to shader compiler executable",
        subtype='FILE_PATH',
        default="shader")

    path_shader_info = StringProperty(
        name="Shader Info Path",
        description="Path to shaderinfo executable",
        subtype='FILE_PATH',
        default="sloinfo")

    path_texture_optimiser = StringProperty(
        name="Texture Optimiser Path",
        description="Path to tdlmake executable",
        subtype='FILE_PATH',
        default="txmake")

    draw_ipr = BoolProperty(
        name="Indicate running IPR",
        description="Draw indicator on View3D when IPR is active",
        default=True)

    draw_panel_icon = BoolProperty(
        name="Draw Panel Icon",
        description="Draw an icon on RenderMan Panels",
        default=True)

    path_display_driver_image = StringProperty(
        name="Main Image path",
        description="Path for the rendered main image",
        subtype='FILE_PATH',
        default=os.path.join('$OUT', 'images', '{scene}.####.{file_type}'))

    path_aov_image = StringProperty(
        name="AOV Image path",
        description="Path for the rendered aov images",
        subtype='FILE_PATH',
        default=os.path.join('$OUT', 'images', '{scene}.{layer}.{pass}.####.{file_type}'))

    env_vars = PointerProperty(
        type=RfB_EnvVarSettings,
        name="Environment Variable Settings")

    auto_check_update = bpy.props.BoolProperty(
        name="Auto-check for Update",
        description="If enabled, auto-check for updates using an interval",
        default=True,
    )

    assets_library = PointerProperty(
        type=RendermanAssetGroup,
    )

    # both these paths are absolute
    active_assets_path = StringProperty(default='')
    assets_path = StringProperty(
        name="Path For Asset Library",
        description="Path for asset files, if not present these will be "
                    "copied from RMANTREE.\nSet this if you want to pull "
                    "in an external library.",
        subtype='FILE_PATH',
        default=os.path.join(
            os.path.dirname(
                os.path.abspath(__file__)
            ), 'data', 'RenderManAssetLibrary')
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, 'rmantree_method')

        if self.rmantree_method == 'DETECT':
            layout.prop(self, 'rmantree_choice')
        elif self.rmantree_method == 'ENV':
            layout.label(text="RMANTREE: %s " % rman.from_env())
        else:
            layout.prop(self, "path_rmantree")

        # if guess_rmantree() is None:
        #     row = layout.row()
        #     row.alert = True
        #     row.label('Error in RMANTREE. Reload addon to reset.', icon='ERROR')

        env = self.env_vars
        layout.prop(env, "out")
        layout.prop(self, 'path_display_driver_image')
        layout.prop(self, 'path_aov_image')
        layout.prop(self, 'draw_ipr')
        layout.prop(self, 'draw_panel_icon')
        layout.prop(self.assets_library, 'path')
        # layout.prop(env, "shd")
        # layout.prop(env, "ptc")
        # layout.prop(env, "arc")
