# Using the bot

1. Talk to the BotFather (https://telegram.me/botfather)
2. Create a bot following his steps and receive your token
3. Put this token into the properties.ini file at the __token__ field
4. You can fill in the __current_raid_bosses__ and __raid_duration__ fields
5. Run the bot
6. Add the bot to your Telegram App
7. Use the _/userid_ command to get your user id and put it into the properties file at the __admins__ field
8. If you have a group or channel where you want to place the bot, use the _/chatid_ command and put it at the __group_chat_id__ field.
The bot will send all the raid messages to this chat.
9. Restart the bot
10. The bot is now ready

# Commands

* _/chatid_ : gives the id of the current chat
* _/userid_ : gives the id of the user issuing this command
* _/addRaid_ : starts the sequence to add a raid, follow the instructions given. Only for admins
* _/testRaid_ : adds a completely randomized raid to the current chat (for testing purposes). Only for admins
* _/recover_ :  loads the data from the backup file. THIS WILL REMOVE ANY RAIDS ALREADY PRESENT! Only for admins

# Running the bot

If you have the source code, just execute the main.py script.
Otherwise run the executable (eg main.exe for Windows), this executable is created using [PyInstaller](http://www.pyinstaller.org/).
You can create your own executable from the source code using ```pyinstaller -F main.py```, for more information check their site.

It is necessary that the following files are in the same folder as the code or executable:
* parsed_moves.json
* parsed_pokemon.json
* properties.ini

The parsed_XXX.json files are created from another file that contains all of the information about moves and pokemon. For this program however, 
we need far less information than they provide. So I wrote a script, *parse_raw_data.py*, that takes only the necessary information from these sources 
and saves them in the parsed files. So normally you will never use this script and just keep the parsed files.

The properties.ini file is something you have to create from the example_properties.ini file using the instructions in the file and the "Using the bot" 
section of this document.