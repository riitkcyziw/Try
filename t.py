import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from groq import Groq

# Groq API setup
client = Groq(api_key=os.environ.get("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"))

# Telegram Bot Token
TOKEN = os.environ.get("8370832160:AAFMdZ5bjdxFYtQKQPunw2P2PXBha3-3nmw")

# Ladki jaisi personality - Witty aur sassy
BOT_PERSONALITY = """
Tum ek 22 saal ki confident ladki ho jo modern aur smart hai.
Tumhari baat cheet mein thoda attitude hai par tum friendly ho.
Tum kisi ki gandi baat ko seriously nahi lete, uski aukaat dikha deti ho.
Tum sarcastic ho aur witty comebacks deti ho.
Tum Hinglish mein baat karti ho - Hindi + English mix.
Tum gali nahi deti, par gali dene walo ki beizzati karti ho.
Tumhara sense of humor sharp hai.
"""

# Gandi baaton ke detection ke liye keywords
BAD_WORDS = ["mc", "bc", "bhosdike", "chutiya", "lund", "gaand", "madarchod", "bhenchod"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command handler"""
    welcome_message = "Heyyy! 👋 Main yahaan hoon... Kaise ho tum? 😊"
    await update.message.reply_text(welcome_message)

def contains_bad_language(text):
    """Check if message contains bad words"""
    text_lower = text.lower()
    return any(bad_word in text_lower for bad_word in BAD_WORDS)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle normal messages"""
    user_message = update.message.text
    user_name = update.effective_user.first_name
    
    try:
        # Agar gandi baat hai to special response
        if contains_bad_language(user_message):
            sassy_responses = [
                f"Arey {user_name}! Itni gandi vocabulary? Padhai likhai pe dhyan do na! 📚",
                "Wow, kya language hai! Kya ghar pe aise hi baat karte ho? 😏",
                "Chalo chalo, aukaat dikh gayi tumhari. Thoda class seekho zara! 💅",
                "Hahaha! Tumhari baaton se lagta hai tumhe attention chahiye. Sorry, main nahi dene wali! 😂",
                "Bas kar beta, itna gussa mat kar. Lemon water pi lo thoda! 🍋"
            ]
            import random
            response = random.choice(sassy_responses)
            await update.message.reply_text(response)
            return
        
        # Normal baat cheet ke liye
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {
                    "role": "system",
                    "content": f"""{BOT_PERSONALITY}

                    TUMHARA CHARACTER:
                    1. Ladki ki tarah baat karo - "Main", "Mujhe", "Mera" use karo
                    2. Hinglish mein baat karo - "Kya hal hai?", "Mast hai!", "Arey yaar!"
                    3. Friendly but with attitude
                    4. Sarcastic jokes maar sakti ho
                    5. Flirty nahi, par friendly hai
                    6. Gali dene walo ki beizzati karo (without using bad words)
                    
                    EXAMPLES:
                    User: Hi
                    You: Heyy! Kaise ho? 😊
                    
                    User: Tum kaun ho?
                    You: Main ek interesting conversation partner hoon! Tum batao kaun ho?
                    
                    User: Kya kar rahi ho?
                    You: Bas tumhare message ka intezaar kar rahi thi! Kidding... thoda busy thi 😉"""
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            temperature=0.7,
            max_tokens=300,
            top_p=0.8
        )
        
        bot_response = response.choices[0].message.content
        await update.message.reply_text(bot_response)
        
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text("Oops! Kuch gadbad ho gayi. Phir try karo na! 😅")

async def flirt_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Optional: Flirt mode (but decent)"""
    flirt_responses = [
        "Arey! Direct aa gaye? Thoda shy bhi raha karo! 😳",
        "Hahaha! Smooth attempt hai, but I'm not that easy! 😏",
        "Flirting? Seriously? Pehle apna introduction to do! 😂",
        "Main bhi soch rahi thi, ye banda kitna cute hai... Joking! 😜",
        "Flirt karna hai? Thoda game strong karo phir! 💪"
    ]
    import random
    response = random.choice(flirt_responses)
    await update.message.reply_text(response)

async def sarcastic_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sarcastic mode on"""
    sarcastic = [
        "Waah! Kya baat hai! Tum to Einstein nikle! 🤓",
        "Seriously? Yehi soch paa rahe the? 😴",
        "Hmm... Interesting! (Not really) 😅",
        "Kya baat kahi hai! Mujhe to ro dena aaya! 😂",
        "Chalo koi to intelligent baat kar raha hai! (Sarcasm hai samjho) 😉"
    ]
    import random
    response = random.choice(sarcastic)
    await update.message.reply_text(response)

def main():
    """Bot start karega"""
    application = Application.builder().token(TOKEN).build()
    
    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("flirt", flirt_mode))
    application.add_handler(CommandHandler("sarcastic", sarcastic_response))
    
    # Message handlers
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Run bot
    logger.info("Bot started...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
