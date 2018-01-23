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
# Python imports
#
import os

#
# Blender Imports
#
import bpy

#
# RenderManForBlender Imports
#
from .. gui import icons
from .. shader_parameters import txmake_options

NODE_LAYOUT_SPLIT = 0.5


def update_func(self, context):
    """Update node during IPR for a socket default_value."""

    # check if this prop is set on an input
    node = self.node if hasattr(self, 'node') else self

    from .. import engine
    if engine.is_ipr_running():
        engine.ipr.issue_shader_edits(node=node)


def link_node(nt, from_node, in_socket):
    out_socket = None
    # first look for resultF/resultRGB
    if type(in_socket).__name__ in ['RendermanNodeSocketColor',
                                    'RendermanNodeSocketVector']:
        out_socket = from_node.outputs.get('resultRGB',
                                           next((s for s in from_node.outputs
                                                 if type(s).__name__ == 'RendermanNodeSocketColor'), None))
    elif type(in_socket).__name__ == 'RendermanNodeSocketStruct':
        out_socket = from_node.outputs.get('pxrMaterialOut', None)
        if not out_socket:
            out_socket = from_node.outputs.get('result', None)
    else:
        out_socket = from_node.outputs.get('resultF',
                                           next((s for s in from_node.outputs
                                                 if type(s).__name__ == 'RendermanNodeSocketFloat'), None))
    if out_socket:
        nt.links.new(out_socket, in_socket)


def draw_panel(layout, context, id_data, output_type, input_name):
    ntree = id_data.node_tree

    n = find_node(id_data, output_type)
    if not n:
        layout.label(text="No output node")
    else:
        # input = find_input(n, input_name)
        # layout.template_node_view(ntree, n, input)
        draw_props_ui(layout, context, ntree)

    return True


def draw_props_ui(layout, context, nt, input_name='Bxdf', output_node_type="output"):
    n_out = (
        next((n for n in nt.nodes
              if hasattr(n, 'renderman_node_type') and
              n.renderman_node_type == output_node_type), None)
    )
    if n_out is None:
        return

    s = n_out.inputs[input_name]
    n = socket_node_input(nt, s)

    layout.context_pointer_set("nodetree", nt)
    layout.context_pointer_set("node", n_out)
    layout.context_pointer_set("socket", s)

    split = layout.split(0.35)
    split.label(s.name + ':')

    if s.is_linked:
        # for lights draw the shading rate ui.
        split.operator_menu_enum("node.add_%s" % input_name.lower(),
                                 "node_type", text=n.bl_label)
    else:
        split.operator_menu_enum("node.add_%s" % input_name.lower(),
                                 "node_type", text='None')
    # if n?
    if n is not None:
        draw_props_recursive(layout, context, nt, n)


