import bpy

from . utils import PropertyLookup

from .. gui import icons


class RendermanShadingNode(bpy.types.ShaderNode):
    """
    Base class for all custom nodes in this tree type.
    Defines a poll function to enable instantiation.
    """
    bl_label = 'Output'

    def update_mat(self, mat):
        if self.renderman_node_type == 'bxdf' and self.outputs['Bxdf'].is_linked:
            mat.specular_color = [1, 1, 1]
            mat.diffuse_color = [1, 1, 1]
            mat.use_transparency = False
            mat.specular_intensity = 0
            mat.diffuse_intensity = 1

            if hasattr(self, "baseColor"):
                mat.diffuse_color = self.baseColor
            elif hasattr(self, "emitColor"):
                mat.diffuse_color = self.emitColor
            elif hasattr(self, "diffuseColor"):
                mat.diffuse_color = self.diffuseColor
            elif hasattr(self, "midColor"):
                mat.diffuse_color = self.midColor
            elif hasattr(self, "transmissionColor"):
                mat.diffuse_color = self.transmissionColor
            elif hasattr(self, "frontColor"):
                mat.diffuse_color = self.frontColor

            # specular intensity
            if hasattr(self, "specular"):
                mat.specular_intensity = self.specular
            elif hasattr(self, "SpecularGainR"):
                mat.specular_intensity = self.specularGainR
            elif hasattr(self, "reflectionGain"):
                mat.specular_intensity = self.reflectionGain

            # specular color
            if hasattr(self, "specularColor"):
                mat.specular_color = self.specularColor
            elif hasattr(self, "reflectionColor"):
                mat.specular_color = self.reflectionColor

            if self.bl_idname in ["PxrGlassBxdfNode", "PxrLMGlassBxdfNode"]:
                mat.use_transparency = True
                mat.alpha = .5

            if self.bl_idname == "PxrLMMetalBxdfNode":
                mat.diffuse_color = [0, 0, 0]
                mat.specular_intensity = 1
                mat.specular_color = self.specularColor
                mat.mirror_color = [1, 1, 1]

            elif self.bl_idname == "PxrLMPlasticBxdfNode":
                mat.specular_intensity = 1

    # all the properties of a shader will go here, also inputs/outputs
    # on connectable props will have the same name
    # node_props = None
    def draw_buttons(self, context, layout):
        self.draw_nonconnectable_props(context, layout, self.prop_names)
        if self.bl_idname == "PxrOSLPatternNode":
            layout.operator("rfb.refresh_shader_osl")

    def draw_buttons_ext(self, context, layout):
        self.draw_nonconnectable_props(context, layout, self.prop_names)

    def draw_nonconnectable_props(self, context, layout, prop_names):
        if self.bl_idname in ['PxrLayerPatternNode', 'PxrSurfaceBxdfNode']:
            col = layout.column(align=True)
            for prop_name in prop_names:
                if prop_name not in self.inputs:
                    for name in getattr(self, prop_name):
                        if name.startswith('enable'):
                            col.prop(self, name, text=prop_name.split('.')[-1])
                            break
            return

        if self.bl_idname == "PxrOSLPatternNode" or self.bl_idname == "PxrSeExprPatternNode":
            # prop = getattr(self, "codetypeswitch")
            layout.prop(self, "codetypeswitch")
            if getattr(self, "codetypeswitch") == 'INT':
                # prop = getattr(self, "internalSearch")
                layout.prop_search(
                    self, "internalSearch", bpy.data, "texts", text="")
            elif getattr(self, "codetypeswitch") == 'EXT':
                # prop = getattr(self, "shadercode")
                layout.prop(self, "shadercode")
            elif getattr(self, "codetypeswitch") == 'NODE':
                layout.prop(self, "expression")
        else:
            if self.plugin_name == 'PxrRamp':
                #
                # temporary until we can create ramps natively
                #
                # TODO:    contact blender devs for status on this:
                #          pointer struct for color ramps can't be
                #          created via python (as far as I know!)
                # DATE:    2017-12-28 (adminradio)
                #
                nt = bpy.data.node_groups[self.node_group]
                if nt:
                    layout.template_color_ramp(
                        nt.nodes["ColorRamp"], 'color_ramp')

            for prop_name in prop_names:
                prop_meta = self.prop_meta[prop_name]

                # A unique id to lookup special handling of
                # props/pages (ARGs) on nodes.
                #
                prop_id = self.bl_idname + prop_name

                # Skip any drawing of props if widget is null
                # or hidden or an empty 'page'
                #
                if ('widget' in prop_meta and prop_meta['widget'] == 'null'
                    or
                    'hidden' in prop_meta and prop_meta['hidden']
                    or
                        PropertyLookup.is_emptypage(prop_id)):
                    continue

                if prop_name not in self.inputs:
                    if prop_meta['renderman_type'] == 'page':

                        # boxed row layout for single prop with label
                        if PropertyLookup.is_single(prop_id):
                            # draw label
                            row_label = prop_name.split('.')[-1] + ':'
                            cl = layout.box()
                            row = cl.row()
                            row.label(row_label)
                            prop = getattr(self, prop_name)
                            self.draw_nonconnectable_props(
                                context, row, prop)

                        # boxed row layout for single props with or withou label
                        elif (PropertyLookup.is_labeled(prop_id) or
                              PropertyLookup.is_unlabeled(prop_id)):
                            cl = layout.box()
                            row = cl.row()
                            prop = getattr(self, prop_name)
                            self.draw_nonconnectable_props(
                                context, row, prop)

                        # box layout for nested multiple props
                        else:
                            ui_prop = prop_name + "_ui_open"
                            ui_open = getattr(self, ui_prop)
                            icn = 'panel_open' if ui_open else 'panel_closed'
                            iid = icons.iconid(icn)
                            sub = layout.box()
                            sub = sub.column()
                            sub.prop(self, ui_prop,
                                     icon_value=iid,
                                     text=prop_name.split('.')[-1],
                                     emboss=False)
                            if ui_open:
                                prop = getattr(self, prop_name)
                                self.draw_nonconnectable_props(
                                    context, sub, prop)
                    elif (
                        "Subset" in prop_name and
                            prop_meta['type'] == 'string'):

                        layout.prop_search(self, prop_name,
                                           bpy.data.scenes[0].renderman,
                                           "object_groups")
                    else:
                        layout.prop(self, prop_name, slider=True)

    def copy(self, node):
        pass

    #    self.inputs.clear()
    #    self.outputs.clear()

    def RefreshNodes(self, context, nodeOR=None, materialOverride=None):

        # Compile shader. If the call was from socket draw get the node
        # information anther way.
        if hasattr(context, "node"):
            node = context.node
        else:
            node = nodeOR
        prefs = bpy.context.user_preferences.addons[__package__].preferences

        out_path = user_path(prefs.env_vars.out)
        compile_path = os.path.join(user_path(prefs.env_vars.out), "shaders")
        if os.path.exists(out_path):
            pass
        else:
            os.mkdir(out_path)
        if os.path.exists(os.path.join(out_path, "shaders")):
            pass
        else:
            os.mkdir(os.path.join(out_path, "shaders"))
        if getattr(node, "codetypeswitch") == "EXT":
            osl_path = user_path(getattr(node, 'shadercode'))
            FileName = os.path.basename(osl_path)
            FileNameNoEXT = os.path.splitext(FileName)[0]
            FileNameOSO = FileNameNoEXT
            FileNameOSO += ".oso"
            export_path = os.path.join(
                user_path(prefs.env_vars.out), "shaders", FileNameOSO)
            if os.path.splitext(FileName)[1] == ".oso":
                out_file = os.path.join(user_path(prefs.env_vars.out), "shaders", FileNameOSO)
                if not os.path.exists(out_file) or not os.path.samefile(osl_path, out_file):
                    shutil.copy(osl_path, out_file)
                # Assume that the user knows what they were doing when they
                # compiled the osl file.
                ok = True
            else:
                ok = node.compile_osl(osl_path, compile_path)
        elif getattr(node, "codetypeswitch") == "INT" and node.internalSearch:
            script = bpy.data.texts[node.internalSearch]
            osl_path = bpy.path.abspath(
                script.filepath, library=script.library)
            if script.is_in_memory or script.is_dirty or \
                    script.is_modified or not os.path.exists(osl_path):
                osl_file = tempfile.NamedTemporaryFile(
                    mode='w', suffix=".osl", delete=False)
                osl_file.write(script.as_string())
                osl_file.close()
                FileNameNoEXT = os.path.splitext(script.name)[0]
                FileNameOSO = FileNameNoEXT
                FileNameOSO += ".oso"
                node.plugin_name = FileNameNoEXT
                ok = node.compile_osl(osl_file.name, compile_path, script.name)
                export_path = os.path.join(
                    user_path(prefs.env_vars.out), "shaders", FileNameOSO)
                os.remove(osl_file.name)
            else:
                ok = node.compile_osl(osl_path, compile_path)
                FileName = os.path.basename(osl_path)
                FileNameNoEXT = os.path.splitext(FileName)[0]
                node.plugin_name = FileNameNoEXT
                FileNameOSO = FileNameNoEXT
                FileNameOSO += ".oso"
                export_path = os.path.join(
                    user_path(prefs.env_vars.out), "shaders", FileNameOSO)
        else:
            ok = False
            debug("osl", "Shader cannot be compiled. Shader name not specified")
        # If Shader compiled successfully then update node.
        if ok:
            debug('osl', "Shader Compiled Successfully!")
            # Reset the inputs and outputs
            node.outputs.clear()
            node.inputs.clear()
            # Read in new properties
            prop_names, shader_meta = readOSO(export_path)
            debug('osl', prop_names, "MetaInfo: ", shader_meta)
            # Set node name to shader name
            node.label = shader_meta["shader"]
            node.plugin_name = shader_meta["shader"]
            # Generate new inputs and outputs
            setattr(node, 'shader_meta', shader_meta)
            node.setOslProps(prop_names, shader_meta)
        else:
            debug("osl", "NODE COMPILATION FAILED")

    def compile_osl(self, inFile, outPath, nameOverride=""):
        if not nameOverride:
            FileName = os.path.basename(inFile)
            FileNameNoEXT = os.path.splitext(FileName)[0]
            out_file = os.path.join(outPath, FileNameNoEXT)
            out_file += ".oso"
        else:
            FileNameNoEXT = os.path.splitext(nameOverride)[0]
            out_file = os.path.join(outPath, FileNameNoEXT)
            out_file += ".oso"
        ok = _cycles.osl_compile(inFile, out_file)

        return ok

    def update(self):
        debug("info", "UPDATING: ", self.name)

    @classmethod
    def poll(cls, ntree):
        if hasattr(ntree, 'bl_idname'):
            return ntree.bl_idname == 'ShaderNodeTree'
        else:
            return True

    def setOslProps(self, prop_names, shader_meta):
        for prop_name in prop_names:
            prop_type = shader_meta[prop_name]["type"]
            if shader_meta[prop_name]["IO"] == "out":
                self.outputs.new(
                    socket_map[prop_type], prop_name)
            else:
                prop_default = shader_meta[prop_name]["default"]
                if prop_type == "float":
                    prop_default = float(prop_default)
                elif prop_type == "int":
                    prop_default = int(float(prop_default))

                if prop_type == "matrix":
                    self.inputs.new(socket_map["struct"], prop_name, prop_name)
                elif prop_type == "void":
                    pass
                elif 'lockgeom' in shader_meta[prop_name] and shader_meta[prop_name]['lockgeom'] == 0:
                    pass
                else:
                    input = self.inputs.new(socket_map[shader_meta[prop_name]["type"]],
                                            prop_name, prop_name)
                    input.default_value = prop_default
                    if prop_type == 'struct' or prop_type == 'point':
                        input.hide_value = True
                    input.renderman_type = prop_type
        debug('osl', "Shader: ", shader_meta["shader"], "Properties: ",
              prop_names, "Shader meta data: ", shader_meta)
        compileLocation = self.name + "Compile"
