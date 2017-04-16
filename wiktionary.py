from telegram import InlineQueryResultArticle, InputTextMessageContent
from uuid import uuid4
import json
from wiktionaryparser import WiktionaryParser
import ast
from config import creator

parser = WiktionaryParser()


def search(bot, update):
    query = update.inline_query.query
    results = list()

    results.append(InlineQueryResultArticle(id=uuid4(),
                                            title="Definition",
                                            input_message_content=InputTextMessageContent(
                                               wt_handler(query, 'define'),
                                               parse_mode = 'Markdown')))

    results.append(InlineQueryResultArticle(id=uuid4(),
                                            title="Pronounciation",
                                            input_message_content=InputTextMessageContent(
                                               wt_handler(query, 'pronounce'))))
    if update.inline_query.from_user.id == creator:
        results.append(InlineQueryResultArticle(id=uuid4(),
                                                title="full",
                                                input_message_content=InputTextMessageContent(
                                                   wt_handler(query, 'full'))))

    update.inline_query.answer(results)


def wt_handler(query, resp_type):
    args = query.split(' ')
    word = args[0]
    if len(args) == 1:
        lang = 'english'
    else:
        lang = args[1] 

    if resp_type == 'define':
        return wt_define(word, lang)
    elif resp_type == 'pronounce':
        return wt_pronounce(word, lang)
    elif resp_type == 'full':
        return wt_full(word, lang)
    else: 
        return None

def wt_define(word, lang):
    resp = []
    definition = parser.fetch(word, lang)[0]['definitions']
    for part in definition:
        partOfSpeech = part['partOfSpeech']
        text = part['text']

        resp.append('_' + partOfSpeech + '_')
        if len(text) < 140:
            resp.append(text)
            complete = True
        else:
            resp.append(text[0:180] + '...')
            complete = False
    if complete == False:
        link = 'https://en.wiktionary.org/wiki/{}'.format(word)
        resp.append('[Read more on Wiktionary]({})'.format(link))
    resp = '\n'.join(resp)
    return resp
        
    return str([0]['text'])


def wt_pronounce(word, lang):
    resp = []
    wt_result = parser.fetch(word, lang)
    ipa = ('\n'.join(wt_result[0]['pronunciations']))
    resp.append(word)
    audio = '\n'.join(wt_result[0]['audioLinks'])

    resp.append(ipa)
    resp.append(audio)

    return '\n'.join(resp)


def wt_full(word, lang):
    return str(parser.fetch(word, lang))
