
import disnake
from disnake.ext import commands
import os
import asyncio

intents = disnake.Intents.all()
bot = commands.Bot(command_prefix='!', reload=True, intents=intents,
                   activity=disnake.Activity(name="стрим Hotaru", type=disnake.ActivityType.watching))
CATEGORY_ID = 1300570620861485086

user_tickets = {}
ticket_owners = {}
ticket_number = 1

@bot.command(name= 'пример')
async def meow(ctx):
    embed = disnake.Embed(
    description= "Пример заявки в клан",
    title = "Заявка в клан",
    color=disnake.Color.red()
    )

    embed.add_field(name="Ваше имя", value= "Илья",inline=False)
    embed.add_field(name="Ваш возраст", value= "16",inline=False)
    embed.add_field(name="Ссылка на профиль yooma.su", value= "https://yooma.su/profile/tailung",inline=False)
    embed.add_field(name="Почему выбрали именно наш клан", value= "Потому что Карина сигма",inline=False)
    embed.add_field(name="Кратко о себе", value= "щавель снится, спс что кончил на...",inline=False)
    embed.set_thumbnail(url = "https://i.imgur.com/IzyaxAK.png")
    embed.set_image(url = "https://media.discordapp.net/attachments/1280097880220110852/1291685804560744509/1.gif?ex=67a479a6&is=67a32826&hm=e767346c4a99f8dcb481b8380c85ba753dd0a1947373e7660f8180020a91a2ee&=&width=400&height=209")
    await ctx.send(embed=embed)

@bot.command(name='юля')
async def gav(ctx):
    embed = disnake.Embed(
    description= "Юля - сука",
    title = "Сука",
    color=disnake.Color.red()
    )
    await ctx.send(embed=embed)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("Bot is ready!")


@bot.command()
async def link(ctx):
    link_message = '[Тык](https://yooma.su/profile/tailung)'
    await ctx.send(link_message)


class AppealModal(disnake.ui.Modal):
    def __init__(self):
        components = [
            disnake.ui.TextInput(label='Имя', style=disnake.TextInputStyle.short, placeholder='Пример: Илья',
                                 required=True, custom_id='**1.Имя**', max_length=100),
            disnake.ui.TextInput(label='Возраст', style=disnake.TextInputStyle.short, placeholder='Пример: 16',
                                 required=True, custom_id='**2.Возраст**', max_length=2),
            disnake.ui.TextInput(label='Профиль на yooma.su', style=disnake.TextInputStyle.short,
                                 placeholder='Пример: https://yooma.su/profile/tailung', required=True,
                                 custom_id='**3.Профиль на yooma.su**',
                                 max_length=200),
            disnake.ui.TextInput(label='Причина вступления в клан', style=disnake.TextInputStyle.paragraph,
                                 placeholder='Пример: Потому что Карина сигма', required=True,
                                 custom_id='**3.Причина вступления в клан**',
                                 max_length=400),
            disnake.ui.TextInput(label='Кратко о себе', style=disnake.TextInputStyle.paragraph,
                                 placeholder='Пример: Я Адекватный, умный. Готов помогать клану!', required=True,
                                 custom_id='**4.Кратко о себе**',
                                 max_length=400),
        ]
        super().__init__(title="Заявка", components=components, custom_id='appeal_modal')

    async def callback(self, interaction: disnake.ModalInteraction) -> None:
        await interaction.response.defer(ephemeral=True)

        profile_link = interaction.text_values['**3.Профиль на yooma.su**']

        embed = disnake.Embed(title="Заявка", color=disnake.Color.red(),
                              description=f"Заявка от {interaction.author.mention}\n Профиль на [yooma.su]({profile_link})")
        embed.set_thumbnail(url=interaction.author.avatar.url)
        for title, resp in interaction.text_values.items():
            if title != '**3.Профиль на yooma.su**':
                ilovefootjob = f"\n```{resp}```\n"
                embed.add_field(name=title, value=ilovefootjob, inline=False)


        channel_id = 1297220001173868626
        channel = interaction.bot.get_channel(channel_id) or await interaction.bot.fetch_channel(channel_id)
        message = await channel.send(embed=embed)
        await interaction.edit_original_response('Заявка успешно отправлена!')


