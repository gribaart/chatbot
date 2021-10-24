#!/usr/bin/env python
# pylint: disable=C0116
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import re
from tempfile import mkstemp

import personality
import utils
import random
import requests
import schedule
from gtts import gTTS
from os import environ, remove


import time
from telegram import Update, ForceReply, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, \
    ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

import logging

from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Open API API token
headers = {
    'Content-type': 'application/json',
    'Authorization': 'Bearer sk-1eNrfXqxLR4XwWFwtPXR2roq4mtb656UNdB65XGF'
}


def text_to_audio(message_text: str):
    fd, path = mkstemp(suffix='.mp3')
    tts = gTTS(message_text, lang='en')
    tts.save(path)

    return path

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, _: CallbackContext) -> None:
    update.message.reply_text("""
    Hello! I am a virtual psychologist and your personal assistant that helps to resolve nicotine addiction issue.""")

    update.message.reply_text("""
    During the day I will send you interesting videos about the dangers of smoking, tips on how to cope with the urge 
    to smoke a cigarette and a questionnaire that measures the strength of your addiction.
    """)
    set_timer(update, _)
    update.message.reply_text(
        """Among other things, we can talk about any topic during the day. 
    You can ask me questions about smoking, nicotine and any other topic. 
    Sometimes I will give strange answers, ignore it. 
    If something bothers you, you just have to write!""")


def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


GENDER, PHOTO, LOCATION, BIO = range(4)


def karl_fagerstrom_daily_test2(context: CallbackContext) -> int:
    list_of_cities = [
        'within the first 5 minutes',
        'from 6 to 30 minutes',
        'from 31 to 60 minutes',
        'more than an hour',
    ]
    job = context.job
    text = "Hello, let's start a daily test developed by a Swedish physician Karl Fagerstrom. " \
           "This test is designed to help you see how severe your nicotine addiction is. \n \n " \
           "Try to answer the test questions as honestly as possible and analyze the result. " \
           "At the end of testing, the system will automatically calculate the result and draw a conclusion. \n \n" \
           "Anyone can quit smoking, if you just want to strongly and not give yourself indulgences. Let's try..."
    context.bot.send_message(job.context, text=text)
    context.bot.send_message(job.context,
                             text="https://image.shutterstock.com/image-photo/test-nicotine-dependence-ecigarette-on-260nw-1311558770.jpg")
    text = '(1) How long after waking up in the morning do you light your first cigarette?'
    reply_markup = ReplyKeyboardMarkup(
        build_menu(list_of_cities, n_cols=1), one_time_keyboard=True)
    context.bot.send_message(job.context,
                             text=text,
                             reply_markup=reply_markup,
                             )

    return GENDER


def karl_fagerstrom_daily_test3(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        text="Okay...",
        reply_markup=ReplyKeyboardRemove(),
    )
    list_of_cities = ['yes', 'no']
    reply_markup = ReplyKeyboardMarkup(
        build_menu(list_of_cities, n_cols=1), one_time_keyboard=True)
    text = '(2) Do you find it difficult to abstain from smoking in non-smoking areas?'

    user = update.message.from_user
    logger.info("Gender of I will notice it%s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        text=text,
        reply_markup=reply_markup,
    )

    return GENDER


def karl_fagerstrom_daily_test4(update: Update, context: CallbackContext) -> int:
    # questions = ["from the first", "from another"]
    # message = context.bot.send_poll(
    #     job.context,
    #     "",
    #     questions,
    #     is_anonymous=False,
    # )
    #

    list_of_cities = ["from the first", "from another"]
    update.message.reply_text(
        text="Good...",
        reply_markup=ReplyKeyboardRemove(),
    )
    reply_markup = ReplyKeyboardMarkup(
        build_menu(list_of_cities, n_cols=1), one_time_keyboard=True)
    text = '(3) What cigarette is the most difficult for you to give up during the day?'
    user = update.message.from_user
    logger.info("Gender of I will notice it%s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        text=text,
        reply_markup=reply_markup,
    )

    return GENDER


def karl_fagerstrom_daily_test5(update: Update, context: CallbackContext) -> int:
    # questions = ["yes", "no"]
    # message = context.bot.send_poll(
    #     job.context,
    #     "Do you continue to smoke when you are very sick and have to stay in bed all day?",
    #     questions,
    #     is_anonymous=False,
    # )
    list_of_cities = ['Of course', 'Absolutely no']
    update.message.reply_text(
        text="Next one...",
        reply_markup=ReplyKeyboardRemove(),
    )
    text = '(4) Do you continue to smoke when you are very sick and have to stay in bed all day?'
    reply_markup = ReplyKeyboardMarkup(
        build_menu(list_of_cities, n_cols=1), one_time_keyboard=True)
    user = update.message.from_user
    logger.info("Gender of I will notice it%s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        text=text,
        reply_markup=reply_markup,
    )
    return GENDER


