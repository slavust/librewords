#!/usr/bin/python3


from telegram import Update, MessageEntity, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ConversationHandler, MessageHandler, ContextTypes, CallbackContext, CallbackQueryHandler, filters

import video_to_cloud
import speech_to_cloud
import text_to_cloud
import document_to_cloud
import url_to_cloud
import language_codes

import tempfile
import os.path

SUPPORT_TEXT = True
SUPPORT_URLS = True
SUPPORT_DOCUMENTS = True
SUPPORT_AUDIO = False
SUPPORT_VIDEO = False

EXPECT_LANGUAGE_SELECT = 0

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    update.effective_message.message.reply_text(
        'Hello! Try to post some message text or url in chat so I\'ll try to find out most frequent words in it.'
    )


async def make_reply_to_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    full_text = message.text
    if full_text is None:
        full_text = ''
    if SUPPORT_URLS:
        hyperlinks = []
        urls = message.parse_entities([MessageEntity.URL])
        if urls:
            hyperlinks = [url for url in urls.values()]
        text_links = message.parse_entities([MessageEntity.TEXT_LINK])
        for text_link in text_links.keys():
            hyperlinks.append(text_link.url)
        
        for url in hyperlinks:
            text = url_to_cloud.get_text_from_url(url)
            if not text:
                continue
            full_text += '\n.\n' + text
    if SUPPORT_DOCUMENTS and message.document:
        doc = message.document
        fname = doc.file_name
        ext = os.path.splitext(fname)
        if ext in ['.doc', '.docx','.ppt', '.odt', '.odp', '.pdf', '.rtf', '.txt']:
            file = doc.get_file()
            with tempfile.TemporaryDirectory() as dir:
                fpath = os.path.join(dir, fname)
                file.download(custom_path=fpath)
                lang = get_user_prefferred_language(context)
                text = document_to_cloud.get_text_from_document(fpath)
                if text:
                    full_text += '\n.\n' + text

    if not full_text:
        await message.reply_text('Unable to recognize text', reply_to_message_id=message.message_id)
        return

    with tempfile.TemporaryDirectory() as dir:
        imgpath = os.path.join(dir, 'librewords.jpg')
        text_to_cloud.render_cloud_from_text(full_text, imgpath, False)
        with open(imgpath, 'rb') as img:
            await message.reply_photo(img, reply_to_message_id=message.message_id)


if __name__ == '__main__':
    API_TOKEN = os.environ['API_TOKEN']
    application = ApplicationBuilder().token(API_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(
        MessageHandler(
            filters=filters.ALL,
            callback=make_reply_to_message
        )
    )
    application.run_polling()