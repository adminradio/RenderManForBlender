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


import os.path
import shutil
# import tempfile
import xml.etree.ElementTree as ET
from operator import attrgetter

# import _cycles

import bpy.props
from bpy.props import *

import nodeitems_utils
from nodeitems_utils import NodeCategory
from nodeitems_utils import NodeItem

from . cycles_convert import *

from . shader_parameters import class_generate_properties
from . shader_parameters import node_add_inputs
from . shader_parameters import node_add_outputs
# from . shader_parameters import socket_map
from . shader_parameters import txmake_options
from . shader_parameters import update_conditional_visops

from . utils import args_files_in_path
# from . utils import debug
# from . utils import readOSO
from . utils import rib
from . utils import user_path


# from . gui import icons

# from . ops import RfB_OT_NODE_RefreshOSL

from . nds.util import PropertyLookup

# from . nds import socket_node_input

from . nds.RM_AddNodeBase import RM_AddNodeBase
from . nds.RM_ShaderSocket import RM_ShaderSocket
from . nds.RM_NodeSocketInt import RM_NodeSocketInt
from . nds.RM_NodeSocketFloat import RM_NodeSocketFloat
from . nds.RM_NodeSocketColor import RM_NodeSocketColor
from . nds.RM_NodeSocketString import RM_NodeSocketString
from . nds.RM_NodeSocketStruct import RM_NodeSocketStruct
from . nds.RM_NodeSocketVector import RM_NodeSocketVector

from . nds.RM_ShaderNodeBase import RM_ShaderNodeBase
from . nds.RendermanOutputNode import RendermanOutputNode
# from . nds.RendermanBxdfNode import RendermanBxdfNode
# from . nds.RendermanDisplacementNode import RendermanDisplacementNode
# from . nds.RendermanPatternNode import RendermanPatternNode
# from . nds.RendermanLightNode import RendermanLightNode

# from . nds.NODE_OT_AddBxdf import NODE_OT_AddBxdf

from . nds.util import find_node
from . nds.util import is_renderman
from . nds.util import get_tex_file_name


# Final output node, used as a dummy to find top level shaders
class RendermanBxdfNode(RM_ShaderNodeBase):
    bl_label = 'Bxdf'
    renderman_node_type = 'bxdf'
    shading_compatibility = {'NEW_SHADING'}


class RendermanDisplacementNode(RM_ShaderNodeBase):
    bl_label = 'Displacement'
    renderman_node_type = 'displacement'


# Final output node, used as a dummy to find top level shaders
class RendermanPatternNode(RM_ShaderNodeBase):
    bl_label = 'Texture'
    renderman_node_type = 'pattern'
    bl_type = 'TEX_IMAGE'
    bl_static_type = 'TEX_IMAGE'


class RendermanLightNode(RM_ShaderNodeBase):
    bl_label = 'Output'
    renderman_node_type = 'light'


def generate_node_type(prefs, name, args):
    """Generate a node type dynamically from pattern."""

    nodetype = args.find("shaderType/tag").attrib['value']
    typename = '%s%sNode' % (name, nodetype.capitalize())
    nodedict = {'bxdf': RendermanBxdfNode,
                'pattern': RendermanPatternNode,
                'displacement': RendermanDisplacementNode,
                'light': RendermanLightNode}
    if nodetype not in nodedict.keys():
        return

    ntype = type(typename, (nodedict[nodetype],), {})
    ntype.bl_label = name
    ntype.typename = typename

    # Todo: Check if we could remove "empty pages" from array!
    #       With simple lookup list? (2917-12-28)
    #
    inputs = [p for p in args.findall('./param')] + \
             [p for p in args.findall('./page')]

    outputs = [p for p in args.findall('.//output')]

    def init(self, context):
        if self.renderman_node_type == 'bxdf':
            self.outputs.new('RendermanShaderSocket', "Bxdf").type = 'SHADER'
            # socket_template = self.socket_templates.new(identifier='Bxdf', name='Bxdf', type='SHADER')
            node_add_inputs(self, name, self.prop_names)
            node_add_outputs(self)
            # if this is PxrLayerSurface set the diffusegain to 0.  The default
            # of 1 is unintuitive
            if self.plugin_name == 'PxrLayerSurface':
                self.diffuseGain = 0
        elif self.renderman_node_type == 'light':
            # only make a few sockets connectable
            node_add_inputs(self, name, self.prop_names)
            self.outputs.new('RendermanShaderSocket', "Light")
        elif self.renderman_node_type == 'displacement':
            # only make the color connectable
            self.outputs.new('RendermanShaderSocket', "Displacement")
            node_add_inputs(self, name, self.prop_names)
        # else pattern
        elif name == "PxrOSL":
            self.outputs.clear()
        else:
            node_add_inputs(self, name, self.prop_names)
            node_add_outputs(self)

        if name == "PxrRamp":
            node_group = bpy.data.node_groups.new(
                'PxrRamp_nodegroup', 'ShaderNodeTree')
            node_group.nodes.new('ShaderNodeValToRGB')
            node_group.use_fake_user = True
            self.node_group = node_group.name
        update_conditional_visops(self)

    def free(self):
        if name == "PxrRamp":
            bpy.data.node_groups.remove(bpy.data.node_groups[self.node_group])

    ntype.init = init
    ntype.free = free

    if name == 'PxrRamp':
        ntype.node_group = StringProperty('color_ramp', default='')

    ntype.plugin_name = StringProperty(name='Plugin Name',
                                       default=name, options={'HIDDEN'})
    # Todo: recheck (2017-12-28)
    # lights cant connect to a node tree in 20.0
    class_generate_properties(ntype, name, inputs + outputs)
    if nodetype == 'light':
        ntype.light_shading_rate = FloatProperty(
            name="Light Shading Rate",
            description="Shading Rate for this light.  \
                Leave this high unless detail is missing",
            default=100.0)
        ntype.light_primary_visibility = BoolProperty(
            name="Light Primary Visibility",
            description="Camera visibility for this light",
            default=True)

    bpy.utils.register_class(ntype)

    return typename, ntype


