from importlib import import_module
from sys import argv

from telethon.errors.rpcerrorlist import PhoneNumberInvalidError
from Akshi import bot
from Akshi.modules import ALL_MODULES

INVALID_PH = '\nERROR: The Phone No. entered is INVALID' \
             '\n Tip: Use Country Code along with number.' \
             '\n or check your phone number and try again !'

try:
    bot.start()
except PhoneNumberInvalidError:
    print(INVALID_PH)
    exit(1)

for module_name in ALL_MODULES:
    imported_module = import_module("Akshi.modules." + module_name)


if len(argv) not in (1, 3, 4):
    bot.disconnect()
else:
    print("bot running now...")
    bot.run_until_disconnected()