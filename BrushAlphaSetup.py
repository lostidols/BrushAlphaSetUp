#  Hey okay so! This probably won't make much sense without having watched the video,
#  unless you know this stuff already in which case it'll be distressingly obvious, I imagine. 

#  If there's a bit that isn't applicable to what you wanna do (like creating a panel or a hotkey),
#  Just delete the whole section! 



#  Below is the info about the addon (the stuff you see in the addon description)!
#  Change it to be relevant! 
bl_info = {
    "name": "Brush Alpha Set Up",
    "author": "Jay Barnett",
    "version": (1, 1),
    "blender": (2, 80, 0),
}



#  Below is just the bit that tells blender, 
#  "Hey, can the blender API python translator help us out here?"
import bpy




#  New Operator
class BrushAlpha(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.brush_alpha"
    bl_label = "Brush Alpha Set Up"

#Necessary

    def execute(self, context):
#camera setup
        bpy.context.scene.camera.rotation_euler = (0,0,0)
        bpy.context.scene.camera.location = (0,0,4)
        bpy.data.cameras['Camera'].type = 'ORTHO'
        bpy.context.scene.render.resolution_x = 1080
        bpy.context.scene.render.resolution_y = 1080
#render settings
        bpy.data.scenes["Scene"].render.image_settings.file_format = 'OPEN_EXR'
        bpy.data.scenes["Scene"].render.image_settings.color_mode = 'BW'
        bpy.data.scenes["Scene"].render.image_settings.exr_codec = 'NONE'
#All the Mist Pass Settings
        bpy.data.cameras['Camera'].show_mist = True
        bpy.data.scenes["Scene"].view_layers["View Layer"].use_pass_mist = True
        bpy.context.scene.world.mist_settings.start = 1
        bpy.context.scene.world.mist_settings.depth = 3
# check Use Nodes
        bpy.context.scene.use_nodes = True
        tree = bpy.context.scene.node_tree
#clear default nodes       
        for node in tree.nodes:
            tree.nodes.remove(node)
# create Render Layers node
        layers_node = tree.nodes.new('CompositorNodeRLayers')   
        layers_node.location = 0,0
# create Gamma node
        gamma_node = tree.nodes.new(type='CompositorNodeGamma')
        gamma_node.location = 300,0
        bpy.data.scenes["Scene"].node_tree.nodes["Gamma"].inputs[1].default_value = 0.05     
# create Invert node
        invert_node = tree.nodes.new('CompositorNodeInvert')   
        invert_node.location = 600,0
#create Mask node
        mask_node = tree.nodes.new('CompositorNodeEllipseMask')   
        mask_node.location = 300,-300
        bpy.data.scenes["Scene"].node_tree.nodes["Ellipse Mask"].width = 0.6
        bpy.data.scenes["Scene"].node_tree.nodes["Ellipse Mask"].height = 0.6
#create Blur node
        blur_node = tree.nodes.new('CompositorNodeBlur')   
        blur_node.location = 650,-300
        bpy.data.scenes["Scene"].node_tree.nodes["Blur"].filter_type = 'CATROM'
        bpy.data.scenes["Scene"].node_tree.nodes["Blur"].use_relative = True
        bpy.data.scenes["Scene"].node_tree.nodes["Blur"].factor_x = 35
        bpy.data.scenes["Scene"].node_tree.nodes["Blur"].factor_y = 35
#create Mix node
        mix_node = tree.nodes.new('CompositorNodeMixRGB')   
        mix_node.location = 900,0
# create output node
        comp_node = tree.nodes.new('CompositorNodeComposite')   
        comp_node.location = 1200,0
# create viewer node
        viewer_node = tree.nodes.new('CompositorNodeViewer')   
        viewer_node.location = 1200,-300
# link nodes
        links = tree.links
        link = links.new(layers_node.outputs[3], gamma_node.inputs[0])
        link = links.new(gamma_node.outputs[0], invert_node.inputs[0])
        link = links.new(invert_node.outputs[0], mix_node.inputs[1])
        link = links.new(mask_node.outputs[0], blur_node.inputs[0])
        link = links.new(blur_node.outputs[0], mix_node.inputs[2])
        link = links.new(mix_node.outputs[0], comp_node.inputs[0])
        link = links.new(mix_node.outputs[0], viewer_node.inputs[0])
# turn on Xray
        for window in bpy.context.window_manager.windows:
            screen = window.screen

        for area in screen.areas:
            if area.type == 'VIEW_3D':
                override = {'window': window, 'screen': screen, 'area': area}
                bpy.ops.view3d.toggle_xray(override)
                break        
#  I changed "FINISHED" to "TaDa!" once because I thought it'd be cute 
#  and it broke everything. 
#  Just leave it as FINISHED. 
        return {'FINISHED'}
    



#  Below is the code you use if you want to add a panel! 
#  Change all the names to be relevant! 
class BrushAlphaPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Brush Alpha Set Up Panel"
    bl_idname = "OBJECT_PT_brushalphapanel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "texture"

    def draw(self, context):
        layout = self.layout
        obj = context.object
        row = layout.row()
# World Mist Settings
        scene = context.scene
        world = scene.world.mist_settings
# Below is where you place the operator your want the button to employ! 
        row.operator("object.brush_alpha")
# Mist Adjustment
        layout.prop(world, "start")
        layout.prop(world, "depth")
        layout.prop(world, "falloff")
            
        
        
#  Below is where you add a hotkey, if you want! Change the operator to the name of your script.
#  Currently it is set to activate when the P key is pressed. 
#  I kinda don't recommend using this, but! It's cool that you can! 
    keyconfig = bpy.context.window_manager.keyconfigs.addon
    keymap = keyconfig.keymaps.new(name="3D View Generic", space_type='VIEW_3D', region_type='WINDOW')  
    keymap_item = keymap.keymap_items.new("object.do_everything_script",'P', 'PRESS')                                
    keymap_item.active = True


#  Below is the bit the addon installation takes care of, installing all of your operators and panels
#  and such so Blender knows they exist, so you can call on them later! 
def register():
    bpy.utils.register_class(BrushAlpha)
    bpy.utils.register_class(BrushAlphaPanel)

def unregister():
    bpy.utils.unregister_class(BrushAlpha)
    bpy.utils.unregister_class(BrushAlphaPanel)

#  Below is the magic python bit that lets you run the script just by 
#  hitting "Run" above (in the blender text editor), without having to instal. 
#  Good for testing. 
if __name__ == "__main__":
    register()
