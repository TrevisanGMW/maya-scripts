"""
 Load MASH Script - This script will try to load the plugin MASH in case it's not already loaded.
 This is used to make Maya open faster (with "auto load" off for the plugin)
 @Guilherme Trevisan - 2020-11-14 - github.com/TrevisanGMW
"""
import sys

# Load Mash
plugin_name = 'MASH'
if not cmds.pluginInfo(plugin_name, q=True, loaded=True):
    try:
        cmds.loadPlugin(plugin_name)
    except:
        message = '<span style=\"color:#FF0000;text-decoration:underline;\">' +  plugin_name + '</span> doesn\'t seem to be installed.'
        cmds.inViewMessage(amg=message, pos='botLeft', fade=True, alpha=.9)
else:
    sys.stdout.write(plugin_name + ' is already loaded')
    