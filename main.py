import discord
from discord.ext import commands
import os, sys
import asyncio
import dotenv

#Since there are user defined packages, adding current directory to python path
current_directory = os.getcwd()
sys.path.append(current_directory)

dotenv.load_dotenv(".env")
intents = discord.Intents.all()

client = commands.Bot(command_prefix='!', intents=intents)

#alert message on commandline that bot has successfully logged in
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

#load cogs
async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with client:
        await load()
        await client.start(os.getenv('YOUR_TOKEN'))#put your token here

@client.command()
async def join(ctx):
    # Verification process
    verified = await verify_user(ctx.author)  # Call your verification function

    if verified:
        # Get the 'contributor' role
        role = discord.utils.get(ctx.guild.roles, name='contributor')

        if role:
            await ctx.author.add_roles(role)
            await ctx.send(f'Congratulations {ctx.author.mention}! You have been awarded the "contributor" role.')
        else:
            await ctx.send('The "contributor" role was not found on this server.')
    else:
        await ctx.send('Verification failed. You are not eligible to receive the "contributor" role.')

async def verify_user(user):
    return True
asyncio.run(main())


