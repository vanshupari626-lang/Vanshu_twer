import json
import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# Configuration
TOKEN = "8383292152:AAE-x4RY09qFwa4qoy0Jpe-sU-jHcyABSv0"
ADMIN_ID = 1146290731  # Aapki Admin ID
QUOTEX_LINK = "https://broker-qx.pro/sign-up/?lid=356370"
CHANNEL_LINK = "https://t.me/Tradewithrajjjj"
ADMIN_CONTACT = "https://t.me/TWR55"

# Database file to store approved users permanently
APPROVED_USERS_FILE = "approved_users.json"

def load_approved_users():
    if os.path.exists(APPROVED_USERS_FILE):
        try:
            with open(APPROVED_USERS_FILE, "r") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return set(data)
        except:
            return set()
    return set()

def save_approved_users():
    try:
        with open(APPROVED_USERS_FILE, "w") as f:
            json.dump(list(approved_users), f)
    except Exception as e:
        print(f"Error saving file: {e}")

# Memory tracking
approved_users = load_approved_users()
user_signals_left = {}
user_selected_pair = {}

# Datasets
CURRENCIES = [
    "USD/INR (OTC)", "USD/MXN (OTC)", "USD/NGN (OTC)", "USD/PHP (OTC)", "EUR/CAD (OTC)",
    "AUD/CAD", "EUR/AUD", "USD/PKR (OTC)", "GBP/CAD", "USD/EGP (OTC)", "AUD/CHF",
    "AUD/USD", "CHF/JPY", "GBP/CHF", "EUR/CHF", "EUR/NZD (OTC)", "USD/CAD", "NZD/CAD",
    "NZD/CAD (OTC)", "USD/BDT (OTC)", "USD/BRL (OTC)", "USD/COP (OTC)", "USD/ARS (OTC)",
    "EUR/GBP", "EUR/JPY", "GBP/NZD (OTC)", "CAD/JPY", "NZD/JPY (OTC)", "AUD/NZD (OTC)",
    "USD/DZD (OTC)", "GBP/JPY", "EUR/USD", "GBP/USD", "AUD/JPY", "CAD/CHF (OTC)"
]
CRYPTO = ["BTCUSD", "ETHUSD", "LTCUSD", "XRPUSD"]
COMMODITIES = ["GOLD", "SILVER", "BRENT", "WTI"]

# Helper function to check VIP/Approved status
def is_user_vip(user_id):
    return (user_id == ADMIN_ID) or (int(user_id) in [int(u) for u in approved_users])

# Start Command Handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if is_user_vip(user_id):
        keyboard = [
            [InlineKeyboardButton("💱 Currencies", callback_data="cat_currencies")],
            [InlineKeyboardButton("🪙 Crypto", callback_data="cat_crypto")],
            [InlineKeyboardButton("🛢️ Commodities", callback_data="cat_commodities")],
            [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK)]
        ]
        await update.message.reply_text(
            "🎉 **Welcome VIP Member!** Aapka account approved hai. Unlimited signals ke liye niche category select karein:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
        return

    user_signals_left.setdefault(user_id, 5)
    keyboard = [
        [InlineKeyboardButton("🔗 Register on Quotex ($50+)", url=QUOTEX_LINK)],
        [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK)],
        [InlineKeyboardButton("📊 Select Trade Pairs & Signals", callback_data="main_menu")],
        [InlineKeyboardButton("✅ Send Trader ID for Approval", callback_data="send_uid")]
    ]
    await update.message.reply_text("🤖 Welcome to TWR QUOTEX VIP Bot! Aapko 5 free signals milte hain.", reply_markup=InlineKeyboardMarkup(keyboard))

