"""
 This script has been modified for Modeling 1.
 GT Screenshot Sender - Send images to your instructor.
 @Guilherme Trevisan - TrevisanGMW@gmail.com - 2021-01-05 - github.com/TrevisanGMW
 Tested on Maya 2018, 2019, 2020 - Windows 10
  
 1.1 - 2021-01-12
 Changed method to viewport only for better compatibility
  
""" 

try:
    from shiboken2 import wrapInstance
except ImportError:
    from shiboken import wrapInstance

try:
    from PySide2 import QtWidgets, QtGui, QtCore
    from PySide2.QtGui import QIcon
    from PySide2.QtWidgets import QWidget
except ImportError:
    from PySide import QtWidgets, QtGui, QtCore
    from PySide.QtGui import QIcon, QWidget

import maya.OpenMayaUI as omui
import maya.utils as utils
import maya.OpenMaya as om
import maya.cmds as cmds
import maya.mel as mel
import threading
import urllib
import base64
import socket
import datetime 
import mimetypes 
import random 
import string 
import copy
import time
import sys
import os
from json import dumps
from json import loads
from httplib2 import Http


# Forced Webhook
hard_coded_webhook = 'https://discord.com/api/webhooks/XXXX'
hard_coded_webhook_name = 'Instructor'

# Script Name
script_name = "Screenshot Sender"

# Versions:
script_version = "1.1"
maya_version = cmds.about(version=True)

# Used to define multipart/form-data boundary
_BOUNDARY_CHARS = string.digits + string.ascii_letters

# Settings
gt_mtod_settings_submit_ss = { 'discord_webhook':hard_coded_webhook,
                          'discord_webhook_name'  : hard_coded_webhook_name,
                          'is_first_time_running' : False,
                          'custom_username' : '',
                          'image_format' : 'jpg',
                          'video_format' : 'mov', 
                          'video_scale_pct' : 40, 
                          'video_compression' : 'Animation', 
                          'video_output_type' : 'qt',
                          'is_new_instance' : True,
                          'is_webhook_valid' : False,
                          'feedback_visibility' : True,
                          'timestamp_visibility' : True }

# Default Settings (Deep Copy)
gt_mtod_settings_submit_ss_default = copy.deepcopy(gt_mtod_settings_submit_ss)   



