from Akshi import CMD_HELP, ALIVE_LOGO, bot
from platform import python_version, uname
from telethon import version, events
import asyncio, datetime, psutil, shutil, time, sys, platform

modules = CMD_HELP
StartTime = time.time()


async def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += time_list.pop() + ", "

    time_list.reverse()
    up_time += ":".join(time_list)

    return up_time


def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


@bot.on(events.NewMessage(outgoing=True, pattern="^[?.]alive$"))
async def alivekora(alive):
    user = await bot.get_me()
    uptime = await get_readable_time((time.time() - StartTime))
    await alive.edit("`hey, you have doubt? ohh shit...`")
    await alive.edit("`i'm really alive re`")

    text = (
        f" **»»------(¯`ƙσɾα UʂҽɾႦσƚ´¯)------»»** \n\n"
        f"┏━━━━━━━━━━━━━━━━━━━\n"
        f"┣[• `Owner :` `{user.first_name}` \n"
        f"┣[• `Username :` `{user.username}` \n"
        f"┣[• `Uptime :` `{uptime}` \n"
        f"┣[• `Telethon :`Ver {version.__version__} \n"
        f"┣[• `Python   :`Ver {python_version()} \n"
        f"┣[• `Modules  :`{len(modules)} Modules \n"
        f"┗━━━━━━━━━━━━━━━━━━━")
    if ALIVE_LOGO:
        try:
            logo = ALIVE_LOGO
            await alive.delete()
            msg = await bot.send_file(alive.chat_id, logo, caption=text)
            await asyncio.sleep(200)
            await msg.delete()
        except BaseException:
            await alive.edit(
                text + "\n\n *`The provided logo is invalid."
                "\nMake sure the link is directed to the logo picture`"
            )
            await asyncio.sleep(200)
            await alive.delete()
    else:
        await alive.edit(text)
        await asyncio.sleep(200)
        await alive.delete()


from datetime import datetime


@bot.on(events.NewMessage(pattern="^[?.]ping$"))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    await event.edit("Pong!")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await event.edit("Pong!\n{}".format(ms))




@bot.on(events.NewMessage(outgoing=True, pattern="^[?.]system$"))
async def psu(event):
    uname = platform.uname()
    softw = "**System Information**\n"
    softw += f"`System   : {uname.system}`\n"
    softw += f"`Release  : {uname.release}`\n"
    softw += f"`Version  : {uname.version}`\n"
    softw += f"`Machine  : {uname.machine}`\n"
    # Boot Time
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    softw += f"`Boot Time: {bt.day}/{bt.month}/{bt.year}  {bt.hour}:{bt.minute}:{bt.second}`\n"
    # CPU Cores
    cpuu = "**CPU Info**\n"
    cpuu += "`Physical cores   : " + str(psutil.cpu_count(logical=False)) + "`\n"
    cpuu += "`Total cores      : " + str(psutil.cpu_count(logical=True)) + "`\n"
    # CPU frequencies
    cpufreq = psutil.cpu_freq()
    cpuu += f"`Max Frequency    : {cpufreq.max:.2f}Mhz`\n"
    cpuu += f"`Min Frequency    : {cpufreq.min:.2f}Mhz`\n"
    cpuu += f"`Current Frequency: {cpufreq.current:.2f}Mhz`\n\n"
    # CPU usage
    cpuu += "**CPU Usage Per Core**\n"
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
        cpuu += f"`Core {i}  : {percentage}%`\n"
    cpuu += "\n**Total CPU Usage**\n"
    cpuu += f"`All Core: {psutil.cpu_percent()}%`\n"
    # RAM Usage
    svmem = psutil.virtual_memory()
    memm = "**Memory Usage**\n"
    memm += f"`Total     : {get_size(svmem.total)}`\n"
    memm += f"`Available : {get_size(svmem.available)}`\n"
    memm += f"`Used      : {get_size(svmem.used)} ({svmem.percent}%)`\n"
    # Disk Usage
    dtotal, dused, dfree = shutil.disk_usage(".")
    disk = "**Disk Usage**\n"
    disk += f"`Total     : {get_size(dtotal)}`\n"
    disk += f"`Free      : {get_size(dused)}`\n"
    disk += f"`Used      : {get_size(dfree)}`\n"
    # Bandwidth Usage
    bw = "**Bandwith Usage**\n"
    bw += f"`Upload  : {get_size(psutil.net_io_counters().bytes_sent)}`\n"
    bw += f"`Download: {get_size(psutil.net_io_counters().bytes_recv)}`\n"
    help_string = f"{str(softw)}\n"
    help_string += f"{str(cpuu)}\n"
    help_string += f"{str(memm)}\n"
    help_string += f"{str(disk)}\n"
    help_string += f"{str(bw)}\n"
    help_string += "**Engine Info**\n"
    help_string += f"`Python {sys.version}`\n"
    help_string += f"`Telethon {version.__version__}`"
    await event.edit(help_string)

CMD_HELP.update(
    {
        "status": "?alive <global command>\
\nUsage: check your bot alive or not.\
\n\n?ping <global command>\
\nUsage: check ping rate of bot.\
\n\n?system <global command>\
\nUsage: check system information."
    }
    
)