def draw_props_recursive(layout, context, nt, node, level=0):
    def indented_label(layout, label, level):
        for i in range(level):
            layout.label('', icon='BLANK1')
        if label:
            layout.label(label)

    layout.context_pointer_set("node", node)
    layout.context_pointer_set("nodetree", nt)

    def draw_props(prop_names, layout, level):
        for prop_name in prop_names:
            # skip showing the shape for PxrStdAreaLight
            if prop_name in ["lightGroup", "rman__Shape", "coneAngle", "penumbraAngle"]:
                continue

            if prop_name == "codetypeswitch":
                row = layout.row()
                if node.codetypeswitch == 'INT':
                    row.prop_search(node, "internalSearch",
                                    bpy.data, "texts", text="")
                elif node.codetypeswitch == 'EXT':
                    row.prop(node, "shadercode")
            elif prop_name == "internalSearch" or prop_name == "shadercode" or prop_name == "expression":
                pass
            else:
                prop_meta = node.prop_meta[prop_name]
                prop = getattr(node, prop_name)

                if 'widget' in prop_meta and prop_meta['widget'] == 'null' or \
                        'hidden' in prop_meta and prop_meta['hidden']:
                    continue

                # else check if the socket with this name is connected
                socket = node.inputs[prop_name] if prop_name in node.inputs \
                    else None
                layout.context_pointer_set("socket", socket)

                if socket and socket.is_linked:
                    input_node = socket_node_input(nt, socket)
                    icon = 'TRIA_DOWN' if socket.ui_open else 'TRIA_RIGHT'

                    split = layout.split(NODE_LAYOUT_SPLIT)
                    row = split.row()
                    indented_label(row, None, level)
                    row.prop(socket, "ui_open", icon=icon, text='',
                             icon_only=True, emboss=False)
                    label = prop_meta.get('label', prop_name)
                    row.label(label + ':')
                    if ('type' in prop_meta and prop_meta['type'] == 'vstruct') or prop_name == 'inputMaterial':
                        split.operator_menu_enum("node.add_layer", "node_type",
                                                 text=input_node.bl_label, icon="LAYER_USED")
                    elif prop_meta['renderman_type'] == 'struct':
                        split.operator_menu_enum("node.add_manifold", "node_type",
                                                 text=input_node.bl_label, icon="LAYER_USED")
                    elif prop_meta['renderman_type'] == 'normal':
                        split.operator_menu_enum("node.add_bump", "node_type",
                                                 text=input_node.bl_label, icon="LAYER_USED")
                    else:
                        split.operator_menu_enum("node.add_pattern", "node_type",
                                                 text=input_node.bl_label, icon="LAYER_USED")

                    if socket.ui_open:
                        draw_props_recursive(layout, context, nt,
                                             input_node, level=level + 1)

                else:
                    row = layout.row(align=True)
                    if prop_meta['renderman_type'] == 'page':
                        ui_prop = prop_name + "_ui_open"
                        ui_open = getattr(node, ui_prop)

                        cl = row.box()
                        row = cl.row()

                        iid = icons.toggle('panel', ui_open)
                        row.prop(node, ui_prop,
                                 icon_value=iid, text='',
                                 icon_only=True, emboss=False)

                        sub_prop_names = list(prop)
                        if node.bl_idname in {"PxrSurfaceBxdfNode", "PxrLayerPatternNode"}:
                            for pn in sub_prop_names:
                                if pn.startswith('enable'):
                                    row.prop(node, pn, text='')
                                    sub_prop_names.remove(pn)
                                    break

                        row.label(prop_name.split('.')[-1] + ':')

                        if ui_open:
                            draw_props(sub_prop_names, cl, level + 1)

                    else:
                        # indented_label(row, None, level)
                        # indented_label(row, socket.name+':')
                        # don't draw prop for struct type
                        # print("Name: {}".format(prop_name))  # devhelp
                        if "Subset" in prop_name and prop_meta['type'] == 'string':
                            row.prop_search(node, prop_name, bpy.data.scenes[0].renderman,
                                            "object_groups")
                        else:
                            if prop_meta['renderman_type'] != 'struct':
                                row.prop(node, prop_name, slider=True)
                            else:
                                row.label(prop_meta['label'])
                        if prop_name in node.inputs:
                            if ('type' in prop_meta and prop_meta['type'] == 'vstruct') or prop_name == 'inputMaterial':
                                row.operator_menu_enum("node.add_layer", "node_type",
                                                       text='', icon="LAYER_USED")
                            elif prop_meta['renderman_type'] == 'struct':
                                row.operator_menu_enum("node.add_manifold", "node_type",
                                                       text='', icon="LAYER_USED")
                            elif prop_meta['renderman_type'] == 'normal':
                                row.operator_menu_enum("node.add_bump", "node_type",
                                                       text='', icon="LAYER_USED")
                            else:
                                row.operator_menu_enum("node.add_pattern", "node_type",
                                                       text='', icon="LAYER_USED")

    # if this is a cycles node do something different
    if not hasattr(node, 'plugin_name') or node.bl_idname == 'PxrOSLPatternNode':
        node.draw_buttons(context, layout)
        for input in node.inputs:
            if input.is_linked:
                input_node = socket_node_input(nt, input)
                icon = 'DISCLOSURE_TRI_DOWN' if input.show_expanded \
                    else 'DISCLOSURE_TRI_RIGHT'

                split = layout.split(NODE_LAYOUT_SPLIT)
                row = split.row()
                indented_label(row, None, level)
                row.prop(input, "show_expanded", icon=icon, text='',
                         icon_only=True, emboss=False)
                row.label(input.name + ':')
                split.operator_menu_enum("node.add_pattern", "node_type",
                                         text=input_node.bl_label, icon="LAYER_USED")

                if input.show_expanded:
                    draw_props_recursive(layout, context, nt,
                                         input_node, level=level + 1)

            else:
                row = layout.row(align=True)
                indented_label(row, None, level)
                # indented_label(row, socket.name+':')
                # don't draw prop for struct type
                if input.hide_value:
                    row.label(input.name)
                else:
                    row.prop(input, 'default_value',
                             slider=True, text=input.name)
                row.operator_menu_enum("node.add_pattern", "node_type",
                                       text='', icon="LAYER_USED")
    else:
        if node.plugin_name == 'PxrRamp':
            dummy_nt = bpy.data.node_groups[node.node_group]
            if dummy_nt:
                layout.template_color_ramp(
                    dummy_nt.nodes['ColorRamp'], 'color_ramp')
        draw_props(node.prop_names, layout, level)
    layout.separator()


