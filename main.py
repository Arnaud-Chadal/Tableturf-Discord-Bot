import discord
from discord.ext import commands
import data
from random import randint
import pickle
from os import path
from dpytools.menus import arrows
import time


if not path.isfile("membre.dat") :
    pickle.dump(data.membre, open("membre.dat", "wb"))
data.membre = pickle.load(open("membre.dat", "rb"))


client = commands.Bot(command_prefix=">", intents=discord.Intents.all())
a = discord.Embed(
        colour=2935808,
        title="- Liste des commandes de Tableturf -",
        description=">claim : récupère des objets toutes les deux heures\n>roll : tire une carte aléatoire\n>shop : ouvre la boutique de Kipik\n>buy [item] : achète des objets\n>pack : ouvre tes packs de cartes\n>info : consulte ton profil et ton inventaire\n>card [rareté] [membre] : affiche la liste de tes cartes\n>top : Affiche le classement\n>see [carte] [membre]: Affiche une carte choisie\n>trade [membre] [carte1] [carte2] : Permet d'échanger une carte avec quelqu'un\n>ok : Permet d'accepter un échange")
a.set_author(name="Tableturf")
a.set_thumbnail(url="https://cdn.discordapp.com/attachments/779442974357585920/1117485781943066754/lun._5_06_2023_22_20_53.png")

s = discord.Embed(
        colour=5505218,
        title="Stock de Tipik",
        description="Pack de cartes C&T (pack) : 25 fragments\nPack C&T classe (freshpack) : 60 fragments\n\nPour acheter un article : >buy + nom de l'article (celui entre paranthèses)")
s.set_author(name="Tipik")
s.set_image(url="https://cdn.discordapp.com/attachments/779442974357585920/1116454436529778738/S3_Banner_1003.png")
s.set_thumbnail(url="https://cdn.discordapp.com/attachments/779442974357585920/1116454209756340334/S3_Tableturf_Card_Spyke.png")

trading = False



@client.event
async def on_ready() :
    print("Success : Bot is connected to Discord")


