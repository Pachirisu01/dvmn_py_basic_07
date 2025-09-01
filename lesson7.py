import ptbot
from dotenv import load_dotenv
import os
from pytimeparse import parse


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)



def notify_progress(secs_left, chat_id, message_id, total_seconds, bot):
    progbar = render_progressbar(total_seconds, total_seconds - secs_left)
    if secs_left >= 0:  
        bot.update_message(
            chat_id,
            message_id,
            f"Осталось: {secs_left} сек\n{progbar}"
        )

    if secs_left == 0:
        bot.send_message(chat_id, "Время вышло")


def try_message(chat_id, text, bot):
    seconds = parse(text)
    message_id = bot.send_message(chat_id,"Осталось: {} сек".format(seconds))
    progbar = render_progressbar
    bot.create_countdown(
        seconds,
        notify_progress,
        bot = bot,
        chat_id = chat_id,
        message_id = message_id,
        total_seconds = seconds
    )


def main():
    load_dotenv()
    bot = ptbot.Bot(os.getenv('tg_token'))
    bot.reply_on_message(try_message, bot=bot)
    bot.run_bot()


if __name__ == '__main__':
    main()