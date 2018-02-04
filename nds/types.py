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

#
# Blender Imports
#

#
# RenderManForBlender Imports
#


def isfloat(socket):
    #
    # this is a renderman node
    #
    if isinstance(socket, dict):
        return socket['renderman_type'] in ['int', 'float']

    elif hasattr(socket.node, 'plugin_name'):
        prop_meta = getattr(socket.node, 'output_meta', []) \
            if socket.is_output \
            else getattr(socket.node, 'prop_meta', [])

        if socket.name in prop_meta:
            return (
                prop_meta[socket.name]['renderman_type']
                in ['int', 'float']
            )
    else:
        return socket.type in ['INT', 'VALUE']


def isfloat3(socket):
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
            return (
                prop_meta[socket.name]['renderman_type']
                in ['color', 'vector', 'normal']
            )
    else:
        return socket.type in ['RGBA', 'VECTOR']


def samesame(a, b):
    return (
        (type(a) == type(b))
        or
        (isfloat(a) and isfloat(b))
        or
        (isfloat3(a) and isfloat3(b))
    )
