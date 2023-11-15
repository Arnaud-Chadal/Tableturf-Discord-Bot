import discord

def makeEmbed(varColour, varTitle, varDescription, varAuthor=None, varImage=None, varThumbnail=None, varFooter=None) :
    embed = discord.Embed(
        colour = varColour,
        title = varTitle,
        description = varDescription
    )
    if varAuthor is not None :
        embed.set_author(name = varAuthor)
    if varImage is not None :
        embed.set_image(url = varImage)
    if varThumbnail is not None :
        embed.set_thumbnail(url = varThumbnail)
    if varFooter is not None :
        embed.set_footer(text = varFooter)
    return embed