import discord
from discord.ext import commands
from enum import Enum
import random
import asyncio

#Talk about discord intens
#Talk about slash commands
#Talk about ids (guild id, channel id, and user id)
#Talk about how to use custom emotes and the such

with open("token.txt", "r") as tokenFile:
    botToken = tokenFile.read().strip()

activity = discord.Game(name="HELLO :3 | .\'COMMANDS\'")

bot = commands.Bot(command_prefix='.', activity=activity, intents=discord.Intents.all(), case_insensitive=True, status=discord.Status.do_not_disturb)

class GameStates(Enum):
    NOT_ = 0
    STARTED = 1
    PLAYING = 2
    ENDED = 3

game_started = GameStates.NOT_
game_channel = None
game_players = list()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)

#@bot.tree.command(name="ping")
#async def ping(interaction: discord.Interaction):
#    await interaction.response.send_message("HELLO!", ephemeral=True)

@bot.command(name="ping")
async def pingcommand(ctx):
    await ctx.send("HELLO!")

@bot.command(name="start")
async def start(ctx):
    global game_started
    global game_channel
    if game_started == GameStates.STARTED:
        await ctx.send("Game has already started!")
        return
    game_started = GameStates.STARTED
    game_channel = ctx.channel
    await ctx.send("Game has started use .join to join the game!")


@bot.command(name="join")
async def join(ctx):
    global game_started
    if game_started != GameStates.STARTED:
        await ctx.send("Game has not started yet!")
        return
    if ctx.author in game_players:
        await ctx.send("You are already in the game!")
        return
    game_players.append(ctx.author)
    await ctx.send(f"Player {ctx.author} has joined the game!")


@bot.command(name="players")
async def players(ctx):
    global game_players
    if len(game_players) == 0:
        await ctx.send("No players have joined the game!")
        return
    players = ", ".join([str(player) for player in game_players])
    await ctx.send(players)

#Make it so only someone with a specific role can use this command, also make it @ the person to teach how to do that
@bot.command(name="playing")
async def playing(ctx):
    global game_started
    if game_started == GameStates.PLAYING:
        await ctx.send("Game Already Started!")
        return
    if len(game_players) == 0:
        await ctx.send("No players have joined the game!")
        return
    if len(game_players) == 1:
        await ctx.send(str(game_players[0]) + " has won the game")
        return
    game_started = GameStates.PLAYING
    await ctx.send("Game has started! Good luck!")


bot.run(botToken)