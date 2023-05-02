import instaloader
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TOKEN = 'YOUR BOT TOKEN'

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="""Hello, I am here to help you.
I confirm that I stole your information :)
Please write in the following format:

username password targetUsername""")


def handle_message(update, context):
    try:
        message = update.message.text
        username, password, targetUser = message.split(' ')[0], message.split(' ')[1], message.split(' ')[2]
        L = instaloader.Instaloader()
        L.context.username = username
        L.context.password = password
        L.login(username, password)
        profile = instaloader.Profile.from_username(L.context, targetUser)
        following = set(profile.get_followees())
        followers = set(profile.get_followers())
        unfollowers = following - followers
        unfollowerUser = [unfollower.username for unfollower in unfollowers]

        unfollowerList = "Accounts not follower:\n" + "\n".join(unfollowerUser)
        result_message = f"Number of unfollower accounts: {len(unfollowerUser)}\n\n{unfollowerList}"
        context.bot.send_message(chat_id=update.effective_chat.id, text=result_message)
    except:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Error, Please try again!!")
def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