def find_input(node, name):
    for ninput in node.inputs:
        if ninput.name == name:
            return ninput
    return None


def find_node(material, nodetype):
    if material and material.node_tree:
        ntree = material.node_tree

        active_output_node = None
        for node in ntree.nodes:
            if getattr(node, "bl_idname", None) == nodetype:
                if getattr(node, "is_active_output", True):
                    return node
                if not active_output_node:
                    active_output_node = node
        return active_output_node
    return None


def is_renderman(material):
    return find_node(material, 'RendermanOutputNode')


def socket_node_input(nt, socket):
    return (
        next(
            (l.from_node
                for l in nt.links
                if l.to_socket == socket), None)
    )


def sockets_socket_input(nt, socket):
    return (
        next(
            (l.from_socket
                for l in nt.links
                if l.to_socket == socket and socket.is_linked),
            None)
    )


def linked_sockets(sockets):
    if sockets is None:
        return []
    return [i for i in sockets if i.is_linked]


def replace_frame_num(prop):
    frame_num = bpy.data.scenes[0].frame_current
    prop = prop.replace('$f4', str(frame_num).zfill(4))
    prop = prop.replace('$F4', str(frame_num).zfill(4))
    prop = prop.replace('$f3', str(frame_num).zfill(3))
    prop = prop.replace('$f3', str(frame_num).zfill(3))
    return prop


# return the output file name if this texture is to be txmade.
def get_tex_file_name(prop):
    prop = replace_frame_num(prop)
    prop = prop.replace('\\', '\/')
    if prop != '' and prop.rsplit('.', 1) != 'tex':
        return os.path.basename(prop).rsplit('.', 1)[0] + '.tex'
    else:
        return prop


def get_textures(id):
    textures = []
    if id is None or not id.node_tree:
        return textures

    nt = id.node_tree
    for node in nt.nodes:
        textures.extend(get_textures_for_node(node, id.name))

    return textures


def get_textures_for_node(node, matName=""):
    textures = []
    if hasattr(node, 'bl_idname'):
        if node.bl_idname == "PxrPtexturePatternNode":
            return textures
        elif node.bl_idname == "PxrOSLPatternNode":
            for input_name, input in node.inputs.items():
                if hasattr(input, 'is_texture') and input.is_texture:
                    prop = input.default_value
                    out_file_name = get_tex_file_name(prop)
                    textures.append((replace_frame_num(prop), out_file_name,
                                     ['-smode', 'periodic', '-tmode',
                                      'periodic']))
            return textures
        elif node.bl_idname == 'ShaderNodeGroup':
            nt = node.node_tree
            for node in nt.nodes:
                textures.extend(get_textures_for_node(node, matName=""))
            return textures

    if hasattr(node, 'prop_meta'):
        for prop_name, meta in node.prop_meta.items():
            if prop_name in txmake_options.index:
                pass
            elif hasattr(node, prop_name):
                prop = getattr(node, prop_name)

                if meta['renderman_type'] == 'page':
                    continue

                # else return a tuple of in name/outname
                else:
                    if ('options' in meta and
                        meta['options'] == 'texture') or \
                        (node.renderman_node_type == 'light' and
                         'widget' in meta and
                         meta['widget'] == 'assetIdInput' and
                         prop_name != 'iesProfile'):

                        out_file_name = get_tex_file_name(prop)
                        # if they don't match add this to the list
                        if out_file_name != prop:
                            if node.renderman_node_type == 'light' and \
                                    "Dome" in node.bl_label:
                                # no options for now
                                textures.append(
                                    (replace_frame_num(prop), out_file_name, ['-envlatl']))
                            else:
                                # Test and see if options like smode are on
                                # this node.
                                if hasattr(node, "smode"):
                                    optionsList = []
                                    for option in txmake_options.index:
                                        partsOfOption = getattr(
                                            txmake_options, option)
                                        if partsOfOption["exportType"] == "name":
                                            optionsList.append("-" + option)
                                            # Float values need converting
                                            # before they are passed to command
                                            # line
                                            if partsOfOption["type"] == "float":
                                                optionsList.append(
                                                    str(getattr(node, option)))
                                            else:
                                                optionsList.append(
                                                    getattr(node, option))
                                        else:
                                            # Float values need converting
                                            # before they are passed to command
                                            # line
                                            if partsOfOption["type"] == "float":
                                                optionsList.append(
                                                    str(getattr(node, option)))
                                            else:
                                                optionsList.append(
                                                    "-" + getattr(node, option))
                                    textures.append(
                                        (replace_frame_num(prop), out_file_name, optionsList))
                                else:
                                    # no options found add the bare minimum
                                    # options for smooth export.
                                    textures.append((replace_frame_num(prop), out_file_name,
                                                     ['-smode', 'periodic',
                                                      '-tmode', 'periodic']))
    return textures


