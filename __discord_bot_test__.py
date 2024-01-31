# This example requires the 'message_content' intent.
import discord

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run('MTIwMjI1NjAzNzI0NDA1MTUzNw.Go8zcp.3VGTHsea0cSXhwJtBKjvfEA90QWpkxGJEAVBSI')
