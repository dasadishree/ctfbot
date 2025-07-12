import discord
import os

# chatgpt debugged this part to get the TOKEN & intent thing to work
from dotenv import load_dotenv
load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
# 

client = discord.Client(intents=intents)

# when bot is run
@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

# when bot sees message
@client.event
async def on_message(message):
    # only tracks others' messages
    if message.author==client.user:
        return
    
    # responds to commands
    if message.content.startswith('$ctfstart'):
        embed = discord.Embed(
            title='Welcome to Capture The Flag (CTF)',
            description='CTF is a cybersecurity competition that can help you practice security skills in a fun way. The goal is to "capture" the "flags" throughout the challenges we will give you. All the flags are formatted like "Flag=thisistheflag".\n\n Run $help for a list of commands. Have fun, and there may or may not be prizes...',
            color=discord.Colour.purple()
        )
        embed.set_footer(text="💙🩷 Techfluences x Cyber Valkyries")
        
        await message.channel.send(embed=embed)

    #view all possible challenges
    if message.content.startswith('$challenges'):
        embed=discord.Embed(
            title="CHALLENGES",
            description="Type $beginner $intermediate or $advanced to sort by difficulty.\nType $webexploit $encrypt $stringanalysis $steg $forensics or $misc to sort by category.\nType each challenge name to view more info and enter the flag.",
            color=discord.Colour.purple()
        )
        embed.add_field(
            name="$infilitrate",
            value="Category: Encryption\nLevel: Beginner",
            inline=True
        )
        embed.add_field(
            name="$hiddeninplainsight",
            value="Category: Web Exploitation\nLevel: Beginner",
            inline=True
        )
        embed.add_field(
            name="$behindtheframe",
            value="Category: Web Exploitation\nLevel: Beginner",
            inline=True
        )
        embed.add_field(
            name="$codecascade1",
            value="Category: String & Code Analysis\nLevel: Beginner",
            inline=True
        )
        embed.add_field(
            name="$doubletrouble",
            value="Category: Encryption\nLevel: Intermediate",
            inline=True
        )
        embed.add_field(
            name="$pagehunt",
            value="Category: Web Exploitation\nLevel: Intermediate",
            inline=True
        )
        embed.add_field(
            name="$easyentry",
            value="Category: Web Exploitation\nLevel: Intermediate",
            inline=True
        )
        embed.add_field(
            name="$codecascade2",
            value="Category: String & Code Analysis\nLevel: Intermediate",
            inline=True
        )
        embed.add_field(
            name="$hiddenlayers",
            value="Category: Image Steganography\nLevel: Intermediate",
            inline=True
        )
        embed.add_field(
            name="$metadata",
            value="Category: Image Steganography\nLevel: Intermediate",
            inline=True
        )
        embed.add_field(
            name="$chatleak",
            value="Category: Forensics\nLevel: Advanced",
            inline=True
        )
        embed.add_field(
            name="$sharkit",
            value="Category: Forensics\nLevel: Advanced",
            inline=True
        )
        embed.add_field(
            name="$domaindive",
            value="Category: Forensics\nLevel: Advanced",
            inline=True
        )
        embed.add_field(
            name="$birdsnest",
            value="Category: Misc.\nLevel: Advanced",
            inline=True
        )
        embed.add_field(
            name="$yranib",
            value="Category: Misc.\nLevel: Advanced",
            inline=True
        )
        embed.add_field(
            name="$catnet",
            value="Category: Misc.\nLevel: Advanced",
            inline=True
        )
        await message.channel.send(embed=embed)

# sort by category beginner
    if message.content.startswith('$beginner'):
        embed = discord.Embed(
            title='BEGINNER CHALLENGES',
            color=discord.Colour.green()
        )
        embed.add_field(
            name="$infilitrate",
            value="Category: Encryption",
            inline=True
        )
        embed.add_field(
            name="$codecascade1",
            value="Category: String & Code Analysis",
            inline=True
        )
        embed.add_field(
            name="$behindtheframe",
            value="Category: Web Exploitation",
            inline=True
        )
        embed.add_field(
            name="$hiddeninplainsight",
            value="Category: Web Exploitation",
            inline=True
        )
        await message.channel.send(embed=embed)

# sort by category intermediate
    if message.content.startswith('$intermediate'):
        embed = discord.Embed(
            title="INTERMEDIATE CHALLENGES",
            color=discord.Colour.yellow()
        )
        embed.add_field(
            name="$pagehunt",
            value="Category: Web Exploitation",
            inline=True
        )
        embed.add_field(
            name="$easyentry",
            value="Category: Web Exploitation",
            inline=True
        )
        embed.add_field(
            name="$codecascade2",
            value="Category: String & Code Analysis",
            inline=True
        )
        embed.add_field(
            name="$hiddenlayers",
            value="Category: Image Steganography",
            inline=True
        )
        embed.add_field(
            name="$metadata",
            value="Category: Image Steganography",
            inline=True
        )
        await message.channel.send(embed=embed)

# sort by category advanced
    if message.content.startswith('$advanced'):
        embed = discord.Embed(
            title="ADVANCED CHALLENGES",
            color=discord.Colour.red()
        )
        embed.add_field(
            name="$metadata",
            value="Category: Image Steganography",
            inline=True
        )
        embed.add_field(
            name="$chatleak",
            value="Category: Forensics",
            inline=True
        )
        embed.add_field(
            name="$sharkit",
            value="Category: Forensics",
            inline=True
        )
        embed.add_field(
            name="$domaindive",
            value="Category: Forensics",
            inline=True
        )
        embed.add_field(
            name="$birdsnest",
            value="Category: Misc.",
            inline=True
        )
        embed.add_field(
            name="$yranib",
            value="Category: Misc.",
            inline=True
        )
        embed.add_field(
            name="$catnet",
            value="Category: Misc.",
            inline=True
        )
        await message.channel.send(embed=embed)

# sort by category webexploit
        
# sort by category steg
# sort by category stringanalysis
# sort by category encryption
# sort by category misc
# sort by category forensics

client.run(os.getenv('TOKEN'))