# Using the bot

1. Talk to the BotFather (https://telegram.me/botfather)
2. Create a bot following his steps and receive your token
3. Put this token into the example_properties.ini file at the __token__ field
4. You can fill in the __current_raid_bosses__ and __raid_duration__ fields
5. Rename example_properties.ini to properties.ini
6. Run the bot
7. Add the bot to your Telegram App
8. Use the _/userid_ command to get your user id and put it into the properties file at the __admins__ field
9. If you have a group or channel where you want to place the bot, use the _/chatid_ command and put it at the __group_chat_id__ field.
The bot will send all the raid messages to this chat.
10. Restart the bot
11. The bot is now ready

# Commands

* _/chatid_ : gives the id of the current chat
* _/userid_ : gives the id of the user issuing this command
* */set_level X*: sets your level to X so that it will be displayed when you join a raid
* _/addRaid_ : starts the sequence to add a raid, follow the instructions given. Only for admins
* _/testRaid_ : adds a completely randomized raid to the current chat (for testing purposes). Only for admins
* _/recover_ :  loads the data from the backup files (raids and users). THIS WILL REMOVE ANY RAIDS ALREADY PRESENT! Only for admins
* _/makeAdmin X_ : makes the user with username X an admin for the bot. Only for admins
* _/removeAdmin X_ : removes the user with username X as admin for the bot. Only for admins

# Running the bot

If you have the source code and python installed just execute the main.py script using ```python main.py```. **The bot is built using Python 3, older version are not guaranteed to work correctly!!!**  
Otherwise run the executable (eg main.exe for Windows), this executable is created using [PyInstaller](http://www.pyinstaller.org/).
You can create your own executable from the source code using ```pyinstaller -F main.py```, for more information check their site.

It is necessary that the following files are in the same folder as the code or executable:
* parsed_moves.json
* parsed_pokemon.json
* properties.ini

The parsed_XXX.json files are created from another file that contains all of the information about moves and pokemon. For this program however, 
we need far less information than they provide. So I wrote a script, *parse_raw_data.py*, that takes only the necessary information from these sources 
and saves them in the parsed files. So normally you will never use this script and just keep the parsed files.

The properties.ini file holds all of the necessary data for the bot to run as you want it to. In order to configure it as intended, carefully read and follow the instructions 
of this document and the instructions in the properties.ini file itself! If you are using the Windows executable file then use the properties.ini file that's in the same folder as 
the executable. Be sure to configure this file before running the program. Otherwise you can use the example_properties.ini file to configure the bot. Just be sure to rename the file 
from example_properties.ini to properties.ini, any other name will not work.  
Edit the file using notepad or another text editor of your choice.


# Python Telegram Bot

This program was made using the **Python Telegram bot**, see [GitHub](https://github.com/python-telegram-bot/python-telegram-bot) for the source code. 
This framework is needed in order to run the bot. To install it, we refer to the link above. In short, it comes down to the following command:  
```pip install python-telegram-bot --upgrade```  
This framework is licensed with [LGPLv3](https://www.gnu.org/licenses/lgpl-3.0.html).

# License

This program is licensed with [GPL-3.0](https://www.gnu.org/licenses/gpl-3.0.html). For a summary, see the GitHub [License page](https://github.com/NielsVW/TelegramPoGoRaidBot/blob/master/LICENSE)
