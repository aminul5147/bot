import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, ChatMemberHandler

BOT_TOKEN = os.getenv("TOKEN")
REQUIRED_NAME_PART = "TABD🇧🇩"
REQUIRED_BIO_PART = "ফ্রীতে ইনকাম করতে জয়েন করুন: @TechnicalAminulBD"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def restrict_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat

    if not user or not chat:
        return

    if user.id == context.bot.id:
        return

    name_ok = REQUIRED_NAME_PART in (user.full_name or "")
    bio_ok = False

    try:
        user_profile = await context.bot.get_chat(user.id)
        bio_ok = REQUIRED_BIO_PART in (user_profile.bio or "")
    except Exception as e:
        logging.warning(f"Could not fetch bio for user {user.id}: {e}")

    if not (name_ok and bio_ok):
        try:
            await context.bot.restrict_chat_member(
                chat_id=chat.id,
                user_id=user.id,
                permissions={"can_send_messages": False}
            )
            await context.bot.send_message(
                chat_id=chat.id,
                text=f"Hello {user.full_name}"

"
                     f"আপনার টেলিগ্রাম নামের সাথে যুত্ত করুন: TABD🇧🇩

"
                     f"এবং আপনার টেলিগ্রাম এর Bio তে যুক্ত করুন:  ফ্রীতে ইনকাম করতে জয়েন করুন @TechnicalAminulBD

"
                     f"তাহলেই আপনি গ্রুপে মেসেজ দিতে পারবেন। ধন্যবাদ।"
            )
        except Exception as e:
            logging.error(f"Could not restrict user {user.id}: {e}")

async def handle_new_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.chat_member.new_chat_members:
        fake_update = Update(update.update_id, message=update.chat_member)
        fake_update.effective_user = member
        fake_update.effective_chat = update.chat_member.chat
        await restrict_user(fake_update, context)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, restrict_user))
    app.add_handler(ChatMemberHandler(handle_new_members, ChatMemberHandler.CHAT_MEMBER))
    app.run_polling()

if __name__ == '__main__':
    main()
