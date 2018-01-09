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

import bpy
import os
import subprocess
import bgl
import blf
import webbrowser
import addon_utils
from operator import attrgetter, itemgetter
from bl_operators.presets import AddPresetBase
from bpy_extras.io_utils import ExportHelper

from bpy.props import (
    IntProperty,
    BoolProperty,
    EnumProperty,
    FloatProperty,
    StringProperty,
    PointerProperty,
    CollectionProperty,
    FloatVectorProperty
)

from .util import init_env
from .util import getattr_recursive
from .util import user_path
from .util import get_addon_prefs
from .util import get_real_path
from .util import readOSO, find_it_path, find_local_queue, find_tractor_spool
from .util import get_Files_in_Directory

from .export import export_archive
from .export import get_texture_list
from .engine import RPass
from .export import debug
from .export import write_archive_RIB
from .export import EXCLUDED_OBJECT_TYPES
from . import engine

# from .nodes import convert_cycles_nodetree, is_renderman_nodetree

#from .nodes import RendermanPatternGraph

from .spool import spool_render


from . import icons

from . ops import (
    RfB_OT_SelectLight,
    RfB_OT_OpenLastRIB,
    RfB_OT_ToggleChannelOutput,
    RfB_OT_ConvertAllCyclesNodes,
    RfB_OT_AddRendermanNodetree,
    RfB_OT_SpoolExternalRender,
    RfB_OT_AddAOVs,
    RfB_OT_ToggleCollection,
    RfB_OT_AddMultilayerList,
    RfB_OT_MoveItemToGroup,
    RfB_OT_RemoveItemFromGroup,

)


###########################
# Presets for integrators.
###########################
def quickAddPresets(presetList, pathFromPresetDir, name):
    def as_filename(name):  # could reuse for other presets
        for char in " !@#$%^&*(){}:\";'[]<>,.\\/?":
            name = name.replace(char, '_')
        return name.strip()

    filename = as_filename(name)
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


class AddPresetRendermanRender(AddPresetBase, bpy.types.Operator):
    '''Add or remove a RenderMan Sampling Preset'''
    bl_idname = "render.renderman_preset_add"
    bl_label = "Add RenderMan Preset"
    bl_options = {'REGISTER', 'UNDO'}
    preset_menu = "presets"
    preset_defines = ["scene = bpy.context.scene", ]

    preset_values = [
        "scene.renderman.pixel_variance",
        "scene.renderman.min_samples",
        "scene.renderman.max_samples",
        "scene.renderman.max_specular_depth",
        "scene.renderman.max_diffuse_depth",
        "scene.renderman.motion_blur",
        "scene.renderman.do_denoise",
    ]

    preset_subdir = os.path.join("renderman", "render")


class PresetsMenu(bpy.types.Menu):
    bl_label = "RenderMan Presets"
    bl_idname = "presets"
    preset_subdir = os.path.join("renderman", "render")
    preset_operator = "script.execute_preset"
    draw = bpy.types.Menu.draw_preset


#################
# Sample scenes menu.
#################
# Watch out for global list!!
# Its name should be too long to be accedenty called but you never know.
#
blenderAddonPaths = addon_utils.paths()
rendermanExampleFilesList = []
names = []
for path in blenderAddonPaths:
    basePath = os.path.join(path, "RenderManForBlender", "examples")
    exists = os.path.exists(basePath)
    if exists:
        names = get_Files_in_Directory(basePath)
for name in names:
    class examplesRenderman(bpy.types.Operator):
        bl_idname = ("rfb.examples_" + name.lower())
        bl_label = name
        bl_description = name

        def invoke(self, context, event):
            sucess = self.loadFile(self, self.bl_label)
            if not sucess:
                self.report({'ERROR'}, "Example Does Not Exist!")
            return {'FINISHED'}

        def loadFile(self, context, exampleName):
            blenderAddonPaths = addon_utils.paths()
            for path in blenderAddonPaths:
                basePath = os.path.join(path, "RenderManForBlender", "examples")
                exists = os.path.exists(basePath)
                if exists:
                    examplePath = os.path.join(
                        basePath, exampleName, exampleName + ".blend")
                    if(os.path.exists(examplePath)):
                        bpy.ops.wm.open_mainfile(filepath=examplePath)
                        return True
                    else:
                        return False
    rendermanExampleFilesList.append(examplesRenderman)


class LoadSceneMenu(bpy.types.Menu):
    bl_label = "RenderMan Examples"
    bl_idname = "examples"
    iid = icons.iconid('prman')

    def get_operator_failsafe(self, idname):
        op = bpy.ops
        for attr in idname.split("."):
            if attr not in dir(op):
                return lambda: None
            op = getattr(op, attr)
        return op

    def draw(self, context):
        for operator in rendermanExampleFilesList:
            self.layout.operator(operator.bl_idname, icon_value=self.iid)


