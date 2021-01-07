"""
 Seamless IK/FK Switch for GT Auto Biped Rigger.
 @Guilherme Trevisan - TrevisanGMW@gmail.com - 2021-01-05
 github.com/TrevisanGMW/gt-tools

 1.0 - 2021-01-05
 Initial Release

"""
try:
    from shiboken2 import wrapInstance
except ImportError:
    from shiboken import wrapInstance
    
try:
    from PySide2.QtGui import QIcon
    from PySide2.QtWidgets import QWidget
except ImportError:
    from PySide.QtGui import QIcon, QWidget

from maya import OpenMayaUI as omui
import maya.cmds as cmds



# Script Name
script_name = "GT - Seamless FK/IK Switcher"

# Version:
script_version = "1.0";

# Settings
left_arm_seamless_dict = { 'switch_ctrl' : 'left_arm_switch_ctrl', # Switch Ctrl
                           'end_ik_ctrl' : 'left_wrist_ik_ctrl', # IK Elements
                           'pvec_ik_ctrl' : 'left_elbow_ik_ctrl',
                           'base_ik_jnt' :  'left_shoulder_ik_jnt',
                           'mid_ik_jnt' : 'left_elbow_ik_jnt',
                           'end_ik_jnt' : 'left_wrist_ik_jnt',
                           'base_fk_ctrl' : 'left_shoulder_ctrl', # FK Elements
                           'mid_fk_ctrl' : 'left_elbow_ctrl',
                           'end_fk_ctrl' : 'left_wrist_ctrl' ,
                           'base_fk_jnt' :  'left_shoulder_fk_jnt',
                           'mid_fk_jnt' : 'left_elbow_fk_jnt',
                           'end_fk_jnt' : 'left_wrist_fk_jnt',
                           'mid_ik_reference' : 'left_elbowSwitch_loc',
                           'end_ik_reference' : ''
                         }

right_arm_seamless_dict = { 'switch_ctrl' : 'right_arm_switch_ctrl', # Switch Ctrl
                            'end_ik_ctrl' : 'right_wrist_ik_ctrl', # IK Elements
                            'pvec_ik_ctrl' : 'right_elbow_ik_ctrl',
                            'base_ik_jnt' :  'right_shoulder_ik_jnt',
                            'mid_ik_jnt' : 'right_elbow_ik_jnt',
                            'end_ik_jnt' : 'right_wrist_ik_jnt',
                            'base_fk_ctrl' : 'right_shoulder_ctrl', # FK Elements
                            'mid_fk_ctrl' : 'right_elbow_ctrl',
                            'end_fk_ctrl' : 'right_wrist_ctrl' ,
                            'base_fk_jnt' :  'right_shoulder_fk_jnt',
                            'mid_fk_jnt' : 'right_elbow_fk_jnt',
                            'end_fk_jnt' : 'right_wrist_fk_jnt',
                            'mid_ik_reference' : 'right_elbowSwitch_loc',
                            'end_ik_reference' : ''
                           }
                            
left_leg_seamless_dict = { 'switch_ctrl' : 'left_leg_switch_ctrl', # Switch Ctrl
                           'end_ik_ctrl' : 'left_foot_ik_ctrl', # IK Elements
                           'pvec_ik_ctrl' : 'left_knee_ik_ctrl',
                           'base_ik_jnt' :  'left_hip_ik_jnt',
                           'mid_ik_jnt' : 'left_knee_ik_jnt',
                           'end_ik_jnt' : 'left_ankle_ik_jnt',
                           'base_fk_ctrl' : 'left_hip_ctrl', # FK Elements
                           'mid_fk_ctrl' : 'left_knee_ctrl',
                           'end_fk_ctrl' : 'left_ankle_ctrl' ,
                           'base_fk_jnt' :  'left_hip_fk_jnt',
                           'mid_fk_jnt' : 'left_knee_fk_jnt',
                           'end_fk_jnt' : 'left_ankle_fk_jnt',
                           'mid_ik_reference' : 'left_kneeSwitch_loc',
                           'end_ik_reference' : 'left_ankleSwitch_loc'
                          }
                           
right_leg_seamless_dict = { 'switch_ctrl' : 'right_leg_switch_ctrl', # Switch Ctrl
                            'end_ik_ctrl' : 'right_foot_ik_ctrl', # IK Elements
                            'pvec_ik_ctrl' : 'right_knee_ik_ctrl',
                            'base_ik_jnt' :  'right_hip_ik_jnt',
                            'mid_ik_jnt' : 'right_knee_ik_jnt',
                            'end_ik_jnt' : 'right_ankle_ik_jnt',
                            'base_fk_ctrl' : 'right_hip_ctrl', # FK Elements
                            'mid_fk_ctrl' : 'right_knee_ctrl',
                            'end_fk_ctrl' : 'right_ankle_ctrl' ,
                            'base_fk_jnt' :  'right_hip_fk_jnt',
                            'mid_fk_jnt' : 'right_knee_fk_jnt',
                            'end_fk_jnt' : 'right_ankle_fk_jnt',
                            'mid_ik_reference' : 'right_kneeSwitch_loc',
                            'end_ik_reference' : 'right_ankleSwitch_loc'
                          }

