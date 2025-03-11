import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from twilio.rest import Client

# Konfigurasi logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Token API Telegram Anda
TELEGRAM_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# Konfigurasi Twilio
TWILIO_SID = 'YOUR_TWILIO_SID'
TWILIO_AUTH_TOKEN = 'YOUR_TWILIO_AUTH_TOKEN'
TWILIO_WHATSAPP_NUMBER = 'whatsapp:+YOUR_TWILIO_WHATSAPP_NUMBER'
RECIPIENT_WHATSAPP_NUMBER = 'whatsapp:+RECIPIENT_WHATSAPP_NUMBER'

# Inisialisasi Twilio Client
twilio_client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

# Fungsi untuk memulai bot
def start(update: Update, context: CallbackContext):
    update.message.reply_text('Halo! Kirimkan pesan yang ingin Anda teruskan ke WhatsApp.')

# Fungsi untuk menangani pesan teks
def echo(update: Update, context: CallbackContext):
    message = update.message.text
    send_whatsapp_message(message)
    update.message.reply_text('Pesan Anda telah diteruskan ke WhatsApp.')

# Fungsi untuk mengirim pesan WhatsApp menggunakan Twilio
def send_whatsapp_message(message: str):
    twilio_client.messages.create(
        body=message,
        from_=TWILIO_WHATSAPP_NUMBER,
        to=RECIPIENT_WHATSAPP_NUMBER
    )

def main():
    # Buat updater dan pasang dispatcher
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Tambahkan handler untuk perintah /start
    dp.add_handler(CommandHandler("start", start))

    # Tambahkan handler untuk pesan teks
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Mulai bot
    updater.start_polling()

    # Jalankan bot sampai Anda menghentikannya dengan Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
