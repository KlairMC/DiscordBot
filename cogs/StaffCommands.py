import discord

from discord import Interaction
from discord.ext import commands
from discord.commands import SlashCommandGroup, Option

from modals.EmbedCreation import EmbedCreation
from modals.ChangeLog import ChangelogModal

from views.NewSuggestionView import CreateSuggestion
from views.NewTicketView import CreateTicket

from random import randint

class StaffCommands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        print(f"{self.__class__.__name__} loaded")

    setup = SlashCommandGroup(name="setup", description="Various Setup Commands")
    embed = SlashCommandGroup(name="embed", description="Various Embed Commands")
    

    @setup.command(name="suggestions", description="Sets up Suggestions")

    async def setup_suggestions(
        self,
        ctx: discord.ApplicationContext,
        panel: Option(discord.TextChannel, "The Channel to send the \"Create a Suggestion\" Panel"), # type: ignore
        suggestion: Option(discord.TextChannel, "The Channel to send the created Suggestion in") # type: ignore
    ):
        if self.bot.settings.get("Suggestions.Panel") != None: # type: ignore
            try:
                channel = await self.bot.fetch_channel(self.bot.settings.get("Suggestions.Panel")) # type: ignore
                message = await channel.history().find(lambda m: m.author == self.bot.user) # type: ignore
                await message.delete() # type: ignore
            except:
                pass
        
        self.bot.settings.set("Suggestions.Panel", panel.id) # type: ignore
        self.bot.settings.set("Suggestions.NewSuggestion", suggestion.id) # type: ignore
        await panel.send(embed=discord.Embed(title="Create a Suggestion", description="Click the button below to create a suggestion"), view=CreateSuggestion(bot=self.bot))
        embed = discord.Embed(title="Setup", description="Suggestion successfully setup")
        embed.add_field(name="Panel Channel", value=panel.mention)
        embed.add_field(name="Suggestion Channel", value=suggestion.mention)
        await ctx.respond(embed=embed)

    @setup.command(name="tickets", description="Sets up Tickets")
    @commands.has_permissions(manage_channels=True)
    async def setup_tickets(
        self,
        ctx: discord.ApplicationContext,
        panel: Option(discord.TextChannel, "The Channel to send the \"Create a Ticket\" Panel"),
        ticket: Option(discord.CategoryChannel, "The Category to create the Ticket Channel in") 
    ):
        if self.bot.settings.get("Tickets.Panel") != None: # type: ignore
            try:
                channel = await self.bot.fetch_channel(self.bot.settings.get("Tickets.Panel")) # type: ignore
                message = await channel.history().find(lambda m: m.author == self.bot.user) # type: ignore
                await message.delete() # type: ignore
            except:
                pass
        
        self.bot.settings.set("Tickets.Panel", panel.id) # type: ignore
        self.bot.settings.set("Tickets.Category", ticket.id) # type: ignore
        await panel.send(embed=discord.Embed(title="Create a Ticket", description="Click the button below to create a suggestion"), view=CreateTicket(bot=self.bot))
        embed = discord.Embed(title="Setup", description="Ticket Creator successfully setup")
        embed.add_field(name="Panel Channel", value=panel.mention)
        embed.add_field(name="Ticket Category", value=ticket.mention)
        await ctx.respond(embed=embed)

    @embed.command(name="rules", description="Sends Rules Embed")
    @commands.has_permissions(manage_messages = True)
    async def embedrules(
        self,
        ctx: discord.ApplicationContext,
    ):
        embed1 = discord.Embed(title="Klair", description="Welcome to the Official Discord Server of Klair Client. We are pleased to have you in our journey :D. Before continuing please read the rules and obey them, any user who breaks the rules is going to face some consequences (that is, ban, mute). NOTE: This Discord Server's Layout is inspired by Hybris.", color=discord.Color.red())
        embed1.set_footer(icon_url="https://asicalug.netlify.app/storage/klair.png",)
        embed2 = discord.Embed(url="https://discord.gg/Hybris", title="Hybris' Discord", color=discord.Color.red())
        embed3 = discord.Embed(title="", color=discord.Color.red())
        embed3.set_image(url="https://media.discordapp.net/attachments/1120373785967738880/1121014281727639684/Klair_Rules.png?width=1040&height=585")
        embed4 = discord.Embed(description="Check out the Rules before Starting Your Journey In our Discord Server - Klair", title="", color=discord.Color.red())
        embed5 = discord.Embed(title="", description="Remember, the rules are applied to all the behaviour on the server including Moderators and Staffs. If you See anyone breaking the Rules, report it to any online Staff/Mod.", color=discord.Color.red())
        embed5.add_field(name="Rules", value="* 1. Be Respectful and dont be mean to others :D\n\n* 2. No Spamming\n\n* 3. No Advertising,\n\n* 4. No Threatening\n\n* 5. Dont share any personal information\n\n* 6. Be a good person :D")
        await ctx.send_response(embeds=(embed1, embed2, embed3, embed4, embed5))
    
    @embed.command(name="changelog", description="Sends a changelog embed")
    @commands.has_permissions(manage_messages=True)
    async def embedchangelog(
        self,
        interaction: discord.Interaction
    ):
        await interaction.response.send_modal(ChangelogModal(bot=self.bot))

    @embed.command(name="create", description="Sends an embeded text")
    @commands.has_permissions(manage_messages=True)
    async def embedchangelog(
        self,
        interaction: discord.Interaction
    ):
        await interaction.response.send_modal(EmbedCreation(bot=self.bot))

    @setup.command(name="log", description="Sets up a logging channel")
    @commands.has_permissions(manage_channels=True)
    async def setuplog(
        self,
        ctx : discord.ApplicationContext,
        channel: Option(discord.TextChannel, "The Channel to send the logs"),
    ):
        self.bot.settings.set("Logs.Channel", channel.id) # type: ignore
        await ctx.send_response("Log Channel set", ephemeral=True)

    @commands.slash_command(name="warn", description="warn a user")
    @commands.has_permissions(moderate_members=True)
    async def warn(
        self, 
        ctx : discord.ApplicationContext,
        user : Option(discord.Member, "The user to warn"),
        reason : Option(str, "The reason the user has been warned")
    ):
        warns = (self.bot.settings.get(f"Warns.{user.id}") or 0) + 1
        self.bot.settings.set(f"Warns.{user.id}", warns)
        channel = self.bot.get_channel(self.bot.settings.get("Logs.Channel"))
        member = ctx.guild.get_member(ctx.user.id)
        await ctx.send_response(f"<@{user.id}> has been warned", ephemeral=True)
        embed = discord.Embed(title="Warned", description=f"You've been warned by <@{member.id}> in the Klair discord server, you now have `{warns}` warns.")
        embed.add_field(name="Reason", value=f"{reason}")
        await user.send(embed=embed)
        await channel.send(f"<@{user.id}> has been warned by <@{member.id}> for {reason} and has now `{warns}` warns.")

    @commands.slash_command(name="remove_warn", description="remove warn(s) from a user")
    @commands.has_permissions(moderate_members=True)
    async def remove_warn(
        self, 
        ctx : discord.ApplicationContext,
        user : Option(discord.Member, "The user to warn"),
        number : Option(int, "How much warns to remove"),
    ): 
        member = ctx.guild.get_member(ctx.user.id)
        remove_warn = self.bot.settings.get(f"Warns.{user.id}")-number
        self.bot.settings.set(f"Warns.{user.id}", remove_warn)
        warns = self.bot.settings.get(f"Warns.{user.id}")
        channel = self.bot.get_channel(self.bot.settings.get("Logs.Channel"))
        await ctx.send_response(f"{number} warns have been removed from <@{user.id}>", ephemeral=True)
        embed = discord.Embed(title="Warns Removed", description=f"{number} warns has been removed from your account on the Klair discord server, you now have `{warns}` warns.")
        await user.send(embed=embed)
        await channel.send(f"<@{member.id}> has removed {number} warns from <@{user.id}> and has now `{warns}` warns.")


    @commands.slash_command(name="info", description="Check a user's informations")
    @commands.has_permissions(moderate_members=True)
    async def info(
        self,
        ctx : discord.ApplicationContext,
        user : discord.Member,
    ):
        warns = self.bot.settings.get(f"Warns.{user.id}")

        if warns==None:
            embed = discord.Embed(title=f"{user}'s Info", description=f"This is {user}'s information")
            embed.set_author(name=f"{user}", icon_url=user.avatar)
            embed.add_field(name="Warns", value=f"{user} has `0` warns.")
            await ctx.send_response(embed=embed)
        else:
            embed = discord.Embed(title=f"{user}'s Info", description=f"This is {user}'s information")
            embed.set_author(name=f"{user}", icon_url=user.avatar)
            embed.add_field(name="Warns", value=f"{user} has `{warns}` warns.")
            await ctx.send_response(embed=embed)


    @commands.slash_command(name="purge", description="Purges a specific amount of messages")
    @commands.has_permissions(moderate_members=True)
    async def purge(
        self,
        ctx : discord.ApplicationContext,
        amount : Option(int)
    ):
        amount = amount
        embed = discord.Embed(title="Purged", description=f"{amount} message.s have been purged")
        await ctx.channel.purge(limit=amount)
        await ctx.send_response(embed=embed, ephemeral=True)
 
        
    
    #=================================
    #============Errors===============
    #================================= 


    @embedrules.error
    async def embedrules_error(self, ctx: discord.ApplicationContext, error: Exception) -> None:
        errorcode = randint(10000, 99999)
        embed = discord.Embed(title="An Error occured", description="Please screenshot the Error Message and report it to a Staff Member", color=discord.Color.red())
        embed.add_field(name="Error", value=f"```\n{error}\n```")
        embed.set_footer(text=f"error #{errorcode}", icon_url="https://asicalug.netlify.app/storage/warning.png")
        if isinstance(error, commands.errors.MissingPermissions):
            await ctx.send_response(embed=embed, ephemeral=True)

    @setup_suggestions.error
    async def embedrules_error(self, ctx: discord.ApplicationContext, error: Exception) -> None:
        errorcode = randint(10000, 99999)
        embed = discord.Embed(title="An Error occured", description="Please screenshot the Error Message and report it to a Staff Member", color=discord.Color.red())
        embed.add_field(name="Error", value=f"```\n{error}\n```")
        embed.set_footer(text=f"error #{errorcode}", icon_url="https://asicalug.netlify.app/storage/warning.png")
        if isinstance(error, commands.errors.MissingPermissions):
            await ctx.send_response(embed=embed, ephemeral=True)

    @setup_tickets.error
    async def embedrules_error(self, ctx: discord.ApplicationContext, error: Exception) -> None:
        errorcode = randint(10000, 99999)
        embed = discord.Embed(title="An Error occured", description="Please screenshot the Error Message and report it to a Staff Member", color=discord.Color.red())
        embed.add_field(name="Error", value=f"```\n{error}\n```")
        embed.set_footer(text=f"error #{errorcode}", icon_url="https://asicalug.netlify.app/storage/warning.png")
        if isinstance(error, commands.errors.MissingPermissions):
            await ctx.send_response(embed=embed, ephemeral=True)

    @embedchangelog.error
    async def embedrules_error(self, ctx: discord.ApplicationContext, error: Exception) -> None:
        errorcode = randint(10000, 99999)
        embed = discord.Embed(title="An Error occured", description="Please screenshot the Error Message and report it to a Staff Member", color=discord.Color.red())
        embed.add_field(name="Error", value=f"```\n{error}\n```")
        embed.set_footer(text=f"error #{errorcode}", icon_url="https://asicalug.netlify.app/storage/warning.png")
        if isinstance(error, commands.errors.MissingPermissions):
            await ctx.send_response(embed=embed, ephemeral=True)

    @warn.error
    async def warn_error(self, ctx: discord.ApplicationContext, error: Exception) -> None:
        errorcode = randint(10000, 99999)
        embed = discord.Embed(title="An Error occured", description="Please screenshot the Error Message and report it to a Staff Member", color=discord.Color.red())
        embed.add_field(name="Error", value=f"```\n{error}\n```")
        embed.set_footer(text=f"error #{errorcode}", icon_url="https://asicalug.netlify.app/storage/warning.png")
        if isinstance(error, commands.errors.MissingPermissions):
            await ctx.send_response(embed=embed, ephemeral=True)

    @remove_warn.error
    async def rmwarn_error(self, ctx: discord.ApplicationContext, error: Exception) -> None:
        errorcode = randint(10000, 99999)
        embed = discord.Embed(title="An Error occured", description="Please screenshot the Error Message and report it to a Staff Member", color=discord.Color.red())
        embed.add_field(name="Error", value=f"```\n{error}\n```")
        embed.set_footer(text=f"error #{errorcode}", icon_url="https://asicalug.netlify.app/storage/warning.png")
        if isinstance(error, commands.errors.MissingPermissions):
            await ctx.send_response(embed=embed, ephemeral=True)
    
    @info.error
    async def info_error(self, ctx: discord.ApplicationContext, error: Exception) -> None:
        errorcode = randint(10000, 99999)
        embed = discord.Embed(title="An Error occured", description="Please screenshot the Error Message and report it to a Staff Member", color=discord.Color.red())
        embed.add_field(name="Error", value=f"```\n{error}\n```")
        embed.set_footer(text=f"error #{errorcode}", icon_url="https://asicalug.netlify.app/storage/warning.png")
        if isinstance(error, commands.errors.MissingPermissions):
            await ctx.send_response(embed=embed, ephemeral=True)

    @purge.error
    async def purge_error(self, ctx: discord.ApplicationContext, error: Exception) -> None:
        errorcode = randint(10000, 99999)
        embed = discord.Embed(title="An Error occured", description="Please screenshot the Error Message and report it to a Staff Member", color=discord.Color.red())
        embed.add_field(name="Error", value=f"```\n{error}\n```")
        embed.set_footer(text=f"error #{errorcode}", icon_url="https://asicalug.netlify.app/storage/warning.png")
        if isinstance(error, commands.errors.MissingPermissions):
            await ctx.send_response(embed=embed, ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(StaffCommands(bot))