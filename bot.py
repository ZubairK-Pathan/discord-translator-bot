# main.py
# This is the main file for the Discord Translator Bot.
# It uses discord.py for bot interaction and googletrans for translation.
# Includes a Flask web server to keep the bot alive on hosting platforms like Render.
#
# Setup:
# 1. Make sure you have a .env file in the same directory.
# 2. The .env file should contain one line: BOT_TOKEN="YOUR_DISCORD_BOT_TOKEN"
# 3. Run the bot using `python bot.py`

import json
import discord
import os
import asyncio
from dotenv import load_dotenv
from googletrans import Translator, LANGUAGES
from flask import Flask
from threading import Thread

# --- Configuration ---

# Load environment variables from the .env file
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# A dictionary to map flag emojis to language codes
FLAG_TO_LANG = {
    '🇦🇫': 'ps', '🇦🇱': 'sq', '🇩🇿': 'ar', '🇦🇸': 'en', '🇦�': 'ca', '🇦🇴': 'pt', '🇦🇮': 'en',
    '🇦🇬': 'en', '🇦🇷': 'es', '🇦🇲': 'hy', '🇦🇼': 'nl', '🇦🇺': 'en', '🇦🇹': 'de', '🇦🇿': 'az',
    '🇧🇸': 'en', '🇧🇭': 'ar', '🇧🇩': 'bn', '🇧🇧': 'en', '🇧🇾': 'be', '🇧🇪': 'nl', '🇧🇿': 'en',
    '🇧🇯': 'fr', '🇧🇲': 'en', '🇧🇹': 'dz', '🇧🇴': 'es', '🇧🇦': 'bs', '🇧🇼': 'en', '🇧🇷': 'pt',
    '🇮🇴': 'en', '🇻🇬': 'en', '🇧🇳': 'ms', '🇧🇬': 'bg', '🇧🇫': 'fr', '🇧🇮': 'fr', '🇰🇭': 'km',
    '🇨🇲': 'en', '🇨🇦': 'en', '🇨🇻': 'pt', '🇰🇾': 'en', '🇨🇫': 'fr', '🇹🇩': 'fr', '🇨🇱': 'es',
    '🇨🇳': 'zh-cn', '🇨🇽': 'en', '🇨🇨': 'ms', '🇨🇴': 'es', '🇰🇲': 'ar', '🇨🇬': 'fr', '🇨🇩': 'fr',
    '🇨🇰': 'en', '🇨🇷': 'es', '🇨🇮': 'fr', '🇭🇷': 'hr', '🇨🇺': 'es', '🇨🇼': 'nl', '🇨🇾': 'el',
    '🇨🇿': 'cs', '🇩🇰': 'da', '🇩🇯': 'fr', '🇩🇲': 'en', '🇩🇴': 'es', '🇪🇨': 'es', '🇪🇬': 'ar',
    '🇸🇻': 'es', '🇬🇶': 'es', '🇪🇷': 'ti', '🇪🇪': 'et', '🇪🇹': 'am', '🇫🇰': 'en', '🇫🇴': 'fo',
    '🇫🇯': 'en', '🇫🇮': 'fi', '🇫🇷': 'fr', '🇬🇫': 'fr', '🇵🇫': 'fr', '🇹🇫': 'fr', '🇬🇦': 'fr',
    '🇬🇲': 'en', '🇬🇪': 'ka', '🇩🇪': 'de', '🇬🇭': 'en', '🇬🇮': 'en', '🇬🇷': 'el', '🇬🇱': 'kl',
    '🇬🇩': 'en', '🇬🇵': 'fr', '🇬🇺': 'en', '🇬🇹': 'es', '🇬🇬': 'en', '🇬🇳': 'fr', '🇬🇼': 'pt',
    '🇬🇾': 'en', '🇭🇹': 'ht', '🇭🇳': 'es', '🇭🇰': 'zh-cn', '🇭🇺': 'hu', '🇮🇸': 'is', '🇮🇳': 'hi',
    '🇮🇩': 'id', '🇮🇷': 'fa', '🇮🇶': 'ar', '🇮🇪': 'ga', '🇮🇲': 'en', '🇮🇱': 'he', '🇮🇹': 'it',
    '🇯🇲': 'en', '🇯🇵': 'ja', '🇯🇪': 'en', '🇯🇴': 'ar', '🇰🇿': 'kk', '🇰🇪': 'sw', '🇰🇮': 'en',
    '🇽🇰': 'sq', '🇰🇼': 'ar', '🇰🇬': 'ky', '🇱🇦': 'lo', '🇱🇻': 'lv', '🇱🇧': 'ar', '🇱🇸': 'st',
    '🇱🇷': 'en', '🇱🇾': 'ar', '🇱🇮': 'de', '🇱🇹': 'lt', '🇱🇺': 'fr', '🇲🇴': 'zh-cn', '🇲🇰': 'mk',
    '🇲🇬': 'mg', '🇲🇼': 'en', '🇲🇾': 'ms', '🇲🇻': 'dv', '🇲🇱': 'fr', '🇲🇹': 'mt', '🇲🇭': 'en',
    '🇲🇶': 'fr', '🇲🇷': 'ar', '🇲🇺': 'en', '🇾🇹': 'fr', '🇲🇽': 'es', '🇫🇲': 'en', '🇲🇩': 'ro',
    '🇲🇨': 'fr', '🇲🇳': 'mn', '🇲🇪': 'sr', '🇲🇸': 'en', '🇲🇦': 'ar', '🇲🇿': 'pt', '🇲🇲': 'my',
    '🇳🇦': 'en', '🇳🇷': 'en', '🇳🇵': 'ne', '🇳🇱': 'nl', '🇳🇨': 'fr', '🇳🇿': 'en', '🇳🇮': 'es',
    '🇳🇪': 'fr', '🇳🇬': 'en', '🇳🇺': 'en', '🇳🇫': 'en', '🇰🇵': 'ko', '🇲🇵': 'en', '🇳🇴': 'no',
    '🇴🇲': 'ar', '🇵🇰': 'ur', '🇵🇼': 'en', '🇵🇸': 'ar', '🇵🇦': 'es', '🇵🇬': 'en', '🇵🇾': 'es',
    '🇵🇪': 'es', '🇵🇭': 'tl', '🇵🇳': 'en', '🇵🇱': 'pl', '🇵🇹': 'pt', '🇵🇷': 'es', '🇶🇦': 'ar',
    '🇷🇪': 'fr', '🇷🇴': 'ro', '🇷🇺': 'ru', '🇷🇼': 'rw', '🇼🇸': 'sm', '🇸🇲': 'it', '🇸🇹': 'pt',
    '🇸🇦': 'ar', '🇸🇳': 'fr', '🇷🇸': 'sr', '🇸🇨': 'fr', '🇸🇱': 'en', '🇸🇬': 'en', '🇸🇽': 'nl',
    '🇸🇰': 'sk', '🇸🇮': 'sl', '🇸🇧': 'en', '🇸🇴': 'so', '🇿🇦': 'af', '🇰🇷': 'ko', '🇸🇸': 'en',
    '🇪🇸': 'es', '🇱🇰': 'si', '🇧🇱': 'fr', '🇸🇭': 'en', '🇰🇳': 'en', '🇱🇨': 'en', '🇲🇫': 'fr',
    '🇵🇲': 'fr', '🇻🇨': 'en', '🇸🇩': 'ar', '🇸🇷': 'nl', '🇸🇿': 'en', '🇸🇪': 'sv', '🇨🇭': 'de',
    '🇸🇾': 'ar', '🇹🇼': 'zh-tw', '🇹🇯': 'tg', '🇹🇿': 'sw', '🇹🇭': 'th', '🇹🇱': 'pt', '🇹🇬': 'fr',
    '🇹🇰': 'en', '🇹🇴': 'to', '🇹🇹': 'en', '🇹🇳': 'ar', '🇹🇷': 'tr', '🇹🇲': 'tk', '🇹🇨': 'en',
    '🇹🇻': 'en', '🇺🇬': 'sw', '🇺🇦': 'uk', '🇦🇪': 'ar', '🇬🇧': 'en', '🇺🇸': 'en', '🇺🇾': 'es',
    '🇺🇿': 'uz', '🇻🇺': 'fr', '🇻🇦': 'it', '🇻🇪': 'es', '🇻🇳': 'vi', '🇼🇫': 'fr', '🇪🇭': 'ar',
    '🇾🇪': 'ar', '🇿🇲': 'en', '🇿🇼': 'en'
}