@bot.slash_command(name='помощь', description='Помощь со вступлением')
async def info(ctx):
    await ctx.response.defer()
    cl = [
        'Для того чтобы вступить в клан, для начала прочтите правила: https://discord.gg/VYE3v5EZ',
        'После чего нажмите на кнопку "Подать заявку"',
        'Вам зададут 5 вопросов,честно отвечайте на них!',
        'После того, как напишет, что ваша заявка отправлена, ожидайте, пока вам напишут',
    ]
    await ctx.followup.send("\n".join(cl))


@bot.command(name='заявка')
async def open_modal(ctx):
    view = disnake.ui.View(timeout=None)
    allowed_channel_id = 1297219838384799754

    if ctx.channel.id != allowed_channel_id:
        await ctx.send("Эта команда недоступна в данном канале.")
        return

    view = disnake.ui.View(timeout=None)

    async def modal_callback(interaction):
        if interaction.component.custom_id == "open_modal":
            modal = AppealModal()
            await interaction.response.send_modal(modal)

    button = disnake.ui.Button(style=disnake.ButtonStyle.red, label="   Подать Заявку", custom_id="open_modal",
                               emoji='💌')
    button.callback = modal_callback

    view.add_item(button)

    embed = disnake.Embed(
        title="**Заявка в клан**",
        description="**Здравствуйте, уважаемый игрок.\nДля начала ознакомьтесь с правилами клана.\nПосле чего нажмите на кнопку, чтобы подать заявку в клан!**",
        color=disnake.Color.red()
    )

    await ctx.send(embed=embed, view=view)