def menu_draw(self, context):
    if context.scene.render.engine != "PRMAN_RENDER":
        return

    iid = icons.iconid("help")
    self.layout.menu("examples", icon_value=iid)


class OT_remove_add_rem_light_link(bpy.types.Operator):
    bl_idname = 'rfb.toggle_lightlink'
    bl_label = 'Add/Remove Selected from Object Group'

    add_remove = StringProperty(default='add')
    ll_name = StringProperty(default='')

    def execute(self, context):
        scene = context.scene

        add_remove = self.properties.add_remove
        ll_name = self.properties.ll_name

        if add_remove == 'add':
            ll = scene.renderman.ll.add()
            ll.name = ll_name
        else:
            ll_index = scene.renderman.ll.keys().index(ll_name)
            if engine.is_ipr_running():
                engine.ipr.remove_light_link(
                    context, scene.renderman.ll[ll_index])
            scene.renderman.ll.remove(ll_index)

        return {'FINISHED'}


class Add_Subdiv_Sheme(bpy.types.Operator):
    bl_idname = "rfb.make_subdiv"
    bl_label = "Make Subdiv Mesh"
    bl_description = ""
    bl_options = {"REGISTER"}

    def execute(self, context):
        bpy.context.object.renderman.primitive = 'SUBDIVISION_MESH'

        return {"FINISHED"}


# FIXME: naming??
class RM_Add_Area(bpy.types.Operator):
    bl_idname = "object.mr_add_area"
    bl_label = "Add RenderMan Area"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):

        bpy.ops.object.lamp_add(type='AREA')
        bpy.ops.rfb.add_renderman_nodetree(
            {'material': None, 'lamp': bpy.context.active_object.data}, idtype='lamp')
        return {"FINISHED"}


# FIXME: naming??
class RM_Add_LightFilter(bpy.types.Operator):
    bl_idname = "object.mr_add_light_filter"
    bl_label = "Add RenderMan Light Filter"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):

        bpy.ops.object.lamp_add(type='POINT')
        lamp = bpy.context.active_object.data
        bpy.ops.rfb.add_renderman_nodetree(
            {'material': None, 'lamp': lamp}, idtype='lamp')
        lamp.renderman.renderman_type = 'FILTER'
        return {"FINISHED"}


# FIXME: naming??
class RM_Add_Hemi(bpy.types.Operator):
    bl_idname = "object.mr_add_hemi"
    bl_label = "Add RenderMan Hemi"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):

        bpy.ops.object.lamp_add(type='HEMI')
        bpy.ops.rfb.add_renderman_nodetree(
            {'material': None, 'lamp': bpy.context.active_object.data}, idtype='lamp')
        return {"FINISHED"}


# FIXME: naming??
class RM_Add_Sky(bpy.types.Operator):
    bl_idname = "object.mr_add_sky"
    bl_label = "Add RenderMan Sky"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        bpy.ops.object.lamp_add(type='SUN')
        bpy.ops.rfb.add_renderman_nodetree(
            {'material': None, 'lamp': bpy.context.active_object.data}, idtype='lamp')
        bpy.context.object.data.renderman.renderman_type = 'SKY'

        return {"FINISHED"}


class Add_bxdf(bpy.types.Operator):
    bl_idname = "rfb.add_bxdf"
    bl_label = "Add BXDF"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    def get_type_items(self, context):
        items = [
            ("PxrSurface",
                "PxrSurface",
                'PxrSurface Uber shader. For most hard surfaces'),
            ("PxrLayerSurface",
                "PxrLayerSurface",
                "PxrLayerSurface, creates a surface with two Layers"),
            ("PxrMarschnerHair",
                "PxrMarschnerHair",
                "Hair Shader"),
            ("PxrDisney",
                "PxrDisney",
                "Disney Bxdf, a simple uber shader with no layering"),
            ("PxrVolume",
                "PxrVolume",
                "Volume Shader")
        ]
        # for nodetype in RendermanPatternGraph.nodetypes.values():
        #    if nodetype.renderman_node_type == 'bxdf':
        #        items.append((nodetype.bl_label, nodetype.bl_label,
        #                      nodetype.bl_label))
        return items

    bxdf_name = EnumProperty(items=get_type_items, name="Bxdf Name")

    def execute(self, context):
        selection = bpy.context.selected_objects if hasattr(
            bpy.context, 'selected_objects') else []
        #selection = bpy.context.selected_objects
        bxdf_name = self.properties.bxdf_name
        mat = bpy.data.materials.new(bxdf_name)

        mat.use_nodes = True
        nt = mat.node_tree

        output = nt.nodes.new('RendermanOutputNode')
        default = nt.nodes.new('%sBxdfNode' % bxdf_name)
        default.location = output.location
        default.location[0] -= 300
        nt.links.new(default.outputs[0], output.inputs[0])

        if bxdf_name == 'PxrLayerSurface':
            mixer = nt.nodes.new("PxrLayerMixerPatternNode")
            layer1 = nt.nodes.new("PxrLayerPatternNode")
            layer2 = nt.nodes.new("PxrLayerPatternNode")

            mixer.location = default.location
            mixer.location[0] -= 300

            layer1.location = mixer.location
            layer1.location[0] -= 300
            layer1.location[1] += 300

            layer2.location = mixer.location
            layer2.location[0] -= 300
            layer2.location[1] -= 300

            nt.links.new(mixer.outputs[0], default.inputs[0])
            nt.links.new(layer1.outputs[0], mixer.inputs['baselayer'])
            nt.links.new(layer2.outputs[0], mixer.inputs['layer1'])

        for obj in selection:
            if(obj.type not in EXCLUDED_OBJECT_TYPES):
                bpy.ops.object.material_slot_add()

                obj.material_slots[-1].material = mat

        return {"FINISHED"}


