import requests
import base64
import os
from io import BytesIO
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Configura tu Token de Telegram
TELEGRAM_TOKEN = "7869727885:AAEJhGCegjLLLGdWWhC7ZWHlf7mOpME8ptg"
# URL de Stable Diffusion WebUI (corriendo localmente o en servidor)
SD_URL = "http://127.0.0.1:7860/sdapi/v1/txt2img"

# Función para generar imágenes con Stable Diffusion
def generate_image(prompt):
    payload = {
        "prompt": prompt,
        "steps": 30,  # Número de pasos de generación
        "width": 512,
        "height": 512
    }
    
    response = requests.post(SD_URL, json=payload)
    if response.status_code == 200:
        image_data = response.json()["images"][0]
        image_bytes = base64.b64decode(image_data)
        return BytesIO(image_bytes)
    else:
        return None

# Función que maneja los mensajes del bot
def handle_message(update: Update, context: CallbackContext):
    prompt = update.message.text
    update.message.reply_text("Generando imagen... ⏳")
    
    image = generate_image(prompt)
    
    if image:
        update.message.reply_photo(photo=image)
    else:
        update.message.reply_text("Error al generar la imagen. 😢")

# Configuración del bot
def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
