cogs = ["cogs.help", "cogs.dev", "cogs.eval", "cogs.general", "cogs.errorhandler", "cogs.guildevents",
        "cogs.modules.on_typing", "cogs.modules.on_member_update"]


modules = {}

modules["Members"] = {
        "Typing": {"Enabled": True, "TypingTime": 10, "Channels": [], "UserMode": "All", "Users": []},
        "UpdateName": {"Enabled": True, "Channels": [], "UserMode": "All", "Users": []},
        "UpdateNickname": {"Enabled": True, "Channels": [], "UserMode": "All", "Users": []},
        "UpdateStatus": {"Enabled": True, "Channels": [], "UserMode": "All", "Users": []}
    }