import os
from pyrogram import Client, filters
from pyrogram.types import Message

# ✅ Put your API details here (from my.telegram.org and BotFather)
API_ID = int(os.getenv("API_ID", "12475131"))
API_HASH = os.getenv("API_HASH", "719171e38be5a1f500613837b79c536f")
BOT_TOKEN = os.getenv("BOT_TOKEN", "7564571951:AAE6xX7b2wPr6jh2SNV4ZH6EoVJXREuyAU8")

# ✅ Domain mapping
DOMAIN_MAP = {
    "https://apps-s3-jw-prod.utkarshapp.com/": 
    "https://d1q5ugnejk3zoi.cloudfront.net/ut-production-jw/"
}

bot = Client(
    "domain_changer_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

def change_domain_in_line(line: str) -> str:
    for old, new in DOMAIN_MAP.items():
        if old in line:
            return line.replace(old, new)
    return line

def process_file(input_path: str, output_path: str):
    with open(input_path, "r", encoding="utf-8") as infile, \
         open(output_path, "w", encoding="utf-8") as outfile:
        for line in infile:
            updated_line = change_domain_in_line(line.strip())
            outfile.write(updated_line + "\n")

@bot.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply_text(
        "👋 Namaste! Send me a `.txt` file with URLs and I will replace domains.\n\n"
        "Current Mapping:\n"
        "`https://apps-s3-jw-prod.utkarshapp.com/`\n➡️\n"
        "`https://d1q5ugnejk3zoi.cloudfront.net/ut-production-jw/`"
    )

@bot.on_message(filters.document)
async def handle_file(client, message: Message):
    file = message.document

    if not file.file_name.endswith(".txt"):
        await message.reply_text("⚠️ Please send a `.txt` file only.")
        return

    input_path = await message.download()
    output_path = "updated_" + file.file_name

    try:
        process_file(input_path, output_path)
        await message.reply_document(output_path, caption="✅ Updated file with new domain")
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")
    finally:
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)

print("🤖 Namaste Domain Changer Bot Running...")
bot.run()