class NODE_OT_add_bxdf(bpy.types.Operator, RM_AddNodeBase):
    """
    For generating cycles-style ui menus to add new bxdfs,
    connected to a given input socket.
    """
    bl_idname = 'node.add_bxdf'
    bl_label = 'Add Bxdf Node'
    bl_description = 'Connect a Bxdf to this socket'
    input_type = StringProperty(default='Bxdf')


class NODE_OT_add_displacement(bpy.types.Operator, RM_AddNodeBase):
    """
    For generating cycles-style ui menus to add new nodes,
    connected to a given input socket.
    """
    bl_idname = 'node.add_displacement'
    bl_label = 'Add Displacement Node'
    bl_description = 'Connect a Displacement shader to this socket'
    input_type = StringProperty(default='Displacement')


class NODE_OT_add_light(bpy.types.Operator, RM_AddNodeBase):
    """
    For generating cycles-style ui menus to add new nodes,
    connected to a given input socket.
    """
    bl_idname = 'node.add_light'
    bl_label = 'Add Light Node'
    bl_description = 'Connect a Light shader to this socket'
    input_type = StringProperty(default='Light')


class NODE_OT_add_pattern(bpy.types.Operator, RM_AddNodeBase):
    """
    For generating cycles-style ui menus to add new nodes,
    connected to a given input socket.
    """
    bl_idname = 'node.add_pattern'
    bl_label = 'Add Pattern Node'
    bl_description = 'Connect a Pattern to this socket'
    input_type = StringProperty(default='Pattern')


class NODE_OT_add_layer(bpy.types.Operator, RM_AddNodeBase):
    """
    For generating cycles-style ui menus to add new nodes,
    connected to a given input socket.
    """
    bl_idname = 'node.add_layer'
    bl_label = 'Add Layer Node'
    bl_description = 'Connect a PxrLayer'
    input_type = StringProperty(default='Layer')


class NODE_OT_add_manifold(bpy.types.Operator, RM_AddNodeBase):
    """
    For generating cycles-style ui menus to add new nodes,
    connected to a given input socket.
    """
    bl_idname = 'node.add_manifold'
    bl_label = 'Add Manifold Node'
    bl_description = 'Connect a Manifold'
    input_type = StringProperty(default='Manifold')


class NODE_OT_add_bump(bpy.types.Operator, RM_AddNodeBase):
    """
    For generating cycles-style ui menus to add new nodes,
    connected to a given input socket.
    """
    bl_idname = 'node.add_bump'
    bl_label = 'Add Bump Node'
    bl_description = 'Connect a bump node'
    input_type = StringProperty(default='Bump')


# return if this param has a vstruct connection or linked independently
def is_vstruct_or_linked(node, param):
    meta = node.prop_meta[param]

    if 'vstructmember' not in meta.keys():
        return node.inputs[param].is_linked
    elif param in node.inputs and node.inputs[param].is_linked:
        return True
    else:
        vstruct_name, vstruct_member = meta['vstructmember'].split('.')
        if node.inputs[vstruct_name].is_linked:
            from_socket = node.inputs[vstruct_name].links[0].from_socket
            vstruct_from_param = "%s_%s" % (
                from_socket.identifier, vstruct_member)
            return vstruct_conditional(from_socket.node, vstruct_from_param)
        else:
            return False


# tells if this param has a vstruct connection that is linked and
# conditional met
def is_vstruct_and_linked(node, param):
    meta = node.prop_meta[param]

    if 'vstructmember' not in meta.keys():
        return False
    else:
        vstruct_name, vstruct_member = meta['vstructmember'].split('.')
        if node.inputs[vstruct_name].is_linked:
            from_socket = node.inputs[vstruct_name].links[0].from_socket
            # if coming from a shader group hookup across that
            if from_socket.node.bl_idname == 'ShaderNodeGroup':
                ng = from_socket.node.node_tree
                group_output = next((n for n in ng.nodes if n.bl_idname == 'NodeGroupOutput'),
                                    None)
                if group_output is None:
                    return False

                in_sock = group_output.inputs[from_socket.name]
                if len(in_sock.links):
                    from_socket = in_sock.links[0].from_socket
            vstruct_from_param = "%s_%s" % (
                from_socket.identifier, vstruct_member)
            return vstruct_conditional(from_socket.node, vstruct_from_param)
        else:
            return False


# gets the value for a node walking up the vstruct chain
def get_val_vstruct(node, param):
    if param in node.inputs and node.inputs[param].is_linked:
        from_socket = node.inputs[param].links[0].from_socket
        return get_val_vstruct(from_socket.node, from_socket.identifier)
    elif is_vstruct_and_linked(node, param):
        return True
    else:
        return getattr(node, param)


# parse a vstruct conditional string and return true or false if should link
def vstruct_conditional(node, param):
    if not hasattr(node, 'shader_meta') and not hasattr(node, 'output_meta'):
        return False
    meta = getattr(
        node, 'shader_meta') if node.bl_idname == "PxrOSLPatternNode" else node.output_meta
    if param not in meta:
        return False
    meta = meta[param]
    if 'vstructConditionalExpr' not in meta.keys():
        return True

    expr = meta['vstructConditionalExpr']
    expr = expr.replace('connect if ', '')
    set_zero = False
    if ' else set 0' in expr:
        expr = expr.replace(' else set 0', '')
        set_zero = True

    tokens = expr.split()
    new_tokens = []
    i = 0
    num_tokens = len(tokens)
    while i < num_tokens:
        token = tokens[i]
        prepend, append = '', ''
        while token[0] == '(':
            token = token[1:]
            prepend += '('
        while token[-1] == ')':
            token = token[:-1]
            append += ')'

        if token == 'set':
            i += 1
            continue

        # is connected change this to node.inputs.is_linked
        if i < num_tokens - 2 and tokens[i + 1] == 'is' \
                and 'connected' in tokens[i + 2]:
            token = "is_vstruct_or_linked(node, '%s')" % token
            last_token = tokens[i + 2]
            while last_token[-1] == ')':
                last_token = last_token[:-1]
                append += ')'
            i += 3
        else:
            i += 1
        if hasattr(node, token):
            token = "get_val_vstruct(node, '%s')" % token

        new_tokens.append(prepend + token + append)

    if 'if' in new_tokens and 'else' not in new_tokens:
        new_tokens.extend(['else', 'False'])
    return eval(" ".join(new_tokens))


