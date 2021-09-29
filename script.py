import bpy
from typing import Tuple

def setupNodesToChooseBackgroundColor(compositorBackgroundColor: Tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0), useNodes: bool = True):
    # NODE SETUP
    bpy.data.scenes['Scene'].use_nodes = useNodes
    nodeTree = bpy.data.scenes['Scene'].node_tree
    for area in bpy.context.screen.areas:
        if area.type == 'DOPESHEET_EDITOR':
            area.type = 'NODE_EDITOR'

    # clear default nodes
    for node in nodeTree.nodes:
        nodeTree.nodes.remove(node)

    # create input image node
    in_node = nodeTree.nodes.new(type='CompositorNodeRLayers')
    in_node.location = -400, 0

    # create mix node
    mix_node = nodeTree.nodes.new(type='CompositorNodeMixRGB')
    mix_node.location = 400, 0
    mix_node.inputs[1].default_value = compositorBackgroundColor

    # create output node
    out_node = nodeTree.nodes.new('CompositorNodeComposite')
    out_node.location = 800, 0

    # link nodes
    nodeTree.links.new(in_node.outputs[0], mix_node.inputs[2])
    nodeTree.links.new(mix_node.outputs[0], out_node.inputs[0])
    nodeTree.links.new(in_node.outputs[1], mix_node.inputs[0])
    
    
def setCameraPositionInRenderSceneToRenderPersonFrontPerspectiveAt200cm():
    pi = 3.14159265
    # Camera location
    camLocationX = 0.0  # -0.003787 m
    camLocationY = -3.25  # -2.42078 m
    camLocationZ = 0.25  # -0.121197 m

    # Camera rotation
    camRotationX = 86  # 90°
    camRotationY = 0.0  # 0°
    camRotationZ = 0.0  # 0°

    # Get render-scene to modify
    scene = bpy.data.scenes["Scene"]

    # Set camera settings
    scene.camera.data.type = 'PERSP'
    scene.camera.data.lens = 50  # 50mm

    # Set camera rotation in radians
    scene.camera.rotation_mode = 'XYZ'
    scene.camera.rotation_euler[0] = camRotationX * (pi / 180.0)
    scene.camera.rotation_euler[1] = camRotationY * (pi / 180.0)
    scene.camera.rotation_euler[2] = camRotationZ * (pi / 180.0)

    # Set camera translation
    scene.camera.location.x = camLocationX
    scene.camera.location.y = camLocationY
    scene.camera.location.z = camLocationZ
    

    
bpy.ops.object.delete(use_global=False)
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()
# bpy.ops.object.select_by_type(type='LIGHT')
bpy.ops.object.add(type='LIGHT')
bpy.data.objects['Light'].select_set(True)
lightData = bpy.data.lights['Light']
print(lightData)
lightData.energy = 300
lightObject = bpy.data.objects['Light']
lightObject.location = (0, 5, 1.75)
# make it active
bpy.context.view_layer.objects.active = lightObject

# Add linked lights:
listOfLightLocations = [
    (0, 5, -1.75),
    (0, -5, 1.75),
    (0, -5, -1.75),
    (5, 0, 1.75),
    (5, 0, -1.75),
    (-5, 0, 1.75),
    (-5, 0, -1.75),
]
for lightNumber, lightLocation in enumerate(listOfLightLocations, start=1):
    # create new object with our light datablock
    newlightObject = bpy.data.objects.new(name="Light." + str(lightNumber), object_data=lightData)
    newlightObject.location = lightLocation
    # link light object
    bpy.context.collection.objects.link(newlightObject)

bpy.data.worlds['World'].node_tree.nodes["Background"].inputs[0].default_value = (1.0, 1.0, 1.0, 1.0)
bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value = 0
bpy.data.scenes['Scene'].view_settings.view_transform = 'Standard'
bpy.data.scenes['Scene'].render.film_transparent = True
compositorBackgroundColor = (1.0, 1.0, 1.0, 1.0)
setupNodesToChooseBackgroundColor(compositorBackgroundColor)

bpy.ops.object.add(type='CAMERA')
bpy.context.scene.camera = bpy.data.objects["Camera"]
setCameraPositionInRenderSceneToRenderPersonFrontPerspectiveAt200cm()
pixelHeight = 1000
bpy.context.scene.render.resolution_x = pixelHeight / 3 * 2
bpy.context.scene.render.resolution_y = pixelHeight
