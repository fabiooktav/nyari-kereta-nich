import os, json, re
import discord
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = os.getenv("SEARCH_CHANNEL_ID", "").strip()
SEARCH_CHANNEL_ID = int(CHANNEL_ID) if CHANNEL_ID.isdigit() else None
DATA_FILE = os.getenv("DATA_FILE", "data.json")

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True
bot = commands.Bot(command_prefix="!", intents=intents)

def norm(s):
    return re.sub(r"\s+", " ", str(s or "").lower().strip())

def load_db():
    with open(DATA_FILE, encoding="utf-8") as f:
        return json.load(f)

def train_matches(t, q):
    qn = norm(q)
    fields = [t.get("name",""), t.get("number",""), t.get("category",""), t.get("rolling_stock",""),
              t.get("route",""), t.get("speed_note",""), t.get("locomotive","")]
    fields += t.get("aliases", [])
    fields += t.get("number_aliases", [])
    return any(qn == norm(x) or qn in norm(x) for x in fields if x)

def embed_train(t):
    e = discord.Embed(title=f"🚆 {t['name']}", color=0x2D89EF)
    e.add_field(name="🔢 Nomor KA (rentang rekap)", value=t.get("number") or "Belum tersedia", inline=True)
    e.add_field(name="🚃 Formasi rangkaian", value=t.get("rolling_stock") or "Belum tersedia", inline=False)
    e.add_field(name="🚂 Lokomotif pendukung menurut rekap", value=t.get("locomotive") or "Belum dipetakan", inline=True)
    e.add_field(name="⚡ Keterangan kecepatan", value=t.get("speed_note") or "Belum tersedia", inline=False)
    if t.get("route"):
        e.add_field(name="🧭 Relasi", value=t["route"], inline=False)
    e.add_field(name="🕒 Jadwal Gapeka", value="Jadwal terpisah; hanya ditampilkan jika cocok dengan data Gapeka yang sudah dimuat.", inline=False)
    e.add_field(name="📌 Catatan", value=t.get("notes","Data mengikuti rekap pengguna."), inline=False)
    e.set_footer(text="RAILWAY FINDER • Data pendukung bukan jaminan penugasan aktual")
    return e

@bot.event
async def on_ready():
    print(f"Railway Finder aktif: {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot or not message.guild:
        return
    if SEARCH_CHANNEL_ID and message.channel.id != SEARCH_CHANNEL_ID:
        await bot.process_commands(message)
        return
    q = message.content.strip()
    if not q or q.startswith("!"):
        await bot.process_commands(message)
        return
    db = load_db()
    trains = db.get("trains", [])
    matches = [t for t in trains if train_matches(t, q)]
    # Number-only queries can match many trains/ranges; show a concise choice list.
    if len(matches) == 1:
        await message.reply(embed=embed_train(matches[0]), mention_author=False)
    elif 1 < len(matches) <= 8:
        e = discord.Embed(title="🔎 Hasil pencarian", description=f"Ada {len(matches)} hasil untuk **{q[:80]}**. Coba nama lebih lengkap.", color=0x2D89EF)
        for t in matches:
            e.add_field(name=f"{t['name']} • {t['number']}", value=t.get("category",""), inline=False)
        await message.reply(embed=e, mention_author=False)
    elif len(matches) > 8:
        await message.reply(f"🔎 Ada {len(matches)} hasil untuk **{q[:80]}**. Ketik nama KA yang lebih lengkap ya.", mention_author=False)
    else:
        # Only reply to likely train/name/number queries, not normal conversation.
        likely = q.isdigit() or re.search(r"\\b(ka|cc\\s?20[1346]|argo|bima|taksaka|gajayana|pandalungan|sembrani|turangga|jayakarta|kertajaya|progo|mataram)\\b", q, re.I)
        if likely:
            await message.reply(f"Belum menemukan **{q[:100]}** di database Railway Finder.", mention_author=False)
    await bot.process_commands(message)

if not TOKEN:
    raise RuntimeError("Atur DISCORD_TOKEN di environment variables.")
bot.run(TOKEN)
