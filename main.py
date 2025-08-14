import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True


client = discord.Client(intents=intents)

# flags (later on maybe i need a way to not store this in plaintext)
infiltrate="!login Cyb3rP@ssw0rd!"
hiddeninplainsight="flag{view_source_master}"
behindtheframe = "flag{you_found_the_real_file}"
pagehunt = "flag{you_found_it_in_the_dom}"
hiddenlayers = "flag{hidden_in_png}"
codecascade = "983472983746598"
birdsnest = "flag{you_found_me}"
yranib = "FLAG{REVERSE_ENGINEERED}"
doubletrouble = "flag{double_encryption}"
metadata = "flag{hidden_in_exif}"

# add points
def get_points(user_id):
    return user_points.get(user_id, 0)

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
            name="$infiltrate",
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
            name="$codecascade",
            value="Category: String & Code Analysis\nLevel: Intermediate",
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
            name="$birdsnest",
            value="Category: Misc.\nLevel: Advanced",
            inline=True
        )
        embed.add_field(
            name="$yranib",
            value="Category: Misc.\nLevel: Advanced",
            inline=True
        )
        await message.channel.send(embed=embed)

# sort by category beginner
    if message.content.startswith('$beginner'):
        embed = discord.Embed(
            title='BEGINNER CHALLENGES (1pt each)',
            color=discord.Colour.green()
        )
        embed.add_field(
            name="$infiltrate",
            value="Category: Encryption",
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
            title="INTERMEDIATE CHALLENGES (2pts each)",
            color=discord.Colour.yellow()
        )
        embed.add_field(
            name="$pagehunt",
            value="Category: Web Exploitation",
            inline=True
        )
        embed.add_field(
            name="$codecascade",
            value="Category: String & Code Analysis",
            inline=True
        )
        embed.add_field(
            name="$hiddenlayers",
            value="Category: Image Steganography",
            inline=True
        )
        embed.set_footer(text="💙🩷 Techfluences x Cyber Valkyries")
        await message.channel.send(embed=embed)

# sort by category advanced
    if message.content.startswith('$advanced'):
        embed = discord.Embed(
            title="ADVANCED CHALLENGES (3pts each)",
            color=discord.Colour.red()
        )
        embed.add_field(
            name="$metadata",
            value="Category: Image Steganography",
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
            title="$infiltrate",
            description="You've'intercepted a suspicious-looking string. Figure out what it says and use the appropriate command to prove you have access. Only then will the system let you through. The flag is the command followed by the decoded string. When you figure it out, type it as a chat. \nThe string is: Q3liM3JQQHNzdzByZCE=",
            color=discord.Color.purple()
        )
        embed.set_footer(text="💙🩷 Techfluences x Cyber Valkyries")
        await message.channel.send(embed=embed)

        def check(m):
            return m.author == message.author and m.channel == message.channel
        response=await client.wait_for('message', check=check) 
        if response.content.strip() == infiltrate:
            get_points(message.author.id, points=1)
            await message.channel.send("Access Granted! You have completed this challenge.")
        else:
            await message.channel.send("Invalid login. Type $infiltrate again to try again.")

# $hiddeninplainsight
    if message.content.startswith('$hiddeninplainsight'):
        embed=discord.Embed(
            title="$hiddeninplainsight",
            description="A suspicious site may be hiding something in plain sight. Not everything is meant to be seen with the naked eye. Type flag{...flaggoeshere...} to submit. When you figure it out, type it as a chat. \n The site is: https://hiddeninplainsight.netlify.app/",
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
            description="Not everything is what it claims to be. A broken link might still lead to something valuable...if you know how to look! Type flag{...flaggoeshere...} to submit. When you figure it out, type it as a chat. \n Link: https://behindtheframe.netlify.app/"
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
            description="The flag isn't always in plain sight, but the browser knows more than it shows. Try digging a little deeper. Flag will be in format flag{...flaggoeshere} When you figure it out, type it as a chat. \n Link: https://pagehunt.netlify.app/ "
        )
        embed.set_footer(text="💙🩷 Techfluences x Cyber Valkyries")
        await message.channel.send(embed=embed)

        def check(m):
            return m.author==message.author and m.channel ==message.channel
        response=await client.wait_for('message',check=check)
        if response.content.strip() == pagehunt:
            await message.channel.send("Congrats! You have completed this challenge.")
        else:
            await message.channel.send("Incorrect. Type $pagehunt to try again.")
    