def karl_fagerstrom_daily_test6(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        text="Well, well, well... thank you for the answers. Don't forget for tomorrow test. See you late!",
        reply_markup=ReplyKeyboardRemove(),
    )
    return GENDER


def remove_job_if_exists(name: str, context: CallbackContext) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


global_update = None


def send_question(context: CallbackContext) -> None:
    job = context.job
    context.bot.send_message(job.context, text=question("Ask me about my personal progress and how I deal with my nicotine addiction."))
    return None


def send_video(context: CallbackContext) -> None:
    youtube_knowledge_base = [
        'https://www.youtube.com/watch?v=o3I0mJ2RfU0&ab_channel=AsapSCIENCE',
        'https://www.youtube.com/watch?v=vUx-b89laPU&ab_channel=WatchMojo.com',
        'https://www.youtube.com/watch?v=HD__r66sFjk&ab_channel=ChrisNotap',
        'https://www.youtube.com/watch?v=5zWB4dLYChM&ab_channel=CentersforDiseaseControlandPrevention%28CDC%29',
        'https://www.youtube.com/watch?v=lW6hwmdZbmE&ab_channel=iheed',
        'https://www.youtube.com/watch?v=sVrb3B5m99M&ab_channel=HuntsmanCancerInstitute',
        'https://www.youtube.com/watch?v=w5c6yvZEQ7M&ab_channel=BaylorScott%26WhiteHealth'
    ]
    job = context.job
    context.bot.send_message(job.context, text=random.choice(youtube_knowledge_base))
    return None


def send_info(context: CallbackContext) -> None:
    tips_to_quit_smoking = [
        "🦷 Take the paste and toothbrush in your hand and brush your teeth. Slowly and thoroughly ...",
        "🚰 Drink water, juice or lemonade. Drink the whole glass slowly and concentrate on each sip.",
        "👄 Get rid of the taste in your mouth quickly. Take a menthol gum or candy and let it gradually release. Focus your attention on the taste you are currently feeling.",
        "☕ How about going to make tea? Mint, lemon balm or chamomile also have calming effects and improve digestion.",
        "😮 Take a deep breath ten times in a row. Close your eyes, inhale through your nose and exhale slowly through your mouth.",
        "🍓 Have something small to eat. Take a break, prepare your favorite food and really enjoy it.",
        "🏃🏿 Pump up your body. Run up the stairs three times, do 5 squats or push-ups and exhale. Then you can continue with a clear head.",
        "🎶 Play your favorite song that will kick you. Immerse yourself fully in the catchy melody.",
        "📲 Do you enjoy playing on your mobile phone? Open your favorite game and overcome the smoking break with a mobile phone in your hand.",
        "🎎 What are your friends doing? Open Messenger and send a greeting to someone you love. You will get rid of the thought of a cigarette and make your loved ones happy.",
        "🤳 Are you interested in cars, technology, fashion or cooking? Browse photos of your favorite topic on Instagram.",
        "🧖 Sit in a quiet room. Take a breath, close your eyes and move your thoughts to your favorite place. It can be a forest, a beach or a family picnic. Concentrate on the sounds, smells and other stimuli of the environment in which you feel good.",
        "🚭 What are your reasons for quitting? Repeat aloud why you want to quit smoking - one reason after another… Your reasons are stronger than the craving for cigarettes!",
        "🥤 Do you miss the cigarette coating? Prepare a glass of your favorite non-alcoholic drink and drink it with a straw. It will confiscate your mouth and the craving for cigarettes will quickly disappear.",
        "🔫 Use nicotine spray or nicotine gum. Leave the released nicotine in the mouth or spit it out. After swallowing, it would irritate the stomach.",
        "🤏 Restless hands are great for a puzzle, anti-stress ball or plasticine. What will you choose from that?",
        "🚪 Quickly change the activity you are doing. Leave the room for a while, open the window and water the flowers, stretch. Your brain needs to be entertained by another activity.",
        "🥺 Mouthwash not only protects the teeth, but also literally kills the craving of the cigarette. Rinse your mouth thoroughly. Try to last at least 20 seconds.",
        "🍌 Let me guess which fruit you like best - is it a banana? Or an apple? Run to the store, buy at least 3 pieces of fruit and enjoy them.",
        "👶 Do you remember the bubble blower from your childhood? Now it will come in handy again. Try to make the biggest bubble possible. You have 10 attempts.",
        "🎈 The inflatable balloon can be used in other ways than at a birthday party. Try to inflate it as quickly as possible. You will practice your lung capacity and you won't even remember smoking.",
        "📰 Open today's newspaper or news website and read what's new. Politics, sports, celebrities ... Anything that interests you. Can you handle at least one whole article?",
        "🧘 Yoga will help you reduce stress and drive away thoughts of smoking. In addition, it can be practiced both at home and in the office and outdoors. Let's face it - what about the position of a lotus flower?",
        "🎒 Do you remember the obligatory recitations in primary school? Deliberately, if you still remember a poem. Look in your memory and try to recite at least three verses.",
        "🎸 Is there music playing nearby? Start dancing as if no one has seen you. Don't be afraid to start it properly.",
        "📚 The smoking break lasts about 7 minutes. During that time, you can read a piece of a chapter of your favorite book. The perfect time to immerse yourself in the action!",
        "📼 Do you like funny videos on YouTube? What are we going to talk about - I like to watch them sometimes. Try to look at some. You will have fun and then the taste for cigarettes will not be so strong.",
        "😎 Do you have someone close to you? Embrace him properly, at least 20 seconds. You will see that you will feel better. Happiness hormones will be flushed out in your brain.",
        "🧠 How about tormenting the brain threads and trying to solve a crossword puzzle or sudoku?",
        "✍️Grab crayons or felt-tip pens and get to work. Try anti-stress coloring books or awaken your own talent and imagination. Simply draw what comes to mind.",
        "📋 We usually have a lot of things on the desk and sometimes a nice mess. Now is the right time to clean the desk. You will entertain your mind and you will work better.",
        "🌲 Go to the park or the forest for a while. Close your eyes and listen to everything that is happening around you - the birdsong, the rustling of leaves, the bubbling stream or the gurgling water in the fountain. Isn't that beautiful?",
        "🚿 Take a quick cold shower. I bet you won't even think about smoking.",
        "🛒 Is your fridge empty? Make a shopping list so you know what to buy. You won't starve!",
        "👚 Are you getting dirty clothes in your laundry basket? Put it in the washing machine with it!",
        "🧫 Is your sink filled with dirty dishes? Put it in the dishwasher or wash it. It will help you to detach yourself from the thought of a cigarette."
    ]
    job = context.job
    context.bot.send_message(job.context, text=random.choice(tips_to_quit_smoking))
    return None


