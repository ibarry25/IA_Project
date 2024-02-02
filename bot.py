import os
import discord
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from transformers import TextDataset, DataCollatorForLanguageModeling
from transformers import Trainer, TrainingArguments
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

def load_model():
    """Charge le modèle GPT-2 pré-entraîné"""
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    model = GPT2LMHeadModel.from_pretrained('gpt2')
    return model, tokenizer

def preprocess_data(data_path):
    """Prétraitement des données"""
    with open(data_path, 'r', encoding='utf-8') as file:
        data = file.read()

    # Ajoutez ici tout prétraitement spécifique à vos données
    data = preprocess_text(data)

    return data

def train_gpt2_model(model, tokenizer, train_data, output_dir):
    """Entraîne le modèle GPT-2 sur les données d'entraînement"""
    print(f"Training data path: {train_data}")
    train_dataset = TextDataset(
        tokenizer=tokenizer,
        file_path=train_data,
        block_size=128
    )

    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False
    )

    training_args = TrainingArguments(
        output_dir=output_dir,
        overwrite_output_dir=True,
        num_train_epochs=100,
        per_device_train_batch_size=4,
        save_steps=10_000,
        save_total_limit=2,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=train_dataset,
    )

    # Débogage
    print("Starting training...")
    
    # Commencer l'entraînement
    trainer.train()

    # Débogage
    print("Training completed.")

    # Créer le répertoire de sortie s'il n'existe pas
    os.makedirs(output_dir, exist_ok=True)

    # Débogage
    print(f"Saving model to: {output_dir}")

    # Sauvegarder le modèle entraîné
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)

    # Débogage
    print("Model saved successfully.")


    # Commencer l'entraînement
    trainer.train()

if __name__ == '__main__':
    # Configuration
    data_path = './data/training-data.txt'
    output_dir = 'output'

    # Prétraitement des données
    training_data = preprocess_data(data_path)

    # Charger le modèle
    model, tokenizer = load_model()

    # Entraîner le modèle
    train_gpt2_model(model, tokenizer, data_path, output_dir)

    # Sauvegarder le modèle entraîné
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)