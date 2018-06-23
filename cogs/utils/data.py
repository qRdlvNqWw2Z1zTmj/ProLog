cogs = ["cogs.help", "cogs.dev", "cogs.eval", "cogs.general", "cogs.errorhandler",
        "cogs.guildevents", "cogs.modules.on_typing", "cogs.modules.on_member_update",
        "cogs.utils.dbfunctions", "cogs.dbcommands", "cogs.utils.dbfunctions"]

modules = {}

modules["Typing"] = {
    "Typing": {"Enabled": False, "Timeout": 10, "Channels": [], "UserMode": "All", "Users": []}
    }

modules["MemberUpdates"] = {
        "UpdateName": {"Enabled": False, "Channels": [], "UserMode": "All", "Users": []},
        "UpdateNickname": {"Enabled": False, "Channels": [], "UserMode": "All", "Users": []},
        "UpdateStatus": {"Enabled": False, "Channels": [], "UserMode": "All", "Users": []}
    }