def set_timer(update: Update, context: CallbackContext) -> None:
    """Add a job to the queue."""
    chat_id = update.message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds
        # due = int(context.args[0]) if context.args[0] else 86400

        # if due < 0:
        #     update.message.reply_text('Sorry we can not go back to future!')
        #     return
        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_repeating(karl_fagerstrom_daily_test2, 86400, context=chat_id, name=str(chat_id))
        context.job_queue.run_repeating(send_video, 28800, context=chat_id, name=str(chat_id))
        context.job_queue.run_repeating(send_info, 10000, context=chat_id, name=str(chat_id))
        context.job_queue.run_repeating(send_question, 7200, context=chat_id, name=str(chat_id))

        text = 'Timer successfully set!'
        if job_removed:
            text += ' Old one was removed.'
        update.message.reply_text(text)

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /set <seconds>')


def unset(update: Update, context: CallbackContext) -> None:
    """Remove the job if the user changed their mind."""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Timer successfully cancelled!' if job_removed else 'You have no active timer.'
    update.message.reply_text(text)


def cron_job(update: Update, _: CallbackContext) -> None:
    schedule.every(5).seconds.do(update.message.reply_text, "update")
    schedule.run_pending()
    # schedule.every(60).seconds.do(send_healthy_news, update)


def cron_job2(update: Update, _: CallbackContext) -> None:
    schedule.every(5).seconds.do(update.message.reply_text, "update2")
    schedule.run_pending()


def send_test(update):
    print("cronjob_send")
    update.message.reply_text('test!')


def send_healthy_news(update):
    print("cronjob_news")
    update.message.reply_text('news!')


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def gender(update: Update, _: CallbackContext) -> int:
    print(update.message.text)
    user = update.message.from_user
    logger.info("Patient %s smoke first %s", user.first_name, update.message.text)
    update.message.reply_text(
        'I see! Please send me a photo of yourself, '
        'so I know what you look like, or send /skip if you don\'t want to.',
        reply_markup=ReplyKeyboardRemove(),
    )

    return 1


