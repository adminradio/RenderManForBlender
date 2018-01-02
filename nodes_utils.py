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


# Parameters on RenderMan nodes with special handling.
#
# These lists containing either no or only one 'NonConnectableParam'
# properties. This can happen if parameters from ARGs file are
# 'consumed' before as input or output ports leaving 'pages' (aka
# property groups) empty or single valued.
#
# TODO: for future use, these values should be go into a JSON file,
#       so we have not to modify code if things are added or changed.

class RfB_LUTs:
    """Utility Class // Data Class."""

    single_props = [
        "PxrBumpPatternNodeAdvanced",
        "PxrProjectorPatternNode2D Parameters",
        "PxrProjectorPatternNodeAdvanced",
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
        "PxrRemapPatternNodeOutput Range"]

    no_label = [
        "PxrVolumeBxdfNodeMultiScatter Optimization"]

    with_label = [
        "PxrMarschnerHairBxdfNodeDiffuse",
        "PxrColorCorrectPatternNodeClamp Output",
        "PxrMatteIDPatternNodeParameters"]

    empty_pages = [
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

    socket_colors = {
        "bxdf": (0.25, 1.00, 0.25, 1.00),
        "float": (0.50, 0.50, 0.50, 1.00),
        "vector": (0.00, 0.00, 0.50, 1.00),
        "rgb": (1.00, 0.50, 0.00, 1.00),
        "euler": (0.00, 0.50, 0.50, 1.00),
        "struct": (1.00, 1.00, 0.00, 1.00),
        "string": (0.00, 0.00, 1.00, 1.00),
        "int": (1.00, 1.00, 1.00, 1.00)}

    @classmethod
    def is_single_prop(cls, ident):
        return ident in cls.single_props

    @classmethod
    def is_single_prop_with_label(cls, ident):
        return ident in cls.with_label

    @classmethod
    def is_single_prop_no_label(cls, ident):
        return ident in cls.no_label

    @classmethod
    def is_empty_page(cls, ident):
        return ident in cls.empty_pages

    @classmethod
    def get_socket_color(cls, ident):
        try:
            return cls.socket_colors[ident]

        except KeyError:
            return (0.00, 0.00, 0.00, 1.00)

    cycles_node_map = {
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

    gains_to_enable = {
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

    group_nodes = [
        'ShaderNodeGroup',
        'NodeGroupInput',
        'NodeGroupOutput']
