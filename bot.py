import discord
from discord.ui import Button, View
from discord.ext import commands

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

#Pre Requirements
CUSTOM_IMAGE_URL = "https://cdn.discordapp.com/attachments/1356557460525027358/1356705709802127460/gorillax_1.png?ex=67ed8a27&is=67ec38a7&hm=2c2d8371ad89de2deb93895834153e7d35f80f2ec52a04ee4d7eac81a717a67f&"
WELCOME_CHANNEL_ID = 1356547513641078796
wanted_channel_id = 1356557703522156624
SECOND_CHANNEL_ID = 1073851406869594154
OWNER_ID = 981969761992843354
GIVEAWAY_MESSAGE_ID = 1395413572443570270
GIVEAWAY_CHANNEL_ID = 1395413242712428654

#Ticket System & Bot Status
@bot.event
async def on_ready():
    members = 0
    for guild in bot.guilds:
        members += guild.member_count - 1

    await bot.change_presence(activity = discord.Activity(
        type = discord.ActivityType.watching,

        #Bot status
        name = f'{members} members' 

    ))
    print('Ready to support ✅')
    print(f'Bot is online as {bot.user}')
    # Directly get the 'wanted' channel by its ID when the bot starts
    
    guild = bot.guilds[0]  # Get the first server the bot is in (assuming only one server)
    wanted_channel = guild.get_channel(wanted_channel_id)

    if not wanted_channel:
        print("Couldn't find the 'wanted' channel. Please check the channel ID.")
        return

    # Check if the bot has permissions to send messages and embed links in the 'wanted' channel
    if not wanted_channel.permissions_for(guild.me).send_messages:
        print("I don't have permission to send messages in the 'wanted' channel.")
        return

    if not wanted_channel.permissions_for(guild.me).embed_links:
        print("I don't have permission to send embeds in the 'wanted' channel.")
        return

    # Get the category for ticket channels (replace with your category ID)
    category_id = 1356601361885560873  # Replace with your category ID
    category = guild.get_channel(category_id)
    if not category:
        print("Couldn't find the ticket category. Please check the category ID.")
        return

    # Create an embed for the ticket system
    embed = discord.Embed(
        title="🛠️ GorillaX Innovations | Support & Consultation",
        description="Need help with a purchase, technical support, or a consultation?\n" "Click the button below to create a ticket, and our team will assist you promptly!",
        color=0xFFFFFF
    )
    embed.set_footer(text="GorillaX Innovations • Quality Service, Always!")
    embed.set_image(url=CUSTOM_IMAGE_URL)  # Set the custom image URL

    # Create the button for ticket opening
    button = Button(label="Open Ticket", style=discord.ButtonStyle.green)

    async def button_callback(interaction):
        member = interaction.user
        # Create a new ticket channel in the specified category
        ticket_channel = await guild.create_text_channel(f'ticket-{member.name}', category=category)
        
        # Set permissions so only the member and staff can view the ticket
        await ticket_channel.set_permissions(guild.default_role, read_messages=False)  # Hide from others
        await ticket_channel.set_permissions(member, read_messages=True)  # Give permission to the member who created the ticket
        
        # Create a close ticket button for the newly created channel
        close_button = Button(label="Close Ticket", style=discord.ButtonStyle.red)

        async def close_button_callback(interaction):
            # Check if the ticket channel still exists
            if not ticket_channel or not ticket_channel.guild.get_channel(ticket_channel.id):
                await interaction.response.send_message("This ticket channel no longer exists.", ephemeral=True)
                return

            # Delete the ticket channel when the button is clicked
            await interaction.response.send_message("The ticket has been closed.", ephemeral=True)
            await ticket_channel.delete()
            

        close_button.callback = close_button_callback
        view = View()
        view.add_item(close_button)

        # Send a message in the new ticket channel with the close button
        embed = discord.Embed(
            title="🎟️ GorillaX Innovations | Support Ticket",
            description=f"Hello {member.mention},\n\n"
        "Welcome to your support ticket! One of our staff members will assist you as soon as possible.\n\n"
        "While you're waiting, feel free to:\n"
        "1. **Address your issue**: Let us know how we can help.\n"
        "2. **Make a purchase**: Our team can assist you with any product inquiries.\n"
        "3. **Consultation**: Ask for any guidance regarding our services.\n\n"
        "If you'd like to close this ticket after your issue is resolved, simply click the close button below.",
            color=0xFFFFFF
        )
        await ticket_channel.send(embed=embed, view=view)

        embed.set_footer(text="GorillaX Innovations • Quality Service, Always!")
        embed.set_image(url=CUSTOM_IMAGE_URL)

        # Acknowledge the interaction
        await interaction.response.send_message(f"Ticket created: {ticket_channel.mention}", ephemeral=True)

    # Attach the button to the embed and create a view
    button.callback = button_callback
    view = View()
    view.add_item(button)

    # Send the embed with the button to the wanted channel
    try:
        await wanted_channel.send(embed=embed, view=view)
    except discord.Forbidden:
        print("I do not have permission to send messages in the wanted channel.")
        return

    print("Ticket system initialized and embed sent.")