# Main Form ============================================================================
def build_gui_seamless_ab_fk_ik():
    window_name = "build_gui_seamless_ab_fk_ik"
    if cmds.window(window_name, exists =True):
        cmds.deleteUI(window_name)    

    # Main GUI Start Here =================================================================================
    
    # Build UI
    build_gui_seamless_ab_fk_ik = cmds.window(window_name, title=script_name + '  (v' + script_version + ')',\
                          titleBar=True, mnb=False, mxb=False, sizeable =True)

    cmds.window(window_name, e=True, s=True, wh=[1,1])

    content_main = cmds.columnLayout(adj = True)

    # Title Text
    title_bgc_color = (.4, .4, .4)
    cmds.separator(h=10, style='none') # Empty Space
    cmds.rowColumnLayout(nc=1, cw=[(1, 270)], cs=[(1, 10)], p=content_main) # Window Size Adjustment
    cmds.rowColumnLayout(nc=3, cw=[(1, 10), (2, 200), (3, 50)], cs=[(1, 10), (2, 0), (3, 0)], p=content_main) # Title Column
    cmds.text(" ", bgc=title_bgc_color) # Tiny Empty Green Space
    cmds.text(script_name, bgc=title_bgc_color,  fn="boldLabelFont", align="left")
    cmds.button( l ="Help", bgc=title_bgc_color, c=lambda x:open_gt_tools_documentation())
    cmds.separator(h=5, style='none') # Empty Space
    
    # Body ====================
    body_column = cmds.rowColumnLayout(nc=1, cw=[(1, 260)], cs=[(1,10)], p=content_main)
    
    
    cmds.text('Namespace:')
    namespace_txt = cmds.textField(text='', pht='Namespace:: (Optional)')
    
 
    
    cmds.separator(h=10, style='none') # Empty Space
    
    btn_margin = 5
    cmds.rowColumnLayout(nc=2, cw=[(1, 129),(2, 130)], cs=[(1,0), (2,5)], p=body_column)
    cmds.text('Right Arm:') #R
    cmds.text('Left Arm:') #L
    cmds.separator(h=btn_margin, style='none') # Empty Space
    cmds.separator(h=btn_margin, style='none') # Empty Space
    cmds.button(l ="Toggle", c=lambda x:gt_ab_seamless_fk_ik_toggle(right_arm_seamless_dict, namespace=cmds.textField(namespace_txt, q=True, text=True)), w=130) #R
    cmds.button(l ="Toggle", c=lambda x:gt_ab_seamless_fk_ik_toggle(left_arm_seamless_dict, namespace=cmds.textField(namespace_txt, q=True, text=True)), w=130) #L
    cmds.button(l ="FK to IK", c=lambda x:gt_ab_seamless_fk_ik_switch(right_arm_seamless_dict, 'fk_to_ik', namespace=cmds.textField(namespace_txt, q=True, text=True)), w=130) #R
    cmds.button(l ="FK to IK", c=lambda x:gt_ab_seamless_fk_ik_switch(left_arm_seamless_dict, 'fk_to_ik', namespace=cmds.textField(namespace_txt, q=True, text=True)), w=130) #L
    cmds.button(l ="IK to FK", c=lambda x:gt_ab_seamless_fk_ik_switch(right_arm_seamless_dict, 'ik_to_fk', namespace=cmds.textField(namespace_txt, q=True, text=True)), w=130) #R
    cmds.button(l ="IK to FK", c=lambda x:gt_ab_seamless_fk_ik_switch(left_arm_seamless_dict, 'ik_to_fk', namespace=cmds.textField(namespace_txt, q=True, text=True)), w=130) #L
    cmds.separator(h=btn_margin, style='none') # Empty Space
    
    cmds.rowColumnLayout(nc=2, cw=[(1, 129),(2, 130)], cs=[(1,0), (2,5)], p=body_column)
    cmds.text('Right Leg:') #R
    cmds.text('Left Leg:') #L
    cmds.separator(h=btn_margin, style='none') # Empty Space
    cmds.separator(h=btn_margin, style='none') # Empty Space
    cmds.button(l ="Toggle", c=lambda x:gt_ab_seamless_fk_ik_toggle(right_leg_seamless_dict, namespace=cmds.textField(namespace_txt, q=True, text=True)), w=130) #R
    cmds.button(l ="Toggle", c=lambda x:gt_ab_seamless_fk_ik_toggle(left_leg_seamless_dict, namespace=cmds.textField(namespace_txt, q=True, text=True)), w=130) #L
    cmds.button(l ="FK to IK", c=lambda x:gt_ab_seamless_fk_ik_switch(right_leg_seamless_dict, 'fk_to_ik', namespace=cmds.textField(namespace_txt, q=True, text=True)), w=130) #R
    cmds.button(l ="FK to IK", c=lambda x:gt_ab_seamless_fk_ik_switch(left_leg_seamless_dict, 'fk_to_ik', namespace=cmds.textField(namespace_txt, q=True, text=True)), w=130) #L
    cmds.button(l ="IK to FK", c=lambda x:gt_ab_seamless_fk_ik_switch(right_leg_seamless_dict, 'ik_to_fk', namespace=cmds.textField(namespace_txt, q=True, text=True)), w=130) #R
    cmds.button(l ="IK to FK", c=lambda x:gt_ab_seamless_fk_ik_switch(left_leg_seamless_dict, 'ik_to_fk', namespace=cmds.textField(namespace_txt, q=True, text=True)), w=130) #L
    
    cmds.rowColumnLayout(nc=1, cw=[(1, 260)], cs=[(1,10)], p=content_main)

                                                                                               
    cmds.separator(h=10, style='none') # Empty Space
    
    # Show and Lock Window
    cmds.showWindow(build_gui_seamless_ab_fk_ik)
    cmds.window(window_name, e=True, s=False)
    
    # Set Window Icon
    qw = omui.MQtUtil.findWindow(window_name)
    widget = wrapInstance(long(qw), QWidget)
    icon = QIcon(':/ikSCsolver.svg')
    widget.setWindowIcon(icon)

    # Remove the focus from the textfield and give it to the window
    cmds.setFocus(window_name)

    # Main GUI Ends Here =================================================================================
    
    
    def object_load_handler(operation):
        ''' 
        Function to handle load buttons. It updates the UI to reflect the loaded data.
        
                Parameters:
                    operation (str): String to determine function (Currently either "ik_handle" or "attr_holder")
        
        '''

        # Check If Selection is Valid
        received_valid_element = False
        
        # ikHandle
        if operation == 'ik_handle':
            current_selection = cmds.ls(selection=True, type='ikHandle')
            
            if len(current_selection) == 0:
                cmds.warning("Nothing selected. Please select an ikHandle and try again.")
            elif len(current_selection) > 1:
                cmds.warning("You selected more than one ikHandle! Please select only one")
            elif cmds.objectType(current_selection[0]) == "ikHandle":
                gt_make_ik_stretchy_settings['ik_handle'] = current_selection[0]
                received_valid_element = True
            else:
                cmds.warning("Something went wrong, make sure you selected just one ikHandle and try again.")
            
            # ikHandle Update GUI
            if received_valid_element:
                cmds.button(ik_handle_status, l=gt_make_ik_stretchy_settings.get('ik_handle'), e=True, bgc=(.6, .8, .6), w=130)
            else:
                cmds.button(ik_handle_status, l ="Failed to Load", e=True, bgc=(1, .4, .4), w=130)
           
        # Attr Holder
        if operation == 'attr_holder':
            current_selection = cmds.ls(selection=True)
            if len(current_selection) == 0:
                cmds.warning("Nothing selected. Assuming you don\'t want an attribute holder. To select an attribute holder, select only one object (usually a control curve) and try again.")
                gt_make_ik_stretchy_settings['attr_holder'] = ''
            elif len(current_selection) > 1:
                cmds.warning("You selected more than one object! Please select only one")
            elif cmds.objExists(current_selection[0]):
                gt_make_ik_stretchy_settings['attr_holder'] = current_selection[0]
                received_valid_element = True
            else:
                cmds.warning("Something went wrong, make sure you selected just one object and try again.")
                
            # Attr Holder Update GUI
            if received_valid_element:
                cmds.button(attr_holder_status, l=gt_make_ik_stretchy_settings.get('attr_holder'), e=True, bgc=(.6, .8, .6), w=130)
            else:
                cmds.button(attr_holder_status, l ="Not provided", e=True, bgc=(.2, .2, .2), w=130)
        
    def validate_operation():
        ''' Checks elements one last time before running the script '''
        
        is_valid = False
        stretchy_name = None
        attr_holder = None
        
        stretchy_prefix = cmds.textField(stretchy_system_prefix, q=True, text=True).replace(' ','')
        
        # Name
        if stretchy_prefix != '':
            stretchy_name = stretchy_prefix

        # ikHandle
        if gt_make_ik_stretchy_settings.get('ik_handle') == '':
            cmds.warning('Please load an ikHandle first before running the script.')
            is_valid = False
        else:
            if cmds.objExists(gt_make_ik_stretchy_settings.get('ik_handle')):
                is_valid = True
            else:
                cmds.warning('"' + str(gt_make_ik_stretchy_settings.get('ik_handle')) + '" couldn\'t be located. Make sure you didn\'t rename or deleted the object after loading it')
            
        # Attribute Holder
        if is_valid:
            if gt_make_ik_stretchy_settings.get('attr_holder') != '':
                if cmds.objExists(gt_make_ik_stretchy_settings.get('attr_holder')):
                    attr_holder = gt_make_ik_stretchy_settings.get('attr_holder')
                else:
                    cmds.warning('"' + str(gt_make_ik_stretchy_settings.get('attr_holder')) + '" couldn\'t be located. Make sure you didn\'t rename or deleted the object after loading it. A simpler version of the stretchy system was created.')
            else:
                sys.stdout.write('An attribute holder was not provided. A simpler version of the stretchy system was created.')
            
        # Run Script
        if is_valid:
            if stretchy_name:
                make_stretchy_ik(gt_make_ik_stretchy_settings.get('ik_handle'), stretchy_name=stretchy_name, attribute_holder=attr_holder)
            else:
                make_stretchy_ik(gt_make_ik_stretchy_settings.get('ik_handle'), stretchy_name='temp', attribute_holder=attr_holder)


def gt_ab_seamless_fk_ik_switch(ik_fk_dict, direction='fk_to_ik', namespace=''):
    '''
    Transfer the position of the FK to IK or IK to FK systems in a seamless way, so the animator can easily switch between one and the other
    
            Parameters:
                ik_fk_ns_dict (dict): A dicitionary containg the elements that are part of the system you want to switch
                direction (string): Either "fk_to_ik" or "ik_to_fk". It determines what is the source and what is the target.
                namespace (string): In case the rig has a namespace, it will be used to properly select the controls.
    '''
    ik_fk_ns_dict = {}
    for obj in ik_fk_dict:
        ik_fk_ns_dict[obj] = namespace + ik_fk_dict.get(obj)
    
    
    fk_pairs = [[ik_fk_ns_dict.get('base_ik_jnt'), ik_fk_ns_dict.get('base_fk_ctrl')],
                [ik_fk_ns_dict.get('mid_ik_jnt'), ik_fk_ns_dict.get('mid_fk_ctrl')],
                [ik_fk_ns_dict.get('end_ik_jnt'), ik_fk_ns_dict.get('end_fk_ctrl')]]            
                
    if direction == 'fk_to_ik':

        if ik_fk_dict.get('end_ik_reference') != '':
            cmds.matchTransform(ik_fk_ns_dict.get('end_ik_ctrl'), ik_fk_ns_dict.get('end_ik_reference'), pos=1, rot=1)
        else:
            cmds.matchTransform(ik_fk_ns_dict.get('end_ik_ctrl'), ik_fk_ns_dict.get('end_fk_jnt'), pos=1, rot=1)
        
        cmds.matchTransform(ik_fk_ns_dict.get('pvec_ik_ctrl'), ik_fk_ns_dict.get('mid_ik_reference'), pos=1, rot=1)
        cmds.setAttr(ik_fk_ns_dict.get('switch_ctrl') + '.influenceSwitch', 1)
    if direction == 'ik_to_fk':
        for pair in fk_pairs:
            cmds.matchTransform(pair[1], pair[0], pos=1, rot=1)
        cmds.setAttr(ik_fk_ns_dict.get('switch_ctrl') + '.influenceSwitch', 0)
   
def open_gt_tools_documentation():
    ''' Opens a web browser with the latest release '''
    cmds.showHelp ('https://github.com/TrevisanGMW/gt-tools/tree/master/docs#-gt-auto-biped-rigger-', absolute=True) 
    
def gt_ab_seamless_fk_ik_toggle(ik_fk_dict, namespace=''):
    ''' Calls gt_ab_seamless_fk_ik_switch, but toggles between fk and ik '''
    current_system = cmds.getAttr(namespace + ik_fk_dict.get('switch_ctrl') + '.influenceSwitch')
    if current_system < 0.5:
        gt_ab_seamless_fk_ik_switch(ik_fk_dict, direction='fk_to_ik', namespace=namespace)
    else:
        gt_ab_seamless_fk_ik_switch(ik_fk_dict, direction='ik_to_fk', namespace=namespace)


#Build UI
if __name__ == '__main__':
    build_gui_seamless_ab_fk_ik()