def gen_params(ri, node, mat_name=None):
    """Generate parameter list."""
    params = {}
    # If node is OSL node get properties from dynamic location.
    if node.bl_idname == "PxrOSLPatternNode":

        if getattr(node, "codetypeswitch") == "EXT":
            prefs = bpy.context.user_preferences.addons[__package__].preferences
            osl_path = user_path(getattr(node, 'shadercode'))
            FileName = os.path.basename(osl_path)
            FileNameNoEXT, ext = os.path.splitext(FileName)
            out_file = os.path.join(
                user_path(prefs.env_vars.out), "shaders", FileName)
            if ext == ".oso":
                if (not os.path.exists(out_file)
                    or not os.path.samefile(osl_path, out_file)):
                    if not os.path.exists(os.path.join(user_path(prefs.env_vars.out), "shaders")):
                        os.mkdir(os.path.join(user_path(prefs.env_vars.out), "shaders"))
                    shutil.copy(osl_path, out_file)

        for input_name, input in node.inputs.items():
            prop_type = input.renderman_type

            if input.is_linked:
                to_socket = input
                from_socket = input.links[0].from_socket
                params['reference %s %s' % (prop_type, input_name)] = \
                    [get_output_param_str(
                        from_socket.node, mat_name, from_socket, to_socket)]

            elif type(input) != RendermanNodeSocketStruct:
                params['%s %s' % (prop_type, input_name)] = \
                    rib(input.default_value,
                        type_hint=prop_type)

    # Special case for SeExpr Nodes. Assume that the code will be in a file so
    # that needs to be extracted.
    elif node.bl_idname == "PxrSeExprPatternNode":
        fileInputType = node.codetypeswitch

        for prop_name, meta in node.prop_meta.items():
            if prop_name in ["codetypeswitch", 'filename']:
                pass
            elif prop_name == "internalSearch" and fileInputType == 'INT':
                if node.internalSearch != "":
                    script = bpy.data.texts[node.internalSearch]
                    params['%s %s' % ("string",
                                      "expression")] = \
                        rib(script.as_string(),
                            type_hint=meta['renderman_type'])
            elif prop_name == "shadercode" and fileInputType == "NODE":
                params['%s %s' % ("string", "expression")] = node.expression
            else:
                prop = getattr(node, prop_name)
                # if input socket is linked reference that
                if prop_name in node.inputs and \
                        node.inputs[prop_name].is_linked:
                    to_socket = node.inputs[prop_name]
                    from_socket = to_socket.links[0].from_socket
                    params['reference %s %s' % (meta['renderman_type'],
                                                meta['renderman_name'])] = \
                        [get_output_param_str(
                            from_socket.node, mat_name, from_socket, to_socket)]
                # else output rib
                else:
                    params['%s %s' % (meta['renderman_type'],
                                      meta['renderman_name'])] = \
                        rib(prop, type_hint=meta['renderman_type'])

    else:

        for prop_name, meta in node.prop_meta.items():
            if prop_name in txmake_options.index:
                pass
            elif node.plugin_name == 'PxrRamp' and prop_name in ['colors', 'positions']:
                pass

            elif (prop_name in ['sblur', 'tblur', 'notes']):
                pass

            else:
                prop = getattr(node, prop_name)
                # if property group recurse
                if meta['renderman_type'] == 'page':
                    continue
                elif prop_name == 'inputMaterial' or \
                        ('type' in meta and meta['type'] == 'vstruct'):
                    continue

                # if input socket is linked reference that
                elif hasattr(node, 'inputs') and prop_name in node.inputs and \
                        node.inputs[prop_name].is_linked:

                    to_socket = node.inputs[prop_name]
                    from_socket = to_socket.links[0].from_socket
                    from_node = to_socket.links[0].from_node
                    if 'arraySize' in meta:
                        params['reference %s[1] %s' % (meta['renderman_type'],
                                                       meta['renderman_name'])] \
                            = [get_output_param_str(
                            from_node, mat_name, from_socket, to_socket)]
                    else:
                        params['reference %s %s' % (meta['renderman_type'],
                                                    meta['renderman_name'])] = \
                            [get_output_param_str(
                                from_node, mat_name, from_socket, to_socket)]

                # see if vstruct linked
                elif is_vstruct_and_linked(node, prop_name):
                    vstruct_name, vstruct_member = meta[
                        'vstructmember'].split('.')
                    from_socket = node.inputs[
                        vstruct_name].links[0].from_socket

                    temp_mat_name = mat_name

                    if from_socket.node.bl_idname == 'ShaderNodeGroup':
                        ng = from_socket.node.node_tree
                        group_output = next((n for n in ng.nodes if n.bl_idname == 'NodeGroupOutput'),
                                            None)
                        if group_output is None:
                            return False

                        in_sock = group_output.inputs[from_socket.name]
                        if len(in_sock.links):
                            from_socket = in_sock.links[0].from_socket
                            temp_mat_name = mat_name + '.' + from_socket.node.name

                    vstruct_from_param = "%s_%s" % (
                        from_socket.identifier, vstruct_member)
                    if vstruct_from_param in from_socket.node.output_meta:
                        actual_socket = from_socket.node.output_meta[
                            vstruct_from_param]
                        params['reference %s %s' % (meta['renderman_type'],
                                                    meta['renderman_name'])] = \
                            [get_output_param_str(
                                from_socket.node, temp_mat_name, actual_socket)]
                    else:
                        print('Warning! %s not found on %s' %
                              (vstruct_from_param, from_socket.node.name))

                # else output rib
                else:
                    # if struct is not linked continue
                    if meta['renderman_type'] in ['struct', 'enum']:
                        continue

                    # if this is a gain on PxrSurface and the lobe isn't
                    # enabled
                    if (node.bl_idname == 'PxrSurfaceBxdfNode'
                        and PropertyLookup.enable_gain(prop_name)
                        and not getattr(node, PropertyLookup.map_gain(prop_name))):

                        val = (
                            [0, 0, 0]
                            if meta['renderman_type'] == 'color'
                            else 0
                        )

                        params['%s %s' % (meta['renderman_type'],
                                          meta['renderman_name'])] = val

                    elif ('options' in meta
                        and meta['options'] == 'texture'
                        and node.bl_idname != "PxrPtexturePatternNode"
                        or ('widget' in meta
                            and meta['widget'] == 'assetIdInput'
                            and prop_name != 'iesProfile')):

                        params['%s %s' % (
                            meta['renderman_type'],
                            meta['renderman_name'])] = rib(
                                get_tex_file_name(prop),
                                type_hint=meta['renderman_type'])

                    elif 'arraySize' in meta:
                        if type(prop) == int:
                            prop = [prop]
                        params['%s[%d] %s' % (
                            meta['renderman_type'],
                            len(prop),
                            meta['renderman_name'])] = rib(prop)
                    else:
                        params['%s %s' % (
                            meta['renderman_type'],
                            meta['renderman_name'])] = rib(
                                prop,
                                type_hint=meta['renderman_type'])

    if node.plugin_name == 'PxrRamp':
        nt = bpy.data.node_groups[node.node_group]
        if nt:
            dummy_ramp = nt.nodes['ColorRamp']
            colors = []
            positions = []
            # double the start and end points
            positions.append(float(dummy_ramp.color_ramp.elements[0].position))
            colors.extend(dummy_ramp.color_ramp.elements[0].color[:3])
            for e in dummy_ramp.color_ramp.elements:
                positions.append(float(e.position))
                colors.extend(e.color[:3])
            positions.append(
                float(dummy_ramp.color_ramp.elements[-1].position))
            colors.extend(dummy_ramp.color_ramp.elements[-1].color[:3])
            params['color[%d] colors' % len(positions)] = colors
            params['float[%d] positions' % len(positions)] = positions

    return params