#Welcome System
@bot.event
async def on_member_join(member):
    # Get the specific channel
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel is not None:
        embed = discord.Embed(            
            description=f"Welcome {member.mention}\n\n"
                    "📌 Make sure to read [Terms](https://discord.com/channels/1356547513158602772/1356556493616582696).\n"
                    "🛡️ Explore the <#1356557218551693393> and <#1356707388308328591> channels.",
            color=0xFFFFFF
        )
        embed.set_image(url=CUSTOM_IMAGE_URL)
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_author(name="GorillaX Innovations")
        await channel.send(embed=embed)

    # Second channel: Plain text welcome
    channel2 = bot.get_channel(SECOND_CHANNEL_ID)  # Replace with your second channel ID
    if channel2 is not None:
        await channel2.send(f"Hi {member.mention} 👋 Welcome to Spades Community! Do participate in the giveaway 🎉")      


#welcome Test System
@bot.command()
async def testw(ctx):
    # Get the specific channel
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel is not None:
        embed = discord.Embed(            
            description=f"Welcome {ctx.author.mention}\n\n"
                    "📌 Make sure to read [Terms](https://discord.com/channels/1356547513158602772/1356556493616582696).\n"
                    "🛡️ Explore the <#1356557218551693393> and <#1356707388308328591> channels.",
            color=0xFFFFFF
        )
        embed.set_image(url=CUSTOM_IMAGE_URL)
        embed.set_author(name="GorillaX Innovations")
        embed.set_thumbnail(url=ctx.author.avatar.url)
        await channel.send(embed=embed)

#Giveaway
giveaway_message = None
entries = set()

