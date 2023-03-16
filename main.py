import json
import asyncio
import subprocess
from os import path
from telethon.sync import TelegramClient

async def read_settings():
    try:
        print('Reading settings...')
        with open('settings.txt', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading settings: {e}")
        raise SystemExit

async def login(client, credential):
    await client.connect()
    if not client.is_user_authorized():  
        await client.send_code_request(credential["phone"])
        print('Further authentication required in order to log in, a code has been sent to the phone number.')
        await client.sign_in(credential["phone"], input('Enter the code: '))
    print(f"Logged in as {await client.get_me()}!")

async def get_users(client, group):
    users_file = "users.txt"
    if path.exists(users_file):
        answer = input(f"{users_file} file already exists. Do you want to scrape again? Yes[y] or No[n]: ")
        if answer.lower() == 'n':
            return
        elif answer.lower() != 'y':
            print("Invalid input")
            await get_users()
            return
    else:
        dialogue = await client.get_dialogs()
        group_chat = next((d for d in dialogue if d.name == group), None)
        if not group_chat:
            print(f"Group chat {group} doesnt exist.")
        else:
            try:
                user_list = await client.get_participants(group_chat, aggressive=True)
                users = [user.username for user in user_list if user.username is not None]
                if not users:
                    print('No users found.')
                else:
                    await save_to_file(users_file, users)
                    print(f"{len(user_list)} users exported to {users_file}!")
            except Exception as e:
                print(f"Error getting user data: {e}")

async def save_to_file(filepath, data):
    try:
        with open(filepath, 'w+') as f:
            f.write('\n'.join(data))
    except Exception as e:
        print(f"Error saving to {filepath}: {e}")

async def setup():
    print('Setting up a new configuration...')
    group = input('Group name: ')
    message = input('Message: ')
    delay = int(input('Delay (in seconds): '))
    credentials = []
    num_of_bots = int(input('How many bots do you wish to have?: '))
    for i in range(num_of_bots):
        print('Now creating Bot ' + str(i+1)+'...')
        credential = {}
        credential['phone'] = input('Phone # (EX: +11234560000): ')
        credential['api_id'] = input('api_id (EX: 101340): ')
        credential['api_hash'] = input('api_hash (EX: ca123req3410fdls343207cc743): ')
        credentials.append(credential)
    await save_to_file('settings.txt', {'group_name': group, 'message': message, 'delay': delay, 'credentials': credentials})
    print('Settings saved.')

async def start():
    try:
        settings = await read_settings()
        client = TelegramClient('telebot', settings['credentials'][0]['api_id'], settings['credentials'][0]['api_hash'])
        await login(client, settings['credentials'][0])
        await get_users(client, settings['group_name'])
        await client.disconnect()
        for i in range(len(settings['credentials'])):
            subprocess.Popen(['python3', 'bot.py', str(i)])
    except Exception as e:
        print(f"Error in start(): {e}")

async def main():
    options = {'1': setup, '2': start}
    action = input("Welcome to Telegram bot by Petko. Choose what you want to do (1 - 2):\n-1 Create new configuration\n-2 Start bot with existing configuration\n")
    try:
        await options[action]()
    except KeyError:
        print("Invalid choice.")

if __name__ == '__main__':
    asyncio.run(main())