def create_rman_surface(nt, parent_node, input_index, node_type="PxrSurfaceBxdfNode"):
    layer = nt.nodes.new(node_type)
    nt.links.new(layer.outputs[0], parent_node.inputs[input_index])
    setattr(layer, 'enableDiffuse', False)

    layer.location = parent_node.location
    layer.diffuseGain = 0
    layer.location[0] -= 300
    return layer


combine_nodes = ['ShaderNodeAddShader', 'ShaderNodeMixShader']


# rman_parent could be PxrSurface or PxrMixer
def convert_cycles_bsdf(nt, rman_parent, node, input_index):
    # if mix or add pass both to parent
    if node.bl_idname in combine_nodes:
        i = 0 if node.bl_idname == 'ShaderNodeAddShader' else 1

        node1 = node.inputs[
            0 + i].links[0].from_node if node.inputs[0 + i].is_linked else None
        node2 = node.inputs[
            1 + i].links[0].from_node if node.inputs[1 + i].is_linked else None

        if not node1 and not node2:
            return
        elif not node1:
            convert_cycles_bsdf(nt, rman_parent, node2, input_index)
        elif not node2:
            convert_cycles_bsdf(nt, rman_parent, node1, input_index)

        # if ones a combiner or they're of the same type and not glossy we need
        # to make a mixer
        elif node.bl_idname == 'ShaderNodeMixShader' or node1.bl_idname in combine_nodes \
                or node2.bl_idname in combine_nodes or \
                node1.bl_idname == 'ShaderNodeGroup' or node2.bl_idname == 'ShaderNodeGroup' \
                or (bsdf_map[node1.bl_idname][0] == bsdf_map[node2.bl_idname][0]):
            mixer = nt.nodes.new('PxrLayerMixerPatternNode')
            # if parent is output make a pxr surface first
            nt.links.new(mixer.outputs["pxrMaterialOut"],
                         rman_parent.inputs[input_index])
            offset_node_location(rman_parent, mixer, node)

            # set the layer masks
            if node.bl_idname == 'ShaderNodeAddShader':
                mixer.layer1Mask = .5
            else:
                convert_cycles_input(
                    nt, node.inputs['Fac'], mixer, 'layer1Mask')

            # make a new node for each
            convert_cycles_bsdf(nt, mixer, node1, 0)
            convert_cycles_bsdf(nt, mixer, node2, 1)

        # this is a heterogenous mix of add
        else:
            if rman_parent.plugin_name == 'PxrLayerMixer':
                old_parent = rman_parent
                rman_parent = create_rman_surface(nt, rman_parent, input_index,
                                                  'PxrLayerPatternNode')
                offset_node_location(old_parent, rman_parent, node)
            convert_cycles_bsdf(nt, rman_parent, node1, 0)
            convert_cycles_bsdf(nt, rman_parent, node2, 1)

    # else set lobe on parent
    elif 'Bsdf' in node.bl_idname or node.bl_idname == 'ShaderNodeSubsurfaceScattering':
        if rman_parent.plugin_name == 'PxrLayerMixer':
            old_parent = rman_parent
            rman_parent = create_rman_surface(nt, rman_parent, input_index,
                                              'PxrLayerPatternNode')
            offset_node_location(old_parent, rman_parent, node)

        node_type = node.bl_idname
        bsdf_map[node_type][1](nt, node, rman_parent)
    # if we find an emission node, naively make it a meshlight
    # note this will only make the last emission node the light
    elif node.bl_idname == 'ShaderNodeEmission':
        output = next((n for n in nt.nodes if hasattr(n, 'renderman_node_type') and
                       n.renderman_node_type == 'output'),
                      None)
        meshlight = nt.nodes.new("PxrMeshLightLightNode")
        nt.links.new(meshlight.outputs[0], output.inputs["Light"])
        meshlight.location = output.location
        meshlight.location[0] -= 300
        convert_cycles_input(
            nt, node.inputs['Strength'], meshlight, "intensity")
        if node.inputs['Color'].is_linked:
            convert_cycles_input(
                nt, node.inputs['Color'], meshlight, "textureColor")
        else:
            setattr(meshlight, 'lightColor',
                    node.inputs['Color'].default_value[:3])

    else:
        rman_node = convert_cycles_node(nt, node)
        nt.links.new(rman_node.outputs[0], rman_parent.inputs[input_index])


