import os
import discord

from dotenv import load_dotenv
from discord import app_commands

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("GUILD_ID")

try:
    MY_GUILD = discord.Object(id=str(GUILD))
except Exception as e:
    print(e)


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


intents = discord.Intents.default()
client = MyClient(intents=intents)


def get_spinning_wheel_channel(
    guild: discord.Guild,
) -> discord.abc.GuildChannel | None:
    for guild in client.guilds:
        for channel in guild.channels:
            if "spinning_wheel_challenge" in channel.name:
                return channel
        print("Spinning Wheel Channel not found. Are you sure it exists?")


async def get_messages(channel: discord.TextChannel) -> list:
    return [message async for message in channel.history()]


def get_upvotes_from_message(message: discord.Message) -> int:
    try:
        return discord.utils.get(message.reactions, emoji="⬆️").count
    except AttributeError:
        return 0


def sort_by_upvotes(messages: list) -> list:
    return sorted(messages, key=lambda message: get_upvotes_from_message(message), reverse=True)


@client.tree.command(
    name="new_generate", description="An updated version of the generated command."
)
async def generate_challenges(interaction: discord.Interaction):
    channel = get_spinning_wheel_channel(MY_GUILD)
    messages = await get_messages(channel)
    sorted_messages = sort_by_upvotes(messages)
    
    for message in sorted_messages:
        print(message.content)

    await interaction.response.send_message(
        "Command Executed Successfully!", ephemeral=True
    )


client.run(TOKEN)
