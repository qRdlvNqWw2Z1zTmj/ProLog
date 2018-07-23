cogs = ["cogs.help", "cogs.dev", "cogs.eval", "cogs.general", "cogs.bot", "cogs.errorhandler", "cogs.guildevents",
        "cogs.modules"]

modules = {}

modules["Member"] = {
    "Typing":
        {"Description": "Logs when a member has been typing for a specified amount of time without sending a message",
         "Options":
             {"Name": "Time", "Description": "The amount of time in seconds before a user is logged. (Default: 10)",
              "Option": 10}
         },

    "StatusUpdates":
        {"Description": "Logs when a member changes their status",
         "Options":
             {"Name": "Status Type", "Description": """The type of status to log. Can be that statuses name or it's corresponding number
                        \n1.) Playing
                        \n2.) Watching
                        \n3.) Streaming
                        \n4.) Listening""", "Option": []}
         },
}

modules["Channel"] = {

}