def build_gui_submit_screenshot():
    ''' Builds the Main GUI for the script '''
    window_name = "build_gui_submit_screenshot"
    if cmds.window(window_name, exists =True):
        cmds.deleteUI(window_name)    

    # Main GUI Start Here =================================================================================
    
    # Build UI
    build_gui_submit_screenshot = cmds.window(window_name, title=' ' + script_name + " - v" + script_version,\
                          titleBar=True, mnb=False, mxb=False, sizeable =True)

    cmds.window(window_name, e=True, s=True, wh=[1,1])
    
    column_main = cmds.columnLayout() 

    form = cmds.formLayout(p=column_main)

    content_main = cmds.columnLayout(adj = True)

    # Title Text
    cmds.separator(h=10, style='none') # Empty Space
    cmds.rowColumnLayout(nc=1, cw=[(1, 270)], cs=[(1, 10)], p=content_main) # Window Size Adjustment
    cmds.rowColumnLayout(nc=4, cw=[(1, 10), (2, 250)], cs=[(1, 10), (2, 0), (3, 0)], p=content_main) # Title Column
    cmds.text(" ", bgc=[.4,.4,.4], h=25) # Tiny Empty Green Space
    cmds.text(script_name, bgc=[.4,.4,.4],  fn="boldLabelFont")
    cmds.separator(h=5, style='none') # Empty Space
    
    # Body ====================
    body_column = cmds.rowColumnLayout(nc=1, cw=[(1, 260)], cs=[(1,10)], p=content_main)
    
    # Generate Images
    # Icon
    icons_folder_dir = cmds.internalVar(userBitmapsDir=True) 
    icon_image = ':/camera.open.svg'
    

        
    # Send Desktop Icon
    send_desktop_btn_ico = icons_folder_dir + 'gt_mtod_send_desktop.png'
    
    if os.path.isdir(icons_folder_dir) and os.path.exists(send_desktop_btn_ico) == False:
        image_enconded = 'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAAsTAAALEwEAmpwYAAAF8WlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4gPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iQWRvYmUgWE1QIENvcmUgNS42LWMxNDggNzkuMTY0MDM2LCAyMDE5LzA4LzEzLTAxOjA2OjU3ICAgICAgICAiPiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPiA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtbG5zOmRjPSJodHRwOi8vcHVybC5vcmcvZGMvZWxlbWVudHMvMS4xLyIgeG1sbnM6cGhvdG9zaG9wPSJodHRwOi8vbnMuYWRvYmUuY29tL3Bob3Rvc2hvcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RFdnQ9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZUV2ZW50IyIgeG1wOkNyZWF0b3JUb29sPSJBZG9iZSBQaG90b3Nob3AgMjEuMCAoV2luZG93cykiIHhtcDpDcmVhdGVEYXRlPSIyMDIwLTExLTAzVDExOjU1OjM4LTA4OjAwIiB4bXA6TW9kaWZ5RGF0ZT0iMjAyMC0xMS0wM1QxMjoyNzoxMi0wODowMCIgeG1wOk1ldGFkYXRhRGF0ZT0iMjAyMC0xMS0wM1QxMjoyNzoxMi0wODowMCIgZGM6Zm9ybWF0PSJpbWFnZS9wbmciIHBob3Rvc2hvcDpDb2xvck1vZGU9IjMiIHBob3Rvc2hvcDpJQ0NQcm9maWxlPSJzUkdCIElFQzYxOTY2LTIuMSIgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDpiZTc1ODU2NC04YThkLTQ2NDUtYmU2Yy1lMmY5ZmQwMWU0YjgiIHhtcE1NOkRvY3VtZW50SUQ9ImFkb2JlOmRvY2lkOnBob3Rvc2hvcDozYjViOWNhMy1lODgwLTgxNGQtYmFjOS1mNTNmNDExMWQ0MDciIHhtcE1NOk9yaWdpbmFsRG9jdW1lbnRJRD0ieG1wLmRpZDo5MGM2ZTQ5My0xZDNkLTNiNGQtODI0ZS1kN2JhZDRlNzQ1MzQiPiA8eG1wTU06SGlzdG9yeT4gPHJkZjpTZXE+IDxyZGY6bGkgc3RFdnQ6YWN0aW9uPSJjcmVhdGVkIiBzdEV2dDppbnN0YW5jZUlEPSJ4bXAuaWlkOjkwYzZlNDkzLTFkM2QtM2I0ZC04MjRlLWQ3YmFkNGU3NDUzNCIgc3RFdnQ6d2hlbj0iMjAyMC0xMS0wM1QxMTo1NTozOC0wODowMCIgc3RFdnQ6c29mdHdhcmVBZ2VudD0iQWRvYmUgUGhvdG9zaG9wIDIxLjAgKFdpbmRvd3MpIi8+IDxyZGY6bGkgc3RFdnQ6YWN0aW9uPSJzYXZlZCIgc3RFdnQ6aW5zdGFuY2VJRD0ieG1wLmlpZDpiZTc1ODU2NC04YThkLTQ2NDUtYmU2Yy1lMmY5ZmQwMWU0YjgiIHN0RXZ0OndoZW49IjIwMjAtMTEtMDNUMTI6Mjc6MTItMDg6MDAiIHN0RXZ0OnNvZnR3YXJlQWdlbnQ9IkFkb2JlIFBob3Rvc2hvcCAyMS4wIChXaW5kb3dzKSIgc3RFdnQ6Y2hhbmdlZD0iLyIvPiA8L3JkZjpTZXE+IDwveG1wTU06SGlzdG9yeT4gPC9yZGY6RGVzY3JpcHRpb24+IDwvcmRmOlJERj4gPC94OnhtcG1ldGE+IDw/eHBhY2tldCBlbmQ9InIiPz7PHrkDAAAFDklEQVRYhe2XT2gUVxzHP+/N7M5kdetG6+ISY1sRak38Q7L9RwyUhlioh4aI1nry3EKgiKcWUS8tVQjkkAZbpLSRVg/anEzFYGJzsU5AAqUhpUuyQdckWje7+bPZnZnXQ3bDanbWikUv/Z5m5v3e+33e7733e78RSimep/ShoaH9QBOQAZ4FjQ5kgV/r6+t/1oEjruvWAdozcA6A4zhOIpE4EI1G0YG6qakpZ3BwUOq6LmzbRgjh2VkIUbJdKcXjllNKiWEYNDc3+zZs2LAR+FQH1JUrV/xdXV0xKeVV13V9QA7wplhqkyW+u5RZRiklVVVVq2tqat6LRCIvAm/oAJqmKV3Xe/r7+6uEEE1CCD/gPMa5KnqnjD2AVErds237m4GBgW8jkcg1YC0sbQiy2SyVlZWmlPJgJpPJ3rx5UxmGoQkhSs4mH+oVESplr5RCCEF9fX1ofHz85IkTJ+jv7884jgOg9EJoNE3LAvT09PhPnTqVBK4Bq8rMqhRcyWULBALi3Llzb7muG3Qc50MppZ0HWIpAXhLAMAyAHyzLaivjfFnRaPSxNtevXw8qpX6LxWKbWDpt9kNOAdRSXFV+h1f8G+dPIqWUVErJYucPATyicifgP5UXwDPT/wArAMql4adUyYFXACwsLHgaP4XmgYyUKwOuw3K2EoCorKxk27ZtGvBqmQGXR7Isq/DolrEPSCkDuq4X+i4fxeVMaNu2C7Bnzx62b9/eksvl3lFKlYyEEIISbV6XkBJCSJ/PVz07O5sB/CsAbNvmzp07i1NTUx/39vZ2GoaxxjRN23XdkjWCKLFRXNcteRcUNDs7+2BwcLBS1/VU8bWtAyIUColIJKKFw+GvOzo65oBawKR8WL2uY09pmpY+dOhQDDhSmIOwLEtls1nu379/LxwOT2iatoD3JtTyTh7k3yuANBAAVrO0DOWqEiNvuxUgGo1mdOBYX1/fSb/fvzYWi2n5imfFTKSUpNNpx3EcGhsb1/n9fjE5OTlXVVUVjMfjMyMjI2nTNCt8Pp/wgsiHXqbT6eTo6GgIMHXgi66uropMJrNFKeXLd14RgVwup9LptLtv377Vzc3NzRcuXMidP3/e6OjoWDRNc017e/v49PT0YCgUWi+l9HtBSClxXZdUKvU3MKoD9u3bt48BL1BmDY8ePbqupaWlzTCMg8lkcrS7u3vL3bt3OxKJxPDOnTvPdnZ2vhYIBL7fu3fvJ0CQ8kWuyPuaFUXnuFgm0AC8DmwCaoBXgOrh4eGR48ePr4/H46PAQSDe1tZ2ZPfu3V9t3rxZptPpqWAwaAG/AxPAQDQaHfYk8QDYqpT6BdgohJDz8/OZoaGh1KVLl8StW7fWp1Kpn4DPLcv6q1CQNDU1tYbD4Y6Ghoaquro65ff7RS6XyyUSiT9bW1s/AkpC6KU+AqYQYtPAwMD86dOnjUwmY87Nzc1ls9leoBu4YVnWg+IOfX19F4EbV69e/cDn8x0A3jxz5oxp2/ZW4Evg/ScBACAYDAZ27NgxcPjw4YvBYFCEQqFF0zSrgZdYWkdlWVZxVayA+ZmZmbPT09PfhcPh9rGxsVVAtZcPL4DU4uLi2K5du16ura1t1HX97bxD4bplc00BXAWDQaSUvrGxsSxlNrcXwGQ8Hu+cmJj4LJlMviCEkHkAz7+fR7KzkFKilHIuX77sB/7wAhCFur2EVgH7gXdZuk6L5ZXtHh2o8APzI9DvCfA89Q9+dgWL9W/IeAAAAABJRU5ErkJggg=='
        image_64_decode = base64.decodestring(image_enconded)
        image_result = open(send_desktop_btn_ico, 'wb')
        image_result.write(image_64_decode)
        image_result.close()
    
    if os.path.exists(send_desktop_btn_ico) == False:
        send_desktop_btn_ico = 'fluidGetExamples.png'


    cmds.separator(h=5)
    cmds.separator(h=7, style='none') # Empty Space
    cmds.rowColumnLayout(nc=2, cw=[(1, 100),(2, 143),(4, 37)], cs=[(1, 18),(2, 0),(3, 0),(4, 0)], p=content_main)
    cmds.text(l='Webhoook Name:', align="center", fn="boldLabelFont")
    webhook_name_text = cmds.text(l='...', align="center", fn="tinyBoldLabelFont")
    cmds.separator(h=7, style='none') # Empty Space
    
    cmds.rowColumnLayout(nc=3, cw=[(1, 100),(2, 50),(3, 100),(4, 50)], cs=[(1, 10),(2, 0),(3, 0),(4, 0)], p=content_main)
    
    cmds.text(l='Web Response:', align="center", fn="boldLabelFont")
    status_code_text = cmds.text(l='', align="center")
    status_message_text = cmds.text(l='', align="center")
    
    
    if gt_mtod_settings_submit_ss['is_first_time_running'] == True:
        cmds.text(webhook_name_text, e=True, l=hard_coded_webhook_name)#, bgc= [1,1,0]) # MODIFIED
    else:
        if 'Error' in gt_mtod_settings_submit_ss.get('discord_webhook_name') or 'Missing Webhook' in gt_mtod_settings_submit_ss.get('discord_webhook_name'):
            cmds.text(webhook_name_text, e=True, l=gt_mtod_settings_submit_ss.get('discord_webhook_name'), bgc=[.5,0,0])
        else:
            cmds.text(webhook_name_text, e=True, l=gt_mtod_settings_submit_ss.get('discord_webhook_name'), nbg=True)
    
    cmds.rowColumnLayout(nc=1, cw=[(1, 260)], cs=[(1, 10)], p=content_main) 
    cmds.separator(h=7, style='none') # Empty Space
    cmds.separator(h=5)
    
    stored_username_exists = cmds.optionVar(exists=("gt_submit_message_username"))
    if stored_username_exists:
        try:
            stored_username = str(cmds.optionVar(q=("gt_submit_message_username")))
        except:
            stored_username = ''
    else:
        stored_username = ''
    
    cmds.separator(h=7, style='none') # Empty Space
    attached_message_txtfield = cmds.textField(pht='Type your name or nickname here...', text=stored_username, cc=lambda x:store_name(cmds.textField(attached_message_txtfield, q=True, text=True)))
    cmds.separator(h=10, style='none') # Empty Space

    def store_name(name):
        cmds.optionVar( sv=('gt_submit_message_username', name) )

    
    screenshot_btn_color = [.4,.4,.4]
    cmds.rowColumnLayout(nc=1, cw=[(1, 260),(2, 1),(3, 5)], cs=[(1, 10),(2, 0),(3, 0)], p=content_main) 
    send_desktop_btn = cmds.iconTextButton( style='iconAndTextVertical', image1=send_desktop_btn_ico, label='Send Screenshot to Instructor',\
                                            statusBarMessage='This button will take a screenshot to your instructor.',\
                                            olc=[1,0,0] , enableBackground=True, bgc=screenshot_btn_color, h=80,\
                                            command=lambda: send_maya_window())
    
    cmds.separator(h=2, style='none') # Empty Space           
    cmds.separator(h=10, style='none') # Empty Space
    
    
    # Functions for the buttons -----------
    def get_date_time_message():
        ''' 
        Returns formated string of date and time to be used as a message 
        
                    Returns:
                        date_and_time (str): A formated string containing current date and time.
        
        ''' 
        now = datetime.datetime.now()
        return now.strftime("Date: %m/%d/%Y - Time: %H:%M:%S")
        
    def get_username(ignore_machine=False):
        ''' 
        Returns string to be used as username, it extracts it from the computer's username.
        A custom username may be used, in which case the function returns the custom username followed by the computer's username.
           
                    Returns:
                        username (str): A string composed of custom username (if it exists) and the computer's username
        ''' 
        stored_username_exists = cmds.optionVar(exists=("gt_submit_message_username"))
        if stored_username_exists:
            try:
                stored_username = str(cmds.optionVar(q=("gt_submit_message_username")))
            except:
                stored_username = ''

        user_name = stored_username + ' (' + socket.gethostname() + ')'

        if ignore_machine:
            return user_name
        else:
            return stored_username
    
    
    def update_text_status(error=False):
        ''' 
        Updates UI texts to say "Uploading" or "Error" 
        
                Parameters:
                    error (bool): Determines if it will update it to be red and say error or yellow to say Uploading. Default = Uploading (False)
        
        ''' 
        if not error:
            cmds.text(status_message_text, e=True, l='Uploading', bgc=(1, 1, 0))
            cmds.text(status_code_text, e=True, l='...', bgc=(1, 1,0))
        else:
            cmds.text(status_message_text, e=True, l='...', bgc=(.5, 0, 0))
            cmds.text(status_code_text, e=True, l='Error', bgc=(.5, 0, 0))

    def clear_attached_message(response):
        ''' 
        Clears the attached message when a success code is received
        
                Parameters:
                    response (dict): A dictionary response received from a HTTP object after post/get operation.
        
        '''
        if len(response) >= 1:
            status_value = response[0].status
            success_codes = [200, 201, 202, 203, 204, 205, 206]

            if status_value in success_codes: 
                pass#cmds.textField(attached_message_txtfield, e=True, text='')

    
    def parse_sending_response(response):
        '''
        Processes response received when sending an image/video and updates UI text accordingly
        
                Parameters:
                    response (dict): A dictionary response received from a HTTP object after post/get operation.
        
        '''
        if len(response) >= 1:
            status_value = response[0].status
            reason_value = response[0].reason
            success_codes = [200, 201, 202, 203, 204, 205, 206]

            if status_value in success_codes: 
                cmds.text(status_message_text, e=True, l=reason_value, bgc=(0, 0.5, 0))
                cmds.text(status_code_text, e=True, l=status_value, bgc=(0, 0.5,0))
            else: # Error
                cmds.text(status_message_text, e=True, l=reason_value, bgc=(0.5, 0, 0))
                cmds.text(status_code_text, e=True, l=status_value, bgc=(0.5, 0,0))
        else :
            cmds.text(status_message_text, e=True, l='Can\'t read response', bgc=(0.5, 0,0))
            cmds.text(status_code_text, e=True, l='Can\'t read response', bgc=(0.5, 0,0))
            
    def attached_text_message(operation_name, response):
        '''
        Attaches message to the content sent according the response received and the content of the message.
        
                Parameters:
                    operation_name (string): Name of the operation, used to write an output message.
                    response (dict): A dictionary response received from a HTTP object after post/get operation. (This should be the response of the previous operation)
        
        '''
        if len(response) >= 1:
            status_value = response[0].status
            success_codes = [200, 201, 202, 203, 204, 205, 206]
            if status_value in success_codes: 
                try:  
                    upload_message = cmds.textField(attached_message_txtfield, q=True, text=True)
                    if upload_message.strip() != '': 
                        def threaded_upload():
                            try:
                                discord_post_message(get_username(), upload_message, gt_mtod_settings_submit_ss.get('discord_webhook'))
                                utils.executeDeferred(response_inview_feedback, operation_name, response, display_inview=gt_mtod_settings_submit_ss.get('feedback_visibility'))
                                utils.executeDeferred(clear_attached_message, response)
                            except Exception as e:
                                print(e)
                            
                        thread = threading.Thread(None, target = threaded_upload)
                        thread.start()
                    else:
                        response_inview_feedback(operation_name, response, display_inview=gt_mtod_settings_submit_ss.get('feedback_visibility'))
                except:
                    pass
        
                    
    def disable_buttons():
        ''' Disable buttons so user don't accidently send multiple requests at once ''' 
        cmds.iconTextButton(send_desktop_btn, e=True, enable=False)
       
    
    def enable_buttons():
        ''' Enable buttons after finishing previously requested function ''' 
        cmds.iconTextButton(send_desktop_btn, e=True, enable=True)
   

    # Button Functions ----------
    webhook_error_message = 'Sorry, something went wrong. Please review your webhook and settings.'
    def send_dekstop_screenshot():
        ''' Attempts to send a desktop screenshot using current settings '''
        if gt_mtod_settings_submit_ss.get('is_new_instance'):
            update_discord_webhook_validity(gt_mtod_settings_submit_ss.get('discord_webhook'))
        
        if gt_mtod_settings_submit_ss.get('is_webhook_valid'):
            try:
                update_text_status()
                temp_path = generate_temp_file(gt_mtod_settings_submit_ss.get('image_format'))
                temp_desktop_ss_file = capture_desktop_screenshot(temp_path)
                if gt_mtod_settings_submit_ss.get('timestamp_visibility'):
                    upload_message = get_date_time_message()
                else:
                    upload_message = ''
                def threaded_upload():
                    try:
                        utils.executeDeferred(disable_buttons)
                        response = discord_post_attachment(get_username(), upload_message, temp_desktop_ss_file, gt_mtod_settings_submit_ss.get('discord_webhook'))
                        utils.executeDeferred(enable_buttons)
                        utils.executeDeferred(parse_sending_response, response)
                        utils.executeDeferred('', 'desktop screenshot', response)
                    except:
                        update_text_status(error=True)
                        cmds.warning(webhook_error_message)
                    
                
                thread = threading.Thread(None, target = threaded_upload)
                thread.start()

            except:
                update_text_status(error=True)
                cmds.warning(webhook_error_message)
        else:
            cmds.warning(webhook_error_message)
    
    def send_maya_window():
        ''' Attempts to send an image of the maya window using current settings '''
        if gt_mtod_settings_submit_ss.get('is_new_instance'):
            update_discord_webhook_validity(gt_mtod_settings_submit_ss.get('discord_webhook'))
        
        if gt_mtod_settings_submit_ss.get('is_webhook_valid'):
            try:  
                update_text_status()
                temp_path = generate_temp_file(gt_mtod_settings_submit_ss.get('image_format'))
                temp_img_file = capture_app_window(temp_path)
                if gt_mtod_settings_submit_ss.get('timestamp_visibility'):
                    upload_message = get_date_time_message()
                else:
                    upload_message = ''                  
                def threaded_upload():
                    try:
                        utils.executeDeferred(disable_buttons)
                        response = discord_post_attachment(get_username(), get_username() + ' - ' + upload_message, temp_img_file, gt_mtod_settings_submit_ss.get('discord_webhook'))
                        utils.executeDeferred(enable_buttons)
                        utils.executeDeferred(parse_sending_response, response)
                        utils.executeDeferred('', 'Maya window screenshot', response)
                    except:
                        update_text_status(error=True)
                        cmds.warning(webhook_error_message)
                    
                thread = threading.Thread(None, target = threaded_upload)
                thread.start()
            except:
                update_text_status(error=True)
                cmds.warning(webhook_error_message)
        else:
            cmds.warning(webhook_error_message)
        
    def send_viewport_only():
        ''' Attempts to send an image of the active viewport using current settings '''
        if gt_mtod_settings_submit_ss.get('is_new_instance'):
            update_discord_webhook_validity(gt_mtod_settings_submit_ss.get('discord_webhook'))
            
        if gt_mtod_settings_submit_ss.get('is_webhook_valid'):
            try:
                update_text_status()
                temp_path = generate_temp_file(gt_mtod_settings_submit_ss.get('image_format'))
                if maya_version in ['2017','2018','2019']:
                    temp_img_file = capture_viewport_playblast(temp_path)
                else:
                    temp_img_file = capture_viewport(temp_path)
                if gt_mtod_settings_submit_ss.get('timestamp_visibility'):
                    upload_message = get_date_time_message()
                else:
                    upload_message = ''
                def threaded_upload():
                    try:
                        utils.executeDeferred(disable_buttons)
                        response = discord_post_attachment(get_username(), get_username(True) + ' - ' + upload_message, temp_img_file, gt_mtod_settings_submit_ss.get('discord_webhook'))
                        utils.executeDeferred(enable_buttons)
                        utils.executeDeferred(parse_sending_response, response)
                        utils.executeDeferred('', 'viewport screenshot', response)
                    except:
                        update_text_status(error=True)
                        cmds.warning(webhook_error_message)
                    
                thread = threading.Thread(None, target = threaded_upload)
                thread.start()
            except:
                update_text_status(error=True)
                cmds.warning(webhook_error_message)
        else:
            cmds.warning(webhook_error_message)
            
    def send_animated_playblast():
        ''' Attempts to record a playblast and upload it using the current settings '''
        if gt_mtod_settings_submit_ss.get('is_new_instance'):
            update_discord_webhook_validity(gt_mtod_settings_submit_ss.get('discord_webhook'))
        
        if gt_mtod_settings_submit_ss.get('is_webhook_valid'):
            try:
                update_text_status()
                current_scene_name = cmds.file(q=True, sn=True).split('/')[-1]
                if current_scene_name == '': # If not saved
                    current_scene_name ='never_saved_untitled_scene'
                else:
                    if current_scene_name.endswith('.ma') or current_scene_name.endswith('.mb'):
                        current_scene_name=current_scene_name[:-3]

                temp_path = generate_temp_file( gt_mtod_settings_submit_ss.get('video_format'), file_name=current_scene_name)
                disable_buttons() # This needs to happen before creating the playblast to avoid multiple clicks
                temp_playblast_file = capture_playblast_animation(temp_path, gt_mtod_settings_submit_ss.get('video_scale_pct'), gt_mtod_settings_submit_ss.get('video_compression'), gt_mtod_settings_submit_ss.get('video_output_type') )
                
                if gt_mtod_settings_submit_ss.get('timestamp_visibility'):
                    upload_message = get_date_time_message()
                else:
                    upload_message = ''
                
                def threaded_upload():
                    try:
                        response = discord_post_attachment(get_username(), upload_message, temp_playblast_file, gt_mtod_settings_submit_ss.get('discord_webhook'))
                        utils.executeDeferred(enable_buttons)
                        utils.executeDeferred(parse_sending_response, response)
                        utils.executeDeferred(attached_text_message, 'playblast', response)
                    except:
                        update_text_status(error=True)
                        cmds.warning(webhook_error_message)
                        utils.executeDeferred(enable_buttons)
                    finally:
                        utils.executeDeferred(enable_buttons)
                    
                thread = threading.Thread(None, target = threaded_upload)
                thread.start()
            except:
                update_text_status(error=True)
                cmds.warning(webhook_error_message)
                enable_buttons()

        else:
            cmds.warning(webhook_error_message)


    def send_message_only():
        ''' Attempts to send the message only (no images/videos) using current settings '''
        if gt_mtod_settings_submit_ss.get('is_new_instance'):
            update_discord_webhook_validity(gt_mtod_settings_submit_ss.get('discord_webhook'))
        
        if gt_mtod_settings_submit_ss.get('is_webhook_valid'):
            try:  
                upload_message = cmds.textField(attached_message_txtfield, q=True, text=True)
                if upload_message.strip() != '':
                    update_text_status()
                    def threaded_upload():
                        try:
                            utils.executeDeferred(disable_buttons)
                            response = discord_post_message(get_username(), upload_message, gt_mtod_settings_submit_ss.get('discord_webhook'))
                            utils.executeDeferred(enable_buttons)
                            utils.executeDeferred(parse_sending_response, response)
                            utils.executeDeferred(response_inview_feedback, 'message', response, display_inview=gt_mtod_settings_submit_ss.get('feedback_visibility'))
                            utils.executeDeferred(clear_attached_message, response)
                        except:
                            update_text_status(error=True)
                            cmds.warning(webhook_error_message)
                        
                    thread = threading.Thread(None, target = threaded_upload)
                    thread.start()
                else:
                    cmds.warning('Your message is empty, please type something in case you want to send only a message.')
            except:
                update_text_status(error=True)
                cmds.warning(webhook_error_message)
        else:
            cmds.warning(webhook_error_message)

    def send_model_obj():
        ''' Attempts to export selected model as an OBJ file and upload it using the current settings '''
        if gt_mtod_settings_submit_ss.get('is_new_instance'):
            update_discord_webhook_validity(gt_mtod_settings_submit_ss.get('discord_webhook'))
        
        if gt_mtod_settings_submit_ss.get('is_webhook_valid'):
            selection = cmds.ls(selection=True)
            if len(selection) > 0:
                try:
                    update_text_status()
       
                    # Determine naming
                    if len(selection) == 1:
                        export_name = selection[-1]
                    else:
                        export_name = str(len(selection)).zfill(2) + '_selected_objects'

                    temp_path = generate_temp_file( 'obj', file_name=export_name)
                    disable_buttons() 
               
                    temp_exported_obj = cmds.file(temp_path, pr=1, typ="OBJexport",es=1, f=True, op="groups=0; ptgroups=0; materials=0; smoothing=0; normals=0")
                    
                    if gt_mtod_settings_submit_ss.get('timestamp_visibility'):
                        upload_message = get_date_time_message()
                    else:
                        upload_message = ''
                    
                    def threaded_upload():
                        try:
                            response = discord_post_attachment(get_username(), upload_message, temp_exported_obj, gt_mtod_settings_submit_ss.get('discord_webhook'))
                            utils.executeDeferred(enable_buttons)
                            utils.executeDeferred(parse_sending_response, response)
                            utils.executeDeferred(attached_text_message, 'OBJ file', response)
                        except:
                            update_text_status(error=True)
                            cmds.warning(webhook_error_message)
                            utils.executeDeferred(enable_buttons)
                        finally:
                            utils.executeDeferred(enable_buttons)
                        
                    thread = threading.Thread(None, target = threaded_upload)
                    thread.start()
                except:
                    update_text_status(error=True)
                    cmds.warning(webhook_error_message)
                    enable_buttons()
            else:
                cmds.warning('Nothing selected. Please, select what you want to send.')
        else:
            cmds.warning(webhook_error_message)

    def send_model_fbx():
        ''' Attempts to export selected model as an FBX file and upload it using the current settings '''
        if gt_mtod_settings_submit_ss.get('is_new_instance'):
            update_discord_webhook_validity(gt_mtod_settings_submit_ss.get('discord_webhook'))
        
        if gt_mtod_settings_submit_ss.get('is_webhook_valid'):
            selection = cmds.ls(selection=True)
            if len(selection) > 0:
                try:
                    update_text_status()
       
                    # Determine naming
                    if len(selection) == 1:
                        export_name = selection[-1]
                    else:
                        export_name = str(len(selection)).zfill(2) + '_selected_objects'

                    temp_path = generate_temp_file( 'fbx', file_name=export_name)
                    disable_buttons() 
               
                    cmds.FBXExport('-file', temp_path, '-s')
                    print(temp_path)
                    
                    if gt_mtod_settings_submit_ss.get('timestamp_visibility'):
                        upload_message = get_date_time_message()
                    else:
                        upload_message = ''
                    
                    def threaded_upload():
                        try:
                            response = discord_post_attachment(get_username(), upload_message, temp_path, gt_mtod_settings_submit_ss.get('discord_webhook'))
                            utils.executeDeferred(enable_buttons)
                            utils.executeDeferred(parse_sending_response, response)
                            utils.executeDeferred(attached_text_message, 'FBX file', response)
                        except:
                            update_text_status(error=True)
                            cmds.warning(webhook_error_message)
                            utils.executeDeferred(enable_buttons)
                        finally:
                            utils.executeDeferred(enable_buttons)
                        
                    thread = threading.Thread(None, target = threaded_upload)
                    thread.start()
                except:
                    update_text_status(error=True)
                    cmds.warning(webhook_error_message)
                    enable_buttons()
            else:
                cmds.warning('Nothing selected. Please, select what you want to send.')
        else:
            cmds.warning(webhook_error_message)


    # Show and Lock Window
    cmds.showWindow(build_gui_submit_screenshot)
    cmds.window(window_name, e=True, s=False)
    
    # Set Window Icon
    qw = omui.MQtUtil.findWindow(window_name)
    widget = wrapInstance(long(qw), QWidget)
    icon = QIcon(icon_image)
    
    widget.setWindowIcon(icon)

    # Main GUI Ends Here =================================================================================

