import os
import re
import logging
from logging import getLogger
from telethon import version, __version__
from telethon.sync import TelegramClient, custom, events
from telethon.sessions import StringSession
from math import ceil
from platform import python_version




logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)

LOGGER = getLogger(__name__)


CMD_HELP = {}
COUNT_PM = {}
LASTMSG = {}

# Telegram App KEY and HASH
API_KEY = 2191715
API_HASH = "f8f5367907ae63115bbdce3524b87671"

# Userbot Session String
STRING_SESSION = os.environ.get("STRING_SESSION", "")

# Logging channel/group ID configuration.
BOTLOG = int(os.environ.get("BOTLOG", ""))
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
BOT_USERNAME = os.environ.get("BOT_USERNAME", "")


# Bleep Blop, this is a bot ;)
PM_AUTO_BAN = os.environ.get("PM_AUTO_BAN", "True")

# Heroku Credentials for updater.
HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME", "")
HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", "")


# Custom (forked) repo URL for updater.
UPSTREAM_REPO_URL = os.environ.get(
    "UPSTREAM_REPO_URL", "https://github.com/Noob-Kittu/KoraUserbot.git")
UPSTREAM_REPO_BRANCH = os.environ.get("UPSTREAM_REPO_BRANCH", "main")


# SQL Database URI
DB_URI = os.environ.get("DATABASE_URL", default=None)

# Default .alive logo
ALIVE_LOGO = os.environ.get("ALIVE_LOGO") or "https://telegra.ph/file/b8a7689c29e999c60292a.jpg"

if STRING_SESSION:
    # pylint: disable=invalid-name
    bot = TelegramClient(StringSession(STRING_SESSION), API_KEY, API_HASH)
else:
    # pylint: disable=invalid-name
    bot = TelegramClient("koraUserbot", API_KEY, API_HASH)


async def check_botlog_chatid():
    if not BOTLOG:
        return

    entity = await bot.get_entity(BOTLOG)
    if entity.default_banned_rights.send_messages:
        LOGGER.info(
            "Your account doesn't have rights to send messages to BOTLOG "
            "group. Check if you typed the Chat ID correctly.")
        quit(1)


async def send_alive_status():
    if BOTLOG:
        message = (
            "**Bot is up and running!**\n\n"
            f"**Telethon:** {version.__version__}\n"
            f"**Python:** {python_version()}\n"
        )
        await bot.send_message(BOTLOG, message)
        return True

def paginate_help(page_number, loaded_modules, prefix):
    number_of_rows = 5
    number_of_cols = 2
    helpable_modules = [p for p in loaded_modules if not p.startswith("_")]
    helpable_modules = sorted(helpable_modules)
    modules = [
        custom.Button.inline("{} {}".format("🔹", x), data="ub_modul_{}".format(x))
        for x in helpable_modules
    ]
    pairs = list(zip(modules[::number_of_cols], modules[1::number_of_cols]))
    if len(modules) % number_of_cols == 1:
        pairs.append((modules[-1],))
    max_num_pages = ceil(len(pairs) / number_of_rows)
    modulo_page = page_number % max_num_pages
    if len(pairs) > number_of_rows:
        pairs = pairs[
            modulo_page * number_of_rows: number_of_rows * (modulo_page + 1)
        ] + [
            (
                custom.Button.inline(
                    "⬅️", data="{}_prev({})".format(prefix, modulo_page)
                ),
                custom.Button.inline(
                    "➡️", data="{}_next({})".format(prefix, modulo_page)
                ),
            )
        ]
    return pairs


