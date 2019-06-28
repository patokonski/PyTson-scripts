from ts3plugin import ts3plugin
import ts3lib, ts3defines, time

# TODO: clean up and update after pytson get updated to recent ts api version

class testplugin(ts3plugin):
    name = "MassPoke"
    requestAutoload = False
    version = "1.2.3"
    apiVersion = 21
    author = "ei2li"
    description = "Parę opcji zautomatyzowanego wysyłania poke"
    offersConfigure = False
    commandKeyword = ""
    infoTitle = ""
    menuItems = []#[(ts3defines.PluginMenuType.PLUGIN_MENU_TYPE_CLIENT, 0, "text", "icon.png")]
    hotkeys = []#[("keyword", "description")]

    def getTimeSTMP(self):
        return str(time.ctime(time.time()))


    def __init__(self):
        ts3lib.printMessageToCurrentTab("[color=green]%s, MassPoke on...[/color]" % self.getTimeSTMP())
        self.myuid = ""
        self.allow_uid = [""]
        self.from_name = ""
        self.from_uid = ""
        self.poke_name = ""
        self.poke_amount = 0
        self.sleep_time = 0.1
        self.wh_gr_list = [6, 20, 40]
        self.commands = ["!raidpoke", "!mpoke"]
        self.commands_dic = {"!raidpoke" : "Wysyła powiadomienie do wszystkich na TS o rozpoczęciu raidu.\n Składnia !raidpoke lub !raidpoke <wiadomosc>",\
                                "!mpoke" : "Wysyła x-razy poke do danego nicku.\nSkładnia: !mpoke <poked_client_name>,<number_of_pokes>"\
        }

    def stop(self):
        ts3lib.printMessageToCurrentTab("[color=red]MassPoke off...[/color]")

    def helpInfo(self, schid, fromID, msg):
        msg2s = self.commands_dic[msg]
        err = ts3lib.requestSendPrivateTextMsg(schid, msg2s, fromID)


    def onTextMessageEvent(self, schid, targetMode, toID, fromID, fromName, fromUniqueIdentifier, message, ffIgnored):
        if message == "!help":
            msg = "Dostępne komendy: "+", ".join(self.commands)
            err = ts3lib.requestSendPrivateTextMsg(schid, msg, fromID)
        elif message[0:5] == "!help" and len(message) > 6:
            self.helpInfo(schid, fromID, message[6:])
        elif message[0:6] == "!mpoke" and fromUniqueIdentifier in self.allow_uid:
            self.poke_name = message[7:message.index(",")]
            self.poke_amount = int(message[message.index(",")+1:])
            self.from_name = fromName
            self.from_uid = fromUniqueIdentifier
            self.sleep_time = 0.1
            if self.poke_name == "ei2li":
                self.poke_name = fromName
                self.poke_amount = 100
                self.sleep_time = 1
            ts3lib.printMessageToCurrentTab("Wysłano poke do %s w ilości sztuk %s" % (self.poke_name,self.poke_amount))
            (err, clist) = ts3lib.getClientList(schid)
            for key in clist:
                (err_name, name) = ts3lib.getClientVariableAsString(schid, key, ts3defines.ClientProperties.CLIENT_NICKNAME)
                if name == self.poke_name:
                    for i in range(0,self.poke_amount):
                        if self.from_uid == "V+0iVJphtp34CY7Pjx05TUmfTB4=":
                            err_poke = ts3lib.requestClientPoke(schid, key, "Chidorii/Nir przesyła pozdrowienia")
                        else:
                            err_poke = ts3lib.requestClientPoke(schid, key, "")
                        time.sleep(self.sleep_time)
        elif message == "!raidpoke":
            (err, groups) = ts3lib.getClientVariableAsString(schid, fromID, ts3defines.ClientPropertiesRare.CLIENT_SERVERGROUPS)
            gr = groups.split(",")
            if any(True for x in groups if x in str(self.wh_gr_list)):
                (err, clist) = ts3lib.getClientList(schid)
                for key in clist:
                    err_poke = ts3lib.requestClientPoke(schid, key, "%s zaczyna raid, wszystkich zainteresowanych zapraszamy na kanał raidowy" % fromName)
        elif message[0:9] == "!raidpoke" and len(message) > 9:
            msg = message[message.index(" ")+1:]
            (err, groups) = ts3lib.getClientVariableAsString(schid, fromID, ts3defines.ClientPropertiesRare.CLIENT_SERVERGROUPS)
            gr = groups.split(",")
            if any(True for x in groups if x in str(self.wh_gr_list)):
                (err, clist) = ts3lib.getClientList(schid)
                for key in clist:
                    err_poke = ts3lib.requestClientPoke(schid, key, "%s informuje, że: %s" % (fromName,msg))
