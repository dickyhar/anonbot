import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Mengaktifkan logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

logger = logging.getLogger(__name__)

# Fungsi untuk menangani perintah /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Halo! Selamat datang di chat bot anonim. Kirim pesan apa pun dan saya akan meneruskannya kepada pengguna lain secara anonim.')

# Fungsi untuk menangani perintah /broadcast
def broadcast(update: Update, context: CallbackContext) -> None:
    if update.effective_user.id in admin_ids:  # Memeriksa apakah pengguna adalah admin
        message = ' '.join(context.args)
        for user_id in bot_users:
            context.bot.send_message(chat_id=user_id, text=message)
    else:
        update.message.reply_text('Anda tidak memiliki izin untuk melakukan broadcast pesan.')

# Fungsi untuk menangani perintah /next
def next_chat(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id not in chat_users:
        update.message.reply_text('Anda tidak sedang dalam sesi chat. Kirim /start untuk memulai sesi chat anonim.')
    else:
        chat_users.remove(user_id)
        update.message.reply_text('Anda telah berpindah ke pengguna selanjutnya. Kirim pesan apa pun dan saya akan meneruskannya kepada pengguna lain secara anonim.')

# Fungsi untuk menangani perintah /stop
def stop_chat(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id not in chat_users:
        update.message.reply_text('Anda tidak sedang dalam sesi chat. Kirim /start untuk memulai sesi chat anonim.')
    else:
        chat_users.remove(user_id)
        update.message.reply_text('Sesi chat anonim telah dihentikan. Kirim /start untuk memulai sesi chat baru.')


# Fungsi untuk menangani pesan yang diterima
def forward_message(update: Update, context: CallbackContext) -> None:
    # Mendapatkan pesan dari pengguna
    message = update.message.text
    
    # Mengirim pesan ke semua pengguna lain
    for user_id in context.bot.users:
        # Mengecualikan pengguna yang mengirim pesan
        if user_id != update.effective_user.id:
            context.bot.send_message(chat_id=user_id, text=message)

# Fungsi untuk menangani kesalahan
def error(update: Update, context: CallbackContext) -> None:
    logger.error(f'Error: {context.error}')

# Fungsi utama
def main() -> None:
    # Menginisialisasi objek Updater
    updater = Updater("6212995307:AAHzsmW7PpK3Qg2Tod_6MKl-IzScRYlC43w", use_context=True)

    # Mendapatkan dispatcher untuk mendaftarkan handler
    dispatcher = updater.dispatcher

    # Menambahkan handler perintah /start
    dispatcher.add_handler(CommandHandler("start", start))

     # Menambahkan handler perintah /broadcast
    dispatcher.add_handler(CommandHandler("broadcast", broadcast))

     # Menambahkan handler perintah /next
    dispatcher.add_handler(CommandHandler("next", next_chat))

    # Menambahkan handler perintah /stop
    dispatcher.add_handler(CommandHandler("stop", stop_chat))


    # Menambahkan handler pesan yang diterima
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, forward_message))

    # Menambahkan handler kesalahan
    dispatcher.add_error_handler(error)

    # Memulai bot
    updater.start_polling()

    # Menjaga bot tetap berjalan hingga diberhentikan secara manual
    updater.idle()

if __name__ == '__main__':
    admin_ids = [22936736]  # Ganti dengan daftar ID admin
    main()