@client.event
async def on_command_error(ctx, error) :
    if isinstance(error, commands.CommandOnCooldown) :
        await ctx.send("Il reste " + str(int(round(error.retry_after, 2)//60)) + " minutes et " + str(int(round(error.retry_after, 2)%60)) + " secondes à attendre avant de pouvoir utiliser ceci...")
        
        
@client.event             
async def on_message(message):
    r = role = discord.utils.find(lambda r: r.name == 'Bot', message.guild.roles)
    if not r in message.author.roles :
        if not str(message.author.id) in data.membre.keys() :
            data.membre[str(message.author.id)] = [0, 0, [2, 5, 21, 27, 55, 70], 0, 0, 0, []]
            pickle.dump(data.membre, open("membre.dat", "wb"))
            print("un membre est maintenant enregistré")
        if not "$" in message.content.lower() and not ">" in message.content.lower() :
            hour, min = map(int, time.strftime("%H %M").split())
            if min > data.membre[str(message.author.id)][5] + 3 or min < data.membre[str(message.author.id)][5] :
                nbr = randint(1, 60)
                if nbr < 3 :
                    data.membre[str(message.author.id)][5] = min
                    data.membre[str(message.author.id)][0] += nbr
                    pickle.dump(data.membre, open("membre.dat", "wb"))
                    embed = discord.Embed(
                        colour=14060288,
                        title="Bravo, tu obtiens ***" + str(nbr) + "*** conque(s) !",
                        description="Fonce l'utiliser !")
                    embed.set_footer(text="Tu possèdes " + str(data.membre[str(message.author.id)][0]) + " conques !")
                    embed.set_thumbnail(url="https://cdn.wikimg.net/en/splatoonwiki/images/0/05/S3_icon_conch_shell.png")
                    await message.channel.send(embed=embed)
    await client.process_commands(message)


@client.command()
@commands.cooldown(1, 3, commands.BucketType.user)
async def roll(ctx) :
    if data.membre[str(ctx.author.id)][0] > 0 :
        data.membre[str(ctx.author.id)][0] -= 1
        n = randint(1, 100)
        if n < 2 :
            nbr = data.classe[randint(0, 14)]
        elif n > 1 and n < 11 :
            nbr = data.rare[randint(0, 60)]
        else : nbr = data.commun[randint(0, 132)]
        embed = discord.Embed(
            colour=[45045, 14730752, 14745855][data.carte[nbr][2]],
            title=data.carte[nbr][1],
            description="Rareté : "+["Commune", "Rare", "Classe !"][data.carte[nbr][2]]+"\nN°"+str(nbr+1))
        embed.set_footer(text="Il te reste " + str(data.membre[str(ctx.author.id)][0]) + " conques")
        embed.set_author(name=str(ctx.author))
        embed.set_image(url=data.carte[nbr][0])
        embed.set_thumbnail(url=data.image[data.carte[nbr][2]])
        await ctx.channel.send(embed=embed)
        if nbr in data.membre[str(ctx.author.id)][2] :
            if n < 3 :
                data.membre[str(ctx.author.id)][1] += 20
                await ctx.channel.send("Tu possèdes déjà cette carte... Voici 20 fragment !")
            elif n > 2 and n < 23 :
                data.membre[str(ctx.author.id)][1] += 5
                await ctx.channel.send("Tu possèdes déjà cette carte... Voici 5 fragment !")
            else :
                data.membre[str(ctx.author.id)][1] += 1
                await ctx.channel.send("Tu possèdes déjà cette carte... Voici 1 fragment !")
        else :
            data.membre[str(ctx.author.id)][2] += [nbr]
            data.membre[str(ctx.author.id)][2].sort()
        pickle.dump(data.membre, open("membre.dat", "wb"))
    else : await ctx.channel.send("Tu n'a plus de conques...")



@client.command()
async def info(ctx, identid=None) :
    if identid == None :
        identid = str(ctx.author.id)
    else : identid = str(identid[2:-1])
    embed_list = []
    com_list = []
    rar_list = []
    cla_list = []
    for i in data.membre[str(identid)][2] :
        if data.carte[i][2] == 0 :
            com_list.append(i)
        if data.carte[i][2] == 1 :
            rar_list.append(i)
        if data.carte[i][2] == 2 :
            cla_list.append(i)
    embed = discord.Embed(
        colour=7929821,
        title="Tu possèdes :",
        description= str(data.membre[str(ctx.author.id)][0]) + " conques\n" + str(data.membre[str(ctx.author.id)][1]) + " fragments\n" + str(data.membre[str(ctx.author.id)][3]) + " pack de cartes C&T\n" + str(data.membre[str(ctx.author.id)][4]) + " pack C&T classe\n\n" + str(len(com_list)) + " /133 cartes communes\n" + str(len(rar_list)) + " /61 cartes rares\n" + str(len(cla_list)) + " /15 cartes classes\n" + "***" + str(len(data.membre[str(ctx.author.id)][2])) + "/209 cartes***")
    embed.set_author(name=str(ctx.author))
    embed.set_thumbnail(url=ctx.message.author.avatar)
    embed.set_image(url="https://cdn.discordapp.com/attachments/779442974357585920/1116087617709166733/S3_Banner_1002.png")
    await ctx.channel.send(embed=embed)


@client.command()
async def card(ctx, rare, identid=None) :
    if identid == None :
        identid = str(ctx.author.id)
    else : identid = str(identid[2:-1])
    embed_list = []
    id_list = []
    if not rare == "all" :
        for i in data.membre[str(identid)][2] :
            if str(data.carte[i][2]) == str(int(rare)-1) :
                id_list.append(i)  
    else : id_list = data.membre[identid][2]
    for i in id_list :
        embed = discord.Embed(
            colour=7929821,
            title=data.carte[i][1],
            description="Rareté : "+["Commune", "Rare", "Classe !"][data.carte[i][2]]+"\nN°"+str(i+1))
        embed.set_author(name=ctx.author)
        embed.set_image(url=data.carte[i][0])
        embed.set_thumbnail(url=data.image[data.carte[i][2]])
        embed_list.append(embed)
    await arrows(ctx, embed_list)
    

@client.command()
@commands.cooldown(1, 3600, commands.BucketType.user)
async def claim(ctx) :
    nbr = randint(1, 100)
    if nbr < 2 :
        data.membre[str(ctx.message.author.id)][4] += 1
        t = "Bravo, tu obtiens un pack C&T classe !"
        i = "https://cdn.discordapp.com/attachments/779442974357585920/1117478293134913646/S3_Fresh_Card_Pack.png"
    elif nbr > 1 and nbr < 6 :
        data.membre[str(ctx.message.author.id)][3] += 1
        t = "Bravo, tu obtiens un pack de cartes C&T !"
        i = "https://cdn.discordapp.com/attachments/779442974357585920/1117478257982447726/S3_Pack_of_Cards.png"
    elif nbr > 5 and nbr < 21 :
        data.membre[str(ctx.message.author.id)][0] += 2
        t = "Bravo, tu obtiens DEUX conques !"
        i = "https://cdn.wikimg.net/en/splatoonwiki/images/0/05/S3_icon_conch_shell.png"
    else :
        data.membre[str(ctx.message.author.id)][0] += 1
        t = "Bravo, tu obtiens UNE conque !"
        i = "https://cdn.wikimg.net/en/splatoonwiki/images/0/05/S3_icon_conch_shell.png"
    pickle.dump(data.membre, open("membre.dat", "wb"))
    embed = discord.Embed(
        colour=14060288,
        title=t,
        description="Fonce l'utiliser !")
    embed.set_footer(text="Tu possèdes " + str(data.membre[str(ctx.message.author.id)][0]) + " conques !")
    embed.set_thumbnail(url=i)
    await ctx.channel.send(embed=embed)

    

@client.command()
async def shop(ctx) :
    global s
    await ctx.message.channel.send(embed=s)


@client.command()
async def buy(ctx, item) :
    if item == "pack" :
        if data.membre[str(ctx.message.author.id)][1] >= 25 :
            data.membre[str(ctx.message.author.id)][1] -= 25
            data.membre[str(ctx.message.author.id)][3] += 1
            pickle.dump(data.membre, open("membre.dat", "wb"))
            embed = discord.Embed(
                colour=16769146,
                title="Pack de cartes C&T",
                description="5 cartes à l'intérieur !\nUtilise >pack pour l'ouvrir !")
            embed.set_author(name=ctx.author)
            embed.set_image(url="https://cdn.discordapp.com/attachments/779442974357585920/1117478257982447726/S3_Pack_of_Cards.png")
            embed.set_thumbnail(url=ctx.message.author.avatar)
            embed.set_footer(text="Il te reste " + str(data.membre[str(ctx.message.author.id)][1]) + " fragments")
            await ctx.message.channel.send(embed=embed)
        else : await ctx.message.channel.send("Tu n'as pas assez de fragments...") 
    elif item == "freshpack" :
        if data.membre[str(ctx.message.author.id)][1] >= 60 :
            data.membre[str(ctx.message.author.id)][1] -= 60
            data.membre[str(ctx.message.author.id)][4] += 1
            pickle.dump(data.membre, open("membre.dat", "wb"))
            embed = discord.Embed(
                colour=13269759,
                title="Pack C&T classe",
                description="Carte classe garantie !\nUtilise >pack pour l'ouvrir !")
            embed.set_author(name=ctx.message.author)
            embed.set_image(url="https://cdn.discordapp.com/attachments/779442974357585920/1117478293134913646/S3_Fresh_Card_Pack.png")
            embed.set_thumbnail(url=ctx.message.author.avatar)
            embed.set_footer(text="Il te reste " + str(data.membre[str(ctx.message.author.id)][1]) + " fragments")
            await ctx.message.channel.send(embed=embed)
        else : await ctx.message.channel.send("Tu n'as pas assez de fragments...") 
    else : await ctx.channel.send("Cet article n'existe pas... Utilise >shop pour connaître la liste des articles !") 
        
        

# #banniere, badges


@client.command()
async def pack(ctx) :
    '''commande qui sert à boire de l'eau'''
    var = False
    embed_list = []
    liste = []
    if data.membre[str(ctx.author.id)][3] > 0 :
        data.membre[str(ctx.author.id)][3] -= 1
        var = True
        for i in range(5) :
            n = randint(1, 100)
            if n < 2 :
                nbr = data.classe[randint(0, 14)]
            elif n > 1 and n < 11 :
                nbr = data.rare[randint(0, 60)]
            else : nbr = data.commun[randint(0, 132)]
            liste.append(nbr)
    elif data.membre[str(ctx.author.id)][4] > 0 :
        data.membre[str(ctx.author.id)][4] -= 1
        var = True
        for i in range(4) :
            n = randint(1, 100)
            if n < 2 :
                nbr = data.classe[randint(0, 14)]
            elif n > 1 and n < 11 :
                nbr = data.rare[randint(0, 60)]
            else : nbr = data.commun[randint(0, 132)]
            liste.append(nbr)
        liste.append(data.classe[randint(0, 14)])
    f = 0
    for i in liste :
        if i in data.membre[str(ctx.author.id)][2] :
            f += 1
        else :
            data.membre[str(ctx.author.id)][2] += [i]
            data.membre[str(ctx.author.id)][2].sort()
    if not liste == [] :
        await ctx.channel.send("Tu as eu " + str(f) + " carte que tu possédais déjà !")
    pickle.dump(data.membre, open("membre.dat", "wb"))
    if var :
        for i in liste :
            embed = discord.Embed(
                colour=[45045, 14730752, 14745855][data.carte[i][2]],
                title=data.carte[i][1],
                description="Rareté : "+["Commune", "Rare", "Classe !"][data.carte[i][2]]+"\nN°"+str(i+1))
            embed.set_author(name=str(ctx.author))
            embed.set_image(url=data.carte[i][0])
            embed.set_thumbnail(url=data.image[data.carte[i][2]])
            embed_list.append(embed)
        await arrows(ctx, embed_list)
    else : await ctx.channel.send("Tu n'as aucun pack à ouvrir...")
    


@client.command()
async def aide(ctx) :
    global a
    await ctx.message.channel.send(embed=a)


    
@client.command()
async def give(ctx, ident, obj, info) :
    if obj == "2" :
        info = int(info)-1
        if not info in data.membre[ident][2] :
            data.membre[ident][2].append(info)
        else : await ctx.channel.send("Ce membre possède déjà cette carte...")  
    else : data.membre[ident][int(obj)] += int(info)
    pickle.dump(data.membre, open("membre.dat", "wb"))
    
 
 
@client.command()
async def top(ctx):
    carte_liste = []
    key_list = list(data.membre.keys())
    print(key_list)
    for i in key_list :
        carte_liste.append([len(data.membre[i][2]), i])
    carte_liste.sort(reverse=True)
    for i in range(len(carte_liste)) :
        if carte_liste[i][1] == str(ctx.author.id) :
            t = i+1
            print(ctx.author.id)
            print(i)
    if len(carte_liste) > 5 :
        carte_liste = carte_liste[:5]
        print(carte_liste)
    titre = ""
    for i in range(len(carte_liste)) :
        titre += str(i+1) + " : " + str(client.get_user(int(str(carte_liste[i][1])))) + " (" + str(carte_liste[i][0]) + " cartes)\n"
    print(titre)
    s=discord.Embed(
        colour=14730752,
        title=titre,
        description="Tu es top " + str(t) + " !\nSi tu es premier du classement tu as le droit à un rôle spécial, n'hésite pas à le demander !")
    print("rerer")
    s.set_author(name="Classement des membres du serveur :")
    s.set_image(url="https://cdn.discordapp.com/attachments/779442974357585920/1123938242841026560/S3_Banner_10001.png")
    s.set_thumbnail(url="https://cdn.discordapp.com/attachments/779442974357585920/1123937911017066567/S3_Badge_Level_999.png")
    print("erer")
    await ctx.channel.send(embed=s)
    


@client.command()
async def see(ctx, idcarte, identid=None) :
    nbr = int(idcarte) - 1
    if identid == None :
        if nbr > -1 and nbr < 209 :
            embed = discord.Embed(
                colour=[45045, 14730752, 14745855][data.carte[nbr][2]],
                title=data.carte[nbr][1],
                description="Rareté : "+["Commune", "Rare", "Classe !"][data.carte[nbr][2]]+"\nN°"+str(nbr+1))
            embed.set_author(name=str(ctx.author))
            embed.set_image(url=data.carte[nbr][0])
            embed.set_thumbnail(url=data.image[data.carte[nbr][2]])
            await ctx.channel.send(embed=embed)
        else : await ctx.channel.send("Cette carte n'existe pas...")
    else :
        if nbr in data.membre[str(identid[2:-1])][2] :
            await ctx.channel.send(str(client.get_user(int(identid[2:-1]))) + " possède la carte " + data.carte[nbr][1])
        else : await ctx.channel.send(str(client.get_user(int(identid[2:-1]))) + " ne possède pas la carte " + data.carte[nbr][1])



@client.command()
async def trade(ctx, identid, card1, card2) :
    global trading
    if trading == False :
        if int(card1)-1 in data.membre[str(ctx.author.id)][2] and int(card2)-1 in data.membre[identid[2:-1]][2] :
            if not int(card2)-1 in data.membre[str(ctx.author.id)][2] and not int(card1)-1 in data.membre[identid[2:-1]][2] :
                trading = [str(ctx.author.id), identid[2:-1], int(card1)-1, int(card2)-1]
                await ctx.channel.send(str(ctx.author) + " propose d'échanger " + data.carte[int(card1)-1][1] + " contre " + data.carte[int(card2)-1][1])
            else : await ctx.channel.send("L'un de vous possède déjà la carte que tu proposes d'échanger...")
        else : await ctx.channel.send("L'un de vous ne possède pas la carte demandée...")   
    else : await ctx.channel.send("Un échange est déjà en cours, merci de patienter.")



@client.command()
async def ok(ctx) :
    global trading
    print(trading)
    if trading == False :
        await ctx.channel.send("Il n'y a aucun échange en cours, utilise '>trade' pour échanger une carte !")
    elif not trading[1] == str(ctx.author.id) :
        await ctx.channel.send("Ce n'est pas à toi de faire ça...")
    else :
        val1 = data.membre[trading[1]][2].pop(data.membre[trading[1]][2].index(trading[3]))
        val2 = data.membre[trading[0]][2].pop(data.membre[trading[0]][2].index(trading[2])) 
        for i in [[trading[0], trading[3]], [trading[1], trading[2]]] :
            data.membre[i[0]][2] += [i[1]]
            data.membre[i[0]][2].sort()
        pickle.dump(data.membre, open("membre.dat", "wb"))
        trading = False
        await ctx.channel.send("L'échange a été effectué !")


@client.command()
async def nope(ctx) :
    global trading
    print(trading)
    if trading == False :
        await ctx.channel.send("Il n'y a aucun échange en cours, utilise '>trade' pour échanger une carte !")
    elif not trading[1] == str(ctx.author.id) :
        await ctx.channel.send("Ce n'est pas à toi de faire ça...")
    else :
        trading = False
        await ctx.channel.send("L'échange a été annulé...")


@client.command()
async def test(ctx, ident) :
    ident = int(ident)-1
    print(ident)
    await ctx.channel.send(data.carte[ident][3] + " : " + data.carte[ident][1])
    





#commandes combat :

plateau = [0]
deck = [0, 0, 0, 0]

@client.command()
async def deck(ctx, a, b, c, d) :
    if a in data.principaux and b in data.principaux and c in data.principaux and d in data.principaux :
        data.membre[5] = [a, b, c, d] #mettre ensuite le spécial et le secondaire qui correspond au principal
    else : await ctx.channel.send("Les cartes ne correspondent pas à l'ordre demandé : Personnage/Arme/Arme/Arme")


    
@client.command()
async def arena(ctx) :
    global deck
    description=":black_large_square:"+data.carte[deck[0]][3]+":black_large_square:\n"+data.carte[deck[1]][3]+data.carte[deck[2]][3]+data.carte[deck[3]][3]+"\n\n"+data.carte[deck[1]][3]+data.carte[deck[2]][3]+data.carte[deck[3]][3]+"\n:black_large_square:"+data.carte[deck[0]][3]+":black_large_square:"+"ererer"
    await ctx.channel.send(description)


@client.command()
async def clash(ctx, card) :
    global deck
    await ctx.channel.send(description)


#MTExNDg0NjA2Njk1Nzg3NzI0OA.G_PCLB.nqsjbv3o6T3BmY3OtO76MF6Mav9HftVVDMCnWc Tableturf
#MTExNzgyODgyODYyMzAzMjM3Mg.GChJdm.ercO74GL6B8aN6xKwVUYVQ4IP3n7StnP9OEMJM Tabletest
client.run("MTExNzgyODgyODYyMzAzMjM3Mg.GChJdm.ercO74GL6B8aN6xKwVUYVQ4IP3n7StnP9OEMJM")