# Creates Help GUI
def build_gui_help_maya_to_discord():
    ''' Builds the Help UI for GT Maya to Discord '''
    window_name = "build_gui_help_maya_to_discord"
    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name, window=True)

    cmds.window(window_name, title= script_name + " Help", mnb=False, mxb=False, s=True)
    cmds.window(window_name, e=True, s=True, wh=[1,1])

    main_column = cmds.columnLayout(p= window_name)
   
    # Title Text
    cmds.separator(h=12, style='none') # Empty Space
    cmds.rowColumnLayout(nc=1, cw=[(1, 310)], cs=[(1, 10)], p=main_column) # Window Size Adjustment
    cmds.rowColumnLayout(nc=1, cw=[(1, 300)], cs=[(1, 10)], p=main_column) # Title Column
    cmds.text(script_name + " Help", bgc=[.4,.4,.4],  fn="boldLabelFont", align="center")
    cmds.separator(h=10, style='none', p=main_column) # Empty Space
    
    # Body ====================
    help_font = 'smallPlainLabelFont'
    cmds.rowColumnLayout(nc=1, cw=[(1, 300)], cs=[(1,10)], p=main_column)
    cmds.text(l=script_name + ' allows you to quickly send', align="center")
    cmds.text(l='images and videos (playblasts) from Maya to Discord', align="center")
    cmds.text(l='using a Discord Webhook to bridge the two programs.', align="center")
    cmds.separator(h=10, style='none') # Empty Space
    cmds.text(l='Webhooks:', align="center", fn="boldLabelFont")
    cmds.text(l='A webhook (a.k.a. web callback or HTTP push API) is a way for', align="center", font=help_font)
    cmds.text(l='an app to provide other applications with real-time information.', align="center", font=help_font)
    cmds.text(l='You can use it to send messages to text channels without', align="center", font=help_font)
    cmds.text(l='needing the discord application.', align="center", font=help_font)
    cmds.separator(h=10, style='none') # Empty Space
    cmds.text(l='How to get a Webhook URL:', align="center", fn="boldLabelFont")
    cmds.text(l='If you own a Discord server or you have the correct privileges, ', align="center", font=help_font)
    cmds.text(l='you can go to the settings to create a Webhook URL.', align="center", font=help_font)
    cmds.separator(h=7, style='none') # Empty Space
    cmds.text(l='To create one go to:', align="center", font=help_font)
    cmds.text(l='Discord > Server > Server Settings > Webhooks > Create Webhook', align="center", font=help_font)
    cmds.text(l='Give your webhook a name and select what channel it will operate.', align="center", font=help_font)
    cmds.text(l='Copy the "Webhook URL" and load it in the setttings for this script.', align="center", font=help_font)
    cmds.separator(h=7, style='none') # Empty Space
    cmds.text(l='If you\'re just an user in the server, you\'ll have to ask the', align="center", font=help_font)
    cmds.text(l='administrator of the server to provide you with a Webhook URL.', align="center", font=help_font)
    cmds.separator(h=10, style='none') # Empty Space
    cmds.text(l='Send Buttons:', align="center", fn="boldLabelFont")
    cmds.text(l='Send Message Only: Sends only the attached message', align="center", font=help_font)
    cmds.text(l='(Use the textfield above the buttons to type your message)', align="center", font=help_font)
    cmds.separator(h=10, style='none') # Empty Space
    cmds.text(l='Send Desktop Screenshot: Sends a screenshot of your desktop.', align="center", font=help_font)
    cmds.text(l='(This includes other programs and windows that are open)', align="center", font=help_font)
    cmds.separator(h=7, style='none') # Empty Space
    cmds.text(l='Send Maya Window: Sends only the main Maya window.', align="center", font=help_font)
    cmds.text(l='(This ignores other windows, even within Maya)', align="center", font=help_font)
    cmds.separator(h=7, style='none') # Empty Space
    cmds.text(l='Send Viewport: Sends an image of the active viewport', align="center", font=help_font)
    cmds.text(l='(Includes Heads Up Display text, but no UI elements)', align="center", font=help_font)
    cmds.separator(h=7, style='none') # Empty Space
    cmds.text(l='Send Playblast: Sends a playblast video', align="center", font=help_font)
    cmds.text(l='(Use the script settings to determine details about the video)', align="center", font=help_font)
    cmds.separator(h=7, style='none') # Empty Space
    cmds.text(l='Send OBJ/FBX: Sends a model using the chosen format', align="center", font=help_font)
    cmds.text(l='For settings, go to "File > Export Selection... > Options"', align="center", font=help_font)
    cmds.separator(h=7, style='none') # Empty Space
    cmds.text(l='Settings:', align="center", fn="boldLabelFont")
    cmds.text(l='The settings are persistent, which means they will stay the same', align="center", font=help_font)
    cmds.text(l='between Maya sessions.', align="center", font=help_font)
    cmds.separator(h=7, style='none') # Empty Space
    cmds.text(l='Custom Username:', align="center", font=help_font)
    cmds.text(l='Nickname used when posting content through the webhook.', align="center", font=help_font)
    cmds.separator(h=7, style='none') # Empty Space
    cmds.text(l='Image & Video Format', align="center", font=help_font)
    cmds.text(l='Extension used for the image and video files.', align="center", font=help_font)
    cmds.separator(h=7, style='none') # Empty Space
    cmds.text(l='Video Options:', align="center", font=help_font)
    cmds.text(l='Determines the settings used when recording a playblast.', align="center", font=help_font)
    cmds.separator(h=7, style='none') # Empty Space
    cmds.text(l='Feedback and Timestamp Options:', align="center", font=help_font)
    cmds.text(l='Determines feedback visibility and timestamp use.', align="center", font=help_font)
    cmds.separator(h=10, style='none') # Empty Space
    cmds.text(l='Limitations:', align="center", fn="boldLabelFont")
    cmds.text(l='Discord has a limit of 8MB for free users and 50MB for paid users', align="center", font=help_font)
    cmds.text(l='for when uploading a file. If you get the error "Payload Too Large"', align="center", font=help_font)
    cmds.text(l='it means your file exceeds the limits. Try changing the settings.', align="center", font=help_font)
    
    cmds.separator(h=15, style='none') # Empty Space
    cmds.rowColumnLayout(nc=2, cw=[(1, 140),(2, 140)], cs=[(1,10),(2, 0)], p=main_column)
    cmds.text('Guilherme Trevisan  ')
    cmds.text(l='<a href="mailto:trevisangmw@gmail.com">TrevisanGMW@gmail.com</a>', hl=True, highlightColor=[1,1,1])
    cmds.rowColumnLayout(nc=2, cw=[(1, 140),(2, 140)], cs=[(1,10),(2, 0)], p=main_column)
    cmds.separator(h=15, style='none') # Empty Space
    cmds.text(l='<a href="https://github.com/TrevisanGMW">Github</a>', hl=True, highlightColor=[1,1,1])
    cmds.separator(h=7, style='none') # Empty Space
    
    # Close Button 
    cmds.rowColumnLayout(nc=1, cw=[(1, 300)], cs=[(1,10)], p=main_column)
    cmds.separator(h=10, style='none')
    cmds.button(l='Reset Persistent Settings', h=30, c=lambda args: reset_persistent_settings_maya_to_discord())
    cmds.separator(h=5, style='none')
    cmds.button(l='OK', h=30, c=lambda args: close_help_gui())
    cmds.separator(h=8, style='none')
    
    # Show and Lock Window
    cmds.showWindow(window_name)
    cmds.window(window_name, e=True, s=False)
    
    # Set Window Icon
    qw = omui.MQtUtil.findWindow(window_name)
    widget = wrapInstance(long(qw), QWidget)
    icon = QIcon(':/question.png')
    widget.setWindowIcon(icon)
    
    def close_help_gui():
        if cmds.window(window_name, exists=True):
            cmds.deleteUI(window_name, window=True)




def build_gui_settings_maya_to_discord():
    ''' Builds the Settings UI for GT Maya to Discord '''
    window_name = "build_gui_settings_maya_to_discord"
    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name, window=True)

    cmds.window(window_name, title= script_name + " Settings", mnb=False, mxb=False, s=True)
    cmds.window(window_name, e=True, s=True, wh=[1,1])


    main_column = cmds.columnLayout(p= window_name)
   
    # Title Text
    cmds.separator(h=12, style='none') # Empty Space
    cmds.rowColumnLayout(nc=1, cw=[(1, 310)], cs=[(1, 10)], p=main_column) # Window Size Adjustment
    cmds.rowColumnLayout(nc=1, cw=[(1, 300)], cs=[(1, 10)], p=main_column) # Title Column
    cmds.text(script_name + " Settings", bgc=[.4,.4,.4],  fn="boldLabelFont", align="center")
    cmds.separator(h=10, style='none', p=main_column) # Empty Space
    
    
    # Current Settings =================
    current_image_format = gt_mtod_settings_submit_ss.get('image_format')
    current_video_format = gt_mtod_settings_submit_ss.get('video_format')
    current_webhook = ''
    current_custom_username = ''
    if not gt_mtod_settings_submit_ss.get('is_first_time_running'):
        if gt_mtod_settings_submit_ss.get('discord_webhook') != '':
            current_webhook = gt_mtod_settings_submit_ss.get('discord_webhook')
        if gt_mtod_settings_submit_ss.get('custom_username') != '':
            current_custom_username = gt_mtod_settings_submit_ss.get('custom_username')
    current_video_scale = gt_mtod_settings_submit_ss.get('video_scale_pct')
    current_compression = gt_mtod_settings_submit_ss.get('video_compression')
    current_output_type = gt_mtod_settings_submit_ss.get('video_output_type')
    
    # Body ====================
    cmds.rowColumnLayout(nc=1, cw=[(1, 300)], cs=[(1,10)], p=main_column) 
    
    cmds.text(l='Discord Webhook Url', align="center")
    cmds.separator(h=5, style='none') # Empty Space
    new_webhook_input = cmds.textField(pht='https://discordapp.com/api/webhooks/...', text=current_webhook, font= 'smallPlainLabelFont', enable=False) # MODIFIED
    
    
    cmds.separator(h=10, style='none') # Empty Space
    cmds.rowColumnLayout(nc=3, cw=[(1, 120),(2, 85),(3, 85)], cs=[(1,10),(2,5),(3,5)], p=main_column)
    
    cmds.text(l='Custom Username ', align="center")
    cmds.text(l='Image Format ', align="center")
    cmds.text(l='Video Format ', align="center")
    new_username_input = cmds.textField(pht='username (not required)', text=current_custom_username, font= 'smallPlainLabelFont')
    new_image_format_input = cmds.textField(pht='jpg', text=current_image_format, font= 'smallPlainLabelFont')
    new_video_format_input = cmds.textField(pht='mov', text=current_video_format, font= 'smallPlainLabelFont')
    

    cmds.separator(h=10, style='none') # Empty Space
    cmds.rowColumnLayout(nc=3, cw=[(1, 90),(2, 95),(3, 105)], cs=[(1,10),(2,5),(3,5)], p=main_column)
    cmds.text(l='Video Scale % ', align="center", font= 'smallPlainLabelFont')
    cmds.text(l='Video Compression ', align="center", font= 'smallPlainLabelFont')
    cmds.text(l='Video Output Type ', align="center", font= 'smallPlainLabelFont')
    
    video_scale_input = cmds.intSliderGrp( field=True, minValue=1, maxValue=100, fieldMinValue=1, fieldMaxValue=100, value=current_video_scale, cw=([1,35],[2,65]))
    
    compression_input = cmds.optionMenu()
    try:
        for name in get_available_playblast_compressions(current_output_type):
            cmds.menuItem( label=name )
            
        # Find stored menuItem and select it
        for idx,obj in enumerate(cmds.optionMenu(compression_input, q=True, itemListLong=True)):
            if cmds.menuItem( obj , q=True, label=True ) == current_compression:
                cmds.optionMenu(compression_input, e=True, select=idx+1) # 1-based selection
    except:
        cmds.menuItem( label='none' )

    output_type_input = cmds.optionMenu(cc=lambda args: update_available_compressions())   
    cmds.menuItem( label='qt' )
    cmds.menuItem( label='avi' )
    cmds.menuItem( label='movie' )
    
    # Find stored menuItem and select it
    for idx,obj in enumerate(cmds.optionMenu(output_type_input,q=True, itemListLong=True)):
        if cmds.menuItem( obj , q=True, label=True ) == current_output_type:
            cmds.optionMenu(output_type_input, e=True, select=idx+1)
     
    
    cmds.separator(h=10, style='none') # Empty Space
    cmds.rowColumnLayout(nc=2, cw=[(1, 140),(2, 140)], cs=[(1,10),(2, 0)], p=main_column)
    
    cmds.rowColumnLayout(nc=4, cw=[(1, 15),(2, 140),(3, 15),(4, 100)], cs=[(1,20),(2,5),(3,5)], p=main_column)
    feedback_visibility_chk = cmds.checkBox(label='', value=gt_mtod_settings_submit_ss.get('feedback_visibility'), cc=lambda args: update_checkbox_settings_data())
    cmds.text(l='Display Viewport Feedback', align="left", font= 'smallPlainLabelFont')
    timestamp_visibility_chk = cmds.checkBox(label='', value=gt_mtod_settings_submit_ss.get('timestamp_visibility'), cc=lambda args: update_checkbox_settings_data())
    cmds.text(l='Include Timestamp', align="center", font= 'smallPlainLabelFont')
    cmds.separator(h=10, style='none') # Empty Space
    
    # Bottom Buttons
    cmds.rowColumnLayout(nc=2, cw=[(1, 145),(2, 145)], cs=[(1,10),(2,10)], p=main_column)
    cmds.button(l='Reset Settings', h=30, c=lambda args: reset_settings())
    cmds.button(l='Reset Webhook', c=lambda args: cmds.textField(new_webhook_input, e=True, text=''))
    cmds.separator(h=5, style='none')
    
    cmds.rowColumnLayout(nc=1, cw=[(1, 300)], cs=[(1,10)], p=main_column)
    cmds.button(l='Apply', h=30, bgc=(.6, .6, .6), c=lambda args: apply_settings())
    cmds.separator(h=8, style='none')
    
    # Show and Lock Window
    cmds.showWindow(window_name)
    cmds.window(window_name, e=True, s=False)
    
    # Set Window Icon
    qw = omui.MQtUtil.findWindow(window_name)
    widget = wrapInstance(long(qw), QWidget)
    icon = QIcon(':/toolSettings.png')
    widget.setWindowIcon(icon)
    
    
    def update_available_compressions():
        ''' Updates items stored in the optionMenu to contain only compatible compressions '''
        try:
            cmds.optionMenu(compression_input, e=True, dai=True)
            for name in get_available_playblast_compressions(cmds.optionMenu(output_type_input, q=True, value=True)):
                cmds.menuItem( label=name, p=compression_input)
        except:
            cmds.menuItem( label='none', p=compression_input )
    
    def reset_settings():
        ''' 
        Resets fields in the settings (do not affect stored variables or persistent setttings)
        It uses a deep copy of the settings dictionary to reset it.
        '''
        
        cmds.textField(new_username_input, e=True, text=gt_mtod_settings_submit_ss_default.get('custom_username'))
        cmds.textField(new_image_format_input, e=True, text=gt_mtod_settings_submit_ss_default.get('image_format'))
        cmds.textField(new_video_format_input, e=True, text=gt_mtod_settings_submit_ss_default.get('video_format') )
        
        for idx,obj in enumerate(cmds.optionMenu(output_type_input,q=True, itemListLong=True)):
            if cmds.menuItem( obj , q=True, label=True ) == gt_mtod_settings_submit_ss_default.get('video_output_type'):
                cmds.optionMenu(output_type_input, e=True, select=idx+1)
        
        update_available_compressions()
    
        found_default = False
        for idx,obj in enumerate(cmds.optionMenu(compression_input, q=True, itemListLong=True)):
            if cmds.menuItem( obj , q=True, label=True ) == gt_mtod_settings_submit_ss_default.get('video_compression'):
                cmds.optionMenu(compression_input, e=True, select=idx+1)
                found_default = True
        
        if not found_default:
            cmds.menuItem( label='none', p=compression_input )
            
        cmds.intSliderGrp(video_scale_input, e=True, value=gt_mtod_settings_submit_ss_default.get('video_scale_pct'))
        
        # Check box Management
        cmds.checkBox(feedback_visibility_chk, e=True, value=gt_mtod_settings_submit_ss_default.get('feedback_visibility'))
        cmds.checkBox(timestamp_visibility_chk, e=True, value=gt_mtod_settings_submit_ss_default.get('timestamp_visibility'))
        update_checkbox_settings_data()
                
        
    def apply_settings():
        ''' Transfer new settings to variables and store them as persistent settings '''
        set_persistent_settings_maya_to_discord(cmds.textField(new_username_input, q=True, text=True), cmds.textField(new_webhook_input, q=True, text=True),\
                                                cmds.textField(new_image_format_input, q=True, text=True), cmds.textField(new_video_format_input, q=True, text=True),\
                                                cmds.intSliderGrp(video_scale_input, q=True, value=True), cmds.optionMenu(compression_input, q=True, value=True),\
                                                cmds.optionMenu(output_type_input, q=True, value=True))
        gt_mtod_settings_submit_ss['is_first_time_running'] = False
        gt_mtod_settings_submit_ss['is_new_instance'] = True
        
        build_gui_submit_screenshot()
        if cmds.window(window_name, exists=True):
            cmds.deleteUI(window_name, window=True)
            
    def update_checkbox_settings_data():
        feedback_visibility = cmds.checkBox(feedback_visibility_chk, q=True, value=True)
        timestamp_visibility = cmds.checkBox(timestamp_visibility_chk, q=True, value=True)

        cmds.optionVar( iv=('gt_maya_to_discord_feedback_visibility', int(feedback_visibility)) )
        gt_mtod_settings_submit_ss['feedback_visibility'] = bool(cmds.optionVar(q=("gt_maya_to_discord_feedback_visibility")))
        
        cmds.optionVar( iv=('gt_maya_to_discord_timestamp_visibility', int(timestamp_visibility)) )
        gt_mtod_settings_submit_ss['timestamp_visibility'] = bool(cmds.optionVar(q=("gt_maya_to_discord_timestamp_visibility")))



