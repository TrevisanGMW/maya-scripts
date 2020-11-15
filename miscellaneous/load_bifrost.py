"""
 Load Bifrost Script - This script will try to load the plugin Bifrost in case it's not already loaded.
 This is used to make Maya open faster (with "Auto Load" checked off in the Plug-in Manager)
 
 How to use it:
 1. Go to your Plug-in Manager and uncheck "Auto Load" for the plugins listed below (under plugins_to_load)
 2. Create a shelf button containing the code in this script
 3. If you ever need to use Bifrost, just click on the shelf button
 
 @Guilherme Trevisan - 2020-11-14 - github.com/TrevisanGMW
"""
import sys

# Load
plugins_to_load = ['bifmeshio', 'bifrostGraph', 'bifrostshellnode', 'bifrostvisplugin', 'Boss', 'mayaVnnPlugin']
feedback = ''

for plugin in plugins_to_load:
    if not cmds.pluginInfo(plugin, q=True, loaded=True):
        try:
            cmds.loadPlugin(plugin)
            if cmds.pluginInfo(plugin, q=True, loaded=True):
                sys.stdout.write(plugin + ' is now loaded.')
        except:
            message = '<span style=\"color:#FF0000;text-decoration:underline;\">' +  plugin_name + '</span> doesn\'t seem to be installed.'
            cmds.inViewMessage(amg=message, pos='botLeft', fade=True, alpha=.9)
    else:
        feedback += plugin + ', '
        
if feedback != '':
    sys.stdout.write(feedback[:-2] + ': already loaded.')