def convert_cycles_displacement(nt, surface_node, displace_socket):
    # for now just do bump
    if displace_socket.is_linked:
        bump = nt.nodes.new("PxrBumpPatternNode")
        nt.links.new(bump.outputs[0], surface_node.inputs['bumpNormal'])
        bump.location = surface_node.location
        bump.location[0] -= 200
        bump.location[1] -= 100

        convert_cycles_input(nt, displace_socket, bump, "inputBump")

    # return
    # if displace_socket.is_linked:
    #    displace = nt.nodes.new("PxrDisplaceDisplacementNode")
    #    nt.links.new(displace.outputs[0], output_node.inputs['Displacement'])
    #    displace.location = output_node.location
    #    displace.location[0] -= 200
    #    displace.location[1] -= 100

    #    setattr(displace, 'dispAmount', .01)
    #    convert_cycles_input(nt, displace_socket, displace, "dispScalar")


# could make this more robust to shift the entire nodetree to below the
# bounds of the cycles nodetree
def set_ouput_node_location(nt, output_node, cycles_output):
    output_node.location = cycles_output.location
    output_node.location[1] -= 500


def offset_node_location(rman_parent, rman_node, cycles_node):
    linked_socket = next((sock for sock in cycles_node.outputs if sock.is_linked),
                         None)
    rman_node.location = rman_parent.location
    if linked_socket:
        rman_node.location += (cycles_node.location -
                               linked_socket.links[0].to_node.location)


def convert_cycles_nodetree(id, output_node, reporter):
    # find base node
    from . import cycles_convert
    cycles_convert.converted_nodes = {}
    nt = id.node_tree
    reporter({'INFO'}, 'Converting material ' + id.name + ' to RenderMan')
    cycles_output_node = find_node(id, 'ShaderNodeOutputMaterial')
    if not cycles_output_node:
        reporter({'WARNING'}, 'No Cycles output found ' + id.name)
        return False

    # if no bsdf return false
    if not cycles_output_node.inputs[0].is_linked:
        reporter({'WARNING'}, 'No Cycles bsdf found ' + id.name)
        return False

    # set the output node location
    set_ouput_node_location(nt, output_node, cycles_output_node)

    # walk tree
    cycles_convert.report = reporter
    begin_cycles_node = cycles_output_node.inputs[0].links[0].from_node
    # if this is an emission use PxrLightEmission
    if begin_cycles_node.bl_idname == "ShaderNodeEmission":
        meshlight = nt.nodes.new("PxrMeshLightLightNode")
        nt.links.new(meshlight.outputs[0], output_node.inputs["Light"])
        offset_node_location(output_node, meshlight, begin_cycles_node)
        convert_cycles_input(nt, begin_cycles_node.inputs[
            'Strength'], meshlight, "intensity")
        if begin_cycles_node.inputs['Color'].is_linked:
            convert_cycles_input(nt, begin_cycles_node.inputs[
                'Color'], meshlight, "textureColor")
        else:
            setattr(meshlight, 'lightColor', begin_cycles_node.inputs[
                                                 'Color'].default_value[:3])
        bxdf = nt.nodes.new('PxrBlackBxdfNode')
        nt.links.new(bxdf.outputs[0], output_node.inputs["Bxdf"])
    else:
        base_surface = create_rman_surface(nt, output_node, 0)
        offset_node_location(output_node, base_surface, begin_cycles_node)
        convert_cycles_bsdf(nt, base_surface, begin_cycles_node, 0)
        convert_cycles_displacement(
            nt, base_surface, cycles_output_node.inputs[2])
    return True


def get_mat_name(mat_name):
    return mat_name.replace(' ', '')


def get_node_name(node, mat_name):
    return "%s.%s" % (mat_name, node.name.replace(' ', ''))


def get_socket_name(node, socket):
    if type(socket) == dict:
        return socket['name'].replace(' ', '')
    # if this is a renderman node we can just use the socket name,
    else:
        if not hasattr('node', 'plugin_name'):
            if socket.name in node.inputs and socket.name in node.outputs:
                suffix = 'Out' if socket.is_output else 'In'
                return socket.name.replace(' ', '') + suffix
        return socket.identifier.replace(' ', '')


def get_socket_type(node, socket):
    sock_type = socket.type.lower()
    if sock_type == 'rgba':
        return 'color'
    elif sock_type == 'value':
        return 'float'
    elif sock_type == 'vector':
        return 'point'
    else:
        return sock_type


# do we need to convert this socket?
def do_convert_socket(from_socket, to_socket):
    if not to_socket:
        return False
    return (is_float_type(from_socket) and is_float3_type(to_socket)) or \
           (is_float3_type(from_socket) and is_float_type(to_socket))


