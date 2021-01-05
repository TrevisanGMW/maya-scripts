"""

 Creates a cube of the size of a standard kitchen cabinet
 @Guilherme Trevisan - TrevisanGMW@gmail.com - 2021-01-04
 
 1.0 - 2021-01-04
 Initial Release

"""
import maya.cmds as cmds

width = 61
height = 91.4
depth = width

if not cmds.objExists('cabinet_volume_geo'):
    # Create Cabinet
    cube = cmds.polyCube(w=width, h=height, d=depth, sx=1, sy=1, sz=1, ax=(0, 1, 0), cuv=4, ch=1)
    cmds.xform(cube, piv=[width*.5, -height*.5, depth*.5], ws=True) # sends pivot to corner
    cmds.move(0, 0, 0, cube, a=True,rpr=True)
    cabinet = cmds.rename(cube[0], 'cabinet_volume_geo')
    
    # Create Measure Tool
    distance_node_height = cmds.distanceDimension(sp=(-width, height, 0), ep=(-width, 0, 0))
    distance_node_height_transform = cmds.listRelatives(distance_node_height, parent=True) or [][0] 
    distance_node_height_locators = cmds.listConnections(distance_node_height)
    
    # Create Cabinet Attributes
    cmds.addAttr(cabinet, ln="measureToolVisibility", at="enum", en="-------------:", keyable=True)
    cmds.setAttr(cabinet + '.measureToolVisibility', e=True, lock=True)
    cmds.addAttr(cabinet, ln="displayHeight", at="bool", keyable=True)
    cmds.setAttr(cabinet + '.displayHeight', 1)
    cmds.addAttr(cabinet, ln="displayDepth", at="bool", keyable=True)
    cmds.setAttr(cabinet + '.displayDepth', 1)
        
    distance_node_depth = cmds.distanceDimension(sp=(0, 0, 0), ep=(0, 0, -depth))
    distance_node_depth_transform = cmds.listRelatives(distance_node_depth, parent=True) or [][0] 
    distance_node_depth_locators = cmds.listConnections(distance_node_depth)

    for obj in distance_node_height_locators + distance_node_height_transform + distance_node_depth_locators + distance_node_depth_transform:
        cmds.setAttr(obj + '.hiddenInOutliner', 1)
        cmds.setAttr(obj + '.overrideEnabled', 1)
        cmds.setAttr(obj + '.overrideDisplayType', 2)
        if obj in distance_node_height_locators or obj in distance_node_depth_locators:
            cmds.setAttr(obj + '.v', 0)
        elif obj in distance_node_height_transform:
            cmds.connectAttr('%s.displayHeight' % cabinet, '%s.v' % obj)
        elif obj in distance_node_depth_transform:
            cmds.connectAttr('%s.displayDepth' % cabinet, '%s.v' % obj)
        
    cmds.parent(distance_node_height_transform, cabinet)
    cmds.parent(distance_node_height_locators, cabinet)
    cmds.parent(distance_node_depth_locators, cabinet)
    cmds.parent(distance_node_depth_transform, cabinet)
    cmds.select(cabinet)
else:
    cmds.warning('You already have a "cabinet_volume_geo" object. Delete it first in case you want to create a new one.')
    
