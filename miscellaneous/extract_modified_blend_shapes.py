"""
 Extract Blend Shapes After Non-Deformer History
 @Guilherme Trevisan - github.com/TrevisanGMW - 2020-12-15
 
 1.0 - 2020-12-15
 Initial Release
 
""" 

import maya.cmds as cmds

selection = cmds.ls(selection=True)[0] # Uses first selected object
history = cmds.listHistory(selection)
my_blendshape_node = cmds.ls( history, type = 'blendShape')[0]
my_blendshape_names = cmds.listAttr( my_blendshape_node + '.w' , m=True )

# Set All to Zero
for target in my_blendshape_names:
    cmds.setAttr(my_blendshape_node + '.' + target, 0)

# Start Duplicating It
for target in my_blendshape_names:
    cmds.setAttr(my_blendshape_node + '.' + target, 1)
    cmds.duplicate( selection, name=target)
    cmds.setAttr(my_blendshape_node + '.' + target, 0)