class New_bxdf(bpy.types.Operator):
    bl_idname = "rfb.new_bxdf"
    bl_label = "New RenderMan Material"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        ob = context.object
        bxdf_name = 'PxrSurface'
        mat = bpy.data.materials.new(bxdf_name)
        ob.active_material = mat
        mat.use_nodes = True
        nt = mat.node_tree

        output = nt.nodes.new('RendermanOutputNode')
        default = nt.nodes.new('PxrSurfaceBxdfNode')
        default.location = output.location
        default.location[0] -= 300
        nt.links.new(default.outputs[0], output.inputs[0])

        return {"FINISHED"}


class add_GeoLight(bpy.types.Operator):
    bl_idname = "rfb.make_emissive"
    bl_label = "Add GeoAreaLight"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        selection = bpy.context.selected_objects
        mat = bpy.data.materials.new("PxrMeshLight")

        mat.use_nodes = True
        nt = mat.node_tree

        output = nt.nodes.new('RendermanOutputNode')
        geoLight = nt.nodes.new('PxrMeshLightLightNode')
        geoLight.location[0] -= 300
        geoLight.location[1] -= 420
        if(output is not None):
            nt.links.new(geoLight.outputs[0], output.inputs[1])
        for obj in selection:
            if(obj.type not in EXCLUDED_OBJECT_TYPES):
                bpy.ops.object.material_slot_add()
                obj.material_slots[-1].material = mat
        return {"FINISHED"}

# ##REFACTOR##
# class Select_Lights(bpy.types.Operator):
#     bl_idname = "object.selectlight"
#     bl_label = "Select Lights"

#     light_name = bpy.props.StringProperty(default="")

#     def execute(self, context):

#         bpy.ops.object.select_all(action='DESELECT')
#         bpy.data.objects[self.light_Name].select = True
#         bpy.context.scene.objects.active = bpy.data.objects[self.light_name]

#         return {'FINISHED'}


class Hemi_List_Menu(bpy.types.Menu):
    bl_idname = "rfb_mt.hemilights"
    bl_label = "EnvLight list"

    icn = icons.iconid('envlight')

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)

        lamps = [obj for obj in bpy.context.scene.objects if obj.type == "LAMP"]

        if len(lamps):
            for lamp in lamps:
                if lamp.data.type == 'HEMI':
                    name = lamp.name
                    op = layout.operator(
                        "object.selectlight", text=name, icon_value=self.icn)
                    op.light_name = name

        else:
            layout.label("No EnvLight in the Scene")


class Area_List_Menu(bpy.types.Menu):
    bl_idname = "rfb_mt.arealights"
    bl_label = "AreaLight list"

    icn = icons.iconid('arealight')

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)

        lamps = [obj for obj in bpy.context.scene.objects if obj.type == "LAMP"]

        if len(lamps):
            for lamp in lamps:
                if lamp.data.type == 'AREA':
                    name = lamp.name
                    op = layout.operator(
                        "object.selectlight", text=name, icon_value=self.icn)
                    op.light_name = name

        else:
            layout.label("No AreaLight in the Scene")


class DayLight_List_Menu(bpy.types.Menu):
    bl_idname = "rfb_mt.daylights"
    bl_label = "DayLight list"

    icn = icons.iconid('sunlight')

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)

        lamps = [obj for obj in bpy.context.scene.objects if obj.type == "LAMP"]

        if len(lamps):
            for lamp in lamps:
                if lamp.data.type == 'SUN':
                    name = lamp.name
                    op = layout.operator(
                        "object.selectlight", text=name, icon_value=self.icn)
                    op.light_name = name

        else:
            layout.label("No Daylight in the Scene")


