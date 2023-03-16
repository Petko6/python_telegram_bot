import json
import sys
import asyncio
from telethon.sync import TelegramClient
from telethon.errors import PeerFloodError


async def read_settings():
    print('Reading settings...')
    with open('settings.txt', 'r') as f:
        global settings
        settings = json.load(f)
    print("bot", settings['credentials'][index])


async def login():
    global client
    credential = settings['credentials'][index]
    client = TelegramClient(credential["phone"], 
                            credential["api_id"], 
                            credential["api_hash"])
    await client.connect()
    
    if not await client.is_user_authorized():
        await client.send_code_request(credential["phone"])
        print('Further authentication required in order to log in, a code has been sent to the phone number.')
        await client.sign_in(credential["phone"], input('Enter the code: '))
    
    print(f"Logged in as {await client.get_me()}!")
    client.flood_sleep_threshold = 60 * 5


async def send_messages(users):
    for user in users:
        try:
            await client.send_message(user, settings['message'])
            print(f"Message sent to {user}.")
            await asyncio.sleep(settings['delay'])
        except PeerFloodError:
            print('PeerFloodError, sleeping...')
            await asyncio.sleep(300)


def load_users():
    with open('users.txt', 'r') as f:
        userList = f.read().split('\n')
        userList = userList[:1000]
        lines = len(userList)
        bot_count = len(settings['credentials'])
        chunk = lines // bot_count
        return userList[(chunk * index): chunk * (index + 1)]


async def main():
    global index, settings
    
    index = int(sys.argv[1])
    with open('settings.txt', 'r') as f:
        settings = json.load(f)

    await read_settings()
    await login()
    await send_messages(load_users())


if __name__ == '__main__':
    asyncio.run(main())
