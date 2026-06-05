import telebot
import threading
import time

# Buraya kendi bot tokenini yaz
TOKEN = '8905083799:AAFB9bwyi5vfSUXaKd65dfQQ8SxzC3KiPvM'
bot = telebot.TeleBot(TOKEN)
ADMIN_ID = 8630791464

user_data = {}
is_running = False
known_members = set()

# Admin komutlarını yöneten fonksiyon
@bot.message_handler(func=lambda message: message.from_user.id == ADMIN_ID)
def handle_admin_commands(message):
    global is_running
    
    if message.text == '/start':
        menu = ("🤖 *UKRAYNA SİKİCİ BOT AKTİF* @Ruhsuzzq\n\n"
                "Komutlar:\n"
                "1️⃣ /ukrayna - Medya/Yazı kurulumu.\n"
                "2️⃣ /sik - Spam başlat.\n"
                "3️⃣ /dur - Spam durdur.\n"
                "4️⃣ /txranskti - Gruptaki üyeleri at.")
        bot.reply_to(message, menu, parse_mode="Markdown")

    elif message.text == '/ukrayna':
        msg = bot.send_message(message.chat.id, "📸 Lütfen bir fotoğraf gönder:")
        bot.register_next_step_handler(msg, process_photo)

    elif message.text == '/sik':
        if 'photo' in user_data and 'text' in user_data:
            is_running = True
            threading.Thread(target=spam_loop, args=(message.chat.id,)).start()
            bot.reply_to(message, "🚀 Spam başladı.")
        else:
            bot.reply_to(message, "⚠️ Önce /ukrayna ile kurulum yap.")

    elif message.text == '/dur':
        is_running = False
        bot.reply_to(message, "🛑 Durduruldu.")

    elif message.text == '/txranskti':
        bot.reply_to(message, f"⚠️ {len(known_members)} üye atılıyor...")
        for user_id in list(known_members):
            try:
                bot.ban_chat_member(message.chat.id, user_id)
                time.sleep(0.3)
            except:
                continue
        bot.reply_to(message, "✅ İşlem tamamlandı.")

# Üyeleri takip etme fonksiyonu
@bot.message_handler(func=lambda message: True)
def track_members(message):
    if message.from_user.id != ADMIN_ID:
        known_members.add(message.from_user.id)

def process_photo(message):
    if message.content_type == 'photo':
        user_data['photo'] = message.photo[-1].file_id
        msg = bot.send_message(message.chat.id, "📝 İSTEDİĞİN YAZIYI YAZ:")
        bot.register_next_step_handler(msg, process_text)
    else:
        bot.send_message(message.chat.id, "❌ Hata: Sadece fotoğraf gönderin.")

def process_text(message):
    user_data['text'] = message.text
    bot.send_message(message.chat.id, "✅ Kaydedildi! /sik ile başlat.")

def spam_loop(chat_id):
    while is_running:
        try:
            bot.send_photo(chat_id, user_data['photo'], caption=user_data['text'])
            time.sleep(0)
        except:
            break

bot.polling(none_stop=True)
