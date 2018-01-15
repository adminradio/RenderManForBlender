# class RENDER_PT_layer_passes(PRManButtonsPanel, Panel):
#     bl_label = "Passes"
#     bl_context = "render_layer"
#     # bl_options = {'DEFAULT_CLOSED'}

#     def draw(self, context):
#         layout = self.layout

#         scene = context.scene
#         rd = scene.render
#         rl = rd.layers.active
#         rm = rl.renderman

#         layout.prop(rm, "combine_outputs")
#         split = layout.split()

        # col = split.column()
        # col.prop(rl, "use_pass_combined")
        # col.prop(rl, "use_pass_z")
        # col.prop(rl, "use_pass_normal")
        # col.prop(rl, "use_pass_vector")
        # col.prop(rl, "use_pass_uv")
        # col.prop(rl, "use_pass_object_index")
        # #col.prop(rl, "use_pass_shadow")
        # #col.prop(rl, "use_pass_reflection")

        # col = split.column()
        # col.label(text="Diffuse:")
        # row = col.row(align=True)
        # row.prop(rl, "use_pass_diffuse_direct", text="Direct", toggle=True)
        # row.prop(rl, "use_pass_diffuse_indirect", text="Indirect", toggle=True)
        # row.prop(rl, "use_pass_diffuse_color", text="Albedo", toggle=True)
        # col.label(text="Specular:")
        # row = col.row(align=True)
        # row.prop(rl, "use_pass_glossy_direct", text="Direct", toggle=True)
        # row.prop(rl, "use_pass_glossy_indirect", text="Indirect", toggle=True)

        # col.prop(rl, "use_pass_subsurface_indirect", text="Subsurface")
        # col.prop(rl, "use_pass_refraction", text="Refraction")
        # col.prop(rl, "use_pass_emit", text="Emission")

        # layout.separator()
        # row = layout.row()
        # row.label('Holdouts')
        # rm = scene.renderman.holdout_settings
        # layout.prop(rm, 'do_collector_shadow')
        # layout.prop(rm, 'do_collector_reflection')
        # layout.prop(rm, 'do_collector_refraction')
        # layout.prop(rm, 'do_collector_indirectdiffuse')
        # layout.prop(rm, 'do_collector_subsurface')

        # col.prop(rl, "use_pass_ambient_occlusion")