class PropertyLookup():

    _single = [
        #
        # Skip drawing of 'page'!
        #
        # These properties are leaved alone on a page (group), because all
        # other properties are consumed by in- or outports. Their 'bl_label'
        # attribut will be used as label.
        #
        "PxrBumpPatternNodeAdvanced",
        "PxrProjectorPatternNode2D Parameters",
        "PxrProjectorPatternNodeAdvanced",
        "PxrDispScalarLayerPatternNodeBase Layer",
        "PxrLayerSurfaceBxdfNodeFuzz",
        "PxrLayerSurfaceBxdfNodeScattering Globals",
        # "PxrLayerSurfaceBxdfNodeDiffuse",
        "aaOceanPrmanShaderPatternNodeCustom UV Parameters",
        "PxrVolumeBxdfNodeDensity",
        "PxrLayeredTexturePatternNodeColor Correct",
        "PxrDispVectorLayerPatternNodeBase Layer",
        "PxrLayerMixerPatternNodeLayer 1",
        "PxrLayerMixerPatternNodeLayer 2",
        "PxrLayerMixerPatternNodeLayer 3",
        "PxrLayerMixerPatternNodeLayer 4",
        "PxrDispVectorLayerPatternNodeBase Layer",
        "PxrRemapPatternNodeInput Range",
        "PxrRemapPatternNodeOutput Range"]

    _unlabeled = [
        #
        # Singles as before but their labels should not be drawn as of
        # cosmetical, due to self explanatory or other maybe unlogical reasons.
        #
        "PxrVolumeBxdfNodeMultiScatter Optimization"]

    _labeled = [
        #
        # Singles as before, but their labels ar not taken from 'bl-label',
        # they would be defined at runtime in the code (should we refactor this?).
        #
        "PxrMarschnerHairBxdfNodeDiffuse",
        "PxrColorCorrectPatternNodeClamp Output",
        "PxrMatteIDPatternNodeParameters"]

    _emptypage = [
        #
        # These property groups are empty because ALL properties
        # are consumed by in- or ouput ports of the nodeleaving the page empty,
        # so a 'page' should not be drawn.
        #
        "PxrBumpPatternNodePattern",
        "PxrMarschnerHairBxdfNodeGlow",
        "PxrLayerSurfaceBxdfNodeGlow",
        "PxrVolumeBxdfNodeAnisotropy",
        "PxrFractalizePatternNodeAdvanced",
        "PxrDirtPatternNodeDirt Color",
        "PxrBakeTexturePatternNodeInput",
        "PxrBakePointCloudPatternNodeInput",
        "PxrGeometricAOVsPatternNodeParameters",
        "PxrHairColorPatternNodeHair Color",
        "PxrHairColorPatternNodeStray Hair Color",
        "PxrHairColorPatternNodeDye Color",
        "PxrColorCorrectPatternNodeInput Range",
        "PxrColorCorrectPatternNodeOutput Range",
        "PxrColorCorrectPatternNodeColor Correct",
        "PxrRemapPatternNodeRemap"]

    _cycles_node_map = {
        'ShaderNodeAttribute': 'node_attribute',
        'ShaderNodeBlackbody': 'node_checker_blackbody',
        'ShaderNodeTexBrick': 'node_brick_texture',
        'ShaderNodeBrightContrast': 'node_brightness',
        'ShaderNodeTexChecker': 'node_checker_texture',
        'ShaderNodeBump': 'node_bump',
        'ShaderNodeCameraData': 'node_camera',
        'ShaderNodeTexChecker': 'node_checker_texture',
        'ShaderNodeCombineHSV': 'node_combine_hsv',
        'ShaderNodeCombineRGB': 'node_combine_rgb',
        'ShaderNodeCombineXYZ': 'node_combine_xyz',
        'ShaderNodeTexEnvironment': 'node_environment_texture',
        'ShaderNodeFresnel': 'node_fresnel',
        'ShaderNodeGamma': 'node_gamma',
        'ShaderNodeNewGeometry': 'node_geometry',
        'ShaderNodeTexGradient': 'node_gradient_texture',
        'ShaderNodeHairInfo': 'node_hair_info',
        'ShaderNodeInvert': 'node_invert',
        'ShaderNodeHueSaturation': 'node_hsv',
        'ShaderNodeTexImage': 'node_image_texture',
        'ShaderNodeHueSaturation': 'node_hsv',
        'ShaderNodeLayerWeight': 'node_layer_weight',
        'ShaderNodeLightFalloff': 'node_light_falloff',
        'ShaderNodeLightPath': 'node_light_path',
        'ShaderNodeTexMagic': 'node_magic_texture',
        'ShaderNodeMapping': 'node_mapping',
        'ShaderNodeMath': 'node_math',
        'ShaderNodeMixRGB': 'node_mix',
        'ShaderNodeTexMusgrave': 'node_musgrave_texture',
        'ShaderNodeTexNoise': 'node_noise_texture',
        'ShaderNodeNormal': 'node_normal',
        'ShaderNodeNormalMap': 'node_normal_map',
        'ShaderNodeObjectInfo': 'node_object_info',
        'ShaderNodeParticleInfo': 'node_particle_info',
        'ShaderNodeRGBCurve': 'node_rgb_curves',
        'ShaderNodeValToRGB': 'node_rgb_ramp',
        'ShaderNodeSeparateHSV': 'node_separate_hsv',
        'ShaderNodeSeparateRGB': 'node_separate_rgb',
        'ShaderNodeSeparateXYZ': 'node_separate_xyz',
        'ShaderNodeTexSky': 'node_sky_texture',
        'ShaderNodeTangent': 'node_tangent',
        'ShaderNodeTexCoord': 'node_texture_coordinate',
        'ShaderNodeUVMap': 'node_uv_map',
        'ShaderNodeValue': 'node_value',
        'ShaderNodeVectorCurves': 'node_vector_curves',
        'ShaderNodeVectorMath': 'node_vector_math',
        'ShaderNodeVectorTransform': 'node_vector_transform',
        'ShaderNodeTexVoronoi': 'node_voronoi_texture',
        'ShaderNodeTexWave': 'node_wave_texture',
        'ShaderNodeWavelength': 'node_wavelength',
        'ShaderNodeWireframe': 'node_wireframe', }

    _enable_gain = {
        'diffuseGain': 'enableDiffuse',
        'specularFaceColor': 'enablePrimarySpecular',
        'specularEdgeColor': 'enablePrimarySpecular',
        'roughSpecularFaceColor': 'enableRoughSpecular',
        'roughSpecularEdgeColor': 'enableRoughSpecular',
        'clearcoatFaceColor': 'enableClearCoat',
        'clearcoatEdgeColor': 'enableClearCoat',
        'iridescenceFaceGain': 'enableIridescence',
        'iridescenceEdgeGain': 'enableIridescence',
        'fuzzGain': 'enableFuzz',
        'subsurfaceGain': 'enableSubsurface',
        'singlescatterGain': 'enableSingleScatter',
        'singlescatterDirectGain': 'enableSingleScatter',
        'refractionGain': 'enableGlass',
        'reflectionGain': 'enableGlass',
        'glowGain': 'enableGlow', }

    # _group_nodes = [
    #     'ShaderNodeGroup',
    #     'NodeGroupInput',
    #     'NodeGroupOutput']

    @classmethod
    def is_single(cls, ident):
        return ident in cls._single

    @classmethod
    def is_labeled(cls, ident):
        return ident in cls._labeled

    @classmethod
    def is_unlabeled(cls, ident):
        return ident in cls._unlabeled

    @classmethod
    def is_emptypage(cls, ident):
        return ident in cls._emptypage

    # @classmethod
    # def is_groupnode(cls, ident):
    #     return ident in cls._group_nodes

    @classmethod
    def enable_gain(cls, ident):
        return ident in cls._enable_gain.keys()

    @classmethod
    def map_cycles(cls, ident):
        return cls._cycles_node_map[ident]

    @classmethod
    def do_map_cycles(cls, ident):
        return ident in cls._cycles_node_map.keys()

    @classmethod
    def map_gain(cls, ident):
        return cls._enable_gain[ident]
