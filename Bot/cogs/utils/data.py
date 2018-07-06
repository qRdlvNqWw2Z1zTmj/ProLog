cogs = ["cogs.help", "cogs.dev", "cogs.eval", "cogs.general", "cogs.bot", "cogs.errorhandler", "cogs.guildevents",
        "cogs.modules.on_typing", "cogs.modules.on_member_update"]


modules = {}

modules["Members"] = {
        "Typing":               {"Enabled": True,"ChannelMode": "Whitelist", "Channels": [], "UserMode": "All", "Users": [], "TypingTime": 10},
        "UpdateName":           {"Enabled": True,"ChannelMode": "Whitelist", "Channels": [], "UserMode": "All", "Users": []},
        "UpdateNickname":       {"Enabled": True,"ChannelMode": "Whitelist", "Channels": [], "UserMode": "All", "Users": []},
        "UpdateStatus":         {"Enabled": True,"ChannelMode": "Whitelist", "Channels": [], "UserMode": "All", "Users": []}
        }