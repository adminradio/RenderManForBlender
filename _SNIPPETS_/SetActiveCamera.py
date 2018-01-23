context = bpy.context
scene = context.scene
selected_cam = bpy.data.objects[bpy.context.active_object.name]
scene.camera = selected_cam