def build_output_param_str(mat_name, from_node, from_socket, convert_socket=False):
    from_node_name = get_node_name(from_node, mat_name)
    from_sock_name = get_socket_name(from_node, from_socket)

    # replace with the convert node's output
    if convert_socket:
        if is_float_type(from_socket):
            return "convert_%s.%s:resultRGB" % (from_node_name, from_sock_name)
        else:
            return "convert_%s.%s:resultF" % (from_node_name, from_sock_name)
    else:
        return "%s:%s" % (from_node_name, from_sock_name)


def get_output_param_str(node, mat_name, socket, to_socket=None):
    # if this is a node group, hook it up to the input node inside!
    if node.bl_idname == 'ShaderNodeGroup':
        ng = node.node_tree
        group_output = next(
            (n for n in ng.nodes if n.bl_idname == 'NodeGroupOutput'), None)
        if group_output is None:
            return "error:error"

        in_sock = group_output.inputs[socket.name]
        if len(in_sock.links):
            link = in_sock.links[0]
            return build_output_param_str(
                mat_name + '.' + node.name,
                link.from_node,
                link.from_socket,
                do_convert_socket(link.from_socket, to_socket))
        else:
            return "error:error"

    if node.bl_idname == 'NodeGroupInput':
        global current_group_node

        if current_group_node is None:
            return "error:error"

        in_sock = current_group_node.inputs[socket.name]
        if len(in_sock.links):
            link = in_sock.links[0]
            return build_output_param_str(
                mat_name,
                link.from_node,
                link.from_socket,
                do_convert_socket(link.from_socket, to_socket))
        else:
            return "error:error"

    return build_output_param_str(
        mat_name,
        node,
        socket,
        do_convert_socket(socket, to_socket))


# hack!!!
current_group_node = None


def translate_node_group(ri, group_node, mat_name):
    ng = group_node.node_tree
    out = next(
        (n for n in ng.nodes if n.bl_idname == 'NodeGroupOutput'), None)

    if out is None:
        return

    nodes_to_export = gather_nodes(out)
    global current_group_node
    current_group_node = group_node
    for node in nodes_to_export:
        shader_node_rib(ri, node, mat_name=(mat_name + '.' + group_node.name))
    current_group_node = None


def translate_cycles_node(ri, node, mat_name):
    if node.bl_idname == 'ShaderNodeGroup':
        translate_node_group(ri, node, mat_name)
        return

    if not PropertyLookup.do_map_cycles(node.bl_idname):
        print('No translation for node of type %s named %s' %
              (node.bl_idname, node.name))
        return

    mapping = PropertyLookup.map_cycles[node.bl_idname]
    params = {}
    for in_name, input in node.inputs.items():
        param_name = "%s %s" % (get_socket_type(
            node, input), get_socket_name(node, input))
        if input.is_linked:
            param_name = 'reference ' + param_name
            link = input.links[0]
            param_val = get_output_param_str(
                link.from_node, mat_name, link.from_socket, input)

        else:
            param_val = rib(input.default_value,
                            type_hint=get_socket_type(node, input))
            # skip if this is a vector set to 0 0 0
            if input.type == 'VECTOR' and param_val == [0.0, 0.0, 0.0]:
                continue

        params[param_name] = param_val

    ramp_size = 256
    if node.bl_idname == 'ShaderNodeValToRGB':
        colors = []
        alphas = []

        for i in range(ramp_size):
            c = node.color_ramp.evaluate(float(i) / (ramp_size - 1.0))
            colors.extend(c[:3])
            alphas.append(c[3])
        params['color[%d] ramp_color' % ramp_size] = colors
        params['float[%d] ramp_alpha' % ramp_size] = alphas
    elif node.bl_idname == 'ShaderNodeVectorCurve':
        colors = []
        node.mapping.initialize()
        r = node.mapping.curves[0]
        g = node.mapping.curves[1]
        b = node.mapping.curves[2]

        for i in range(ramp_size):
            v = float(i) / (ramp_size - 1.0)
            colors.extend([r.evaluate(v), g.evaluate(v), b.evaluate(v)])

        params['color[%d] ramp' % ramp_size] = colors

    elif node.bl_idname == 'ShaderNodeRGBCurve':
        colors = []
        node.mapping.initialize()
        c = node.mapping.curves[0]
        r = node.mapping.curves[1]
        g = node.mapping.curves[2]
        b = node.mapping.curves[3]

        for i in range(ramp_size):
            v = float(i) / (ramp_size - 1.0)
            c_val = c.evaluate(v)
            colors.extend([
                r.evaluate(v) * c_val,
                g.evaluate(v) * c_val,
                b.evaluate(v) * c_val])

        params['color[%d] ramp' % ramp_size] = colors

    # print('doing %s %s' % (node.bl_idname, node.name))
    # print(params)
    ri.Pattern(mapping, get_node_name(node, mat_name), params)