with bot:
    try:
        tgbot = TelegramClient(
            "KoraBot",
            api_id=API_KEY,
            api_hash=API_HASH).start(
            bot_token=BOT_TOKEN)

        dugmeler = CMD_HELP
        me = bot.get_me()
        uid = me.id

        @tgbot.on(events.NewMessage(pattern="^[?/]start"))
        async def handler(event):
            if event.message.from_id != uid:
                await event.reply("I'm [Akshi](https://github.com/Noob-kittu/Akshi-Userbot) modules helper...\nplease make your own bot, don't use mine 😋")
            else:
                await event.reply(f"`Hey there {me.first_name}\n\nI work for you :)`")

        @tgbot.on(events.InlineQuery)  # pylint:disable=E0602
        async def inline_handler(event):
            builder = event.builder
            result = None
            query = event.text
            if event.query.user_id == uid and query.startswith("@KoraUserbot"):
                buttons = paginate_help(0, dugmeler, "helpme")
                result = builder.article(
                    "Please Use Only With .help Command",
                    text="{}\nTotal loaded modules: {}".format(
                        "KoraUserbot' modules helper.\n",
                        len(dugmeler),
                    ),
                    buttons=buttons,
                    link_preview=False,
                )
            elif query.startswith("tb_btn"):
                result = builder.article(
                    "KoraUserbot' Helper",
                    text="List of Modules",
                    buttons=[],
                    link_preview=True)
            else:
                result = builder.article(
                    "KoraUserbot'",
                    text="""You can convert your account to bot and use them. Remember, you can't manage someone else's bot! All installation details are explained from GitHub address below.""",
                    buttons=[
                        [
                            custom.Button.url(
                                "GitHub Repo",
                                "https://github.com/Noob-Kittu/Akshi-Userbot"),
                            custom.Button.url(
                                "Support",
                                "https://t.me/KoraSupport")],
                    ],
                    link_preview=False,
                )
            await event.answer([result] if result else None)

        @tgbot.on(
            events.callbackquery.CallbackQuery(  # pylint:disable=E0602
                data=re.compile(rb"helpme_next\((.+?)\)")
            )
        )
        async def on_plug_in_callback_query_handler(event):
            if event.query.user_id == uid:  # pylint:disable=E0602
                current_page_number = int(
                    event.data_match.group(1).decode("UTF-8"))
                buttons = paginate_help(
                    current_page_number + 1, dugmeler, "helpme")
                await event.edit(buttons=buttons)
            else:
                reply_pop_up_alert = "Please make for yourself, don't use my bot!"
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

        @tgbot.on(
            events.callbackquery.CallbackQuery(  # pylint:disable=E0602
                data=re.compile(rb"helpme_prev\((.+?)\)")
            )
        )
        async def on_plug_in_callback_query_handler(event):
            if event.query.user_id == uid:  # pylint:disable=E0602
                current_page_number = int(
                    event.data_match.group(1).decode("UTF-8"))
                buttons = paginate_help(
                    current_page_number - 1, dugmeler, "helpme"  # pylint:disable=E0602
                )
                await event.edit(buttons=buttons)
            else:
                reply_pop_up_alert = "Please make for yourself, don't use my bot!"
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

        @tgbot.on(
            events.callbackquery.CallbackQuery(  # pylint:disable=E0602
                data=re.compile(b"ub_modul_(.*)")
            )
        )
        async def on_plug_in_callback_query_handler(event):
            if event.query.user_id == uid:  # pylint:disable=E0602
                modul_name = event.data_match.group(1).decode("UTF-8")

                cmdhel = str(CMD_HELP[modul_name])
                if len(cmdhel) > 150:
                    help_string = (
                        str(CMD_HELP[modul_name]).replace('`', '')[:150] + "..."
                        + "\n\nRead more ?help "
                        + modul_name
                        + " "
                    )
                else:
                    help_string = str(CMD_HELP[modul_name]).replace('`', '')

                reply_pop_up_alert = (
                    help_string
                    if help_string is not None
                    else "{} No document has been written for module.".format(
                        modul_name
                    )
                )
            else:
                reply_pop_up_alert = "Please make for yourself, don't use my bot!"

            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

    except BaseException:
        LOGGER.info(
            "Support for inline is disabled on your bot. "
            "To enable it, define a bot token and enable inline mode on your bot. "
            "If you think there is a problem other than this, contact us.")

    try:
        tgbot.loop.run_until_complete(check_botlog_chatid())
    except BaseException:
        LOGGER.info(
            "BOTLOG environment variable isn't a "
            "valid entity. Check your environment variables/config.env file."
        )
        quit(1)

    try:
        tgbot.loop.run_until_complete(send_alive_status())
    except BaseException:
        pass



