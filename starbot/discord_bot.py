"""Discord bot entry point for StarBot."""

from __future__ import annotations

import logging

import discord
from discord import app_commands
from discord.ext import commands

from .agent import agent
from .config import settings

logger = logging.getLogger(__name__)


class StarBot(commands.Bot):
    """Discord bot wired to the StarBot agent."""

    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.messages = True
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self) -> None:  # pragma: no cover - Discord lifecycle
        await self.tree.sync()
        logger.info("StarBot is ready and commands are synced.")

    async def on_ready(self) -> None:  # pragma: no cover - Discord lifecycle
        logger.info("Logged in as %s", self.user)

    async def on_message(self, message: discord.Message) -> None:
        if message.author == self.user:
            return
        if message.guild is None:
            reply = agent.generate_reply(message.author.display_name, message.content)
            await message.channel.send(reply)
        await self.process_commands(message)


bot = StarBot()


@bot.tree.command(name="ask", description="Ask StarBot a question.")
@app_commands.describe(question="What would you like to know?")
async def ask_command(interaction: discord.Interaction, question: str) -> None:
    """Handle the /ask slash command."""

    await interaction.response.defer(thinking=True)
    reply = agent.generate_reply(interaction.user.display_name, question)
    await interaction.followup.send(reply)


@bot.command(name="ping")
async def ping(ctx: commands.Context[commands.Bot]) -> None:
    """Basic health-check command."""

    await ctx.send("Pong! StarBot is operational.")


def run() -> None:
    """Run the Discord bot."""

    if not settings.discord_token:
        raise RuntimeError("DISCORD_TOKEN is required to start StarBot.")
    bot.run(settings.discord_token)
