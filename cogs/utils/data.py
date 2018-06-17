cogs = ["cogs.help", "cogs.dev", "cogs.eval", "cogs.general", "cogs.errorhandler",
        "cogs.guildevents", "cogs.modules.on_typing", "cogs.modules.on_member_update",
        "cogs.utils.dbfunctions", "cogs.dbcommands", "cogs.utils.dbfunctions"]

modules = []

modules.append(
    {"Typing": {
             "Typing": {"Enabled": False, "Timeout": 10, "Channels": None, "UserMode": "All", "Users": []}
         }})

modules.append(
    {"MemberUpdates": {
        "UpdateName": {"Enabled": False, "Channels": None, "UserMode": "All", "Users": []},
        "UpdateNickname": {"Enabled": False, "Channels": None, "UserMode": "All", "Users": []},
        "UpdateStatus": {"Enabled": False, "Channels": None, "UserMode": "All", "Users": []}
    }})