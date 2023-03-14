from telethon.sync import TelegramClient
import asyncio
import time
import json
import os
import sys
import subprocess
from subprocess import CREATE_NEW_CONSOLE
from os import path
# Logging configuration


async def read_settings():
    print('Reading settings...')
    with open('settings.txt', 'r') as f:
        global settings
        settings = f.read()
        settings = json.loads(settings)
    print("bot", settings['credentials'][index])


async def login():
    if settings is not None:
        # for credential in credentials:
        credential = settings['credentials'][index]
        global client
        client = TelegramClient(
            credential["phone"], credential["api_id"], credential["api_hash"])
        await client.connect()
        if not await client.is_user_authorized():  # If further authentication is needed via text
            await client.send_code_request(credential["phone"])
            print(
                'Further authentication required in order to log in, a code has been sent to the phone number.')
            await client.sign_in(credential["phone"], input('Enter the code: '))
        print(f"Logged in as {await client.get_me()}!")

    else:
        os.execlp('python3', 'python3', 'setup.py', 'setup()')


async def send_messages(users):
    for user in users:
        await client.send_message(user, settings['message'])
        print(f"Message sent to {user}.")
        time.sleep(settings['delay'])


def load_users():
    with open('users.txt', 'r') as f:
        userList = f.read().split('\n')
        lines = len(userList)
        bot_count = len(settings['credentials'])
        chunk = lines//bot_count
        # print(userList[(lines//len(settings['credentials']))*(index+1):(lines//len(settings['credentials']))*(index+1)+(lines//len(settings['credentials']))])
        return userList[chunk*index:chunk*(index+1)]
        # return userList


def main():
    global index
    index = int(sys.argv[1])

    # Async routines

    loop = asyncio.get_event_loop()
    loop.run_until_complete(read_settings())
    loop.run_until_complete(login())
    loop.run_until_complete(send_messages(load_users()))
    loop.close()


main()
