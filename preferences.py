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

import os
import platform

import bpy
from bpy.types import AddonPreferences

from bpy.props import IntProperty
from bpy.props import BoolProperty
from bpy.props import EnumProperty
from bpy.props import StringProperty
from bpy.props import PointerProperty
from bpy.props import CollectionProperty
from bpy.props import FloatVectorProperty

from . rfb.lib import guess_rmantree
from . rfb.lib import rmantree_from_env
from . rfb.lib import get_installed_rendermans

from . gui.utils import split_ll
from . assets.properties import RendermanAssetGroup


class RendermanPreferencePath(bpy.types.PropertyGroup):
    name = StringProperty(name="", subtype='DIR_PATH')


class RendermanEnvVarSettings(bpy.types.PropertyGroup):
    if platform.system() == "Windows":
        home = os.environ.get('USERPROFILE')
        temp = os.environ.get('TEMP')
        # outpath = os.path.join(home, "Documents", "RenderMan")
        out = StringProperty(
            name="OUT (Output Root)",
            description="Default RIB export path root",
            subtype='DIR_PATH',
            default=os.path.join(temp, 'rfb', '{blend}'))

    else:
        # outpath = os.path.join(os.environ.get('HOME'), "Documents", "RenderMan")
        out = StringProperty(
            name="OUT (Output Root)",
            description="Default RIB export path root",
            subtype='DIR_PATH',
            default='/tmp/rfb/{blend}')

    shd = StringProperty(
        name="SHD (Shadow Maps)",
        description="SHD environment variable",
        subtype='DIR_PATH',
        default=os.path.join('$OUT', 'shadowmaps'))

    ptc = StringProperty(
        name="PTC (Point Clouds)",
        description="PTC environment variable",
        subtype='DIR_PATH',
        default=os.path.join('$OUT', 'pointclouds'))

    arc = StringProperty(
        name="ARC (Archives)",
        description="ARC environment variable",
        subtype='DIR_PATH',
        default=os.path.join('$OUT', 'archives'))


