"""Final project · Milestone 5 - Your assistant ON YOUR PHONE (Telegram bot).

Why Telegram: free, works on iPhone and Android, gives you a chat screen AND
push notifications (for reminders and the morning briefing), and needs no app
store. The bot runs on your computer and talks to Telegram's servers, so you
don't have to open any network ports.

SET-UP (10 minutes, once) - full steps in final_project/README.md:
  1. In Telegram, open @BotFather, send /newbot, choose a name. Copy the token.
  2. In .env:  TELEGRAM_BOT_TOKEN=<the token>
  3. Run:      python final_project/p5_telegram_bot.py
  4. In Telegram, open your new bot and send /start. It replies with YOUR user id.
  5. In .env:  TELEGRAM_OWNER_ID=<that id>   then restart the bot.
     From now on the bot answers ONLY you.

COMMANDS:  /brief  morning briefing now     /reminders  list reminders
           /start  help                     anything else = chat with the assistant
AUTOMATIC: the briefing arrives every day at BRIEFING_TIME (.env, default 07:00);
           reminders are pushed to your phone when they are due (checked every minute).
The bot only works while this script is running (see README: "Keep it running").
"""
import asyncio
import datetime as dt
import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import pa_core  # noqa: E402

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
OWNER = int(os.getenv("TELEGRAM_OWNER_ID", "0") or 0)
BRIEFING_TIME = os.getenv("BRIEFING_TIME", "07:00")
HELP = ("Hi! I'm your assistant.\n"
        "• Ask me anything: your day, emails, weather, money, facts\n"
        "• 'Remind me tomorrow at 9 to call Finance'\n"
        "• /brief - today's briefing   • /reminders - upcoming reminders\n"
        f"I send your briefing every day at {BRIEFING_TIME}.")

assistant = pa_core.Assistant()


async def send_long(bot, chat_id: int, text: str) -> None:
    """Telegram messages are limited to 4096 characters: split if needed."""
    for start in range(0, len(text), 3800):
        await bot.send_message(chat_id, text[start:start + 3800])


async def start(update, context):
    user_id = update.effective_user.id
    if not OWNER:
        await update.message.reply_text(
            f"Your Telegram user id is {user_id}.\nPut TELEGRAM_OWNER_ID={user_id} in the .env "
            "file and restart me. After that I will only talk to you.")
    elif user_id != OWNER:
        await update.message.reply_text("Sorry, this is a private assistant.")
    else:
        await update.message.reply_text(HELP)


async def brief(update, context):
    await update.message.reply_text("Preparing your briefing…")
    _, markdown = await asyncio.to_thread(pa_core.make_briefing)
    await send_long(context.bot, update.effective_chat.id, markdown)


async def reminders(update, context):
    items = assistant.reminders.upcoming()
    text = "\n".join(f"• {r['due'].replace('T', ' ')} - {r['text']} (id {r['id']})" for r in items)
    await update.message.reply_text(text or "No upcoming reminders.")


async def chat(update, context):
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    answer = await asyncio.to_thread(assistant.ask, update.message.text)
    await send_long(context.bot, update.effective_chat.id, answer)


async def push_due_reminders(context):
    for item in assistant.reminders.due_now():
        await context.bot.send_message(OWNER, f"⏰ Reminder: {item['text']}")
        assistant.reminders.mark_sent(item["id"])


async def morning_briefing(context):
    _, markdown = await asyncio.to_thread(pa_core.make_briefing)
    await send_long(context.bot, OWNER, markdown)


def build_app():
    from telegram.ext import Application, CommandHandler, MessageHandler, filters

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    if OWNER:
        only_owner = filters.User(user_id=OWNER)  # everyone else is ignored
        app.add_handler(CommandHandler("brief", brief, filters=only_owner))
        app.add_handler(CommandHandler("reminders", reminders, filters=only_owner))
        app.add_handler(MessageHandler(only_owner & filters.TEXT & ~filters.COMMAND, chat))
        app.job_queue.run_repeating(push_due_reminders, interval=60, first=10)
        hour, minute = (int(x) for x in BRIEFING_TIME.split(":"))
        local_tz = dt.datetime.now().astimezone().tzinfo
        app.job_queue.run_daily(morning_briefing, time=dt.time(hour, minute, tzinfo=local_tz))
    return app


if __name__ == "__main__":
    if not TOKEN:
        sys.exit("TELEGRAM_BOT_TOKEN is missing in .env - see the set-up steps at the top of this file.")
    print("Assistant bot running. Open Telegram and message your bot. Press Ctrl+C to stop.")
    if not OWNER:
        print("TELEGRAM_OWNER_ID is not set yet: send /start to your bot to get your id.")
    build_app().run_polling()