# Main Button Handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id
    vip_status = is_user_vip(user_id)

    if data == "send_uid":
        await query.edit_message_text(
            "📲 Kripya apne Quotex account ki **Trader ID** yahan chat mein type karke bhej dein, taaki admin verify kar sake.",
            parse_mode="Markdown"
        )
        
    elif data == "main_menu":
        if not vip_status:
            remaining = user_signals_left.get(user_id, 5)
            if remaining <= 0:
                keyboard = [
                    [InlineKeyboardButton("🔗 Register & Deposit Now", url=QUOTEX_LINK)],
                    [InlineKeyboardButton("✅ Send Trader ID for Approval", callback_data="send_uid")]
                ]
                await query.edit_message_text(
                    "❌ Aapke 5 Free Signals khatam ho chuke hain!\n\n"
                    "Unlimited VIP signals ke liye kripya Quotex par account banakar $50+ deposit karein aur apni Trader ID admin ko bhejein.",
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )
                return

        keyboard = [
            [InlineKeyboardButton("💱 Currencies", callback_data="cat_currencies")],
            [InlineKeyboardButton("🪙 Crypto", callback_data="cat_crypto")],
            [InlineKeyboardButton("🛢️ Commodities", callback_data="cat_commodities")],
            [InlineKeyboardButton("⬅️ Back", callback_data="back_start")]
        ]
        await query.edit_message_text("📂 Select Pair Category:", reply_markup=InlineKeyboardMarkup(keyboard))
        
    elif data == "cat_currencies":
        keyboard = [[InlineKeyboardButton(pair, callback_data=f"signal_{pair}")] for pair in CURRENCIES[:20]]
        keyboard.append([InlineKeyboardButton("⬅️ Back to Menu", callback_data="main_menu")])
        await query.edit_message_text("💱 Select Currency Pair for Signal:", reply_markup=InlineKeyboardMarkup(keyboard))
        
    elif data == "cat_crypto":
        keyboard = [[InlineKeyboardButton(pair, callback_data=f"signal_{pair}")] for pair in CRYPTO]
        keyboard.append([InlineKeyboardButton("⬅️ Back to Menu", callback_data="main_menu")])
        await query.edit_message_text("🪙 Select Crypto Pair for Signal:", reply_markup=InlineKeyboardMarkup(keyboard))
        
    elif data == "cat_commodities":
        keyboard = [[InlineKeyboardButton(pair, callback_data=f"signal_{pair}")] for pair in COMMODITIES]
        keyboard.append([InlineKeyboardButton("⬅️ Back to Menu", callback_data="main_menu")])
        await query.edit_message_text("🛢️ Select Commodity Pair for Signal:", reply_markup=InlineKeyboardMarkup(keyboard))
        
    elif data == "back_start":
        if vip_status:
            keyboard = [
                [InlineKeyboardButton("💱 Currencies", callback_data="cat_currencies")],
                [InlineKeyboardButton("🪙 Crypto", callback_data="cat_crypto")],
                [InlineKeyboardButton("🛢️ Commodities", callback_data="cat_commodities")],
                [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK)]
            ]
            await query.edit_message_text("🤖 **VIP Menu:** Select category:", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
            return

        keyboard = [
            [InlineKeyboardButton("🔗 Register on Quotex ($50+)", url=QUOTEX_LINK)],
            [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK)],
            [InlineKeyboardButton("📊 Select Trade Pairs & Signals", callback_data="main_menu")],
            [InlineKeyboardButton("✅ Send Trader ID for Approval", callback_data="send_uid")]
        ]
        await query.edit_message_text("🤖 Welcome back to TWR QUOTEX VIP Bot!", reply_markup=InlineKeyboardMarkup(keyboard))
        
    elif data.startswith("signal_"):
        pair_name = data.replace("signal_", "")
        user_selected_pair[user_id] = pair_name
        
        keyboard = [
            [InlineKeyboardButton("⏱️ 1 Minute", callback_data="time_1m"), InlineKeyboardButton("⏱️ 2 Minutes", callback_data="time_2m")],
            [InlineKeyboardButton("⏱️ 5 Minutes", callback_data="time_5m")],
            [InlineKeyboardButton("🔙 Choose Another Pair", callback_data="main_menu")]
        ]
        await query.edit_message_text(
            f"📊 Selected Pair: **{pair_name}**\n\nAb apna **Timeframe / Expiry** select karein:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    elif data.startswith("time_"):
        if not vip_status:
            remaining = user_signals_left.get(user_id, 5)
            if remaining <= 0:
                keyboard = [
                    [InlineKeyboardButton("🔗 Register & Deposit", url=QUOTEX_LINK)],
                    [InlineKeyboardButton("✅ Send Trader ID for Approval", callback_data="send_uid")]
                ]
                await query.edit_message_text(
                    "❌ Aapke 5 free trades poore ho chuke hain! Full access ke liye account verify karwayein.",
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )
                return
            user_signals_left[user_id] = remaining - 1

        time_map = {
            "time_1m": "1 Minute",
            "time_2m": "2 Minutes",
            "time_5m": "5 Minutes"
        }
        time_frame = time_map.get(data, "1 Minute")
        pair_name = user_selected_pair.get(user_id, "EUR/USD")
        
        signal_type = random.choice(["🟢 CALL (UP)", "🔴 PUT (DOWN)"])
        
        if vip_status:
            rem_text = "\n\n⭐ **VIP Full Access (Unlimited Signals)**"
        else:
            rem_text = f"\n\n🎁 Baaki Free Signals: {user_signals_left.get(user_id, 0)}"

        signal_msg = (
            f"🎯 VIP Signal Generated (90% Accuracy)\n\n"
            f"📊 Pair: {pair_name}\n"
            f"📈 Action: {signal_type}\n"
            f"⏱️ Timeframe: {time_frame}"
            f"{rem_text}"
        )
        
        keyboard = [[InlineKeyboardButton("🔙 Choose Another Pair", callback_data="main_menu")]]
        await query.edit_message_text(signal_msg, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

# Message Handler for Trader ID or Text
async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message_text = update.message.text
    user_id = user.id
    
    if is_user_vip(user_id):
        keyboard = [
            [InlineKeyboardButton("📊 Select Trade Pairs & Signals", callback_data="main_menu")],
            [InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK)]
        ]
        await update.message.reply_text(
            "✅ Aapka account pehle se Approved hai! Niche diye gaye button se unlimited signals lein:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    keyboard = [
        [
            InlineKeyboardButton("✅ Approve", callback_data=f"approve_{user.id}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"reject_{user.id}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    forward_text = (
        f"📥 New Verification Request:\n\n"
        f"👤 Name: {user.first_name}\n"
        f"🆔 Telegram ID: {user.id}\n"
        f"🔗 Username: @{user.username if user.username else 'None'}\n"
        f"💬 Trader ID Data: {message_text}"
    )
    
    await context.bot.send_message(chat_id=ADMIN_ID, text=forward_text, reply_markup=reply_markup)
    await update.message.reply_text("Aapki Trader ID admin ke paas verification ke liye bhej di gayi hai. Kripya intezaar karein.")

# Admin Delete Command for Access Revocation
async def delete_user_access(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        return
    
    if not context.args:
        await update.message.reply_text("⚠️ Kripya user ki Telegram ID bhi likhein.\nExample: `/delete 1146290731`", parse_mode="Markdown")
        return
    
    try:
        target_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("❌ Galat ID format! Kripya sirf number wali Telegram ID likhein.")
        return
    
    if target_id in approved_users:
        approved_users.remove(target_id)
        save_approved_users()
        
        try:
            await context.bot.send_message(
                chat_id=target_id, 
                text="❌ **Aapka VIP Access Hata Diya Gaya Hai!**\nAapka account ya verification cancel ho chuki hai.",
                parse_mode="Markdown"
            )
        except:
            pass
        
        await update.message.reply_text(f"✅ Success! User `{target_id}` ka VIP access hata diya gaya hai.", parse_mode="Markdown")
    else:
        await update.message.reply_text(f"ℹ️ User `{target_id}` approved list mein nahi mila.", parse_mode="Markdown")

# Admin Action Handler
async def admin_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    action, target_user_id = data.split("_")
    target_user_id = int(target_user_id)
    
    if action == "approve":
        approved_users.add(target_user_id)
        save_approved_users()
        
        approved_msg = (
            "🎉 **Aapka Account Approve Ho Chuka Hai!**\n\n"
            "Ab aapko Full Access mil gaya hai. Ab aap bot par `/start` bhej kar ya menu se **unlimited signals** use kar sakte hain!"
        )
        try:
            await context.bot.send_message(chat_id=target_user_id, text=approved_msg, parse_mode="Markdown")
        except:
            pass
        await query.edit_message_text(text=f"✅ User {target_user_id} successfully APPROVED kar diya gaya hai.")
        
    elif action == "reject":
        rejected_msg = (
            "❌ Verification Rejected!\n\n"
            f"Kripya sahi process follow karke dobara contact karein: {ADMIN_CONTACT}"
        )
        try:
            await context.bot.send_message(chat_id=target_user_id, text=rejected_msg)
        except:
            pass
        await query.edit_message_text(text=f"❌ User {target_user_id} ka request REJECT kar diya gaya hai.")

def main():
    application = (
        ApplicationBuilder()
        .token(TOKEN)
        .connect_timeout(30)
        .read_timeout(30)
        .build()
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("delete", delete_user_access))
    application.add_handler(CallbackQueryHandler(admin_action, pattern="^(approve|reject)_"))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_message))

    print("Bot is running...")
    application.run_polling()

if __name__ == '__main__':
    main()
                                                      