# Export to rib
def shader_node_rib(ri, node, mat_name, disp_bound=0.0, portal=False):
    # this is tuple telling us to convert
    if isinstance(node, tuple):
        shader, from_node, from_socket = node
        input_type = 'float' if shader == 'PxrToFloat3' else 'color'

        node_name = 'convert_%s.%s' % (
            get_node_name(from_node, mat_name),
            get_socket_name(from_node, from_socket))

        if from_node.bl_idname == 'ShaderNodeGroup':
            node_name = 'convert_' + get_output_param_str(
                from_node, mat_name, from_socket).replace(':', '.')

        params = {"reference %s input" % input_type: get_output_param_str(
            from_node, mat_name, from_socket)}

        params['__instanceid'] = node_name

        ri.Pattern(shader, node_name, params)
        return
    elif not hasattr(node, 'renderman_node_type'):
        return translate_cycles_node(ri, node, mat_name)

    params = gen_params(ri, node, mat_name)
    instance = mat_name + '.' + node.name

    params['__instanceid'] = instance

    if 'string filename' in params:
        params['string filename'] = bpy.path.abspath(params['string filename'])

    # patterns
    if node.renderman_node_type == "pattern":
        if node.bl_label == 'PxrOSL':
            shader = node.plugin_name
            if shader:
                ri.Pattern(shader, instance, params)
        else:
            ri.Pattern(node.bl_label, instance, params)

    # lights
    elif node.renderman_node_type == "light":
        light_group_name = ''
        scene = bpy.context.scene
        for lg in scene.renderman.light_groups:
            if mat_name in lg.members.keys():
                light_group_name = lg.name
                break
        params['string lightGroup'] = light_group_name
        params['__instanceid'] = mat_name

        light_name = node.bl_label
        if light_name == 'PxrPortalLight':
            if mat_name in bpy.data.lamps:
                lamp = bpy.context.scene.objects.active
                if (lamp
                    and lamp.parent
                    and lamp.parent.type == 'LAMP'
                    and lamp.parent.data.renderman.renderman_type == 'ENV'):

                    from .export import property_group_to_params

                    parent_node = lamp.parent.data.renderman.get_light_node()
                    parent_params = property_group_to_params(parent_node)
                    params['string domeSpace'] = lamp.parent.name
                    params['string portalName'] = mat_name
                    params['string domeColorMap'] = parent_params['string lightColorMap']
                    params['float intensity'] = parent_params['float intensity'] * params['float intensityMult']
                    del params['float intensityMult']
                    params['float exposure'] = parent_params['float exposure']
                    params['color lightColor'] = [
                        i * j for i, j in zip(
                            parent_params['color lightColor'],
                            params['color tint'])]
                    del params['color tint']

                    if not params['int enableTemperature']:
                        params['int enableTemperature'] = parent_params['int enableTemperature']
                        params['float temperature'] = parent_params['float temperature']
                    params['float specular'] *= parent_params['float specular']
                    params['float diffuse'] *= parent_params['float diffuse']
        ri.Light(light_name, mat_name, params)

    # lightfilter
    elif node.renderman_node_type == "lightfilter":
        params['__instanceid'] = mat_name

        light_name = node.bl_label
        ri.LightFilter(light_name, mat_name, params)

    # displacement
    elif node.renderman_node_type == "displacement":
        ri.Attribute('displacementbound', {'sphere': disp_bound})
        ri.Displace(node.bl_label, mat_name, params)

    # bxdf
    else:
        ri.Bxdf(node.bl_label, instance, params)


def is_same_type(socket1, socket2):
    return (
        (type(socket1) == type(socket2))
        or (is_float_type(socket1) and is_float_type(socket2))
        or (is_float3_type(socket1) and is_float3_type(socket2))
    )


def is_float_type(socket):
    # this is a renderman node
    if isinstance(socket, dict):
        return socket['renderman_type'] in ['int', 'float']
    elif hasattr(socket.node, 'plugin_name'):
        prop_meta = (
            getattr(socket.node, 'output_meta', [])
            if socket.is_output
            else getattr(socket.node, 'prop_meta', [])
        )
        if socket.name in prop_meta:
            return prop_meta[socket.name]['renderman_type'] in ['int', 'float']
    else:
        return socket.type in ['INT', 'VALUE']


def is_float3_type(socket):
    # this is a renderman node
    if isinstance(socket, dict):
        return socket['renderman_type'] in ['int', 'float']
    elif hasattr(socket.node, 'plugin_name'):
        prop_meta = (
            getattr(socket.node, 'output_meta', [])
            if socket.is_output
            else getattr(socket.node, 'prop_meta', [])
        )
        if socket.name in prop_meta:
            return prop_meta[socket.name]['renderman_type'] in ['color', 'vector', 'normal']
    else:
        return socket.type in ['RGBA', 'VECTOR']


# walk the tree for nodes to export
def gather_nodes(node):
    nodes = []
    for socket in node.inputs:
        if socket.is_linked:
            link = socket.links[0]
            for sub_node in gather_nodes(socket.links[0].from_node):
                if sub_node not in nodes:
                    nodes.append(sub_node)

            # if this is a float -> color inset a tofloat3
            if is_float_type(link.from_socket) and is_float3_type(socket):
                convert_node = ('PxrToFloat3', link.from_node,
                                link.from_socket)
                if convert_node not in nodes:
                    nodes.append(convert_node)
            elif is_float3_type(link.from_socket) and is_float_type(socket):
                convert_node = ('PxrToFloat', link.from_node, link.from_socket)
                if convert_node not in nodes:
                    nodes.append(convert_node)

    if hasattr(node, 'renderman_node_type') and node.renderman_node_type != 'output':
        nodes.append(node)
    elif (
        not hasattr(node, 'renderman_node_type')
        and node.bl_idname not in [
            'ShaderNodeOutputMaterial',
            'NodeGroupInput',
            'NodeGroupOutput']):
        nodes.append(node)

    return nodes


# for an input node output all "nodes"
def export_shader_nodetree(
    ri, id,
    handle=None,
    disp_bound=0.0,
    iterate_instance=False):

    if id and id.node_tree:

        if is_renderman(id):
            portal = (
                type(id).__name__ == 'AreaLamp'
                and id.renderman.renderman_type == 'PORTAL'
            )
            # if id.renderman.nodetree not in bpy.data.node_groups:
            #    load_tree_from_lib(id)

            nt = id.node_tree
            if not handle:
                handle = id.name
                if type(id) == bpy.types.Material:
                    handle = get_mat_name(handle)

            # if ipr we need to iterate instance num on nodes for edits
            from . import engine
            if engine.ipr and hasattr(id.renderman, 'instance_num'):
                if iterate_instance:
                    id.renderman.instance_num += 1
                if id.renderman.instance_num > 0:
                    handle += "_%d" % id.renderman.instance_num

            out = next((n for n in nt.nodes if hasattr(n, 'renderman_node_type') and
                        n.renderman_node_type == 'output'),
                       None)
            if out is None:
                return

            nodes_to_export = gather_nodes(out)
            ri.ArchiveRecord('comment', "Shader Graph")
            for node in nodes_to_export:
                shader_node_rib(ri, node, mat_name=handle,
                                disp_bound=disp_bound, portal=portal)
        elif find_node(id, 'ShaderNodeOutputMaterial'):
            print("Error Material %s needs a RenderMan BXDF" % id.name)


