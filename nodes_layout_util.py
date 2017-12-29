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

# Author: Timm Wimmers, Adminradio
# Date:   2017-12-29


# ############################################# #
#  NODES LAYOUT UTILITIES: No classes, please!  #
# ############################################# #


# Parameters on RenderMan nodes with special handling.
#
# These lists containing either no or only one 'NonConnectableParam'
# properties. This can happen if parameters from ARGs file are
# 'consumed' before as input or output ports leaving 'pages' (aka
# property groups) empty or single valued.
#
# TODO: for future use, these values should be go into a JSON file,
#       so we have not to modify code if things are added or changed.
#
# TODO: While doing ths, I wonder if this can be concatenatet into
#       single dict items {"PxrNode": ([prop_list], [prop_list], [prop_list])
#
#       DO THIS!!!!!!!!!!!!!!!!!!!!!!!!!!
#
def is_single_prop(_id):
    """Return True if single prop, else False."""
    single_props = ["PxrBumpPatternNodeAdvanced",
                    "PxrProjectorBxdfNode2D Parameters",
                    "PxrProjectorBxdfNodeAdvance",
                    "PxrDispScalarLayerPatternNodeBase Layer",
                    "PxrLayerSurfaceBxdfNodeFuzz",
                    "PxrLayerSurfaceBxdfNodeScattering Globals",
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
                    "PxrRemapPatternNodeOutput Range"
                    ]
    return True if _id in single_props else False


def is_single_prop_with_label(_id):
    prop_list = ["PxrMarschnerHairBxdfNodeDiffuse",
                 "PxrColorCorrectPatternNodeClamp Output",
                 "PxrMatteIDPatternNodeParameters"
                 ]
    return True if _id in prop_list else False


def is_single_prop_no_label(_id):
    prop_list = ["PxrVolumeBxdfNodeMultiScatter Optimization"
                 ]
    return True if _id in prop_list else False


def is_empty_page(_id):
    """Return True if empty page, else False."""
    empty_pages = ["PxrBumpPatternNodePattern",
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
                   "PxrRemapPatternNodeRemap"
                   ]
    return True if _id in empty_pages else False