@bot.command(name='ticket')
async def ticket(ctx):
    if ctx.channel.id != 1300883170551533678:
        await ctx.send("**Эта команда доступна только в определенном канале.**")
        return

    global ticket_number

    embed = disnake.Embed(
        title="**Связь с администрацией**",
        description="**Нажмите кнопку ниже, чтобы открыть тикет\n В нем вы можете подать жалобу на игрока\n Задать интересующий вас вопрос**",
        color=disnake.Color.red()
    )

    ticket_button = disnake.ui.Button(label="Открыть тикет", style=disnake.ButtonStyle.red, emoji='✉️')

    async def ticket_callback(interaction):
        global ticket_number

        if interaction.user.id in user_tickets:
            await interaction.response.send_message(
                content="**У вас уже открыт тикет. Закройте его, чтобы открыть новый.**", ephemeral=True)
            return

        channel_name = f'ticket-{ticket_number}'
        guild = ctx.guild
        category = guild.get_channel(CATEGORY_ID)
        overwrites = {
            guild.default_role: disnake.PermissionOverwrite(read_messages=False),
            interaction.user: disnake.PermissionOverwrite(read_messages=True),
        }

        for role in guild.roles:
            if role.permissions.administrator:
                overwrites[role] = disnake.PermissionOverwrite(read_messages=True)

        ticket_channel = await guild.create_text_channel(channel_name, category=category, overwrites=overwrites)
        user_tickets[interaction.user.id] = ticket_channel.id
        ticket_owners[ticket_channel.id] = interaction.user.id

        await interaction.response.send_message(
            content=f"**{interaction.user.mention}, ваш тикет открыт в канале {ticket_channel.mention}!**",
            ephemeral=True)

        close_without_reason_button = disnake.ui.Button(label="Закрыть", style=disnake.ButtonStyle.danger)
        close_with_reason_button = disnake.ui.Button(label="Закрыть с причиной", style=disnake.ButtonStyle.danger)
        take_ticket_button = disnake.ui.Button(label="Взять тикет", style=disnake.ButtonStyle.green)

        ticket_taken = False

        async def take_ticket_callback(interaction):
            nonlocal ticket_taken
            if ticket_taken:
                await interaction.response.send_message(content="**Этот тикет уже взят другим администратором.**",
                                                        ephemeral=True)
                return

            if not any(role.permissions.administrator for role in interaction.user.roles):
                await interaction.response.send_message(content="**Вы не имеете прав для взятия тикета.**",
                                                        ephemeral=True)
                return

            ticket_taken = True
            ticket_number_from_channel = ticket_channel.name.split('-')[1]
            new_name = f"{interaction.user.name}-ticket-{ticket_number_from_channel}"
            await ticket_channel.edit(name=new_name)
            await interaction.response.send_message(content=f"**Тикет был переименован в: {new_name}**", ephemeral=True)

        async def close_with_reason_callback(interaction):
            if not any(role.permissions.administrator for role in interaction.user.roles):
                await interaction.response.send_message("**У вас нет прав для закрытия тикета с причиной.**",
                                                        ephemeral=True)
                return

            await interaction.response.send_message("**Введите причину закрытия тикета:**", ephemeral=True)

            def check(msg):
                return msg.author == interaction.user and msg.channel == ticket_channel

            try:
                reason_msg = await bot.wait_for('message', check=check, timeout=30)
                reason = reason_msg.content
            except asyncio.TimeoutError:
                reason = "Без причины"

            if ticket_channel.guild.get_channel(ticket_channel.id):
                await ticket_channel.send(f"Тикет закрыт. Причина: {reason}")
            await ticket_channel.delete()

            owner_id = ticket_owners.pop(ticket_channel.id, None)
            if owner_id:
                user_tickets.pop(owner_id, None)

            user_tickets.pop(interaction.user.id, None)  #
            ticket_taken = False

            if owner_id:
                owner = ctx.guild.get_member(owner_id)
                if owner:
                    embed_message = disnake.Embed(
                        title="**Ваш тикет был закрыт**",
                        description=f"**Причина: {reason}**",
                        color=disnake.Color.red()
                    )
                    await owner.send(embed=embed_message)

        async def close_without_reason_callback(interaction):
            await interaction.response.send_message("**Вы уверены, что хотите закрыть этот тикет без причины?**",
                                                    ephemeral=True)

            confirm_button = disnake.ui.Button(label="Подтвердить", style=disnake.ButtonStyle.green)
            cancel_button = disnake.ui.Button(label="Отмена", style=disnake.ButtonStyle.red)

            async def confirm_callback(interaction):
                if ticket_channel.guild.get_channel(ticket_channel.id):
                    await ticket_channel.send("Тикет закрыт.")
                await ticket_channel.delete()

                owner_id = ticket_owners.pop(ticket_channel.id, None)
                if owner_id:
                    user_tickets.pop(owner_id, None)

                user_tickets.pop(interaction.user.id, None)
                ticket_taken = False

            async def cancel_callback(interaction):
                await interaction.response.send_message("**Закрытие тикета отменено.**", ephemeral=True)
                await confirmation_message.delete()

            confirm_button.callback = confirm_callback
            cancel_button.callback = cancel_callback

            view = disnake.ui.View(timeout=None)
            view.add_item(confirm_button)
            view.add_item(cancel_button)

            confirmation_message = await ticket_channel.send("**Подтвердите закрытие тикета:**", view=view)

        close_with_reason_button.callback = close_with_reason_callback
        close_without_reason_button.callback = close_without_reason_callback
        take_ticket_button.callback = take_ticket_callback

        view = disnake.ui.View(timeout=None)
        view.add_item(close_with_reason_button)
        view.add_item(close_without_reason_button)
        view.add_item(take_ticket_button)

        await ticket_channel.send(embed=disnake.Embed(
            title="**Ваш тикет**",
            description=f"**У Вас есть 2 минуты написать жалобу/вопрос.\n Вы можете самостоятельно закрыть тикет в любое время\n {interaction.user.mention}**",
            color=disnake.Color.red()
        ), view=view)
        ticket_number += 1

    ticket_button.callback = ticket_callback
    view = disnake.ui.View(timeout=None)
    view.add_item(ticket_button)

    await ctx.send(embed=embed, view=view)


bot.run("TOKEN")
