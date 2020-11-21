"""
 Load Arnold Script - This script will try to load the plugin Arnold in case it's not already loaded.
 This is used to make Maya open faster (with "Auto Load" checked off in the Plug-in Manager)
 
 How to use it:
 1. Go to your Plug-in Manager and uncheck "Auto Load" for the plugin redshift4maya.mll
 2. Create a shelf button containing the code in this script
 3. If you ever need to use Arnold, just click on the shelf button
 
 @Guilherme Trevisan - 2020-11-14 - github.com/TrevisanGMW
 
 1.1 - 2020-11-20
 Updated with a function and better feedback
"""
plugins_to_load = ['mtoa']

def gtu_load_plugins(plugin_list):
    ''' 
    Attempts to load provided plug-ins, then gives the user feedback about their current state. (Feedback through inView messages and stdout.write messages)
    
            Parameters:
                plugin_list (list): A list of strings containing the name of the plug-ings yo uwant to load
    
    '''
    already_loaded = []
    not_installed = []
    now_loaded = []
    
    # Load Plug-in
    for plugin in plugin_list:
        if not cmds.pluginInfo(plugin, q=True, loaded=True):
            try:
                cmds.loadPlugin(plugin)
                if cmds.pluginInfo(plugin, q=True, loaded=True):
                    now_loaded.append(plugin)
            except:
                not_installed.append(plugin)
        else:
            already_loaded.append(plugin)
    
    # Give Feedback
    if len(not_installed) > 0:
        message_feedback = ''
        for str in not_installed:
            message_feedback += str + ', '
        is_plural = 'plug-ins don\'t'
        if len(not_installed) == 1:
            is_plural = 'plug-in doesn\'t'
        message = '<span style=\"color:#FF0000;text-decoration:underline;\">' +  message_feedback[:-2] + '</span> ' + is_plural + ' seem to be installed.'
        cmds.inViewMessage(amg=message, pos='botLeft', fade=True, alpha=.9)
        sys.stdout.write(message_feedback[:-2] + ' ' + is_plural + ' seem to be installed.')
        
    if len(now_loaded) > 0:
        message_feedback = ''
        for str in now_loaded:
            message_feedback += str + ', '
        is_plural = 'plug-ins are'
        if len(now_loaded) == 1:
            is_plural = 'plug-in is'
        message = '<span style=\"color:#FF0000;text-decoration:underline;\">' +  message_feedback[:-2] + '</span> ' + is_plural + ' now loaded.'
        cmds.inViewMessage(amg=message, pos='botLeft', fade=True, alpha=.9)
        sys.stdout.write(message_feedback[:-2] + ' ' + is_plural + ' now loaded.')
    
    if len(already_loaded) > 0:
        message_feedback = ''
        for str in already_loaded:
            message_feedback += str + ', '
        is_plural = 'plug-ins are'
        if len(already_loaded) == 1:
            is_plural = 'plug-in is'
        message = '<span style=\"color:#FF0000;\">' +  message_feedback[:-2] + '</span> ' + is_plural +  ' already loaded.'
        cmds.inViewMessage(amg=message, pos='botLeft', fade=True, alpha=.9)
        sys.stdout.write(message_feedback[:-2] + ' ' + is_plural + ' already loaded.')


# Run Script
if __name__ == '__main__':
    gtu_load_plugins(plugins_to_load)