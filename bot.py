import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from transformers import pipeline

# Initialize Hugging Face pipeline
model_name = "EleutherAI/gpt-neo-2.7B"
hf_pipeline = pipeline("text-generation", model=model_name, tokenizer=model_name)

def query_gpt(question):
    result = hf_pipeline(question, max_length=150, num_return_sequences=1)
    return result[0]['generated_text']

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hi! I'm your educational assistant bot. Ask me anything!")

def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    answer = query_gpt(user_message)
    update.message.reply_text(answer)

def main():
    token = os.getenv("TELEGRAM_API_TOKEN")
    if not token:
        print("No token provided. Please set the TELEGRAM_API_TOKEN environment variable.")
        return

    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    print("Bot started")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
