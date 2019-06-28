from ts3plugin import ts3plugin

import ts3lib, ts3defines, time

# TODO: clean up and update after pytson get updated to recent ts api version

class testplugin(ts3plugin):
    name = "NewMember"
    requestAutoload = False
    version = "1.2.3"
    apiVersion = 21
    author = "ei2li"
    description = "Wykrywanie osób bez rang"
    offersConfigure = False
    commandKeyword = ""
    infoTitle = ""
    menuItems = []#[(ts3defines.PluginMenuType.PLUGIN_MENU_TYPE_CLIENT, 0, "text", "icon.png")]
    hotkeys = []#[("keyword", "description")]


    def __init__(self):
        ts3lib.printMessageToCurrentTab("[color=green]%s, Skrypt 'NewMember' został włączony...[/color]" % str(time.ctime(time.time())))
        self.myuid = ""
        self.last_name = ""
        self.flagnm = 0
        self.wh_gr_list = [6, 40, 21]


    def stop(self):
        ts3lib.printMessageToCurrentTab("[color=red]Skrypt 'NewMember' został wyłączony...[/color]")

    def onClientIDsEvent(self, serverConnectionHandlerID, uniqueClientIdentifier, clientID, clientName):
        if self.flagnm == 1:
            self.flagnm = 0
            (err, clist) = ts3lib.getClientList(serverConnectionHandlerID)
            msg = "Osoba bez rangi, nick: " + self.last_name
            for key in clist:
                (err, groups) = ts3lib.getClientVariableAsString(serverConnectionHandlerID, key, ts3defines.ClientPropertiesRare.CLIENT_SERVERGROUPS)
                if any(True for x in groups if x in str(self.wh_gr_list)):
                    err_poke = ts3lib.requestClientPoke(serverConnectionHandlerID, key, msg)
            ts3lib.printMessageToCurrentTab(time.ctime(time.time()))
            ts3lib.printMessageToCurrentTab(msg)
            ts3lib.printMessageToCurrentTab("------------------------------------------------")


    def onClientMoveEvent(self, serverConnectionHandlerID, clientID, oldChannelID, newChannelID, visibility, moveMessage):
        if oldChannelID == 0:
            (err, groups) = ts3lib.getClientVariableAsString(serverConnectionHandlerID, clientID, ts3defines.ClientPropertiesRare.CLIENT_SERVERGROUPS)
            if groups[0] == "8":
                (err_name, name) = ts3lib.getClientVariableAsString(serverConnectionHandlerID, clientID, ts3defines.ClientProperties.CLIENT_NICKNAME)
                self.last_name = str(name)
                self.flagnm = 1
                err = ts3lib.requestClientIDs(serverConnectionHandlerID, self.myuid)
