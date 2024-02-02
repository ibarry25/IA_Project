import discord
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import TOKEN
import responses
import string
import re
import extract_data

async def send_message(message, user_message, is_private):
    """Méthode permettant d'envoyer une réponse  à un utilisateur ou à un canal.

    Args:
        message (string): Un simple message
        user_message (string): Un simple message
        is_private (bool): Si le message est envoyé en DM ou non
    """    
    try:
        # Si le message commence par '?', on fait traiter la requête en tant que commande.
        if user_message.startswith('?'):
            user_message = user_message[1:]
            response = responses.handle_response(user_message)
        else:
            # Sinon, on répond au message avec le modèle GPT-2
            response = generate_gpt2_response(user_message)

        # On envoie la réponse
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

def generate_gpt2_response(user_message):
    """Méthode permettant de générer une réponse en fonction de ce que saisie un utilisateur

    Args:
        user_message (String): Un message envoyé par un utilisateur

    Returns:
        String: réponse du bot
    """    
    # On charge le modèle GPT-2
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    model = GPT2LMHeadModel.from_pretrained('gpt2')

    # Tokenize and generate a response
    input_ids = tokenizer.encode(user_message, return_tensors='pt')
    output = model.generate(input_ids, max_length=50, num_return_sequences=1, no_repeat_ngram_size=2)

    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return response

def preprocess_text(text):
    # Supprimer les balises HTML (si elles existent)
    text = re.sub(r'<.*?>', '', text)

    # Normaliser la casse
    text = text.lower()
    
    return text

def process_text(text):
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

    tokens = tokenizer(text)

    return tokens

def run_discord_bot():
    """Méthode permettant simplement de lancer le bot et le connecter aux serveurs discord
    """    
    intents = discord.Intents.default()
    intents.message_content = True
    intents.presences = True

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
        
    print(process_text(preprocess_text(extract_data.DATA)))
    
    client.run(TOKEN.TOKEN)