# $hiddenlayers
    if message.content.startswith('$hiddenlayers'):
        embed=discord.Embed(
            title='$pagehunt',
            description="Looks like just an ordinary picture... or is it? Try peeling back a few digital layers. Flag will be in format flag{...flaggoeshere...} When you figure it out, type it as a chat. \n Link to image: https://drive.google.com/file/d/1BnbaDnG5DICcrVUVLwIBZB9p1njInjx4/view?usp=sharing"
        )
        embed.set_footer(text="💙🩷 Techfluences x Cyber Valkyries")
        await message.channel.send(embed=embed)

        def check(m):
            return m.author==message.author and m.channel == message.channel
        response=await client.wait_for('message', check=check)
        if response.content.strip() == hiddenlayers:
            await message.channel.send("Congrats! You have completed this challenge.")
        else:
            await message.channel.send("Incorrect. Type $hiddenlayers to try again.")

# $codecascade
    if message.content.startswith('$codecascade'):
        embed=discord.Embed(
            title="$codecascade",
            description="Sometimes the signal is buried in noise. We intercepted a corrupted message, but it still contains a secret code. The flag will be 15 digits in a row, undisturbed. Can you pull it out? \n Link to message: https://tinyurl.com/codecascade"
        )
        embed.set_footer(text="💙🩷 Techfluences x Cyber Valkyries")
        await message.channel.send(embed=embed)

        def check(m):
            return m.author==message.author and m.channel==message.channel
        response=await client.wait_for("message", check=check)
        if response.content.strip() == codecascade:
            await message.channel.send("Congrats! You've completed this challenge.")
        else: await message.channel.send("Incorrect. Type $codecascade to try again.")

# $birdsnest
    if message.content.startswith('$birdsnest'):
        embed=discord.Embed(
            title="$birdsnest",
            description="You've intercepted a suspicious archive containing hundreds of files and dozens of folders, one of these files has the flag in flag{...} format. \n Link to download zip: https://drive.google.com/file/d/14JaIUjbzTehlbzXXlCv_u_6RbnB-x3Lw/view?usp=sharing"
        )
        embed.set_footer(text="💙🩷 Techfluences x Cyber Valkyries")
        await message.channel.send(embed=embed)

        def check(m):
            return m.author==message.author and m.channel==message.channel
        response=await client.wait_for("message", check=check)
        if response.content.strip() == birdsnest:
            await message.channel.send("Congrats! You've completed this challenge.")
        else: await message.channel.send("Incorrect. Type $birdsnest to try again.")

# $yranib
    if message.content.startswith("$yranib"):
        embed=discord.Embed(
            title="$yranib",
            description="You are given a binary. Reverse engineer it to find the secret code to get the flag. Flag format will be: FLAG{...}\n Link to zip file: https://drive.google.com/file/d/1_qcJBQVAU98FNTg99Jy1zikiODtIXocO/view?usp=sharing"
        )
        embed.set_footer(text="💙🩷 Techfluences x Cyber Valkyries")
        await message.channel.send(embed=embed)

        def check(m):
            return m.author==message.author and m.channel==message.channel
        response=await client.wait_for("message", check=check)
        if response.content.strip() == yranib:
            await message.channel.send("Congrats! You've completed this challenge.")
        else: await message.channel.send("Incorrect. Type $yranib to try again")

# $doubletrouble
    if message.content.startswith("$doubletrouble"):
        embed=discord.Embed(
            title="$doubletrouble",
            description="The secret flag is hidden behind layer(s) of encryption. Can you reverse the encryption to get the flag?\nThe flag is: c3ludHtxaG95eXJfcmFwZWxjZ3JhZ30="
        )
        embed.set_footer(text="💙🩷 Techfluences x Cyber Valkyries")
        await message.channel.send(embed=embed)

        def check(m):
            return m.author==message.author and m.channel==message.channel
        response=await client.wait_for("message", check=check)
        if response.content.strip() == doubletrouble:
            await message.channel.send("Congrats! You've completed this challenge.")
        else: await message.channel.send("Incorrect. Type $doubletrouble to try again")

# $metadata
    if message.content.startswith("$metadata"):
        embed=discord.Embed(
            title="$metadata",
            description="The flag is hidden somewhere in this image...\n Download directly from Google Drive: https://drive.google.com/file/d/1hUbX6GtjPadQhABoNXeO2OD6GdWNXP_B/view?usp=sharing"
        )
        embed.set_footer(text="💙🩷 Techfluences x Cyber Valkyries")
        await message.channel.send(embed=embed)

        def check(m):
            return m.author==message.author and m.channel==message.channel
        response=await client.wait_for("message", check=check)
        if response.content.strip() == metadata:
            await message.channel.send("Congrats! You've completed this challenge.")
        else: await message.channel.send("Incorrect. Type $metadata to try again")
client.run('MTM5MDQ3NzM4Mjg1ODcwNjk5NA.GzwHpB.oi1MKeGhXa4UZHwGKK6qTXevNruYs3xueafO0E')