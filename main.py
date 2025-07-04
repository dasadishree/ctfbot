import discord
import os

# chatgpt debugged this part to get the TOKEN & intent thing to work
from dotenv import load_dotenv
load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
# 

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author==client.user:
        return
    
    if message.content.startswith('$ctfstart'):
        embed = discord.Embed(
            title='Welcome to Capture The Flag (CTF)',
            description='CTF is a cybersecurity competition that can help you practice security skills in a fun way. The goal is to "capture" the "flags" throughout the challenges we will give you. All the flags are formatted like "Flag=thisistheflag".\n\n Run $challenges to see each challenge, and $flag to enter a flag. Have fun, and there may or may not be prizes...',
            color=discord.Colour.purple()
        )
        
        await message.channel.send(embed=embed)


client.run(os.getenv('TOKEN'))