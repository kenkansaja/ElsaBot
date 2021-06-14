import re
import sre_constants

import telegram
from telegram import Update, Bot
from telegram.ext import run_async

from DaisyX import sample_config, LOGGER
from DaisyX.modules.disable import DisableAbleRegexHandler

DELIMITERS = ("/", ":", "|", "_")


def separate_sed(sed_string):
    if len(sed_string) >= 3 and sed_string[1] in DELIMITERS and sed_string.count(sed_string[1]) >= 2:
        delim = sed_string[1]
        start = counter = 2
        while counter < len(sed_string):
            if sed_string[counter] == "\\":
                counter += 1

            elif sed_string[counter] == delim:
                replace = sed_string[start:counter]
                counter += 1
                start = counter
                break

            counter += 1

        else:
            return None

        while counter < len(sed_string):
            if sed_string[counter] == "\\" and counter + 1 < len(sed_string) and sed_string[counter + 1] == delim:
                sed_string = sed_string[:counter] + sed_string[counter + 1:]

            elif sed_string[counter] == delim:
                replace_with = sed_string[start:counter]
                counter += 1
                break

            counter += 1
        else:
            return replace, sed_string[start:], ""

        flags = ""
        if counter < len(sed_string):
            flags = sed_string[counter:]
        return replace, replace_with, flags.lower()


@run_async
def sed(bot: Bot, update: Update):
    sed_result = separate_sed(update.effective_message.text)
    if sed_result and update.effective_message.reply_to_message:
        if update.effective_message.reply_to_message.text:
            to_fix = update.effective_message.reply_to_message.text
        elif update.effective_message.reply_to_message.caption:
            to_fix = update.effective_message.reply_to_message.caption
        else:
            return

        repl, repl_with, flags = sed_result

        if not repl:
            update.effective_message.reply_to_message.reply_text("You're trying to replace... "
                                                                 "nothing with something?")
            return

        try:
            check = re.match(repl, to_fix, flags=re.IGNORECASE)

            if check and check.group(0).lower() == to_fix.lower():
                update.effective_message.reply_to_message.reply_text("Hey everyone, {} is trying to make "
                                                                     "me say stuff I don't wanna "
                                                                     "say!".format(update.effective_user.first_name))
                return

            if 'i' in flags and 'g' in flags:
                text = re.sub(repl, repl_with, to_fix, flags=re.I).strip()
            elif 'i' in flags:
                text = re.sub(repl, repl_with, to_fix, count=1, flags=re.I).strip()
            elif 'g' in flags:
                text = re.sub(repl, repl_with, to_fix).strip()
            else:
                text = re.sub(repl, repl_with, to_fix, count=1).strip()
        except sre_constants.error:
            LOGGER.warning(update.effective_message.text)
            LOGGER.exception("SRE constant error")
            update.effective_message.reply_text("Do you even sed? Apparently not.")
            return

        # empty string errors -_-
        if len(text) >= telegram.MAX_MESSAGE_LENGTH:
            update.effective_message.reply_text("The result of the sed command was too long for \
                                                 telegram!")
        elif text:
            update.effective_message.reply_to_message.reply_text(text)


__help__ = """
-s/<text1>/<text2>(/<flag>): Membalas pesan dengan ini untuk melakukan operasi sed pada pesan itu, mengganti semua\
kemunculan 'text1' dengan 'text2'. Bendera bersifat opsional, dan saat ini menyertakan 'i' untuk huruf abaikan, 'g' untuk global,\
atau tidak sama sekali. Pembatas termasuk `/`, `_`, `|`, dan `:`. Pengelompokan teks didukung. Pesan yang dihasilkan tidak dapat\
lebih besar dari {}.
*Pengingat:* Sed menggunakan beberapa karakter khusus untuk mempermudah pencocokan, seperti ini: `+*.? \\ `
Jika Anda ingin menggunakan karakter ini, pastikan Anda menghindarinya!
misalnya:\\?.
""".format(telegram.MAX_MESSAGE_LENGTH)

__mod_name__ = "😊SED/REGEX"


SED_HANDLER = DisableAbleRegexHandler(r's([{}]).*?\1.*'.format("".join(DELIMITERS)), sed, friendly="sed")

dispatcher.add_handler(SED_HANDLER)