# --- Bot Initialization ---

# Define the bot's intents.
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.reactions = True

# Create the bot instance
bot = discord.Bot(intents=intents)

# Initialize the translator
translator = Translator()

# A dictionary to store auto-translation channel configurations
auto_translate_channels = {}
SETTINGS_FILE = "settings.json"

# --- Functions for Saving/Loading ---

def save_settings():
    """Saves the auto_translate_channels dictionary to a file."""
    try:
        string_keys_channels = {str(k): v for k, v in auto_translate_channels.items()}
        with open(SETTINGS_FILE, "w") as f:
            json.dump(string_keys_channels, f, indent=4)
        print("Settings saved successfully.")
    except Exception as e:
        print(f"Error saving settings: {e}")

def load_settings():
    """Loads the auto_translate_channels dictionary from a file."""
    global auto_translate_channels
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r") as f:
                loaded_channels = json.load(f)
                auto_translate_channels = {int(k): v for k, v in loaded_channels.items()}
                print("Settings loaded successfully.")
        else:
            print("No settings file found, starting with empty settings.")
    except Exception as e:
        print(f"Error loading settings: {e}")
        auto_translate_channels = {}

# --- Event Handlers ---

@bot.event
async def on_ready():
    """Event handler for when the bot has successfully connected to Discord."""
    load_settings()
    print(f"Bot is logged in as {bot.user}")
    print("Ready to translate!")
    print("-" * 20)


