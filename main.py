import disnake
from disnake.ext import commands
from pymongo import MongoClient as mc


db = mc("БД")
us = db.s.user
support = db.s.supports

client = commands.Bot(command_prefix="s.", intents=disnake.Intents.all())

@client.command(name="Принять")
async def p(ctx, id:int):
    if us.count_documents({"id":id}) == 1:
        user = client.get_user(id)
        us.update_one({"id":id}, {"$inc":{"pr":1}})
        support.insert_one({"s":ctx.author.id, "sob":id})
        await ctx.send(f"Вы приняли диалог с ID {id}")
        embed = disnake.Embed(title="К вам присоединился агент поддержки!", description=f"Агент:{ctx.author}", color=disnake.Colour.green())
        await user.send(embed=embed)

@client.command(name="Завершить")
async def o(ctx, id:int):
    if us.count_documents({"id":id}) == 1:
            user = client.get_user(id)
            us.delete_one({"id":id})
            support.delete_one({"s":ctx.author.id})
            await ctx.send(f"Вы завершили диалог с ID {id}")
            embed = disnake.Embed(title="Тикет завершён!", description=f"Агент:{ctx.author}", color=disnake.Colour.red())
            await user.send(embed=embed)

@client.event
async def on_presence_update(before, after):
    if before.id == 934002793973415956:
        status = after.status
        user = client.get_user(933978213070307428)
        if before.status != status:


            if status == disnake.Status.offline:
                message = "Бот отключился!"
            if status == disnake.Status.online:
                message = "Бот включился!"
            await user.send(message)        


@client.event
async def on_message(message):
    await client.process_commands(message)
    if message.author.bot: return
    if message.guild: return

    guild = client.get_guild(933377687572078602)

    try:
        author = guild.get_member(message.author.id)
    except:
        return await message.author.send("Нужно быть на сервере PlanetMod!")   
    role = author.guild.get_role(934830041639055360)

    if role in memberrrr.roles:
        if support.count_documents({"s":message.author.id}) == 0: return
        member = client.get_user(support.find_one({"s":message.author.id})['sob'])


        await member.send(f"**{message.author}**: {message.content}")
        

    else:
        
        if us.count_documents({"id":message.author.id}) == 0:
            us.insert_one({"id":message.author.id, "pr":0})
            ch2 = client.get_channel(977538484317339688) 
            await ch2.send(f"Новый тикет!\nТекст:{message.content}\nАйди:{message.author.id}\тКоманда: s.Принять {message.author.id}")
            embed = disnake.Embed(title="Добрый день!", description="Ожидайте, скоро Вам будет назначен агент поддержки!", color=disnake.Colour.red())
            await message.reply(embed=embed)
        else:
            if support.count_documents({"sob":message.author.id}) == 0: return await message.reply("К вам не присоединился агент поддержки!")

            sup = client.get_user(support.find_one({"sob":message.author.id})['s'])
            await sup.send(f"**{message.author}**:{message.content}")



    
    


client.run("Токен")