def generate_temp_file(file_format, file_name='tmp'):
    ''' 
    Generates a temporary file in the temp folder (Usually "C:/Users/USERNAME/AppData/Local/Temp/tmp.ext")
    
            Parameters:
                file_format (str) : Extension of the temp file
                file_name (str): File name (Optional)
    
            Returns:
                file ('unicode'): Path to generated file
    
    '''
    temp_dir = cmds.internalVar(userTmpDir=True)
    tmp_file = temp_dir + file_name + '.' + file_format
    return tmp_file
      

def capture_desktop_screenshot(image_file):
    ''' 
    Takes a snapshot of the entire Desktop and writes it to an image
    
            Parameters:
                image_file (str): File path for where to store generated image
                
            Returns:
                image_file (str): Returns the same path after storing data in it
    
    '''
    app = QtWidgets.QApplication.instance()
    win = omui.MQtUtil_mainWindow()
    ptr = wrapInstance(long(win), QtWidgets.QMainWindow)
    screen_number = app.desktop().screenNumber(ptr)
    screen_geometry = app.desktop().screenGeometry(screen_number)
    frame = app.primaryScreen().grabWindow(0, screen_geometry.x(), screen_geometry.y(), screen_geometry.width(), screen_geometry.height())
    frame.save(image_file)
    return image_file


