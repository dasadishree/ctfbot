import discord
from discord.ext import commands
import os
import asyncio

# chatgpt debugged this part to get the TOKEN & intent thing to work
from dotenv import load_dotenv
load_dotenv()
intents = discord.Intents.default()
intents.message_content = True


client = discord.Client(intents=intents)

# flags (later on maybe i need a way to not store this in plaintext)
infiltrate="!login Cyb3rP@ssw0rd!"
hiddeninplainsight="flag{view_source_master}"
behindtheframe = "flag{you_found_the_real_file}"


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
            description='CTF is a cybersecurity competition that can help you practice security skills in a fun way. The goal is to "capture" the "flags" throughout the challenges we will give you. Each flag\'s format will be specified per challenge.\n\n Run $help for a list of commands. Have fun, and there may or may not be prizes...',
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
        embed.set_footer(text="💙🩷 Techfluences x Cyber Valkyries")
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
        embed.set_footer(text="💙🩷 Techfluences x Cyber Valkyries")
        await message.channel.send(embed=embed)

# help
    if message.content.startswith('$help'):
       embed=discord.Embed(
           title="HELP",
           description="$ctfstart for initial instructions & description\n\n$challenges to view all challenges\n\n$beginner to view only beginner challenges\n\n$intermediate to view all intermediate challenges\n\n$advanced to view only advanced challenges\n\nLastly, type the challenge name (including the dollarsign) to view more instructions and submit flags.",
           color=discord.Color.purple()
       )
       embed.set_footer(text="💙🩷 Techfluences x Cyber Valkyries")
       await message.channel.send(embed=embed)

# $infiltrate
    if message.content.startswith('$infiltrate'):
        embed=discord.Embed(
            title="$infilitrate",
            description="You've'intercepted a suspicious-looking string. Figure out what it says and use the appropriate command to prove you have access. Only then will the system let you through. The flag is the command followed by the decoded string. When you figure it out, type \nThe string is: Q3liM3JQQHNzdzByZCE=",
            color=discord.Color.purple()
        )
        embed.set_footer(text="💙🩷 Techfluences x Cyber Valkyries")
        await message.channel.send(embed=embed)

        def check(m):
            return m.author == message.author and m.channel == message.channel
        response=await client.wait_for('message', check=check) 
        if response.content.strip() == infiltrate:
            await message.channel.send("Access Granted! You have completed this challenge.")
        else:
            await message.channel.send("Invalid login. Type $infiltrate again to try again.")

# $hiddeninplainsight
    if message.content.startswith('$hiddeninplainsight'):
        embed=discord.Embed(
            title="$hiddeninplainsight",
            description="A suspicious site may be hiding something in plain sight. Not everything is meant to be seen with the naked eye. Type flag{...flaggoeshere...} to submit. \n The site is: https://hiddeninplainsight.netlify.app/",
            color=discord.Color.purple()
        )
        embed.set_footer(text="💙🩷 Techfluences x Cyber Valkyries")
        await message.channel.send(embed=embed)

        def check(m):
            return m.author == message.author and m.channel == message.channel
        response=await client.wait_for('message', check=check)
        if response.content.strip() == hiddeninplainsight:
            await message.channel.send("Access Granted! You have completed this challenge.")
        else:
            await message.channel.send("Incorrect. Type $hiddeninplainsight to try again.")

# $behindtheframe
    if message.content.startswith('$behindtheframe'):
        embed=discord.Embed(
            title="$behindtheframe",
            description="Not everything is what it claims to be. A broken link might still lead to something valuable...if you know how to look! Type flag{...flaggoeshere...} to submit. \n Link: https://behindtheframe.netlify.app/"
        )
        embed.set_footer(text="💙🩷 Techfluences x Cyber Valkyries")
        await message.channel.send(embed=embed)

        def check(m):
            return m.author==message.author and m.channel ==message.channel
        response=await client.wait_for('message',check=check)
        if response.content.strip() == behindtheframe:
            await message.channel.send("Congrats! You have completed this challenge.")
        else:
            await message.channel.send("Incorrect. Type $behindtheframe to try again.")

# $pagehunt
    if message.content.startswith('$pagehunt'):
        embed=discord.Embed(
            title="$pagehunt",
            description="Looks like just an ordinary picture... or is it? Try peeling back a few digital layers."
        )
        embed.set_footer(text="💙🩷 Techfluences x Cyber Valkyries")
        await message.channel.send(embed=embed)

        def check(m):
            return m.author==message.author and m.channel ==message.channel
        response=await client.wait_for('message',check=check)
        if response.content.strip() == behindtheframe:
            await message.channel.send("Congrats! You have completed this challenge.")
        else:
            await message.channel.send("Incorrect. Type $behindtheframe to try again.")

client.run(os.getenv('TOKEN'))