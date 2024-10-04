import telebot
import yt_dlp
import os
from youtubesearchpython import VideosSearch

# Masukkan token bot Telegram dari BotFather
TOKEN = '7591766767:AAG4c9XfQlxvtCw36uNgGL7JCkhNh4EWj0Q'
bot = telebot.TeleBot(TOKEN)

# Fungsi untuk menangani perintah /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Halo! Saya bot musik YouTube. Gunakan perintah /play <judul_lagu> untuk memainkan musik dari YouTube.")

# Fungsi untuk menangani perintah /play
@bot.message_handler(commands=['play'])
def play_music(message):
    title = ' '.join(message.text.split()[1:])  # Ambil judul lagu dari pesan
    if not title:
        bot.reply_to(message, "Mohon masukkan judul lagu setelah perintah /play.")
        return

    # Mencari video YouTube berdasarkan judul
    videos_search = VideosSearch(title, limit = 1)
    results = videos_search.next()
    
    if not results:
        bot.reply_to(message, "Tidak ada hasil ditemukan.")
        return
    
    video_url = results[0]['link']  # Ambil URL video pertama dari hasil pencarian

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'downloaded_song.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        bot.reply_to(message, "Mengunduh musik dari YouTube...")
        ydl.download([video_url])

    # Kirim file audio ke grup setelah diunduh
    with open("downloaded_song.mp3", 'rb') as audio:
        bot.send_audio(message.chat.id, audio)

    # Hapus file audio setelah dikirim
    os.remove("downloaded_song.mp3")

# Menjalankan bot
bot.polling()
                 