def capture_app_window(image_file):
    ''' 
    Takes a snapshot of the entire Qt App (Maya) and writes it to an image
    
            Parameters:
                image_file (str): File path for where to store generated image
                
            Returns:
                image_file (str): Returns the same path after storing data in it
    
    '''
    win = omui.MQtUtil_mainWindow()
    ptr = wrapInstance(long(win), QtWidgets.QMainWindow)
    main_window_id = ptr.winId()
    long_win_id = long(main_window_id)
    frame = QtGui.QPixmap.grabWindow(long_win_id)
    frame.save(image_file)
    return image_file

def capture_viewport(image_file):
    ''' 
    Takes a snapshot of the active viewport and writes it to an image
    
            Parameters:
                image_file (str): File path for where to store generated image
                
            Returns:
                image_file (str): Returns the same path after storing data in it
    
    '''

    view = omui.M3dView.active3dView()
    image = om.MImage()
    view.readColorBuffer(image, True)
    image.writeToFile(image_file)
    return image_file

    

def discord_post_message(username, message, webhook_url):
    '''
    Sends a string message to Discord using a webhook
    
            Parameters:
                username (str): A string to be used as the username (Replaces bot name)
                message (str): A string to be used as a message
                webhook_url (str): A Discord Webhook to make the request
                
            Returns:
                response (dict): Returns the response generated by the http object
                
    '''       
    bot_message = {
    'username': username,
    'content': message
    } 

    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}

    http_obj = Http()

    response = http_obj.request(
        uri=webhook_url,
        method='POST',
        headers=message_headers,
        body=dumps(bot_message),
    )

    return response


