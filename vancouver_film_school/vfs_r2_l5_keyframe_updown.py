"""
 Script for creating a sequence of keyframes on the selected objects so they move up and down
 Used to quickly test joints when rigging
 
 How to use:
    1. Select all objects you want to test.
    2. Run the script
    
 WARNING:
    This script deletes all keyframes (not including set driven keys)
    If for some reason you have keys that you want to keep in your scene, 
    comment out the line "delete_all_keyframes()" at the bottom of the script
    
  Todo:
    Create a GUI to make it easier for less technical students
    Add the option to test rotation and other dimensions
"""


def delete_all_keyframes():
    ''' 
    Deletes all nodes of the type keyframe (Doesn't include set driven keys) 
    '''
    keys_ta = cmds.ls(type='animCurveTA') # List all keyframes in the scene
    keys_tl = cmds.ls(type='animCurveTL')
    keys_tt = cmds.ls(type='animCurveTT')
    keys_tu = cmds.ls(type='animCurveTU')
    all_keyframes = keys_ta + keys_tl + keys_tt + keys_tu # Combine all keys into one list
    for obj in all_keyframes:
        try:
            cmds.delete(obj) # Try to delete every keyframe node
        except:
            pass # In case something goes wrong, don't alert the user


def auto_keyframe_updown(value, attribute, interval):
    '''
    Creates a sequence of keyframes on the selected objects so they move up and down
    Used to quickly test joints when rigging
    
            Parameters:
                value (float, int): keyframe value, how much it will move up and down (e.g. 1 or 2...)
                attribute (string): name of the attribute "e.g. rotation"
                interval (int): Interval between keyframes (frequency)
    '''
    selection = cmds.ls(selection=True) # Gets a list with of the current selection
    current_frame = cmds.playbackOptions( animationStartTime=True, q=True ) # Gets the first frame available in the timeline (usually 0 or 1)
    current_max_time = cmds.playbackOptions( maxTime=True, q=True ) # Gets the max time (work area end frame) to see if it needs to expand the timeline
    cmds.currentTime(current_frame) # Resets timeline to first frame 
    
    up_value = value # Positive Up value
    down_value = (value * -1) # Negative Down Value
    
    for obj in selection:
        if cmds.objExists(obj):
            # Create key at neutral position
            cmds.setKeyframe(obj, at=attribute, t=current_frame, itt='linear')
            
            # Create key at up position
            current_frame += interval
            cmds.move(up_value, obj, y=True, relative=True, ws=True)
            cmds.setKeyframe(obj, at=attribute, t=current_frame, itt='linear')
            
            # Create key at down position
            current_frame += interval
            cmds.move(down_value*2, obj, y=True, relative=True, ws=True)
            cmds.setKeyframe(obj, at=attribute, t=current_frame, itt='linear')
            
            # Create key at neutral position
            current_frame += interval
            cmds.move(up_value, obj, y=True, relative=True, ws=True)
            cmds.setKeyframe(obj, at=attribute, t=current_frame, itt='linear')
   
    print(current_frame)
    print(current_max_time)
    if current_frame > current_max_time:
        cmds.playbackOptions( maxTime=current_frame )


# Calls functions using a try and catch operation and undo chunk for better handling
errors = ''
function_name = 'Auto Keyframe Up Down'
try:
    cmds.undoInfo(openChunk=True, chunkName=function_name)
    current_frame = cmds.playbackOptions( animationStartTime=True, q=True ) # Gets the first frame available in the timeline (usually 0 or 1)
    cmds.currentTime(current_frame) # Resets timeline to first frame
    delete_all_keyframes()
    auto_keyframe_updown(1, 'translate', 5)
except Exception as e:
    errors += str(e) + '\n'
finally:
    cmds.undoInfo(closeChunk=True, chunkName=function_name)
if errors != '':
    cmds.warning('An error occured when creating the up and down keyframes. Open the script editor for more information.')
    print('######## Errors: ########')
    print(errors)
    print('#########################')