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

    _group_nodes = [
        'ShaderNodeGroup',
        'NodeGroupInput',
        'NodeGroupOutput']

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

    @classmethod
    def is_groupnode(cls, ident):
        return ident in cls._group_nodes

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
