#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import logging
import settings
import telepot
from telepot.aio.loop import MessageLoop
import asyncio
from telepot.aio.delegate import pave_event_space, per_chat_id, create_open
from flask import Flask
import requests,random
from database.redis import RedisClient
import concurrent

app = Flask(__name__)
redis=RedisClient.get_redis()
cache_prefix="limit_cache_"
loop = asyncio.get_event_loop()

class MessageHandler(telepot.aio.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(MessageHandler, self).__init__(*args, **kwargs)

    async def on_chat_message(self, msg):
        logging.info("recieved message:%s", msg)
        try:
            content_type, chat_type, chat_id = telepot.glance(msg)
            params = {'content_type': content_type, "chat_type": chat_type, "chat_id": chat_id, "msg": json.dumps(msg)}
            acceptId = int(chat_id)
            if checkTimeLimit(chat_id, acceptId):
                sendMsg(chat_id,chatMsg=params,triedUrl=None)
            else:
                await self.sender.sendMessage(chat_id,settings.overvisit)
        except Exception as e:
            try:
                self.close()
            except Exception as e:
                logging.error('close chathandler expcetion')
            logging.error('recieve chat message error')



bot = telepot.aio.DelegatorBot(settings.token, [
    pave_event_space()(
        per_chat_id(), create_open, MessageHandler, timeout=30),
])



'''def handle(msg):
    try:
        logging.info("recieved message:%s", msg)
        content_type, chat_type, chat_id = telepot.glance(msg)
        logging.info("after glance message")
        params = {'content_type': content_type, "chat_type": chat_type, "chat_id": chat_id, "msg": json.dumps(msg)}
        sendMsg(chat_id, params,None)
    except Exception as e:
        logging.error('handling message error:%s,%s', msg, e)'''


def getChatHanlderServer(triedUrl):
    handlers = list(settings.HANDLER_SERVERS)
    if handlers:
        if triedUrl and handlers.count(triedUrl) > 0:
            leftHanlders=handlers.remove(triedUrl)
            if leftHanlders:
                return random.choice(leftHanlders)
        else:
            return random.choice(handlers)
    return None

def checkTimeLimit(chat_id,acceptId):
    allowed=True
    try:
        if acceptId > 0:
            times = redis.get(cache_prefix + str(chat_id))
            number = 1
            if times:
                number = int(times)
            else:
                redis.set(cache_prefix + str(chat_id), number,ex=60)
            if number > 5:
                allowed = False
            else:
                redis.incr(cache_prefix + str(chat_id))
    except Exception as e:
        logging.error('get limit number error:%s',e)
    return True


def sendMsg(chat_id,chatMsg,triedUrl):
    url=getChatHanlderServer(triedUrl)
    if url:
        try:
            triedUrl = url
            postMsgToServer(url,chatMsg=chatMsg)
        except Exception as e:
            logging.error('send message error,url:%s,%s',url,e)
            try:
                url = getChatHanlderServer(triedUrl)
                postMsgToServer(url, chatMsg=chatMsg)
            except Exception as e:
                logging.error('send message error again,url:%s,%s', url, e)
    else:
        bot.sendMessage(chat_id,'processing!')

def postMsg(url, chatMsg):
    return requests.post(url, data = chatMsg)

async def handle(msg):
    logging.info("recieved message:%s", msg)
    try:
        content_type, chat_type, chat_id = telepot.glance(msg)
        params = {'content_type': content_type, "chat_type": chat_type, "chat_id": chat_id, "msg": json.dumps(msg)}
        acceptId = int(chat_id)
        if checkTimeLimit(chat_id, acceptId):
            sendMsg(chat_id, chatMsg=params, triedUrl=None)
    except Exception as e:
        if e==None:
            logging.error('handling message error:%s','')
        else:
            logging.error('handling message error:%s', e)

def postMsgToServer(url,chatMsg):
    with concurrent.futures.ThreadPoolExecutor(max_workers=300) as executor:
        future_to_url = {executor.submit(postMsg, "http://" + url + "/chat/msg", chatMsg)}
        logging.info("send msg success!,%s,%s", url, chatMsg)
    #res = requests.post("http://" + url + "/chat/msg", data=chatMsg)
    #if res and res.ok:
        #logging.info("send msg success!,%s,%s", url, chatMsg)

def main():
    logging.basicConfig(filename=settings.LOG_FILE,level=settings.LOG_LEVEL,format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S')
    #loop.create_task(MessageLoop(bot).run_forever())
    asyncio.ensure_future(MessageLoop(bot, handle).run_forever(relax=0.01,offset=-1))
    print('Messge Listening ...')
    loop.run_forever()


if __name__ == '__main__':
    main()