class RendermanPreferences(AddonPreferences):
    bl_idname = __package__

    # find the renderman options installed
    def find_installed_rendermans(self, context):
        options = [('NEWEST', 'Newest Version Installed',
                    'Automatically updates when new version installed.')]
        for vers, path in get_installed_rendermans():
            options.append((path, vers, path))
        return options

    shader_paths = CollectionProperty(type=RendermanPreferencePath,
                                      name="Shader Paths")

    shader_paths_index = IntProperty(min=-1, default=-1)

    texture_paths = CollectionProperty(type=RendermanPreferencePath,
                                       name="Texture Paths")
    texture_paths_index = IntProperty(min=-1, default=-1)

    procedural_paths = CollectionProperty(type=RendermanPreferencePath,
                                          name="Procedural Paths")

    procedural_paths_index = IntProperty(min=-1, default=-1)

    archive_paths = CollectionProperty(type=RendermanPreferencePath,
                                       name="Archive Paths")
    archive_paths_index = IntProperty(min=-1, default=-1)

    use_default_paths = BoolProperty(
        name="Use RenderMan default paths",
        description="Includes paths for default shaders etc. from RenderMan Pro\
            Server install",
        default=True)
    use_builtin_paths = BoolProperty(
        name="Use built in paths",
        description="Includes paths for default shaders etc. from RenderMan\
            exporter",
        default=False)

    rmantree_choice = EnumProperty(
        name='RenderMan Version to use',
        description='Leaving as "Newest" will automatically update when you install a new RenderMan version',
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
                "Scan for installed RenderMan locations to choose from"
            ), (
                "ENV",
                "Get From RMANTREE Environment Variable",
                "This will use the RMANTREE set in the enviornment variables"
            ), (
                "MANUAL",
                "Set Manually",
                "Manually set the RenderMan installation (for expert users)"
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

    rfb_ipr_indicator = BoolProperty(
        name="Indicate IPR",
        description="Draw indicator on View3D when IPR is active.\n"
                    "(Requires restarting IPR if it's currently running)",
        default=True)

    rfb_panel_icon = BoolProperty(
        name="Panel Icons",
        description="Draw a nice icon on RenderMan Panels (recommended)",
        default=True)

    rfb_nesting = BoolProperty(
        name="Box nested properties",
        description="Draw a box around nested property sections",
        default=True)

    rfb_info = BoolProperty(
        name="Info to console",
        description="Echo some useful infos to console (recommended "
                    "for questions in support forum)",
        default=True)

    rfb_debug = BoolProperty(
        name="Debugging (messy!)",
        description="Echo debugging infos to console. This is a bit "
                    "messy and may be easy to follow!",
        default=False)

    #
    # TODO:   requestuesting userpref for laptimes doesn't wotk
    #         as expected (option is always none), have to investigate.
    # DATE:   2018-02-06
    # AUTHOR: Timm Wimmers
    # STATUS: assigned to self, 2018-02-06
    #
    rfb_laptime = BoolProperty(
        name="Time Tasks",
        description="Echo lap times of some critical tasks to console (not "
                    "widely implemented yet, may slightly impact performace)",
        default=True)

    rfb_sc_float = FloatVectorProperty(
        name="Scalar (Float)",
        default=(0.500000, 0.500000, 0.500000, 1.000000),
        size=4,
        min=0, max=1,
        subtype='COLOR')

    rfb_sc_vector = FloatVectorProperty(
        name="Vector (XYZ)",
        default=(0.000000, 0.000000, 1.000000, 1.000000),
        size=4,
        min=0, max=1,
        subtype='COLOR')

    rfb_sc_bxdf = FloatVectorProperty(
        name="Shader (any BxDF)",
        default=(0.000000, 1.000000, 0.000000, 1.000000),
        size=4,
        min=0, max=1,
        subtype='COLOR')

    rfb_sc_color = FloatVectorProperty(
        name="Color (RGB, RGBA)",
        default=(1.000000, 1.000000, 0.000000, 1.000000),
        size=4,
        min=0, max=1,
        subtype='COLOR')

    rfb_sc_string = FloatVectorProperty(
        name="String",
        default=(0.00, 0.00, 1.00, 1.00),
        size=4,
        min=0, max=1,
        subtype='COLOR')

    rfb_sc_int = FloatVectorProperty(
        name="Number (Integer)",
        default=(1.000000, 1.000000, 1.000000, 1.000000),
        size=4,
        min=0, max=1,
        subtype='COLOR')

    rfb_sc_euler = FloatVectorProperty(
        name="Euler",
        default=(0.00, 0.50, 0.50, 1.00),
        size=4,
        min=0, max=1,
        subtype='COLOR')

    rfb_ipr_border = FloatVectorProperty(
        name="IPR Indicator",
        description="Color of IPR indicator (View3D Border)",
        default=(0.870, 0.325, 0.375, 0.750),
        size=4,
        min=0, max=1,
        subtype='COLOR')

    rfb_tabname = StringProperty(
        name="Toolshelf category",
        description="Name of the RenderMan tab in the toolshelf",
        default="RenderMan")

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
        type=RendermanEnvVarSettings,
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
        name="Asset Library Path",
        description="Path for asset files, if not present these will be "
                    "copied from RMANTREE.\nSet this if you want to pull "
                    "in an external library.",
        subtype='FILE_PATH',
        default=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'RenderManAssetLibrary'))

    def draw(self, context):
        layout = self.layout
        layout.prop(self, 'rmantree_method')

        if self.rmantree_method == 'DETECT':
            layout.prop(self, 'rmantree_choice')
        elif self.rmantree_method == 'ENV':
            layout.label(text="RMANTREE: %s " % rmantree_from_env())
        else:
            layout.prop(self, "path_rmantree")

        if guess_rmantree() is None:
            row = layout.row()
            row.alert = True
            row.label('Error in RMANTREE. Reload addon to reset.', icon='ERROR')

        env = self.env_vars
        layout.prop(env, "out")
        layout.prop(self, 'path_display_driver_image')
        layout.prop(self, 'path_aov_image')
        # layout.prop(self.assets_library, 'path', text="Assets Library Path")
        layout.prop(self, 'assets_path')
        layout.prop(self, 'rfb_tabname')
        layout.separator()
        lc, rc = split_ll(layout, alignment=False)
        lc = lc.column()
        row = lc.row()
        row.prop(self, 'rfb_ipr_indicator')
        row.prop(self, 'rfb_ipr_border', text="")
        lc.prop(self, 'rfb_panel_icon')
        lc.prop(self, 'rfb_nesting')
        lc.separator()
        lc.separator()
        lc.separator()
        lc.prop(self, 'rfb_info')
        lc.prop(self, 'rfb_debug')
        #
        #
        # FIXME:  Timing with @laptime currently doesn't support user
        #         preferences (it's none during request), have to
        #         investigate
        # DATE:   2018-02-04
        # AUTHOR: Timm Wimmers
        # STATUS: assigned to self, 2018-02-06
        #
        # lc.prop(self, 'rfb_laptime')

        box = rc.box()
        box.label("Node Tree Socket Colors:")
        box = box.column(align=True)
        row = box.row()
        row.prop(self, 'rfb_sc_bxdf')
        row = box.row()
        row.prop(self, 'rfb_sc_color')
        row = box.row()
        row.prop(self, 'rfb_sc_float')
        row = box.row()
        row.prop(self, 'rfb_sc_int')
        row = box.row()
        row.prop(self, 'rfb_sc_vector')
        # layout.prop(self, 'rfb_sc_string')
        # layout.prop(self, 'rfb_sc_euler')

        # layout.prop(env, "shd")
        # layout.prop(env, "ptc")
        # layout.prop(env, "arc")


def register():
    try:
        from . assets import properties
        properties.register()
        bpy.utils.register_class(RendermanPreferencePath)
        bpy.utils.register_class(RendermanEnvVarSettings)
        bpy.utils.register_class(RendermanPreferences)
    except Exception:
        #
        # already registered
        #
        pass


def unregister():
    bpy.utils.unregister_class(RendermanPreferences)
    bpy.utils.unregister_class(RendermanEnvVarSettings)
    bpy.utils.unregister_class(RendermanPreferencePath)
