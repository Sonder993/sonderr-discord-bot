
import os
import discord
from discord.ext import commands
from discord import app_commands

TOKEN = os.environ["DISCORD_TOKEN"]

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

CATEGORIES = {
    "01・INFORMATION": [
        "👋・welcome",
        "📜・rules",
        "✅・verification",
        "🎭・roles",
    ],
    "02・IMPORTANT": [
        "📢・announcements",
        "🛠️・script-updates",
        "🎬・social-media",
        "📋・applications",
    ],
    "03・STORE": [
        "🛒・r6-scripts",
        "💰・pricing",
        "💳・payment-methods",
        "🎟️・purchase-ticket",
    ],
    "04・SUPPORT": [
        "🎫・open-ticket",
        "📦・order-info",
        "❓・faq",
        "⭐・reviews",
    ],
    "05・COMMUNITY": [
        "💬・general",
        "🎮・r6-chat",
        "📸・clips",
        "💡・suggestions",
    ],
    "06・STAFF": [
        "🔒・staff-chat",
        "🔒・ticket-logs",
        "🔒・staff-updates",
        "🔊・staff-voice",
    ],
}

ROLES = [
    ("Owner", 0xE8A4E8),
    ("Admin", 0xB58AE8),
    ("Staff", 0x8B78D9),
    ("Customer", 0x80C7FF),
    ("Member", 0xB8B8B8),
]

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    if not getattr(bot, "synced", False):
        await bot.tree.sync()
        bot.synced = True

@bot.tree.command(
    name="setup",
    description="Create the SONDERR store layout"
)
@app_commands.guild_only()
@app_commands.default_permissions(administrator=True)
async def setup(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            "Only server administrators can run setup.",
            ephemeral=True
        )
        return

    await interaction.response.defer(ephemeral=True)
    guild = interaction.guild

    for name, colour in ROLES:
        if not discord.utils.get(guild.roles, name=name):
            await guild.create_role(
                name=name,
                colour=discord.Colour(colour),
                reason="SONDERR initial setup"
            )

    staff_role = discord.utils.get(guild.roles, name="Staff")
    admin_role = discord.utils.get(guild.roles, name="Admin")
    owner_role = discord.utils.get(guild.roles, name="Owner")

    for category_name, channels in CATEGORIES.items():
        category = discord.utils.get(
            guild.categories, name=category_name
        )

        if category is None:
            category = await guild.create_category(
                category_name,
                reason="SONDERR initial setup"
            )

        if category_name == "06・STAFF":
            await category.set_permissions(
                guild.default_role, view_channel=False
            )
            for role in (staff_role, admin_role, owner_role):
                await category.set_permissions(
                    role, view_channel=True,
                    send_messages=True
                )

        for channel_name in channels:
            if discord.utils.get(
                category.channels, name=channel_name
            ):
                continue

            if channel_name == "🔊・staff-voice":
                await guild.create_voice_channel(
                    channel_name, category=category
                )
            else:
                await guild.create_text_channel(
                    channel_name, category=category
                )

    await interaction.followup.send(
        "SONDERR store layout created successfully!",
        ephemeral=True
    )

bot.run(TOKEN)