def echo(update: Update, _: CallbackContext) -> None:
    """Echo the user message."""
    text = update.message.text
    # update.message.reply_text(update.message.text)
    if "kill myself" in text or "want to die" in text or "wanna die" in text:
        update.message.reply_text(personality.assistent_personality.suicidal_warning)
    elif ("want" in text or "wanna" in text) and "smoke" in text:
        update.message.reply_text(random.choice(personality.assistent_personality.tips_to_quit_smoking))
    elif "video" in text or "youtube" in text:
        update.message.reply_text(random.choice(personality.assistent_personality.youtube_knowledge_base))
    elif bool(random.getrandbits(1)) or bool(random.getrandbits(1)) or "?" in update.message.text:
        audio_path = text_to_audio(" ".join(filter(lambda x: x[0] != '/', answer(update.message.text).split())))
        with open(audio_path, 'rb') as f:
            update.message.reply_voice(f, reply_to_message_id=update.message.message_id)
        # this is not safe, but...
        remove(audio_path)
    elif bool(random.getrandbits(1)) and bool(random.getrandbits(1)):
        # update.message.reply_text(answer(update.message.text))
        # update.message.reply_text(question(update.message.text))
        audio_path = text_to_audio(" ".join(filter(lambda x: x[0] != '/', answer(update.message.text).split())))
        with open(audio_path, 'rb') as f:
            update.message.reply_voice(f, reply_to_message_id=update.message.message_id)
        # this is not safe, but...
        remove(audio_path)
        update.message.reply_text(question(update.message.text))
    else:
        update.message.reply_text(question(update.message.text))


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    TOKEN = "1867248939:AAExbP5eFDDDnC31IUNSfvriF_vpbFaTN5w"
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    # dispatcher.add_handler(CommandHandler("wannasmoke", start))
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", start))
    dispatcher.add_handler(CommandHandler("set", set_timer))
    dispatcher.add_handler(CommandHandler("unset", unset))
    # dispatcher.add_handler(CommandHandler("cron", cron_job))
    # dispatcher.add_handler(CommandHandler("cron2", cron_job2))
    dispatcher.add_handler(MessageHandler(
        Filters.regex('^(within the first 5 minutes|from 6 to 30 minutes|from 31 to 60 minutes|more than an hour)$'),
        karl_fagerstrom_daily_test3))
    dispatcher.add_handler(MessageHandler(
        Filters.regex('^(yes|no)$'),
        karl_fagerstrom_daily_test4))
    dispatcher.add_handler(MessageHandler(
        Filters.regex('^(from the first|from another)$'),
        karl_fagerstrom_daily_test5))
    dispatcher.add_handler(MessageHandler(
        Filters.regex('^(Of course|Absolutely no)$'),
        karl_fagerstrom_daily_test6))

    # Buttons handler
    # dispatcher.add_handler(CallbackQueryHandler("within the first 5 minutes", print))
    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO

    # on non command i.e message - echo the message on Telegram
    # dispatcher.add_handler(MessageHandler(Filters.all, print))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


def question(text):
    data = '{"prompt": ' + personality.assistent_personality.question_template + text + \
           ' Question:' + '", "max_tokens": 24}'
    response = requests.post('https://api.openai.com/v1/engines/davinci/completions', headers=headers,
                             data=data)
    response_data = response.json()
    response_string = response_data['choices'][0]['text']
    delimiters = "Answer:", "Question:"
    regex_pattern = '|'.join(map(re.escape, delimiters))
    split_response = re.split(regex_pattern, response_string)[0]
    questionary_index = split_response.rfind('?')
    if questionary_index != -1:
        sub_response_string = split_response[0:questionary_index]
        # dispatcher.utter_message(text=f"{sub_response_string}?")
        return sub_response_string + "?"
    else:
        # dispatcher.utter_message(text=f"{split_response}")
        return split_response


def answer(text):
    data = '{"prompt": ' + personality.assistent_personality.initial_template + \
           'Me:' + text + ' Psychologist:"' + ', "max_tokens": 64}'
    response = requests.post('https://api.openai.com/v1/engines/davinci/completions', headers=headers,
                             data=data)
    response_data = response.json()
    response_string = response_data['choices'][0]['text']
    delimiters = "Me:", "Psychologist:"
    regex_pattern = '|'.join(map(re.escape, delimiters))
    split_response = re.split(regex_pattern, response_string)[0]
    dot_index = split_response.rfind('.')
    if dot_index != -1:
        sub_response_string = split_response[0:dot_index]
        if utils.censorship.Censorship().is_output_safe(sub_response_string):
            # dispatcher.utter_message(text=f"{sub_response_string}.")
            return sub_response_string + "."
        else:
            # dispatcher.utter_message(text="Censorship module was affected!")
            return "Censorship module was affected!"
    else:
        # dispatcher.utter_message(text=f"{split_response}")
        return split_response


if __name__ == '__main__':
    main()
