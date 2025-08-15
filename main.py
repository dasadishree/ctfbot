import discord
from discord.ext import commands
import firebase_admin
from firebase_admin import credentials, firestore
import asyncio

# Initialize Firebase
try:
    cred = credentials.Certificate('firebase-service-account.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("Firebase initialized successfully!")
except Exception as e:
    print(f"Warning: Firebase initialization failed: {e}")
    print("Bot will run with local storage only (data will not persist)")
    db = None

# points & leaderboard
user_points = {}
solved_challenges = {}

user_channels = {}

# create priv channel
async def get_user_channel(user):
    """Get or create a private channel for a user"""
    user_id = str(user.id)
    
    if user_id in user_channels:
        try:
            channel = client.get_channel(user_channels[user_id])
            if channel:
                return channel
        except:
            del user_channels[user_id]
    
    try:
        guild = user.guild
        if not guild:
            return None
            
        target_category = None
        for category in guild.categories:
            if "capture the flag" in category.name.lower():
                target_category = category
                break
        
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_channels=True)
        }
        
        if target_category:
            channel = await guild.create_text_channel(
                f"ctf-{user.display_name}",
                category=target_category,
                overwrites=overwrites,
                topic=f"Private CTF channel for {user.display_name}"
            )
        else:
            channel = await guild.create_text_channel(
                f"ctf-{user.display_name}",
                overwrites=overwrites,
                topic=f"Private CTF channel for {user.display_name}"
            )
        
        user_channels[user_id] = channel.id
        
        return channel
        
    except Exception as e:
        print(f"Error creating channel for user {user_id}: {e}")
        return None

# load firebase data
async def load_data_from_firebase():
    global user_points, solved_challenges
    if db is None:
        print("Firebase not available, starting with empty data")
        user_points = {}
        solved_challenges = {}
        return
        
    try:
        points_doc = db.collection('leaderboard').document('user_points').get()
        if points_doc.exists:
            user_points = points_doc.to_dict()
        else:
            user_points = {}
        
        challenges_doc = db.collection('leaderboard').document('solved_challenges').get()
        if challenges_doc.exists:
            solved_challenges = challenges_doc.to_dict()
        else:
            solved_challenges = {}
        
        print(f"Loaded {len(user_points)} users and {len(solved_challenges)} challenge records from Firebase")
    except Exception as e:
        print(f"Error loading data from Firebase: {e}")
        user_points = {}
        solved_challenges = {}

# save firebase datas
async def save_data_to_firebase():
    if db is None:
        print("Firebase not available, data not saved")
        return
        
    try:
        db.collection('leaderboard').document('user_points').set(user_points)
        
        db.collection('leaderboard').document('solved_challenges').set(solved_challenges)
        
        print("Data saved to Firebase successfully")
    except Exception as e:
        print(f"Error saving data to Firebase: {e}")

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

#manage points and stuff
def add_points(user_id, points_to_add, challenge_name):
    user_id_str = str(user_id)
    current_points = user_points.get(user_id_str, 0)
    user_points[user_id_str] = current_points + points_to_add

    if user_id_str not in solved_challenges:
        solved_challenges[user_id_str] = []
    solved_challenges[user_id_str].append(challenge_name)
    
    # save to firebase after updating
    asyncio.create_task(save_data_to_firebase())

# checks if challenge has been solved or not
def is_solved(user_id, challenge_name):
    return str(user_id) in solved_challenges and challenge_name in solved_challenges[str(user_id)]

# when bot is run
@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))
    await load_data_from_firebase()
    print("Bot is ready!")

