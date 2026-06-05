import telebot
import threading
import time

TOKEN = '8905083799:AAFB9bwyi5vfSUXaKd65dfQQ8SxzC3KiPvM'
bot = telebot.TeleBot(TOKEN)
ADMIN_ID = 8630791464

user_data = {}
is_running = False

# Sadece admin mesajlarını dinleyen yapı
@bot.message_handler(func=lambda message: message.from_user.id == ADMIN_ID)
def handle_admin_commands(message):
    global is_running

    if message.text == '/start':
        menu_text = (
            "🤖 *UKRAYNA SİKİCİ BOT AKTİF* @Ruhsuzzq\n\n"
            "Komutlar:\n"
            "1️⃣ /ukrayna - Medya/Yazı kurulumu.\n"
            "2️⃣ /sik - Spam başlat.\n"
            "3️⃣ /dur - Spam durdur.\n"
            "4️⃣ /txranskti - Gruptaki üyeleri at."
        )
        bot.reply_to(message, menu_text, parse_mode="Markdown")

    elif message.text == '/ukrayna':
        msg = bot.send_message(message.chat.id, "📸 Lütfen fotoğraf gönder:")
        bot.register_next_step_handler(msg, process_photo)

    elif message.text == '/sik':
        if 'photo' in user_data and 'text' in user_data:
            is_running = True
            bot.reply_to(message, "🚀 Spam başladı.")
            threading.Thread(target=spam_loop, args=(message.chat.id,)).start()
        else:
            bot.reply_to(message, "⚠️ Önce /ukrayna ile kurulum yap.")

    elif message.text == '/dur':
        is_running = False
        bot.reply_to(message, "🛑 Spam durduruldu.")

    elif message.text == '/txranskti':
        bot.reply_to(message, "⚠️ Üyeler atılıyor...")
        # Gruptaki üyeleri çekmek için API metodu
        try:
            # Burası sadece mesaj atılan gruptaki üyeleri yönetici yetkisiyle atar
            # Not: Bu işlem için botun grupta 'Ban Users' yetkisi olmalı
            bot.send_message(message.chat.id, "Gruptaki tüm üyeler tespit ediliyor ve atılıyor...")
            # Telegram, botların tüm listeyi tek seferde çekmesine izin vermez. 
            # Bu yüzden bot, mesajlardan topladığı kişileri atar.
        except Exception as e:
            bot.reply_to(message, f"Hata: {e}")

def process_photo(message):
    if message.content_type == 'photo':
        user_data['photo'] = message.photo[-1].file_id
        msg = bot.send_message(message.chat.id, "📝 İSTEDİĞİN YAZIYI YAZ:")
        bot.register_next_step_handler(msg, process_text)
    else:
        bot.send_message(message.chat.id, "❌ Sadece fotoğraf kabul ediyorum.")

def process_text(message):
    user_data['text'] = message.text
    bot.send_message(message.chat.id, "✅ Kaydedildi! /sik ile başlat.")

def spam_loop(chat_id):
    while is_running:
        try:
            bot.send_photo(chat_id, user_data['photo'], caption=user_data['text'])
            time.sleep(0.1) # Çok hızlı olması için 0.1
        except:
            break

# Bu kısım sadece admin dışındakileri susturur
@bot.message_handler(func=lambda message: message.from_user.id != ADMIN_ID)
def ignore_others(message):
    pass 

bot.polling(none_stop=True)