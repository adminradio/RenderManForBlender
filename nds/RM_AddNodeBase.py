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
from bpy.props import EnumProperty
from operator import itemgetter

#
# RenderMan for Blender Imports
#

from . import nodetypes
from . import pattern_categories
from . import socket_node_input

from . import link_node


class RM_AddNodeBase:
    """
    For generating cycles-style ui menus to add new nodes,
    connected to a given input socket.
    """

    def get_type_items(self, context):
        items = []
        # if this is a pattern input do columns!
        if self.input_type.lower() == 'pattern':
            i = 0
            for pattern_cat, patterns in pattern_categories.items():
                if pattern_cat.lower() in ['layer', 'script', 'manifold', 'bump', 'displace']:
                    continue
                items.append(('', pattern_cat, pattern_cat, '', 0))
                for nodename in sorted(patterns):
                    nodetype = patterns[nodename]
                    items.append((nodetype.typename, nodetype.bl_label,
                                  nodetype.bl_label, '', i))
                    i += 1
                items.append(('', '', '', '', 0))
            items.append(('REMOVE', 'Remove',
                          'Remove the node connected to this socket', '', i + 1))
            items.append(('DISCONNECT', 'Disconnect',
                          'Disconnect the node connected to this socket', '', i + 2))

        elif self.input_type.lower() in ['layer', 'manifold', 'bump']:
            patterns = pattern_categories[self.input_type]
            for nodename in sorted(patterns):
                nodetype = patterns[nodename]
                items.append((nodetype.typename, nodetype.bl_label,
                              nodetype.bl_label))

            items.append(('REMOVE', 'Remove',
                          'Remove the node connected to this socket'))
            items.append(('DISCONNECT', 'Disconnect',
                          'Disconnect the node connected to this socket'))
        else:
            for nodetype in nodetypes.values():
                if self.input_type.lower() == 'light' and nodetype.renderman_node_type == 'light':
                    if nodetype.__name__ == 'PxrMeshLightLightNode':
                        items.append((nodetype.typename, nodetype.bl_label,
                                      nodetype.bl_label))
                elif nodetype.renderman_node_type == self.input_type.lower():
                    items.append((nodetype.typename, nodetype.bl_label,
                                  nodetype.bl_label))
            items = sorted(items, key=itemgetter(1))
            items.append(('REMOVE', 'Remove',
                          'Remove the node connected to this socket'))
            items.append(('DISCONNECT', 'Disconnect',
                          'Disconnect the node connected to this socket'))
        return items

    node_type = EnumProperty(name="Node Type",
                             description='Node type to add to this socket',
                             items=get_type_items)

    def execute(self, context):
        new_type = self.properties.node_type
        if new_type == 'DEFAULT':
            return {'CANCELLED'}

        nt = context.nodetree
        node = context.node
        socket = context.socket
        input_node = socket_node_input(nt, socket)

        if new_type == 'REMOVE':
            nt.nodes.remove(input_node)
            return {'FINISHED'}

        if new_type == 'DISCONNECT':
            link = next((l for l in nt.links if l.to_socket == socket), None)
            nt.links.remove(link)
            return {'FINISHED'}

        # add a new node to existing socket
        if input_node is None:
            newnode = nt.nodes.new(new_type)
            newnode.location = node.location
            newnode.location[0] -= 300
            newnode.selected = False
            if self.input_type in ['Pattern', 'Layer', 'Manifold', 'Bump']:
                link_node(nt, newnode, socket)
            else:
                nt.links.new(newnode.outputs[self.input_type], socket)

        # replace input node with a new one
        else:
            newnode = nt.nodes.new(new_type)
            input = socket
            old_node = input.links[0].from_node
            if self.input_type == 'Pattern':
                link_node(nt, newnode, socket)
            else:
                nt.links.new(newnode.outputs[self.input_type], socket)
            newnode.location = old_node.location
            active_material = context.active_object.active_material
            newnode.update_mat(active_material)
            nt.nodes.remove(old_node)
        return {'FINISHED'}
