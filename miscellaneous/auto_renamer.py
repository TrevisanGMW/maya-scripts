"""
 Auto Renamer (With Template)
 @Guilherme Trevisan - github.com/TrevisanGMW - 2020-12-15
 
 1.0 - 2020-12-15
 Initial Release
 
""" 

import maya.cmds as cmds
import copy

key_prefix = ''
new_left_prefix = 'left_'
new_right_prefix = 'right_'
old_left_prefix = 'L_'
old_right_prefix = 'R_'

# Dictionary of names. Key is current name, value is new name e.g. { 'current_name' : 'new_name' }
renamer_dict = { key_prefix + 'Hip' : 'cog_jnt',
                 key_prefix + 'Pelvis' : 'hip_jnt',
                 key_prefix + 'Waist' : 'spine01_jnt',
                 key_prefix + 'Spine01' : 'spine02_jnt',
                 key_prefix + 'Spine02' : 'spine03_jnt',
                 key_prefix + 'NeckTwist01' : 'neckBase_jnt',
                 key_prefix + 'NeckTwist02' : 'neckMid_jnt',
                 key_prefix + 'Head' : 'head_jnt',
                 key_prefix + 'JawRoot' : 'jaw_jnt',
                 
                 # Left Side (Right side is auto populated
                 key_prefix + 'L_Eye' : 'left_eye_jnt',
                 
                 key_prefix + 'L_Clavicle' : 'left_clavicle_jnt',
                 key_prefix + 'L_Upperarm' : 'left_shoulder_jnt',
                 key_prefix + 'L_Forearm' : 'left_elbow_jnt',
                 key_prefix + 'L_ForearmTwist02' : 'left_forearm_jnt',
                 key_prefix + 'L_Hand' : 'left_wrist_jnt',
                 
                 key_prefix + 'L_Thumb1' : 'left_thumb01_jnt',
                 key_prefix + 'L_Thumb2' : 'left_thumb02_jnt',
                 key_prefix + 'L_Thumb3' : 'left_thumb03_jnt',
                 key_prefix + 'L_Index1' : 'left_index01_jnt',
                 key_prefix + 'L_Index2' : 'left_index02_jnt',
                 key_prefix + 'L_Index3' : 'left_index03_jnt',
                 key_prefix + 'L_Mid1' : 'left_middle01_jnt',
                 key_prefix + 'L_Mid2' : 'left_middle02_jnt',
                 key_prefix + 'L_Mid3' : 'left_middle03_jnt',
                 key_prefix + 'L_Ring1' : 'left_ring01_jnt',
                 key_prefix + 'L_Ring2' : 'left_ring02_jnt',
                 key_prefix + 'L_Ring3' : 'left_ring03_jnt',
                 key_prefix + 'L_Pinky1' : 'left_pinky01_jnt',
                 key_prefix + 'L_Pinky2' : 'left_pinky02_jnt',
                 key_prefix + 'L_Pinky3' : 'left_pinky03_jnt',
                 
                 key_prefix + 'L_ThighTwist01' : 'left_hip_jnt',
                 key_prefix + 'L_CalfTwist01' : 'left_knee_jnt',
                 key_prefix + 'L_Foot' : 'left_ankle_jnt',
                 key_prefix + 'L_ToeBase' : 'left_ball_jnt',
                 key_prefix + 'L_MidToe1' : 'left_toe_jnt',
               }
              
# Auto Populate Right Side (Copy from Left to Right)
renamer_dict_list = list(renamer_dict)
for item in renamer_dict_list:
    
    if old_left_prefix in item:
        renamer_dict[item.replace(old_left_prefix, old_right_prefix)] = renamer_dict.get(item).replace(new_left_prefix, new_right_prefix) # Add right copy
        
# Rename it
for item in renamer_dict:
    if cmds.objExists(item):
        cmds.rename(item, renamer_dict.get(item))
