import discord
import responses

async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)
        
def run_discord_bot():
    TOKEN = 'MTIwMjY1ODAwMzgxNjI4ODMwNg.GNHtXu.hu5ZqxWhZ_gZZvPmLPAUgIttVpjU_5a6sDW3T0'
    
    # Declare necessary intents
    intents = discord.Intents.default()
    intents.message_content = True  # This allows your bot to receive message content
    intents.presences = True  # This allows your bot to receive presence updates
    
    client = discord.Client(intents=intents)
    
    @client.event
    async def on_connect():
        print(f'Bot connected to Discord: {client.user.name}')

    
    @client.event
    async def on_ready():
        print(f'{client.user} is now running')
        
    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        
        print(f'{username} said: {user_message} ({channel})')
        
        if user_message.startswith('?'):
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)
    
    client.run(TOKEN)
