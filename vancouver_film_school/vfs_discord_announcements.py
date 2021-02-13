"""
 This script is a modified version of GT Maya to Discord.
 VFS Discord Announcement Script 
 @Guilherme Trevisan - TrevisanGMW@gmail.com - 2021-02-12 - github.com/TrevisanGMW

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

# Script Name
script_name = "VFS Discord Announcement Script"

# Versions:
script_version = "1.0"
maya_version = cmds.about(version=True)

# Used to define multipart/form-data boundary
_BOUNDARY_CHARS = string.digits + string.ascii_letters

# Settings
gt_mtod_vfs_announcement = { 'discord_username'  : 'Announcement Bot',
                             'current_webhook' : ''}

# Default Settings (Deep Copy)
gt_mtod_vfs_announcement_default = copy.deepcopy(gt_mtod_vfs_announcement)   

def build_gui_send_vfs_announcement():
    ''' Builds the Main GUI for the script '''
    window_name = "build_gui_send_vfs_announcement"
    if cmds.window(window_name, exists =True):
        cmds.deleteUI(window_name)    

    # Main GUI Start Here =================================================================================
    
    # Build UI
    build_gui_send_vfs_announcement = cmds.window(window_name, title=' ' + script_name + " - v" + script_version,\
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
    send_announcement_btn_ico = icons_folder_dir + 'gt_mtod_send_desktop.png'
    
    if os.path.isdir(icons_folder_dir) and os.path.exists(send_announcement_btn_ico) == False:
        image_enconded = 'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAAsTAAALEwEAmpwYAAAF8WlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4gPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iQWRvYmUgWE1QIENvcmUgNS42LWMxNDggNzkuMTY0MDM2LCAyMDE5LzA4LzEzLTAxOjA2OjU3ICAgICAgICAiPiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPiA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtbG5zOmRjPSJodHRwOi8vcHVybC5vcmcvZGMvZWxlbWVudHMvMS4xLyIgeG1sbnM6cGhvdG9zaG9wPSJodHRwOi8vbnMuYWRvYmUuY29tL3Bob3Rvc2hvcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RFdnQ9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZUV2ZW50IyIgeG1wOkNyZWF0b3JUb29sPSJBZG9iZSBQaG90b3Nob3AgMjEuMCAoV2luZG93cykiIHhtcDpDcmVhdGVEYXRlPSIyMDIwLTExLTAzVDExOjU1OjM4LTA4OjAwIiB4bXA6TW9kaWZ5RGF0ZT0iMjAyMC0xMS0wM1QxMjoyNzoxMi0wODowMCIgeG1wOk1ldGFkYXRhRGF0ZT0iMjAyMC0xMS0wM1QxMjoyNzoxMi0wODowMCIgZGM6Zm9ybWF0PSJpbWFnZS9wbmciIHBob3Rvc2hvcDpDb2xvck1vZGU9IjMiIHBob3Rvc2hvcDpJQ0NQcm9maWxlPSJzUkdCIElFQzYxOTY2LTIuMSIgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDpiZTc1ODU2NC04YThkLTQ2NDUtYmU2Yy1lMmY5ZmQwMWU0YjgiIHhtcE1NOkRvY3VtZW50SUQ9ImFkb2JlOmRvY2lkOnBob3Rvc2hvcDozYjViOWNhMy1lODgwLTgxNGQtYmFjOS1mNTNmNDExMWQ0MDciIHhtcE1NOk9yaWdpbmFsRG9jdW1lbnRJRD0ieG1wLmRpZDo5MGM2ZTQ5My0xZDNkLTNiNGQtODI0ZS1kN2JhZDRlNzQ1MzQiPiA8eG1wTU06SGlzdG9yeT4gPHJkZjpTZXE+IDxyZGY6bGkgc3RFdnQ6YWN0aW9uPSJjcmVhdGVkIiBzdEV2dDppbnN0YW5jZUlEPSJ4bXAuaWlkOjkwYzZlNDkzLTFkM2QtM2I0ZC04MjRlLWQ3YmFkNGU3NDUzNCIgc3RFdnQ6d2hlbj0iMjAyMC0xMS0wM1QxMTo1NTozOC0wODowMCIgc3RFdnQ6c29mdHdhcmVBZ2VudD0iQWRvYmUgUGhvdG9zaG9wIDIxLjAgKFdpbmRvd3MpIi8+IDxyZGY6bGkgc3RFdnQ6YWN0aW9uPSJzYXZlZCIgc3RFdnQ6aW5zdGFuY2VJRD0ieG1wLmlpZDpiZTc1ODU2NC04YThkLTQ2NDUtYmU2Yy1lMmY5ZmQwMWU0YjgiIHN0RXZ0OndoZW49IjIwMjAtMTEtMDNUMTI6Mjc6MTItMDg6MDAiIHN0RXZ0OnNvZnR3YXJlQWdlbnQ9IkFkb2JlIFBob3Rvc2hvcCAyMS4wIChXaW5kb3dzKSIgc3RFdnQ6Y2hhbmdlZD0iLyIvPiA8L3JkZjpTZXE+IDwveG1wTU06SGlzdG9yeT4gPC9yZGY6RGVzY3JpcHRpb24+IDwvcmRmOlJERj4gPC94OnhtcG1ldGE+IDw/eHBhY2tldCBlbmQ9InIiPz7PHrkDAAAFDklEQVRYhe2XT2gUVxzHP+/N7M5kdetG6+ISY1sRak38Q7L9RwyUhlioh4aI1nry3EKgiKcWUS8tVQjkkAZbpLSRVg/anEzFYGJzsU5AAqUhpUuyQdckWje7+bPZnZnXQ3bDanbWikUv/Z5m5v3e+33e7733e78RSimep/ShoaH9QBOQAZ4FjQ5kgV/r6+t/1oEjruvWAdozcA6A4zhOIpE4EI1G0YG6qakpZ3BwUOq6LmzbRgjh2VkIUbJdKcXjllNKiWEYNDc3+zZs2LAR+FQH1JUrV/xdXV0xKeVV13V9QA7wplhqkyW+u5RZRiklVVVVq2tqat6LRCIvAm/oAJqmKV3Xe/r7+6uEEE1CCD/gPMa5KnqnjD2AVErds237m4GBgW8jkcg1YC0sbQiy2SyVlZWmlPJgJpPJ3rx5UxmGoQkhSs4mH+oVESplr5RCCEF9fX1ofHz85IkTJ+jv7884jgOg9EJoNE3LAvT09PhPnTqVBK4Bq8rMqhRcyWULBALi3Llzb7muG3Qc50MppZ0HWIpAXhLAMAyAHyzLaivjfFnRaPSxNtevXw8qpX6LxWKbWDpt9kNOAdRSXFV+h1f8G+dPIqWUVErJYucPATyicifgP5UXwDPT/wArAMql4adUyYFXACwsLHgaP4XmgYyUKwOuw3K2EoCorKxk27ZtGvBqmQGXR7Isq/DolrEPSCkDuq4X+i4fxeVMaNu2C7Bnzx62b9/eksvl3lFKlYyEEIISbV6XkBJCSJ/PVz07O5sB/CsAbNvmzp07i1NTUx/39vZ2GoaxxjRN23XdkjWCKLFRXNcteRcUNDs7+2BwcLBS1/VU8bWtAyIUColIJKKFw+GvOzo65oBawKR8WL2uY09pmpY+dOhQDDhSmIOwLEtls1nu379/LxwOT2iatoD3JtTyTh7k3yuANBAAVrO0DOWqEiNvuxUgGo1mdOBYX1/fSb/fvzYWi2n5imfFTKSUpNNpx3EcGhsb1/n9fjE5OTlXVVUVjMfjMyMjI2nTNCt8Pp/wgsiHXqbT6eTo6GgIMHXgi66uropMJrNFKeXLd14RgVwup9LptLtv377Vzc3NzRcuXMidP3/e6OjoWDRNc017e/v49PT0YCgUWi+l9HtBSClxXZdUKvU3MKoD9u3bt48BL1BmDY8ePbqupaWlzTCMg8lkcrS7u3vL3bt3OxKJxPDOnTvPdnZ2vhYIBL7fu3fvJ0CQ8kWuyPuaFUXnuFgm0AC8DmwCaoBXgOrh4eGR48ePr4/H46PAQSDe1tZ2ZPfu3V9t3rxZptPpqWAwaAG/AxPAQDQaHfYk8QDYqpT6BdgohJDz8/OZoaGh1KVLl8StW7fWp1Kpn4DPLcv6q1CQNDU1tYbD4Y6Ghoaquro65ff7RS6XyyUSiT9bW1s/AkpC6KU+AqYQYtPAwMD86dOnjUwmY87Nzc1ls9leoBu4YVnWg+IOfX19F4EbV69e/cDn8x0A3jxz5oxp2/ZW4Evg/ScBACAYDAZ27NgxcPjw4YvBYFCEQqFF0zSrgZdYWkdlWVZxVayA+ZmZmbPT09PfhcPh9rGxsVVAtZcPL4DU4uLi2K5du16ura1t1HX97bxD4bplc00BXAWDQaSUvrGxsSxlNrcXwGQ8Hu+cmJj4LJlMviCEkHkAz7+fR7KzkFKilHIuX77sB/7wAhCFur2EVgH7gXdZuk6L5ZXtHh2o8APzI9DvCfA89Q9+dgWL9W/IeAAAAABJRU5ErkJggg=='
        image_64_decode = base64.decodestring(image_enconded)
        image_result = open(send_announcement_btn_ico, 'wb')
        image_result.write(image_64_decode)
        image_result.close()
    
    if os.path.exists(send_announcement_btn_ico) == False:
        send_announcement_btn_ico = 'fluidGetExamples.png'

    cmds.separator(h=5)
    cmds.separator(h=7, style='none') # Empty Space
    #cmds.rowColumnLayout(nc=2, cw=[(1, 235)], cs=[(1, 18)], p=content_main)
    cmds.rowColumnLayout(nc=3, cw=[(1, 100),(2, 50),(3, 100),(4, 50)], cs=[(1, 10),(2, 0),(3, 0),(4, 0)], p=content_main)
    #cmds.text(l='Feedback Will Be Printed to the Viewport', align="center", fn="boldLabelFont")
    cmds.text(l='Web Response:', align="center", fn="boldLabelFont")
    status_code_text = cmds.text(l='...', align="center")
    status_message_text = cmds.text(l='...', align="center")
 

    cmds.rowColumnLayout(nc=1, cw=[(1, 260)], cs=[(1, 10)], p=content_main) 
    cmds.separator(h=7, style='none') # Empty Space
    cmds.separator(h=5)
    
    stored_webhooks_exists = cmds.optionVar(exists=("gt_vfs_servers_webhooks_list"))
    if stored_webhooks_exists:
        try:
            stored_webhooks = str(cmds.optionVar(q=("gt_vfs_servers_webhooks_list")))
        except:
            stored_webhooks = ''
    else:
        stored_webhooks = ''
        
    cmds.separator(h=7, style='none') # Empty Space
    cmds.text(l='Paste Webhooks Below:', align="center", font='tinyBoldLabelFont')
    cmds.text(l='Use commas "," to separate them', align="center", font='tinyBoldLabelFont')
    cmds.separator(h=7, style='none') # Empty Space
    webhooks_scrollfield = cmds.scrollField(wordWrap=True, fontPointSize=2 ,fn="smallPlainLabelFont", cc=lambda x:store_webhooks(cmds.scrollField(webhooks_scrollfield, q=True, text=True)), height=100, text=stored_webhooks)

    cmds.separator(h=7, style='none') # Empty Space
    cmds.text(l='Type Announcement Below:', align="center", font='tinyBoldLabelFont')
    cmds.separator(h=7, style='none') # Empty Space
    announcement_scrollfield = cmds.scrollField(wordWrap=True, fn="obliqueLabelFont", height=100)
    cmds.separator(h=10, style='none') # Empty Space
    
    def store_webhooks(webhooks):
        cmds.optionVar( sv=('gt_vfs_servers_webhooks_list', webhooks) )

    
    screenshot_btn_color = [.4,.4,.4]
    cmds.rowColumnLayout(nc=1, cw=[(1, 260),(2, 1),(3, 5)], cs=[(1, 10),(2, 0),(3, 0)], p=content_main) 
    send_announcement_btn = cmds.iconTextButton( style='iconAndTextVertical', image1=send_announcement_btn_ico, label='Send Announcement to Webhooks',\
                                            statusBarMessage='This button will send an announcement to all provided webhooks.',\
                                            olc=[1,0,0] , enableBackground=True, bgc=screenshot_btn_color, h=80,\
                                            command=lambda: send_announcement())
    
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
        stored_username_exists = cmds.optionVar(exists=("gt_vfs_servers_webhooks_list"))
        if stored_username_exists:
            try:
                stored_username = str(cmds.optionVar(q=("gt_vfs_servers_webhooks_list")))
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
                                discord_post_message(get_username(), upload_message, gt_mtod_vfs_announcement.get('discord_webhook'))
                                utils.executeDeferred(response_inview_feedback, operation_name, response, display_inview=gt_mtod_vfs_announcement.get('feedback_visibility'))
                                utils.executeDeferred(clear_attached_message, response)
                            except Exception as e:
                                print(e)
                            
                        thread = threading.Thread(None, target = threaded_upload)
                        thread.start()
                    else:
                        response_inview_feedback(operation_name, response, display_inview=gt_mtod_vfs_announcement.get('feedback_visibility'))
                except:
                    pass
        
                    
    def disable_buttons():
        ''' Disable buttons so user don't accidently send multiple requests at once ''' 
        cmds.iconTextButton(send_announcement_btn, e=True, enable=False)
       
    
    def enable_buttons():
        ''' Enable buttons after finishing previously requested function ''' 
        cmds.iconTextButton(send_announcement_btn, e=True, enable=True)
   

    # Button Functions ----------
    
    webhook_error_message = 'Sorry, something went wrong. Please review your webhook links and try again.'

    def get_discord_webhook_validity(webhook_url):
        '''
        Updates Validity of a webhook for when running the script again a second time.
        This function updates the "settings" dictionary directly.
        
                Parameters:
                    webhook_url (str): Discord Webhook URL
                    
                Returns:
                    is_valid (bool) Whether or not it's a valid webhook
                    name (string) Name of the webhook
        
        '''
        try: 
            http_obj = Http()
            response, content = http_obj.request(webhook_url)

            success_codes = [200, 201, 202, 203, 204, 205, 206]
            if response.status in success_codes: 
                #response_content_dict = eval(content)
                response_content_dict = loads(content)
                name = response_content_dict.get('name')
                return True, name
            else:
                return False, ''
        except:
            return False, ''



    def send_announcement(): #@@@
        ''' Attempts to send an announcement to all provided webhooks '''

        webhooks_string = cmds.scrollField(webhooks_scrollfield, q=True, text=True)
        webhooks_list = webhooks_string.replace(' ', '').split(',') or []
        
        print(webhooks_list)
        if webhooks_string.strip() != '':
            for whk in webhooks_list:
                gt_mtod_vfs_announcement['current_webhook'] = whk
                try:  
                    upload_message = cmds.scrollField(announcement_scrollfield, q=True, text=True)
                    
                    if upload_message.strip() != '':
                        update_text_status()
                        def threaded_upload():
                            current_webhook = gt_mtod_vfs_announcement.get('current_webhook')
                            try:
                                validity = get_discord_webhook_validity(current_webhook)
                                if validity[0]:
                                    utils.executeDeferred(disable_buttons)
                                    response = discord_post_message(gt_mtod_vfs_announcement.get('discord_username'), upload_message, current_webhook)
                                    utils.executeDeferred(enable_buttons)
                                    utils.executeDeferred(parse_sending_response, response)
                                    utils.executeDeferred(response_inview_feedback, '"' + validity[1] + '" announcement', response, display_inview=True)
                                else:
                                    update_text_status(error=True)
                                    cmds.warning(webhook_error_message)
                            except:
                                update_text_status(error=True)
                                cmds.warning(webhook_error_message)
                            
                        thread = threading.Thread(None, target = threaded_upload)
                        thread.start()
                    else:
                        cmds.warning('Your announcement is empty, please type something before sending it.')
                except:
                    update_text_status(error=True)
                    cmds.warning(webhook_error_message)
        else:
            cmds.warning('Please, provide one or more webhooks before sending announcements.')

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
                message += 'Server ' + str(operation_name) + ' was <span style=\"color:#00FF00;text-decoration:underline;\">sent successfully</span>.'
                if write_output:
                    sys.stdout.write('Server ' + str(operation_name) + ' was sent successfully.  Web response: ' + str(reason_value) + ' (' + str(status_value) + ')\n')
            else: # Error
                message += 'Server ' + str(operation_name) + ' was <span style=\"color:#FF0000;text-decoration:underline;\">not sent.'
                if write_output:
                    sys.stdout.write('Server ' + str(operation_name) + ' was sent.  Web response: ' + str(reason_value) + ' (' + str(status_value) + ')\n')
        else :
            message += 'Server ' + str(operation_name) + ' was <span style=\"color:#FF0000;text-decoration:underline;\">not sent.'
            if write_output:
                sys.stdout.write('Server ' + str(operation_name) + ' was not sent.  Error: Web responsed can\'t be read.\n')
         
        if display_inview:
            cmds.inViewMessage(amg=message, pos='botLeft', fade=True, alpha=.9)


    # Show and Lock Window
    cmds.showWindow(build_gui_send_vfs_announcement)
    cmds.window(window_name, e=True, s=False)
    
    # Set Window Icon
    qw = omui.MQtUtil.findWindow(window_name)
    widget = wrapInstance(long(qw), QWidget)
    icon = QIcon(icon_image)
    
    widget.setWindowIcon(icon)

    # Main GUI Ends Here =================================================================================


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



if __name__ == '__main__':
    build_gui_send_vfs_announcement()