@bot.command()
async def start_giveaway(ctx):
    global giveaway_message, entries
    entries.clear()

    embed = discord.Embed(
        title="🎉 GIVEAWAY: 1 Month Discord Nitro 🎉",
        description=(
        "It's time to renunite! We're giving away **1 Month of Discord Nitro** to one lucky winner!\n\n"
        "🔹 **How to enter:** React with 🎉 below.\n"
        "🔹 **Requirement:** You must have **at least 5 invites** to be eligible to win.\n"
        "🔹 **Prize:** 1 Month of Discord Nitro, delivered directly to your DMs.\n"
        "🔹 **Ends:** <t:1753626600:R>\n\n"
        "✨ Make sure you stay in the server so we can contact you if you win!"
    ),
        color=0xd6b23c
    )
    embed.set_footer(text=f"Hosted by {ctx.author}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
    embed.set_thumbnail(
    url="https://cdn.discordapp.com/attachments/1073869023751712858/1395103412164493392/image.png?ex=68793acd&is=6877e94d&hm=de190389ee4389a93a50d04c2d5ee1f7431ca0a96a27b2eb2526c4e24cc0d6ff&")
    giveaway_message = await ctx.send(embed=embed)
    await giveaway_message.add_reaction("🎉")
    await ctx.message.delete()  # Deletes the command message

@bot.event
async def on_reaction_add(reaction, user):
    global giveaway_message, entries
    if user.bot:
        return
    if giveaway_message and reaction.message.id == giveaway_message.id and reaction.emoji == "🎉":
        entries.add(user.id)

@bot.command()
async def pick_winner(ctx, user: discord.Member):
    if ctx.author.id != OWNER_ID:
        await ctx.send("You don't have permission to pick the winner.")
        await ctx.message.delete()
        return

    if giveaway_message is None:
        await ctx.send("No giveaway running.")
        await ctx.message.delete()
        return

    if user.id not in entries:
        await ctx.send(f"{user.mention} did not enter the giveaway.")
        await ctx.message.delete()
        return

    # 🎉 Winner embed
    winner_embed = discord.Embed(
        title="🎊 We Have a Winner! 🎊",
        description=(
            f"🥳 Congratulations {user.mention}!\n\n"
            "You’ve won **1 Month of Discord Nitro** in our giveaway!\n\n"
            "A huge thank you to everyone who participated — stay tuned for more giveaways and events soon!\n\n"
            "🔔 **Winner Instructions:**\n"
            "Please check your DMs for prize details. Make sure your DMs are open so we can deliver your reward!"
        ),
        color=0xd6b23c  # Gold color
    )

    winner_embed.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/1073869023751712858/1395103412164493392/image.png?ex=68793acd&is=6877e94d&hm=de190389ee4389a93a50d04c2d5ee1f7431ca0a96a27b2eb2526c4e24cc0d6ff&"
    )

    winner_embed.set_footer(
        text="Thanks for being part of our community! 🎉"
    )

    await ctx.send(embed=winner_embed)
    await ctx.message.delete()
    
@bot.command()
async def cleanup_giveaway(ctx, message_id: int):
    guild = ctx.guild

    try:
        channel = ctx.channel  # or specify the channel if different
        message = await channel.fetch_message(message_id)
    except discord.NotFound:
        await ctx.send("❌ Message not found.")
        return

    invites = await guild.invites()

    for reaction in message.reactions:
        if str(reaction.emoji) == "🎉":
            users = [user async for user in reaction.users()]
            for user in users:
                if user.bot:
                    continue

                total_invites = sum(invite.uses for invite in invites if invite.inviter and invite.inviter.id == user.id)

                if total_invites < 5:
                    await reaction.remove(user)
                    try:
                        await user.send(
                            f"❌ You need at least 5 invites to stay in the giveaway. "
                            f"You currently have {total_invites}. Your reaction has been removed."
                        )
                    except discord.Forbidden:
                        pass  # Can't DM

    await ctx.send("✅ Cleanup complete.")
    
@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id != GIVEAWAY_MESSAGE_ID:
        return

    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)

    if member.bot:
        return

    # Your logic to get invites count
    invites = await guild.invites()
    total_invites = 0
    for invite in invites:
        if invite.inviter == member:
            total_invites += invite.uses

    if total_invites < 5:
        channel = bot.get_channel(GIVEAWAY_CHANNEL_ID)
        message = await channel.fetch_message(GIVEAWAY_MESSAGE_ID)

        # Remove the user's reaction
        for reaction in message.reactions:
            async for user in reaction.users():
                if user.id == payload.user_id:
                    await reaction.remove(member)


        # Optionally DM the user
        try:
            await member.send(f"Your reaction have been removed, You need at least 5 invites to enter this giveaway.\nYou currently have {total_invites} out of 5.")
        except:
            pass    

bot.run('BOT_TOKEN')
