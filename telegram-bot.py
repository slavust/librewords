#!/usr/bin/python3

from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters

import video_to_cloud
import speech_to_cloud
import text_to_cloud
import document_to_cloud
import url_to_cloud

import tempfile

def get_user_prefferred_language(context):
    # todo
    return 'en'


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Hello! Try to post some message, video or audio in chat so I\'ll try to find out most frequent words in it.'
    )

def incoming_message(update: Update, context: CallbackContext):
    full_text = update.message.text
    if full_text is None:
        full_text = ''
    
    hyperlinks = []
    urls = update.message.parse_entities([telegram.MessageEntity.URL, telegram.MessageEntity.TEXT_LINK])
    if urls:
        hyperlinks = [url.url for url in urls]
    for url in urls:
        text = url_to_cloud.get_text_from_url(url)
        if not text:
            continue
        full_text += '\n.\n' + text

    if update.message.audio:
        audio = update.message.audio
        fname = audio.file_name
        file = audio.get_file()
        with tempfile.TemporaryDirectory() as dir:
            fpath = os.path.join(dir, fname)
            file.download(custom_path=fpath)
            lang = get_user_prefferred_language(context)
            text = speech_to_cloud.get_large_audio_transcription(fpath, lang)
            if text:
                full_text += '\n.\n' + text
    elif update.message.video:
        video = update.message.video
        fname = video.file_name
        file = video.get_file()
        with tempfile.TemporaryDirectory() as dir:
            fpath = os.path.join(dir, fname)
            file.download(custom_path=fpath)
            lang = get_user_prefferred_language(context)
            text = video_to_cloud.get_video_transcription(fpath, lang)
            if text:
                full_text += '\n.\n' + text
    elif update.message.voice:
        voice = update.message.voice
        fname = voice.file_name
        file = voice.get_file()
        with tempfile.TemporaryDirectory() as dir:
            fpath = os.path.join(dir, fname)
            file.download(custom_path=fpath)
            lang = get_user_prefferred_language(context)
            text = speech_to_cloud.get_large_audio_transcription(fpath, lang)
            if text:
                full_text += '\n.\n' + text
    elif update.message.document:
        doc = update.message.document
        fname = document.file_name
        file = document.get_file()
        with tempfile.TemporaryDirectory() as dir:
            fpath = os.path.join(dir, fname)
            file.download(custom_path=fpath)
            lang = get_user_prefferred_language(context)
            text = document_to_cloud.get_text_from_document(fpath, lang)
            if text:
                full_text += '\n.\n' + text

    if not full_text:
        update.message.reply_text('Unable to recognize text')
        return
    with tempfile.TemporaryDirectory() as dir:
        imgpath = os.path.join(dir, 'librewords.jpg')
        text_to_cloud.render_cloud_from_text(text, imgpath, False)
        update.context.reply_photo(imgpath)


if __name__ == '__main__':
    updater = Updater("your_own_API_Token got from BotFather", use_context=True)
    updater.dispathcer.add_handler(CommandHabdler('start', start))
    updater.dispathcer.add_handler(
        MessageHandler(
            telegram.ext.filters.AUDIO 
            | telegram.ext.filters.Document.ALL 
            | telegram.ext.filters.VOICE 
            | telegram.ext.filters.TEXT 
            | telegram.ext.filters.Entity(URL) 
            | telegram.ext.entity(TEXT_LINK)
        )
    )
    updater.start_polling()