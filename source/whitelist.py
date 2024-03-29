import json
import os
import sys

import nextcord
import pymongo
import requests
from mctools import RCONClient

from source.log import Log
from source.verify_command import verify_command


class Whitelist:
    def __init__(self):
        self.my_client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.my_db = self.my_client["computing-bot"]
        self.my_col = self.my_db["whitelist"]

    # If "add" is True then it will add a username otherwise itll remove one
    def whitelist_add_remove(self, username, add):
        # Connect to RCON - port is not open to the internet
        rcon = RCONClient('localhost')
        rcon.login('remoteaccesspassword')

        # Execute command on RCON - rcon,command() returns "    "
        # if it fails to execute otherwise it returns the output of the command
        feedback = rcon.command(f'whitelist {"add" if add else "remove"} {username}')
        rcon.stop()
        print(feedback)
        return feedback

    def check_on_whitelist(self, username: str):  # Working, given data.json is not empty
        with open("data.json", encoding="utf-8") as file:
            data = json.load(file)
            userdata = data["whitelist"]

        musers = userdata['discord-to-minecraft'].values()

        if username in musers:
            return True

        return False

    def uname_exists(self, uname):  # Working
        request = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{uname}')
        request_code = request.status_code

        if request_code == 200:
            return True

        else:
            return False

    def one_uname_one_user(self, duname):

        with open("data.json", encoding="utf-8") as file:
            data = json.load(file)
            userdata = data["whitelist"]

        flag = False
        dusers = [*userdata['discord-to-minecraft']]
        if duname in dusers:
            self.whitelist_add_remove(userdata['discord-to-minecraft'].pop(duname), False)
            flag = True

        # Updating data.json
        with open("data.json", 'w', encoding="utf-8") as file:
            data["whitelist"] = userdata
            json.dump(data, file, indent=4)

        return flag

    def update_json(self, discord, minecraft):
        with open("data.json", 'r', encoding="utf-8") as file:
            data = json.load(file)
            userdata = data["whitelist"]

        userdata['discord-to-minecraft'][discord] = minecraft

        with open("data.json", 'w', encoding="utf-8") as file:
            data["whitelist"] = userdata
            json.dump(data, file, indent=4)


async def whitelist_start(interaction: nextcord.interactions, username: str, log: Log):
    #
    # This function checks the username:
    #   Makes sure the username is valid
    #   Makes sure a username was sent
    #   Isnt on the whitelist
    #   Ensures only one discord user can whitelist only one minecraft username
    #   Whitelists the username
    #
    # Check a username was sent
    #try:
    wl_req = Whitelist()

    log.append_log("Whitelist command received")

    #reply_message = interaction.message
    #await interaction.message.edit(content="Got Em")
    #var: nextcord.InteractionMessage = await interaction.
    #var.edit(content="lmao")
    #.edit(content="Got Em")

    return
    #except Exception as e:
        #print(e, interaction)

    #     error = verify_command(ctx=ctx, role_allowed='PISS', no_parameters=1, command="whitelist", log=log)
    #     if error:
    #         await reply_message.edit(error)
    #         await interaction.message.add_reaction('\N{THUMBS DOWN SIGN}')
    #         return
    #
    #     log.append_log(f'Whitelist request received from {interaction.message.author} (Discord ID {interactionauthor.id}) for {username}')
    #
    #     # Check username exists
    #     log.append_log("Checking username Exists")
    #     if not wl_req.uname_exists(username):
    #         log.append_log(f'{username} does not exist')
    #         await interaction.message.edit(content='{username} does not exist.')
    #         await interaction.message.add_reaction('\N{THUMBS DOWN SIGN}')
    #         await reply_message.edit("Complete")
    #         return
    #
    #     # Check the username isnt already whitelisted
    #     log.append_log("Checking the username isnt already whitelisted")
    #     if wl_req.check_on_whitelist(username):
    #         log.append_log(
    #             f'Username {username} requested by {interaction.message.author} is already on the whitelist')
    #         await interaction.message.author.send(f'{username} is already whitelisted.')
    #         await interaction.message.add_reaction('\N{THUMBS DOWN SIGN}')
    #         await reply_message.edit("Complete")
    #         return
    #
    #     # Each discord user should be allowed one username whitelisted
    #     # If the discord user already has a username whitelisted, we replace it with the new one they sent
    #     log.append_log("Checking the user hasnt already whitelisted a username")
    #     if wl_req.one_uname_one_user(str(interaction.message.author.id)):
    #         log.append_log(f"Removed username previously whitelised by {interaction.message.author}")
    #         await interaction.message.author.send('The username you previously whitelisted has been removed.')
    #
    #     # Whitelist add
    #     log.append_log(f'attempting to add {username} to whitelist')
    #     feedback = wl_req.whitelist_add_remove(username, True)
    #     if feedback.split(' ')[0] == "Added":
    #         log.append_log(f'{username} added to the whitelist')
    #         await interaction.message.add_reaction('\N{THUMBS UP SIGN}')
    #         await reply_message.edit("Complete")
    #         await interaction.message.author.send(f'{username} has been added to the whitelist')
    #
    #         log.append_log('Updating json file')
    #         wl_req.update_json(interaction.message.author.id, username)
    #         log.append_log('Whitelist request successfully complete')
    #         return
    #
    #     log.append_log(f'Failed to add {username} to the whitelist')
    #     await interaction.message.add_reaction('\N{THUMBS DOWN SIGN}')
    #     await reply_message.edit("Complete")
    #     await interaction.message.author.send(f'Failed to add {username} to the whitelist')
    #
    # except Exception as e:
    #     exc_type, exc_obj, exc_tb = sys.exc_info()
    #     fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #     err_name = str(type(e)).split()[1].strip("> '")
    #     log.append_log(f"{err_name}: File: {fname}, Line: {exc_tb.tb_lineno}, Error: {e}")
    #     await reply_message.edit(f'Fatal Error Occured: {e}')
