import discord
from discord.ext import commands, tasks
import random
import datetime
from time import sleep

#Talk about discord intens
#Talk about slash commands
#Talk about ids (guild id, channel id, and user id)
#Talk about how to use custom emotes and the such


#Explain how discord.js makes coustom emotes easier since it checks EVERY message and not just ones with the prefix
#Can emulate with discord.py by checking every message with on_message event

with open("token.txt", "r") as tokenFile:
    botToken = tokenFile.read().strip()

activity = discord.Game(name="HELLO :3 | .\'COMMANDS\'")

bot = commands.Bot(command_prefix='.', activity=activity, intents=discord.Intents.all(), case_insensitive=True, status=discord.Status.do_not_disturb)

#Election Stuff
election_in_progress = False
candidates = {}
votes = {}


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    check_remind_me.start()
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)


@bot.tree.command(name="ping")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("HELLO!", ephemeral=True)

#@bot.command(name="ping")
#async def pingcommand(ctx):
#    await ctx.send("HELLO!")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if "shocked" in message.content.lower():
        await message.add_reaction("<:shocked:1230034617755762758>")
    await bot.process_commands(message)


@bot.command(name="8ball")
async def eightball(ctx):
    responses = ["It is certain.", "It is decidedly so.", "Without a doubt.", "Yes - definitely.", "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.", "Reply hazy, try again.", "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good.", "Very doubtful."]
    await ctx.reply(random.choice(responses), mention_author=False)


@bot.command(name="roll")
async def roll(ctx, dice: str):
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.reply("Format has to be in NdN!")
        return

    result = 0
    for _ in range(rolls):
        result += random.randint(1, limit)
        
    await ctx.reply(result)


@bot.command(name="rps")
async def rps(ctx, choice: str):
    choices = ["rock", "paper", "scissors"]
    if choice.lower() not in choices:
        await ctx.reply("Invalid choice! Choose rock, paper, or scissors.")
        return

    botChoice = random.choice(choices)
    if choice.lower() == botChoice:
        await ctx.reply(f"Bot chose {botChoice}. You live another day.")
    elif (choice.lower() == "rock" and botChoice == "scissors") or (choice.lower() == "paper" and botChoice == "rock") or (choice.lower() == "scissors" and botChoice == "paper"):
        await ctx.reply(f"Bot chose {botChoice}. Good job.....")
    else:
        await ctx.reply(f"Bot chose {botChoice}. Everyone say bye bye!")
        await ctx.send("3...")
        sleep(1)
        await ctx.send("2...")
        sleep(1)
        await ctx.send("1...")
        sleep(1)
        await ctx.send("https://tenor.com/view/cat-wave-hi-gif-24278813")
        sleep(1)
        await ctx.author.kick(reason="You lost.")


@bot.command(name="remindme")
async def remindme(ctx, time: str, *, message: str):
    try:
        hour, minute = map(int, time.split(':'))
    except Exception:
        await ctx.reply("Format has to be in HH:MM!")
        return

    with open("remindmefile", "a") as file:
        file.write(f"{hour} {minute} {ctx.author.id} {ctx.guild.id} {ctx.channel.id} {message}\n")
    await ctx.reply(f"Reminder set for {hour}:{minute} with message: {message}")


@tasks.loop(seconds=1)
async def check_remind_me():
    today = datetime.datetime.now()
    lines_to_keep = []
    with open("remindmefile", "r") as file:
        lines = file.read().splitlines()
    for line in lines:
        hour, minute, author, guild_id, channel_id = line.split()[0:5]
        message = " ".join(line.split()[5:])
        if int(hour) == today.hour and int(minute) == today.minute:
            #DM Reminder
            #user = await bot.fetch_user(int(author))
            #await user.send(f"Reminder: {message}")
            #Same server reminder (good for tutorial)
            user = await bot.fetch_user(int(author))
            guild = bot.get_guild(int(guild_id))
            if guild is not None:
                channel = guild.get_channel(int(channel_id))
                if channel is not None:
                    await channel.send(f"{user.mention}'s reminder: {message}")
        else:
            lines_to_keep.append(line)
    with open("remindmefile", "w") as file:
        file.write("\n".join(lines_to_keep))


@bot.command(name="electionstart")
async def electionstart(ctx, role: str, *names: str):
    if ctx.author.id == 284536152680300552:
        global election_in_progress
        global candidates
        global votes
        if election_in_progress:
            await ctx.send("An election is already in progress.")
            return
        election_in_progress = True
        candidates = {name: 0 for name in names}
        votes = {}
        await ctx.send(f"Election for {role} started! Candidates: {', '.join(names)}")


@bot.tree.command(name="vote")
async def vote(ctx: discord.Interaction, name: str):
    global election_in_progress
    global candidates
    global votes
    if not election_in_progress:
        await ctx.response.send_message("No election in progress.", ephemeral=True)
        return
    if name not in candidates:
        await ctx.response.send_message(f"{name} is not a candidate in this election.", ephemeral=True)
        return
    if ctx.user.id in votes:
        await ctx.response.send_message("You have already voted in this election.", ephemeral=True)
        return
    candidates[name] += 1
    votes[ctx.user.id] = name
    await ctx.response.send_message(f"Vote for {name} registered.", ephemeral=True)


@bot.command(name="electionstop")
async def electionstop(ctx):
    if ctx.author.id == 284536152680300552:
        global election_in_progress
        global candidates
        if not election_in_progress:
            await ctx.send("No election in progress.")
            return
        election_in_progress = False
        winner = max(candidates, key=candidates.get)
        await ctx.send(f"Election ended! The winner is {winner} with {candidates[winner]} votes.")


bot.run(botToken)