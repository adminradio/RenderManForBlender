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
import bpy


class RfB_OT_AOVsAddRenderman(bpy.types.Operator):
    bl_idname = 'rfb.aovs_add_renderman'
    bl_label = "Switch to RenderMan Passes"

    def execute(self, context):
        scene = context.scene
        scene.renderman.render_layers.add()
        active_layer = scene.render.layers.active
        # this sucks.  but can't find any other way to refer to render layer
        scene.renderman.render_layers[-1].render_layer = active_layer.name

        # add the already existing passes
        scene = context.scene
        rm = scene.renderman
        rm_rl = scene.renderman.render_layers[-1]
        active_layer = scene.render.layers.active

        rl = active_layer

        aovs = [
            # (name, do?, declare type/name, source)
            ("color rgba", active_layer.use_pass_combined, "rgba"),
            ("float z", active_layer.use_pass_z, "z"),
            ("normal Nn", active_layer.use_pass_normal, "Normal"),
            ("vector dPdtime", active_layer.use_pass_vector, "Vectors"),
            ("float u", active_layer.use_pass_uv, "u"),
            ("float v", active_layer.use_pass_uv, "v"),
            ("float id", active_layer.use_pass_object_index, "id"),
            ("color lpe:shadows;C[<.D%G><.S%G>]<L.%LG>",
             active_layer.use_pass_shadow, "Shadows"),
            ("color lpe:C<RS%G>([DS]+<L.%LG>)|([DS]*O)",
             active_layer.use_pass_reflection, "Reflections"),
            ("color lpe:C<.D%G><L.%LG>",
             active_layer.use_pass_diffuse_direct, "Diffuse"),
            ("color lpe:(C<RD%G>[DS]+<L.%LG>)|(C<RD%G>[DS]*O)",
             active_layer.use_pass_diffuse_indirect, "IndirectDiffuse"),
            ("color lpe:nothruput;noinfinitecheck;noclamp;unoccluded;overwrite;C(U2L)|O",
             active_layer.use_pass_diffuse_color, "Albedo"),
            ("color lpe:C<.S%G><L.%LG>",
             active_layer.use_pass_glossy_direct, "Specular"),
            ("color lpe:(C<RS%G>[DS]+<L.%LG>)|(C<RS%G>[DS]*O)",
             active_layer.use_pass_glossy_indirect, "IndirectSpecular"),
            ("color lpe:(C<TD%G>[DS]+<L.%LG>)|(C<TD%G>[DS]*O)",
             active_layer.use_pass_subsurface_indirect, "Subsurface"),
            ("color lpe:(C<T[S]%G>[DS]+<L.%LG>)|(C<T[S]%G>[DS]*O)",
             active_layer.use_pass_refraction, "Refraction"),
            ("color lpe:emission", active_layer.use_pass_emit, "Emission"),
        ]

        for aov_type, attr, name in aovs:
            if attr:
                aov_setting = rm_rl.custom_aovs.add()
                aov_setting.aov_name = aov_type
                aov_setting.name = name
                aov_setting.channel_name = name

        return {'FINISHED'}