pattern_node_categories_map = {
    "texture": [
        "PxrFractal",
        "PxrBakeTexture",
        "PxrBakePointCloud",
        "PxrProjectionLayer",
        "PxrPtexture",
        "PxrTexture",
        "PxrVoronoise",
        "PxrWorley",
        "PxrFractalize",
        "PxrDirt",
        "PxrLayeredTexture",
        "PxrMultiTexture"],

    "bump": [
        "PxrBump",
        "PxrNormalMap",
        "PxrFlakes",
        "aaOceanPrmanShader",
        "PxrAdjustNormal"],

    "color": [
        "PxrBlackBody",
        "PxrBlend",
        "PxrChecker",
        "PxrClamp",
        "PxrColorCorrect",
        "PxrExposure",
        "PxrGamma",
        "PxrHairColor",
        "PxrHSL",
        "PxrInvert",
        "PxrLayeredBlend",
        "PxrMix",
        "PxrProjectionStack",
        "PxrRamp",
        "PxrRemap",
        "PxrThinFilm",
        "PxrThreshold",
        "PxrVary"],

    "manifold": [
        "PxrBumpManifold2D",
        "PxrManifold2D",
        "PxrManifold3D",
        "PxrManifold3DN",
        "PxrProjector",
        "PxrRandomTextureManifold",
        "PxrRoundCube",
        "PxrTileManifold"],

    "geometry": [
        "PxrDot",
        "PxrCross",
        "PxrFacingRatio",
        "PxrTangentField"],

    "script": [
        "PxrOSL",
        "PxrSeExpr"],

    "utility": [
        "PxrAttribute",
        "PxrGeometricAOVs",
        "PxrMatteID",
        "PxrPrimvar",
        "PxrShadedSide",
        "PxrTee",
        "PxrToFloat",
        "PxrToFloat3",
        "PxrVariable"],

    "displace": [
        "PxrDispScalarLayer",
        "PxrDispTransform",
        "PxrDispVectorLayer"],

    "layer": [
        'PxrLayer',
        'PxrLayerMixer']
}


# Node Chatagorization List
def GetPatternCategory(name):
    for cat_name, node_names in pattern_node_categories_map.items():
        if name in node_names:
            return cat_name
    else:
        return 'deprecated'


# our own base class with an appropriate poll function,
# so the categories only show up in our own tree type
class RendermanPatternNodeCategory(NodeCategory):

    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'ShaderNodeTree'


from . nds import nodetypes
from . nds import pattern_categories

classes = [
    RM_ShaderSocket,
    RM_NodeSocketVector,
    RM_NodeSocketColor,
    RM_NodeSocketFloat,
    RM_NodeSocketInt,
    RM_NodeSocketString,
    RM_NodeSocketStruct,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    user_preferences = bpy.context.user_preferences
    prefs = user_preferences.addons[__package__].preferences

    categories = {}

    for name, arg_file in args_files_in_path(prefs, None).items():
        vals = generate_node_type(prefs, name, ET.parse(arg_file).getroot())
        if vals:
            typename, nodetype = vals
            nodetypes[typename] = nodetype
    node_cats = {
        'bxdf': ('RenderMan Bxdfs', []),
        'light': ('RenderMan Lights', []),
        'patterns_texture': ('RenderMan Texture Patterns', []),
        'patterns_bump': ('RenderMan Bump Patterns', []),
        'patterns_color': ('RenderMan Color Patterns', []),
        'patterns_manifold': ('RenderMan Manifold Patterns', []),
        'patterns_geometry': ('RenderMan Geometry Patterns', []),
        'patterns_utility': ('RenderMan Utility Patterns', []),
        'patterns_script': ('RenderMan Script Patterns', []),
        'patterns_displace': ('RenderMan Displacement Patterns', []),
        'patterns_layer': ('RenderMan Layers', []),
        'displacement': ('RenderMan Displacements', [])
    }

    for name, node_type in nodetypes.items():
        node_item = NodeItem(name, label=node_type.bl_label)

        if node_type.renderman_node_type == 'pattern':
            # insert pxr layer in bxdf
            pattern_cat = GetPatternCategory(node_type.bl_label)
            if pattern_cat == 'deprecated':
                continue
            node_cat = 'patterns_' + pattern_cat
            node_cats[node_cat][1].append(node_item)
            pattern_cat = pattern_cat.capitalize()
            if pattern_cat not in pattern_categories:
                pattern_categories[pattern_cat] = {}
            pattern_categories[pattern_cat][name] = node_type

        elif 'LM' in name and node_type.renderman_node_type == 'bxdf':
            # skip LM materials
            continue
        elif node_type.renderman_node_type == 'light' and 'PxrMeshLight' not in name:
            # skip light nodes
            continue
        else:
            node_cats[node_type.renderman_node_type][1].append(node_item)

    # all categories in a list
    node_categories = [
        # identifier, label, items list
        RendermanPatternNodeCategory(
            "PRMan_output_nodes",
            "RenderMan Outputs",
            items=[
                NodeItem('RendermanOutputNode',
                label=RendermanOutputNode.bl_label)
            ]
        ),
    ]

    for name, (desc, items) in node_cats.items():
        node_categories.append(
            RendermanPatternNodeCategory(
                name,
                desc,
                items=sorted(items, key=attrgetter('_label'))
            )
        )

    nodeitems_utils.register_node_categories(
        "RENDERMANSHADERNODES", node_categories)


def unregister():
    nodeitems_utils.unregister_node_categories("RENDERMANSHADERNODES")
    # bpy.utils.unregister_module(__name__)

    for cls in classes:
        bpy.utils.unregister_class(cls)