# when bot sees message
@client.event
async def on_message(message):
    # only tracks others' messages
    if message.author == client.user:
        return
    
    # check & redirect
    ctf_commands = ['$challenges', '$beginner', '$intermediate', '$advanced', 
                    '$mypoints', '$infiltrate', '$hiddeninplainsight', '$behindtheframe', 
                    '$pagehunt', '$hiddenlayers', '$codecascade', '$birdsnest', '$yranib', 
                    '$doubletrouble', '$metadata']
    
    if any(message.content.startswith(cmd) for cmd in ctf_commands):
        user_id = str(message.author.id)
        if user_id in user_channels and message.channel.id == user_channels[user_id]:
            pass
        else:
            embed = discord.Embed(
                title="🔐 Private Channel Required",
                description="CTF commands only work in your private channel. Use `$ctfstart` in #ctf-start to create one!",
                color=discord.Color.blue()
            )
            embed.set_footer(text="💙🩷 Techfluences x Cyber Valkyries")
            await message.channel.send(embed=embed)
            return
    
    # responds to commands
    if message.content.startswith('$ctfstart'):
        # only allow $ctfstart in the ctf-start channel
        if message.channel.name != "ctf-start":
            embed = discord.Embed(
                title="❌ Wrong Channel",
                description="Use `$ctfstart` in the #ctf-start channel only!",
                color=discord.Color.red()
            )
            embed.set_footer(text="💙🩷 Techfluences x Cyber Valkyries")
            await message.channel.send(embed=embed)
            return
            
        # create private channel
        private_channel = await get_user_channel(message.author)
        
        if private_channel:
            embed = discord.Embed(
                title='🎯 Welcome to Capture The Flag (CTF)',
                description='CTF is a cybersecurity competition that can help you practice security skills in a fun way. The goal is to "capture" the "flags" throughout the challenges we will give you. Each flag\'s format will be specified per challenge.\n\n **This is your private CTF channel!** All your challenge attempts and progress will be private here.\n\n Run $help for a list of commands. Have fun, and there may or may not be prizes...',
                color=discord.Colour.purple()
            )
            embed.add_field(
                name="🚀 Get Started",
                value="Try these commands:\n• `$challenges` - View all challenges\n• `$leaderboard` - see top scorers\n• `$help` - See all commands\n• `$mypoints` - See your points",
                inline=False
            )
            embed.set_footer(text="💙🩷 Techfluences x Cyber Valkyries")
            
            await private_channel.send(embed=embed)
            
            embed_public = discord.Embed(
                title="🎯 CTF Started!",
                description=f"Welcome to CTF, {message.author.display_name}! I've created your private channel: {private_channel.mention}\n\n**All your CTF interactions will happen there!**",
                color=discord.Colour.green()
            )
            embed_public.set_footer(text="💙🩷 Techfluences x Cyber Valkyries")
            await message.channel.send(embed=embed_public)
        else:
            embed = discord.Embed(
                title="❌ Error",
                description="Could not create your private channel. Make sure I have permission to create channels in this server.",
                color=discord.Color.red()
            )
            embed.set_footer(text="💙🩷 Techfluences x Cyber Valkyries")
            await message.channel.send(embed=embed)
        return
    
    # Redirect any other CTF commands used in #ctf-start channel
    if message.channel.name == "ctf-start" and message.content.startswith('$'):
        embed = discord.Embed(
            title="❌ Wrong Channel",
            description="This channel is only for `$ctfstart` to create your private channel.\n\n**Use your private CTF channel for all other commands like $help, $challenges, etc. \n Ping @adishreeed for questions/help.",
            color=discord.Color.blue()
        )
        embed.set_footer(text="💙🩷 Techfluences x Cyber Valkyries")
        await message.channel.send(embed=embed)
        return

    #view all possible challenges
    if message.content.startswith('$challenges'):
        embed=discord.Embed(
            title="🎯 CHALLENGES",
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
        return

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
        return

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
        return

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
        return

# help
    if message.content.startswith('$help'):
       embed=discord.Embed(
           title="HELP",
           description="$ctfstart for initial instructions & description\n\n$challenges to view all challenges\n\n$beginner to view only beginner challenges\n\n$intermediate to view all intermediate challenges\n\n$advanced to view only advanced challenges\n\nLastly, type the challenge name (including the dollarsign) to view more instructions and submit flags.\n\n$mypoints to see your stats\n$leaderboard to a leaderboard of players",
           color=discord.Color.purple()
       )
       embed.set_footer(text="💙🩷 Techfluences x Cyber Valkyries")
       await message.channel.send(embed=embed)
       return
       
# $mypoints
    if message.content.startswith("$mypoints"):
        user_id = message.author.id
        current_points = user_points.get(str(user_id), 0)
        solved_count = len(solved_challenges.get(str(user_id), []))
        
        embed=discord.Embed(
            title=f"{message.author.display_name}'s Stats",
            description=f"You currently have **{current_points}** points\nYou have solved **{solved_count}** challenges",
            color=discord.Color.purple()
        )
        
        if solved_count > 0:
            solved_list = ", ".join(solved_challenges[user_id])
            embed.add_field(name="Solved Challenges", value=solved_list, inline=False)
        
        embed.set_footer(text="💙🩷 Techfluences x Cyber Valkyries")
        await message.channel.send(embed=embed)
        return

# $leaderboard
    if message.content.startswith("$leaderboard"):
        if not user_points:
            await message.channel.send("No one has solved any challenges yet!")
            return
        
        sorted_users = sorted(user_points.items(), key=lambda x: x[1], reverse=True)
        
        embed = discord.Embed(
            title="Leaderboard",
            description="Top players by points",
            color=discord.Color.purple()
        )
        
        for i, (user_id, points) in enumerate(sorted_users[:10], 1): 
            try:
                user = await client.fetch_user(int(user_id))
                username = user.display_name
            except:
                username = f"User {user_id}"
            
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"#{i}"
            embed.add_field(
                name=f"{medal} {username}",
                value=f"{points} points",
                inline=False
            )
        
        embed.set_footer(text="💙🩷 Techfluences x Cyber Valkyries")
        await message.channel.send(embed=embed)
        return

# $infiltrate
    if message.content.startswith('$infiltrate'):
        if is_solved(message.author.id, "$infiltrate"):
            embed = discord.Embed(
                title="Already Solved!",
                description="You have already solved this challenge!",
                color=discord.Color.green()
            )
            embed.set_footer(text="💙🩷 Techfluences x Cyber Valkyries")
            await message.channel.send(embed=embed)
            return
        
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
            add_points(message.author.id, 1, "$infiltrate")
            await message.channel.send("Access Granted! You have completed this challenge.")
        else:
            await message.channel.send("Invalid login. Type $infiltrate again to try again.")
        return

# $hiddeninplainsight
    if message.content.startswith('$hiddeninplainsight'):
        if is_solved(message.author.id, "$hiddeninplainsight"):
            await message.channel.send("You have already solved this challenge!")
            return
        
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
            add_points(message.author.id, 1, "$hiddeninplainsight")
            await message.channel.send("Access Granted! You have completed this challenge.")
        else:
            await message.channel.send("Incorrect. Type $hiddeninplainsight to try again.")
        return

# $behindtheframe
    if message.content.startswith('$behindtheframe'):
        if is_solved(message.author.id, "$behindtheframe"):
            await message.channel.send("You have already solved this challenge!")
            return
        
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
            add_points(message.author.id, 1, "$behindtheframe")
            await message.channel.send("Congrats! You have completed this challenge.")
        else:
            await message.channel.send("Incorrect. Type $behindtheframe to try again.")
        return

# $pagehunt
    if message.content.startswith('$pagehunt'):
        if is_solved(message.author.id, "$pagehunt"):
            await message.channel.send("You have already solved this challenge!")
            return

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
            add_points(message.author.id, 2, "$pagehunt")
            await message.channel.send("Congrats! You have completed this challenge.")
        else:
            await message.channel.send("Incorrect. Type $pagehunt to try again.")
        return
    
# $hiddenlayers
    if message.content.startswith('$hiddenlayers'):
        if is_solved(message.author.id, "$hiddenlayers"):
            await message.channel.send("You have already solved this challenge!")
            return
        
        embed=discord.Embed(
            title='$hiddenlayers',
            description="Looks like just an ordinary picture... or is it? Try peeling back a few digital layers. Flag will be in format flag{...flaggoeshere...} When you figure it out, type it as a chat. \n Link to image: https://drive.google.com/file/d/1BnbaDnG5DICcrVUVLwIBZB9p1njInjx4/view?usp=sharing"
        )
        embed.set_footer(text="💙🩷 Techfluences x Cyber Valkyries")
        await message.channel.send(embed=embed)

        def check(m):
            return m.author==message.author and m.channel == message.channel
        
        response=await client.wait_for('message', check=check)
        if response.content.strip() == hiddenlayers:
            add_points(message.author.id, 2, "$hiddenlayers")
            await message.channel.send("Congrats! You have completed this challenge.")
        else:
            await message.channel.send("Incorrect. Type $hiddenlayers to try again.")
        return

# $codecascade
    if message.content.startswith('$codecascade'):
        if is_solved(message.author.id, "$codecascade"):
            await message.channel.send("You have already solved this challenge!")
            return
        
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
            add_points(message.author.id, 2, "$codecascade")
            await message.channel.send("Congrats! You've completed this challenge.")
        else: await message.channel.send("Incorrect. Type $codecascade to try again.")
        return

# $birdsnest
    if message.content.startswith('$birdsnest'):
        if is_solved(message.author.id, "$birdsnest"):
            await message.channel.send("You have already solved this challenge!")
            return

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
            add_points(message.author.id, 3, "$birdsnest")
            await message.channel.send("Congrats! You've completed this challenge.")
        else: await message.channel.send("Incorrect. Type $birdsnest to try again.")
        return

# $yranib
    if message.content.startswith("$yranib"):
        if is_solved(message.author.id, "$yranib"):
            await message.channel.send("You have already solved this challenge!")
            return
        
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
            add_points(message.author.id, 3, "$yranib")
            await message.channel.send("Congrats! You've completed this challenge.")
        else: await message.channel.send("Incorrect. Type $yranib to try again")
        return

# $doubletrouble
    if message.content.startswith("$doubletrouble"):
        if is_solved(message.author.id, "$doubletrouble"):
            await message.channel.send("You have already solved this challenge!")
            return
        
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
            add_points(message.author.id, 2, "$doubletrouble")
            await message.channel.send("Congrats! You've completed this challenge.")
        else: await message.channel.send("Incorrect. Type $doubletrouble to try again")
        return

# $metadata
    if message.content.startswith("$metadata"):
        if is_solved(message.author.id, "$metadata"):
            await message.channel.send("You have already solved this challenge!")
            return
        
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
            add_points(message.author.id, 3, "$metadata")
            await message.channel.send("Congrats! You've completed this challenge.")
        else: await message.channel.send("Incorrect. Type $metadata to try again")
        return
client.run("MTM5MDQ3NzM4Mjg1ODcwNjk5NA.G8x4yX.iocAxv_If3C-bWu2_-03XKJiqhO3BHcHgDrU0c")