def encode_multipart(fields, files, boundary=None):
    '''
    Encode dict of form fields and dict of files as multipart/form-data.
    Return tuple of (body_string, headers_dict). Each value in files is a dict
    with required keys 'filename' and 'content', and optional 'mimetype' (if
    not specified, tries to guess mime type or uses 'application/octet-stream').

    >>> body, headers = encode_multipart({'FIELD': 'VALUE'},
    ...                                  {'FILE': {'filename': 'F.TXT', 'content': 'CONTENT'}},
    ...                                  boundary='BOUNDARY')
    >>> print('\n'.join(repr(l) for l in body.split('\r\n')))
    '--BOUNDARY'
    'Content-Disposition: form-data; name="FIELD"'
    ''
    'VALUE'
    '--BOUNDARY'
    'Content-Disposition: form-data; name="FILE"; filename="F.TXT"'
    'Content-Type: text/plain'
    ''
    'CONTENT'
    '--BOUNDARY--'
    ''
    '''
    def escape_quote(s):
        return s.replace('"', '\\"')

    if boundary is None:
        boundary = ''.join(random.choice(_BOUNDARY_CHARS) for i in range(30))
    lines = []

    for name, value in fields.items():
        lines.extend((
            '--{0}'.format(boundary),
            'Content-Disposition: form-data; name="{0}"'.format(escape_quote(name)),
            '',
            str(value),
        ))

    for name, value in files.items():
        filename = value['filename']
        if 'mimetype' in value:
            mimetype = value['mimetype']
        else:
            mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        lines.extend((
            '--{0}'.format(boundary),
            'Content-Disposition: form-data; name="{0}"; filename="{1}"'.format(
                    escape_quote(name), escape_quote(filename)),
            'Content-Type: {0}'.format(mimetype),
            '',
            value['content'],
        ))

    lines.extend((
        '--{0}--'.format(boundary),
        '',
    ))
    body = '\r\n'.join(lines)

    headers = {
        'Content-Type': 'multipart/form-data; boundary={0}'.format(boundary),
        'Content-Length': str(len(body)),
    }

    return (body, headers)
    

