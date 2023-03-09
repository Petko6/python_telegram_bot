from telethon.sync import TelegramClient
import asyncio
import time
import json
import os
from os import path

import bot2 as bot2
# Logging configuration


def login(credential):
    global client
    client = TelegramClient(
        credential["phone"], credential["api_id"], credential["api_hash"])
    client.connect()
    if not client.is_user_authorized():  # If further authentication is needed via text
        client.send_code_request(credential["phone"])
        print('Further authentication required in order to log in, a code has been sent to the phone number.')
        client.sign_in(credential["phone"], input('Enter the code: '))
    print(f"Logged in as {client.get_me().username}!")


async def get_users(group):
    await client.get_dialogs()

    try:
        user_list = await client.get_participants(group, aggressive=True)
        users = [user.username for user in user_list if user.username is not None]
        with open("users.txt", 'w+') as f:
            for user in users:
                f.write(user+"\n")
            print(f"{len(user_list)} users exported to {f.name}!")
    except:
        print('One of the given settings is invalid!')
        save_settings(
            input('Group name: '), input('Message: '), input('Delay: '))


async def send_messages(message, users, delay):
    os.system("start cmd /k python3 bot2.py")
    for user in users:
        await client.send_message(user, message)
        print(f"Message sent to {user}.")
        time.sleep(delay)


def save_credentials(*args):
    print('Saving credentials...')
    with open('creds.txt', 'w+') as f:
        for arg in args:
            f.write(f'{arg}\n')


def read_credentials():
    print('Reading credentials...')
    with open('creds.txt', 'r') as f:
      #  return [line for line in f.read().split('\n') if line != '']
        data = f.read()
        return json.loads(data)


async def save_settings(group_name, message, delay):
    print('Saving settings...')
    try:
        settings = {'group_name': group_name,
                    'message': message, 'delay': int(delay)}
        with open('settings.txt', 'w+') as f:
            f.write(json.dumps(settings))
    except:
        print("Input for delay isn't a number")


def read_settings(setting):
    print('Reading '+setting+'...')
    with open('settings.txt', 'r') as f:
        data = f.read()
        return json.loads(data)[setting]


def load_users():
    with open('users.txt', 'r') as f:
        userList = f.read().split('\n')
        lines = len(userList)
        return userList[0:lines//5]


def main():
    # Check if credentials are saved, otherwise get them from the user
    if path.exists('creds.txt'):
        credentials = read_credentials()

        # for credential in credentials:
        login(credentials[0])

    else:
        # Needed for login authentication
        print('Find these at https://my.telegram.org/ under API Development tools.')
        save_credentials(
            input('Phone # (EX: +11234560000): '),
            input('api_id (EX: 101340): '),
            input('api_hash (EX: ca123req3410fdls343207cc743): ')
        )
        credentials = read_credentials()
        login(*credentials)
    # Async routines
    print("bot1", credentials[0])
    loop = asyncio.get_event_loop()
    loop.run_until_complete(save_settings(
        input('Group name: '), input('Message: '), input('Delay: ')))
    loop.run_until_complete(get_users(read_settings('group_name')))
    loop.run_until_complete(send_messages(read_settings(
        'message'), load_users(), read_settings('delay')))
    loop.close()


if __name__ == '__main__':
    main()
