import discord
from discord import app_commands
from discord.ext import commands

# ========= CONFIG =========
TOKEN = "MTM1ODk0NDUwNDQ2MzM2MDA0MA.GhJUkB.X9HPigv7wh5yituhlhSEZH-dWROK6oJ38ATcM0"
OWNER_ID = 1306023492956848228  # coloque seu ID aqui
# ==========================

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Estados (você pode salvar em JSON se quiser persistir)
painel_config = {
    "anti_bot": False,
    "anti_raid": False,
    "anti_nuke": False
}

# Classe do Painel
class PainelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != OWNER_ID:
            await interaction.response.send_message("❌ Apenas o dono pode usar este painel.", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="Anti-Bot", style=discord.ButtonStyle.danger, custom_id="painel_antibot")
    async def antibot(self, interaction: discord.Interaction, button: discord.ui.Button):
        painel_config["anti_bot"] = not painel_config["anti_bot"]
        estado = "✅ Ativado" if painel_config["anti_bot"] else "❌ Desativado"
        await interaction.response.edit_message(embed=gerar_embed(), view=PainelView())
        await interaction.followup.send(f"Anti-Bot agora está **{estado}**", ephemeral=True)

    @discord.ui.button(label="Anti-Raid", style=discord.ButtonStyle.danger, custom_id="painel_antiraid")
    async def antiraid(self, interaction: discord.Interaction, button: discord.ui.Button):
        painel_config["anti_raid"] = not painel_config["anti_raid"]
        estado = "✅ Ativado" if painel_config["anti_raid"] else "❌ Desativado"
        await interaction.response.edit_message(embed=gerar_embed(), view=PainelView())
        await interaction.followup.send(f"Anti-Raid agora está **{estado}**", ephemeral=True)

    @discord.ui.button(label="Anti-Nuke", style=discord.ButtonStyle.danger, custom_id="painel_antinuke")
    async def antinuke(self, interaction: discord.Interaction, button: discord.ui.Button):
        painel_config["anti_nuke"] = not painel_config["anti_nuke"]
        estado = "✅ Ativado" if painel_config["anti_nuke"] else "❌ Desativado"
        await interaction.response.edit_message(embed=gerar_embed(), view=PainelView())
        await interaction.followup.send(f"Anti-Nuke agora está **{estado}**", ephemeral=True)


# Função para gerar a embed do painel
def gerar_embed():
    embed = discord.Embed(
        title="⚙️ Painel do Administrador",
        description="Aqui você pode alternar os sistemas de segurança.\n\n"
                    f"**Anti-Bot:** {'✅ Ativado' if painel_config['anti_bot'] else '❌ Desativado'}\n"
                    f"**Anti-Raid:** {'✅ Ativado' if painel_config['anti_raid'] else '❌ Desativado'}\n"
                    f"**Anti-Nuke:** {'✅ Ativado' if painel_config['anti_nuke'] else '❌ Desativado'}",
        color=discord.Color.red()
    )
    embed.set_footer(text="Somente o dono pode usar este painel")
    return embed


# Comando /painel
@bot.tree.command(name="painel", description="Abrir o painel do administrador")
async def painel(interaction: discord.Interaction):
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("❌ Apenas o dono pode usar este comando.", ephemeral=True)
        return

    await interaction.response.send_message(embed=gerar_embed(), view=PainelView())


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Bot online como {bot.user}")


bot.run(TOKEN)