@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    """Event handler for reaction-based translation."""
    if payload.user_id == bot.user.id:
        return

    emoji = str(payload.emoji)
    if emoji in FLAG_TO_LANG:
        try:
            channel = bot.get_channel(payload.channel_id)
            if not isinstance(channel, discord.TextChannel): return
            
            message = await channel.fetch_message(payload.message_id)
            
            if not message.content:
                return

            target_lang = FLAG_TO_LANG[emoji]
            translation = translator.translate(message.content, dest=target_lang)
            
            embed = discord.Embed(
                description=f"**Translated to {LANGUAGES.get(target_lang, 'Unknown').capitalize()}**\n{translation.text}",
                color=discord.Color.blue()
            )
            embed.set_footer(text=f"Original message by {message.author.display_name}")

            await message.reply(embed=embed, mention_author=False)

        except discord.errors.Forbidden:
            print(f"Error: Missing permissions to send message in channel {payload.channel_id}")
        except Exception as e:
            print(f"An error occurred during reaction translation: {e}")


@bot.event
async def on_message(message: discord.Message):
    """Event handler for auto-translation channels."""
    if message.author == bot.user:
        return

    if message.channel.id in auto_translate_channels:
        try:
            target_lang = auto_translate_channels[message.channel.id]
            
            if not message.content:
                return

            translation = translator.translate(message.content, dest=target_lang)
            
            embed = discord.Embed(
                description=f"```{translation.text}```",
                color=discord.Color.green()
            )
            author_name = message.author.display_name
            original_lang_code = translation.src
            original_lang_name = LANGUAGES.get(original_lang_code, "Unknown").capitalize()
            
            embed.set_footer(text=f"Auto-translated from {original_lang_name} for {author_name}")
            
            await message.channel.send(embed=embed)

        except Exception as e:
            print(f"An error occurred during auto-translation: {e}")


# --- Slash Commands ---

@bot.slash_command(
    name="set_channel",
    description="Set this channel for automatic translation to a specific language."
)
@discord.commands.default_permissions(manage_channels=True)
async def set_channel(ctx: discord.ApplicationContext, target_language: str):
    """Command to set up a channel for auto-translation."""
    target_language = target_language.lower().strip()

    if target_language not in LANGUAGES:
        await ctx.respond(
            f"'{target_language}' is not a valid language code. Please use a valid code (e.g., 'en', 'es', 'ja').",
            ephemeral=True
        )
        return

    auto_translate_channels[ctx.channel.id] = target_language
    save_settings()

    lang_name = LANGUAGES.get(target_language, "this language").capitalize()
    await ctx.respond(f"✅ This channel will now automatically translate all messages to **{lang_name}**.")


@bot.slash_command(
    name="remove_channel",
    description="Remove this channel from automatic translation."
)
@discord.commands.default_permissions(manage_channels=True)
async def remove_channel(ctx: discord.ApplicationContext):
    """Command to remove a channel from auto-translation."""
    if ctx.channel.id in auto_translate_channels:
        del auto_translate_channels[ctx.channel.id]
        save_settings()
        await ctx.respond("✅ Automatic translation has been disabled for this channel.")
    else:
        await ctx.respond("This channel is not configured for automatic translation.", ephemeral=True)

# --- Web Server to Keep Bot Alive on Render (NEW CODE) ---
app = Flask('')

@app.route('/')
def home():
    return "I'm alive"

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- Bot Execution (MODIFIED) ---
if __name__ == "__main__":
    if BOT_TOKEN is None:
        print("Error: BOT_TOKEN not found in .env file.")
    else:
        keep_alive()  # Starts the web server
        bot.run(BOT_TOKEN)
�
