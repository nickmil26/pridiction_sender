import os
import random
import pandas as pd
from telethon import TelegramClient
from telethon.tl.functions.messages import SendReactionRequest
from telethon.tl.types import ReactionEmoji

# Load accounts from CSV
accounts = pd.read_csv('accounts.csv')

# Telegram API credentials
api_id = '25805299'  # Replace with your API ID
api_hash = '77a9f45c0d8e3b5004ff1f689ad91aad'  # Replace with your API hash

# Telegram channel username
channel_username = 'testsub01'  # Replace with your channel username

# List of reactions (Telegram emojis)
reactions = ['👍', '❤️', '🔥', '🎉', '👏']

# Function to authenticate accounts
def authenticate_accounts():
    clients = []
    for index, account in accounts.iterrows():
        session_file = f"session_{account['phone_number']}"
        client = TelegramClient(session_file, account['api_id'], account['api_hash'])
        client.connect()
        if not client.is_user_authorized():
            client.send_code_request(account['phone_number'])
            code = input(f"Enter the code sent to {account['phone_number']}: ")
            client.sign_in(account['phone_number'], code)
        clients.append(client)
    return clients

# Function to send image to Telegram channel using the main account
async def send_image_to_channel(main_client, image_path):
    try:
        # Send the image to the channel
        message = await main_client.send_file(channel_username, image_path)
        print("Image sent successfully by main account!")
        return message.id  # Return the message ID for reactions
    except Exception as e:
        print(f"Failed to send image: {e}")
        return None

# Function to add random reactions using a client
async def add_reaction(client, message_id):
    try:
        reaction = random.choice(reactions)
        await client(SendReactionRequest(
            peer=channel_username,
            msg_id=message_id,
            reaction=[ReactionEmoji(emoticon=reaction)]
        ))
        print(f"Reaction {reaction} added by {client.session.filename}")
    except Exception as e:
        print(f"Failed to add reaction: {e}")

# Main function
async def main(image_path):
    clients = authenticate_accounts()
    if not clients:
        print("No accounts authenticated.")
        return

    # Use the first account as the main account to send the image
    main_client = clients[0]
    await main_client.start()

    # Send the image using the main account
    message_id = await send_image_to_channel(main_client, image_path)
    if not message_id:
        print("Failed to send image. Exiting.")
        await main_client.disconnect()
        return

    # Add reactions using all accounts (including the main account)
    for client in clients:
        await client.start()
        await add_reaction(client, message_id)
        await client.disconnect()

# Run the script
if __name__ == "__main__":
    import asyncio
    image_path = "betting_card.png"  # Path to the downloaded image
    asyncio.run(main(image_path))
