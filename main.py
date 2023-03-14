import os
import json
import subprocess
from subprocess import PIPE
from operator import methodcaller
from os import path
from telethon.sync import TelegramClient


def read_settings():
    print('Reading settings...')
    with open('settings.txt', 'r') as f:
        global settings
        settings = f.read()
        settings = json.loads(settings)


def login():
    if settings is not None:
        # for credential in credentials:
        credential = settings['credentials'][0]
        global client
        client = TelegramClient(
            credential["phone"], credential["api_id"], credential["api_hash"])
        client.connect()
        if not client.is_user_authorized():  # If further authentication is needed via text
            client.send_code_request(credential["phone"])
            print(
                'Further authentication required in order to log in, a code has been sent to the phone number.')
            client.sign_in(credential["phone"], input('Enter the code: '))
        print(f"Logged in as { client.get_me()}!")


def get_users():
    group = settings['group_name']
    if path.exists('users.txt'):
        print('Users already scraped, to reset the user list delete "users.txt"')
    else:
        client.get_dialogs()

        try:
            user_list = client.get_participants(group, aggressive=True)
            users = [
                user.username for user in user_list if user.username is not None]
            with open("users.txt", 'w+') as f:
                for user in users:
                    f.write(user+"\n")
                print(f"{len(user_list)} users exported to {f.name}!")
        except:
            print('Couldnt get users.')


def setup():
    print('Setting up a new configuration...')
    try:
        group_name = input('Group name: ')
        message = input('Message: ')
        delay = input('Delay (in seconds): ')
        credentials = []
        for i in range(int(input('How many bots do you wish to have?: '))):
            print('Now creating Bot ' + str(i+1)+'...')
            credentials.append({'phone': input('Phone # (EX: +11234560000): '), 'api_id': input(
                'api_id (EX: 101340): '), 'api_hash': input('api_hash (EX: ca123req3410fdls343207cc743): ')})

        settings = {'group_name': group_name,
                    'message': message, 'delay': int(delay), 'credentials': credentials}

        with open('settings.txt', 'w+') as f:
            f.write(json.dumps(settings))
            print('Settings saved.')

        options = ['start()', 'os._exit(1)']
        option = options[int(input(
            'Choose what you want to do next(1 - 2):\n-1 Start your bot\n-2 Exit\n '))-1]
        print(option.capitalize() + ' is running...')
        eval(option)

    except KeyboardInterrupt:
        os._exit(1)
    except:
        print('One of inserted values is incorrect. Try again!')
        setup()


def start():

    read_settings()
    login()
    get_users()
    credentials = settings['credentials']
    for i in range(len(credentials)):
        os.system("start cmd /k python3 bot.py"+' '+str(i))


def main():
    options = ['setup()', 'start()']
    option = options[int(input(
        'Welcome to Telegram bot by Petko. Choose what you want to do (1 - 2):\n-1 Create new configuration\n-2 Start bot with existing configuration\n '))-1]
    print(option.capitalize() + ' is running...')
    eval(option)


if __name__ == '__main__':
    main()
