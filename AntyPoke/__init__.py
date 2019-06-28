from ts3plugin import ts3plugin
import ts3lib
import ts3defines
import time

# TODO: clean up and update after pytson get updated to recent ts api version

class testplugin(ts3plugin):
    name = "AntyPoke"
    requestAutoload = False
    version = "1.2.3"
    apiVersion = 21
    author = "ei2li"
    description = "AntiPoke"
    offersConfigure = False
    commandKeyword = ""
    infoTitle = ""
    menuItems = []  # [(ts3defines.PluginMenuType.PLUGIN_MENU_TYPE_CLIENT, 0, "text", "icon.png")]
    hotkeys = []  # [("keyword", "description")]

    def __init__(self):
        ts3lib.printMessageToCurrentTab("[color=green]%s, Anti Poke on ...[/color]") % str(time.ctime(time.time()))
        self.white_list = [""]
        self.msg = "Poke disabled, write private message."

    def onClientPokeEvent(self, schid, fromClientID, pokerName, pokerUniqueIdentity, message, ffIgnored):
        if pokerUniqueIdentity not in self.white_list:
            ts3lib.requestClientPoke(schid, fromClientID, self.msg)
            return True
        else:
            return False
