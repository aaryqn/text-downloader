import discord
from discord.ext import commands
import asyncio

token = 'your_user_token_here'
channel_id = 'your_channel_id_here'
output_file = 'messages.txt'

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    channel = bot.get_channel(int(channel_id))
    if not channel:
        print(f'Error: Channel with ID {channel_id} not found.')
        return
    print(f'Downloading messages from {channel}...')

    try:
        messages = await channel.history(limit=None).flatten()
        if messages:
            with open(output_file, 'w', encoding='utf-8') as f:
                for message in messages:
                    f.write(f'{message.created_at} - {message.author}: {message.content}\n')

            print('Messages saved to file.')
        else:
            print('No messages found.')
    except discord.errors.HTTPException as e:
        print(f'Failed to download messages: {e}')

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command()
async def clear(ctx, amount=1):
    await ctx.channel.purge(limit=amount + 1)

@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'Kicked {member.mention}')

@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention}')

@bot.command()
async def greet(ctx):
    await ctx.send(f'Hello {ctx.author.mention}!')

@bot.command()
async def echo(ctx, *, message):
    await ctx.send(message)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Invalid command. Use !help to see available commands.')

@bot.command()
async def help(ctx):
    help_embed = discord.Embed(title="Bot Commands", description="List of available commands:", color=discord.Color.blue())
    help_embed.add_field(name="!ping", value="Check if the bot is online.", inline=False)
    help_embed.add_field(name="!clear [amount]", value="Delete the specified number of messages (default 1).", inline=False)
    help_embed.add_field(name="!kick [user] [reason]", value="Kick the specified user from the server.", inline=False)
    help_embed.add_field(name="!ban [user] [reason]", value="Ban the specified user from the server.", inline=False)
    help_embed.add_field(name="!greet", value="Greet the user who invoked the command.", inline=False)
    help_embed.add_field(name="!echo [message]", value="Echo the specified message.", inline=False)
    await ctx.send(embed=help_embed)

loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(bot.start(token))
except KeyboardInterrupt:
    loop.run_until_complete(bot.close())
finally:
    loop.close()
