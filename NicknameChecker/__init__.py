from ts3plugin import ts3plugin

import ts3lib, ts3defines, time, logging as log

# TODO: clean up and update after pytson get updated to recent ts api version

class testplugin(ts3plugin):
    """Nickname checker (based on client description)

    Check if user nickname as the same as description. Works on any client moving/joining server.
    """
    name = "Nickname checker (based on client description)"
    requestAutoload = False
    version = "1.2.3"
    apiVersion = 21
    author = "ei2li"
    description = "Check if user nickname as the same as description. Works on client moving/joining server."
    offersConfigure = False
    commandKeyword = ""
    infoTitle = ""
    menuItems = []#[(ts3defines.PluginMenuType.PLUGIN_MENU_TYPE_CLIENT, 0, "text", "icon.png")]
    hotkeys = []#[("keyword", "description")]
    log.basicConfig(filename="NicknameChecker.log", level=logging.INFO)

    msgDict = {
        nCon : "Script 'Nickname checker' on...",
        nCoff : "Script 'Nickname checker' off...",
        errNameLog : "Error while obtaining client nickname",
        errDescLog : "Error while obtaining client description",
        newClientLog : "New client joining server",
        newClientOKLog : "Client OK.",
        descEmptyMsg : "Your description is empty. Ask server admin to set it",
        descEmptyLog : "Client without description",
        msmtLog : "Nick/desc mismatch - kicking client",
        msmtMsg : "Set your nickname as follows",
        nckChngLog : "Nickname change detected. New nickname"
    }

    def __init__(self):
        log.info("Script 'Nickname checker' on... {} ".format(time.ctime(time.time())))

    def stop(self):
        log.info("Script 'Nickname checker' off... {} ".format(time.ctime(time.time())))

    # on client move event handler
    def onClientMoveEvent(self, serverConnectionHandlerID, clientID, oldChannelID, newChannelID, visibility, moveMessage):
        # when client joins server
        if oldChannelID == 0:
            (err_name, name) = ts3lib.getClientVariableAsString(serverConnectionHandlerID, clientID, ts3defines.ClientProperties.CLIENT_NICKNAME)
            (err_desc, desc) = ts3lib.getClientVariableAsString(serverConnectionHandlerID, clientID, ts3defines.ClientPropertiesRare.CLIENT_DESCRIPTION)
            if err_name != ts3defines.ERROR_ok:
                log.error("{} - Error while obtaining client nickname".format(time.ctime(time.time())))
            elif err_desc != ts3defines.ERROR_ok:
                log.error("{} - Error while obtaining client description".format(time.ctime(time.time())))
            else:
                log.info("{} - New client joining server. Nickname {}, desc: {}".format(time.ctime(time.time()), name, desc))
                # if nickname == desc
                if name == desc:
                    log.info("{} - Client OK. Nickname: {}".format(time.ctime(time.time()), name))
                # if desc not set
                elif desc == "":
                    err_poke = ts3lib.requestClientPoke(serverConnectionHandlerID, clientID, "Your description is empty. Ask server admin to set it")
                    log.warning("{} - Client without description. Nickname: {}".format(time.ctime(time.time()), name))
                # if nickname/desc mismatch
                elif name != desc:
                    err_kick = ts3lib.requestClientKickFromServer(serverConnectionHandlerID, clientID, "Set your nickname as follows: %s" % desc)
                    log.warning("{} - Nick/desc mismatch - kicking client. Nickname: {}, description: {}".format(time.ctime(time.time()), name, desc))
        # on client changing channel
        elif newChannelID != 0:
            (err_name, name) = ts3lib.getClientVariableAsString(serverConnectionHandlerID, clientID, ts3defines.ClientProperties.CLIENT_NICKNAME)
            (err_desc, desc) = ts3lib.getClientVariableAsString(serverConnectionHandlerID, clientID, ts3defines.ClientPropertiesRare.CLIENT_DESCRIPTION)
            if err_name != ts3defines.ERROR_ok:
                log.error("{} - Error while obtaining client nickname".format(time.ctime(time.time())))
            elif err_desc != ts3defines.ERROR_ok:
                log.error("{} - Error while obtaining client description".format(time.ctime(time.time())))
            else:
                # if desc not set
                if desc == "":
                    message = "Your description is empty. Ask server admin to set it"
                    ts3lib.requestSendPrivateTextMsg(serverConnectionHandlerID, message, clientID)
                    log.warning("{} - Client without description. Nickname: {}".format(time.ctime(time.time()), name))
                # if nickname/desc mismatch
                elif name != desc:
                    err_kick = ts3lib.requestClientKickFromServer(serverConnectionHandlerID, clientID, "Set your nickname as follows: %s" % desc)
                    log.warning("{} - Nick/desc mismatch - kicking client. Nickname: {}, description: {}".format(time.ctime(time.time()), name, desc))


    # on client changing nickname while connected to server
    def onClientDisplayNameChanged(self, serverConnectionHandlerID, clientID, displayName, uniqueClientIdentifier):
        name = displayName
        (err_desc, desc) = ts3lib.getClientVariableAsString(serverConnectionHandlerID, clientID, ts3defines.ClientPropertiesRare.CLIENT_DESCRIPTION)
        if err_desc != ts3defines.ERROR_ok:
            log.error("{} - Error while obtaining client description".format(time.ctime(time.time())))
        else:
            log.info("{} - Nickname change detected. New nickname: {}, desc: {}".format(time.ctime(time.time()), name, desc))
            # if nickname == desc
            if name == desc:
                log.info("{} - Client OK. Nickname: {}".format(time.ctime(time.time()), name))
            # if desc not set
            elif desc == "":
                message = "Your description is empty. Ask server admin to set it"
                err_msg = ts3lib.requestSendPrivateTextMsg(serverConnectionHandlerID, message, clientID)
                log.warning("{} - Client without description. Nickname: {}".format(time.ctime(time.time()), name))
            # if name/desc mismatch
            elif name != desc:
                err_kick = ts3lib.requestClientKickFromServer(serverConnectionHandlerID, clientID, "Set your nickname as follows: %s" % desc)
                log.warning("{} - Nick/desc mismatch - kicking client. Nickname: {}, description: {}".format(time.ctime(time.time()), name, desc))