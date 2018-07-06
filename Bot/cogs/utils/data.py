cogs = ["cogs.help", "cogs.dev", "cogs.eval", "cogs.general", "cogs.bot", "cogs.errorhandler", "cogs.guildevents",
        "cogs.modules.on_typing", "cogs.modules.on_member_update"]


modules = {}

modules["Members"] = {
        "Typing":             {"Enabled": [], "ChannelMode": "All", "Channels": [], "UserMode": "All", "Users": [], "TypingTime": 10},
        "UpdateName":         {"Enabled": [], "UserMode": "All", "Users": []},
        "UpdateNickname":     {"Enabled": [], "UserMode": "All", "Users": []},
        "UpdateStatus":       {"Enabled": [], "UserMode": "All", "Users": []},
        "UpdateActivity"      {"Enabled": [], "UserMode": "All", "Users": []},
        "UpdateRole"          {"Enabled": [], "UserMode": "All", "Users": []},
        "Join":               {"Enabled": [], "UserMode": "All", "Users": []},
        "Leave":              {"Enabled": [], "UserMode": "All", "Users": []},
        "Kick":               {"Enabled": [], "UserMode": "All", "Users": []},
        "Banned":             {"Enabled": [], "UserMode": "All", "Users": []},
        "VoiceJoin":          {"Enabled": [], "ChannelMode": "All", "Channels": [], "UserMode": "All", "Users": []},
        "VoiceLeave":         {"Enabled": [], "ChannelMode": "All", "Channels": [], "UserMode": "All", "Users": []},
        "VoiceMute":          {"Enabled": [], "ChannelMode": "All", "Channels": [], "UserMode": "All", "Users": []},
        "VoiceUnmute":        {"Enabled": [], "ChannelMode": "All", "Channels": [], "UserMode": "All", "Users": []},
        "VoiceDeafen":        {"Enabled": [], "ChannelMode": "All", "Channels": [], "UserMode": "All", "Users": []},
        "VoiceUndeafen":      {"Enabled": [], "ChannelMode": "All", "Channels": [], "UserMode": "All", "Users": []},
        "VoiceAdminMute":     {"Enabled": [], "ChannelMode": "All", "Channels": [], "UserMode": "All", "Users": []},
        "VoiceAdminUnmute":   {"Enabled": [], "ChannelMode": "All", "Channels": [], "UserMode": "All", "Users": []},
        "VoiceAdminDeafen":   {"Enabled": [], "ChannelMode": "All", "Channels": [], "UserMode": "All", "Users": []},
        "VoiceAdminUndeafen": {"Enabled": [], "ChannelMode": "All", "Channels": [], "UserMode": "All", "Users": []},
}

modules["Channels"] = {
        "ChannelCreate":      {"Enabled": []},
        "ChannelDelete":      {"Enabled": []},
        "TextChannelUpdate":  {"Enabled": [], "ChannelMode": "All", "Channels": []},
        "CategoryUpdate":     {"Enabled": [], "ChannelMode": "All", "Channels": []},
        "VoiceChannelUpdate": {"Enabled": [], "ChannelMode": "All", "Channels": []},
        "MessagePinned":      {"Enabled": [], "ChannelMode": "All", "Channels": []}
}