class Select_Cameras(bpy.types.Operator):
    bl_idname = "rfb.select_camera"
    bl_label = "Select Cameras"

    camera_name = bpy.props.StringProperty(default="")

    def execute(self, context):

        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects[self.camera_name].select = True
        bpy.context.scene.objects.active = bpy.data.objects[self.camera_name]

        return {'FINISHED'}


class Camera_List_Menu(bpy.types.Menu):
    bl_idname = "rfb_mt.cameralist"
    bl_label = "Camera list"

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)

        cameras = [
            obj for obj in bpy.context.scene.objects if obj.type == "CAMERA"]

        if len(cameras):
            for cam in cameras:
                name = cam.name
                op = layout.operator(
                    "rfb.select_camera", text=name, icon='CAMERA_DATA')
                op.camera_name = name

        else:
            layout.label("No Camera in the Scene")


class DeleteLights(bpy.types.Operator):
    bl_idname = "rfb.delete_light"
    bl_label = "Delete Lights"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):

        type_light = bpy.context.object.data.type
        bpy.ops.object.delete()

        lamps = [obj for obj in bpy.context.scene.objects if obj.type ==
                 "LAMP" and obj.data.type == type_light]

        if len(lamps):
            lamps[0].select = True
            bpy.context.scene.objects.active = lamps[0]
            return {"FINISHED"}

        else:
            return {"FINISHED"}


class Deletecameras(bpy.types.Operator):
    bl_idname = "rfb.delete_camera"
    bl_label = "Delete Cameras"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):

        type_camera = bpy.context.object.data.type
        bpy.ops.object.delete()

        camera = [obj for obj in bpy.context.scene.objects if obj.type ==
                  "CAMERA" and obj.data.type == type_camera]

        if len(camera):
            camera[0].select = True
            bpy.context.scene.objects.active = camera[0]
            return {"FINISHED"}

        else:
            return {"FINISHED"}


class AddCamera(bpy.types.Operator):
    bl_idname = "rfb.add_camera"
    bl_label = "Add Camera"
    bl_description = "Add a Camera in the Scene"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):

        bpy.context.space_data.lock_camera = False

        bpy.ops.object.camera_add()

        bpy.ops.view3d.object_as_camera()

        bpy.ops.view3d.viewnumpad(type="CAMERA")

        bpy.ops.view3d.camera_to_view()

        bpy.context.object.data.clip_end = 10000
        bpy.context.object.data.lens = 85

        return {"FINISHED"}


# This operator should not be exposed to the UI as
#   this can cause the loss of data since Blender does not
#   preserve any information during script restart.
class RM_restart_addon(bpy.types.Operator):
    bl_idname = "rfb.restartaddon"
    bl_label = "Restart Addon"
    bl_description = "Restarts the RenderMan for Blender addon"

    def execute(self, context):
        bpy.ops.script.reload()
        return {"FINISHED"}


# Menus
compile_shader_menu_func = (lambda self, context: self.layout.operator(
    TEXT_OT_compile_shader.bl_idname))


def register():
    #
    # Not usual here, but looks reasonable to me. (TW)
    #
    from . utils.RFB_STATIC_RenderPresets import RFB_STATIC_RenderPresets

    bpy.types.TEXT_MT_text.append(compile_shader_menu_func)
    bpy.types.TEXT_MT_toolbox.append(compile_shader_menu_func)
    bpy.types.INFO_MT_help.append(menu_draw)

    # Register any default presets here. This includes render based and
    # Material based
    quickAddPresets(RFB_STATIC_RenderPresets.FinalDenoisePreset,
                    os.path.join("renderman", "render"), "FinalDenoisePreset")
    quickAddPresets(RFB_STATIC_RenderPresets.FinalHighPreset,
                    os.path.join("renderman", "render"), "FinalHigh_Preset")
    quickAddPresets(RFB_STATIC_RenderPresets.FinalPreset,
                    os.path.join("renderman", "render"), "FinalPreset")
    quickAddPresets(RFB_STATIC_RenderPresets.MidPreset,
                    os.path.join("renderman", "render"), "MidPreset")
    quickAddPresets(RFB_STATIC_RenderPresets.PreviewPreset,
                    os.path.join("renderman", "render"), "PreviewPreset")
    quickAddPresets(RFB_STATIC_RenderPresets.TractorLocalQueuePreset, os.path.join(
        "renderman", "render"), "TractorLocalQueuePreset")


def unregister():
    bpy.types.TEXT_MT_text.remove(compile_shader_menu_func)
    bpy.types.TEXT_MT_toolbox.remove(compile_shader_menu_func)
    bpy.types.INFO_MT_help.remove(menu_draw)

    # It should be fine to leave presets registered as they are not in memory.
