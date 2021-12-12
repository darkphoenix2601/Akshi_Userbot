from Akshi import CMD_HELP, BOT_USERNAME, BOT_TOKEN
from Akshi import bot
from telethon import events
import logging



@bot.on(events.NewMessage(outgoing=True, pattern="^[?.]help(?: |$)(.*)"))
async def help(event):
    """ For ?help command,"""
    args = event.pattern_match.group(1).lower()
    if args:
        if args in CMD_HELP:
            await event.edit(str(CMD_HELP[args]))
        else:
            await event.edit("Please specify a valid module name.")
    else:
        string = ""
        for i in CMD_HELP:
            string += "`" + str(i)
            string += "`\t\t\t||\t\t\t "
        await event.edit(
            f"{string}"
            "\n\nSpecify which module do you want help for !!\
                        \n**Usage:** `?help` <module name>"
        )



from telethon.errors.rpcerrorlist import BotInlineDisabledError

logging.basicConfig(
    format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
    level=logging.WARNING)


@bot.on(events.NewMessage(pattern="^[?.]helpme$"))
async def helpme(event):
    tgbotusername = BOT_USERNAME
    if tgbotusername and BOT_TOKEN:
        try:
            results = await event.client.inline_query(
                tgbotusername,
                "@KoraUserbot"
            )
        except BotInlineDisabledError:
            return await event.edit("`Bot can't be used in inline mode.\nMake sure to turn on inline mode!`")
        await results[0].click(
            event.chat_id,
            reply_to=event.reply_to_msg_id,
            hide_via=True
        )
        await event.delete()
    else:
        return await event.edit("`The bot doesn't work! Please set the Bot Token and Username correctly.`"
                                "\n`The module has been stopped.`")