def discord_post_attachment(username, message, file_path, webhook_url):
    '''
    Sends a message and an attachment to Discord using a webhook
  
            Parameters:
                username (str): A string to be used as the username (replaces bot name)
                message (str): A string to be used as a message
                file_path (str): A path for a file that will be uploaded
                webhook_url (str): A Discord Webhook to make the request
                
            Returns:
                response (dict): Returns the response generated by the http object
                
    '''
    
    fields = { 'content' : message, 'username' : username}
    file_name = file_path.split('/')[-1]
    files = {'file1': {'filename': file_name, 'content': open(file_path, "rb").read()}}
    data, headers = encode_multipart(fields, files)
    
    http_obj = Http()

    response = http_obj.request(
        uri=webhook_url,
        method='POST',
        headers=headers,
        body=data
    )

    return response
    



def get_available_playblast_compressions(format):
        return mel.eval('playblast -format "{0}" -q -compression;'.format(format))

def update_discord_webhook_validity(webhook_url):
    '''
    Updates Validity of a webhook for when running the script again a second time.
    This function updates the "settings" dictionary directly.
    
            Parameters:
                webhook_url (str): Discord Webhook URL
    
    '''
    try: 
        http_obj = Http()
        response, content = http_obj.request(webhook_url)

        success_codes = [200, 201, 202, 203, 204, 205, 206]
        if response.status in success_codes: 
            #response_content_dict = eval(content)
            response_content_dict = loads(content)
            response_content_dict.get('name')
            gt_mtod_settings_submit_ss['is_new_instance'] = False
            gt_mtod_settings_submit_ss['is_webhook_valid'] = True 
        else:
            gt_mtod_settings_submit_ss['is_new_instance'] = False
            gt_mtod_settings_submit_ss['is_webhook_valid'] = False 
    except:
        gt_mtod_settings_submit_ss['is_new_instance'] = False
        gt_mtod_settings_submit_ss['is_webhook_valid'] = False 
        

def discord_get_webhook_name(webhook_url):
    '''
    Requests the name of the webhook and returns a string representing it
    
            Parameters:
                webhook_url (str): Discord Webhook URL
                
            Returns:
                name (str): The name of the webhook (or error string, if operation failed)
    '''
    try: 
        http_obj = Http()
        response, content = http_obj.request(webhook_url)
        success_codes = [200, 201, 202, 203, 204, 205, 206]
        if response.status in success_codes: 
            response_content_dict = loads(content) 
            return response_content_dict.get('name')
        else:
            return 'Error reading webhook response'
    except:
        cmds.warning('Error connecting to provided webhook. Make sure you\'re pasting the correct URL')
        return 'Error connecting to webhook'

def get_readable_size(size, precision=2):
    ''' 
    Returns a human redable version of the size of a file 
    
            Parameters:
                size (float or int) : size of the file in bytes
                precision (int) : precision of the returned result
                    
            Returns:
                formated_string (string) : Size + Suffix
                
    '''
    suffixes=['B','KB','MB','GB','TB']
    suffix_index = 0
    while size > 1024 and suffix_index < 4:
        suffix_index += 1
        size = size/1024.0
    return "%.*f%s"%(precision, size, suffixes[suffix_index])
    
    
def response_inview_feedback(operation_name, response, write_output=True, display_inview=True):
    '''
    Prints an inViewMessage to give feedback to the user about what is being executed.
    Uses the module "random" to force identical messages to appear at the same time.

            Parameters:
                    operation_name (string): name of the operation being display (e.g. playblast)
                    response (dict): A dictionary response received from a HTTP object after post/get operation.
                    write_output (bool): Determines if the functions will write an extra output text (Like a "Result: pCube1" text output)
                    display_inview (bool): Determines if generated message will be displayed as an inView message or not (visibility)
    '''

    message = '<' + str(random.random()) + '>'
            
    if len(response) >= 1:
        status_value = response[0].status
        reason_value = response[0].reason
        success_codes = [200, 201, 202, 203, 204, 205, 206]

        if status_value in success_codes: 
            message += 'The ' + str(operation_name) + ' was <span style=\"color:#00FF00;text-decoration:underline;\">sent successfully</span>.'
            if write_output:
                sys.stdout.write('The ' + str(operation_name) + ' was sent successfully.  Web response: ' + str(reason_value) + ' (' + str(status_value) + ')')
        else: # Error
            message += 'The ' + str(operation_name) + ' was <span style=\"color:#FF0000;text-decoration:underline;\">not sent.'
            if write_output:
                sys.stdout.write('The ' + str(operation_name) + ' was sent.  Web response: ' + str(reason_value) + ' (' + str(status_value) + ')')
    else :
        message += 'The ' + str(operation_name) + ' was <span style=\"color:#FF0000;text-decoration:underline;\">not sent.'
        if write_output:
            sys.stdout.write('The ' + str(operation_name) + ' was not sent.  Error: Web responsed can\'t be read.')
     
    if display_inview:
        cmds.inViewMessage(amg=message, pos='botLeft', fade=True, alpha=.9)


if __name__ == '__main__':
    build_gui_submit_screenshot()