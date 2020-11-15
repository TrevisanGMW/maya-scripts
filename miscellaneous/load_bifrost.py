"""
 Load Bifrost Script - This script will try to load the plugin Bifrost in case it's not already loaded.
 This is used to make Maya open faster (with "auto load" off for the plugin)
 @Guilherme Trevisan - 2020-11-14 - github.com/TrevisanGMW
"""
import sys

# Load Bifrost
plugins_to_load = ['bifmeshio', 'bifrostGraph', 'bifrostshellnode', 'bifrostvisplugin', 'Boss', 'mayaVnnPlugin']
feedback = ''

for plugin in plugins_to_load:
    if not cmds.pluginInfo(plugin, q=True, loaded=True):
        try:
            cmds.loadPlugin(plugin)
        except:
            message = '<span style=\"color:#FF0000;text-decoration:underline;\">' +  plugin_name + '</span> doesn\'t seem to be installed.'
            cmds.inViewMessage(amg=message, pos='botLeft', fade=True, alpha=.9)
    else:
        feedback += plugin + ' '
        
if feedback != '':
    sys.stdout.write(feedback + ' was/were already loaded.')
