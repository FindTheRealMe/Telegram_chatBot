#!/usr/bin/python
# -*- coding: utf-8 -*-
from database.redis import RedisClient
import json
import base64
import settings
import telepot
import time
from database.mongo import MongoMgr
from robots.TokenBucket import TokenBucket
from flask import Flask
import logging

bot = telepot.Bot(settings.token)
mongoconnect = MongoMgr.get_mongo()
redis = RedisClient.get_redis()

COLLECTION_USER = mongoconnect['tel_user']
COLLECTION_INVITER = mongoconnect['tel_inviter']
COLLECTION_GROUP = mongoconnect['tel_group']
# redis前缀
userId = "user_id"
updateId = "update_id"
AdressPrefix = "address"
GroupPrefix = "group"

tokenBucket = TokenBucket(3000,1500)

app = Flask(__name__)

gunicorn_error_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.INFO)

# 方法定义区

def removeGroup(chat_id):
    COLLECTION_GROUP.delete_one({'_id': chat_id})
    redis.delete(GroupPrefix + str(chat_id))

def saveGroup(groupInfoList):
    try:
         COLLECTION_GROUP.insert_many(groupInfoList)
    except:
        for item in groupInfoList:
            COLLECTION_GROUP.save(item)

def getGroup(chat_id):
    groupInfo = redis.get(GroupPrefix + str(chat_id))
    if groupInfo:
        return json.loads(groupInfo)
    result = COLLECTION_GROUP.find({'USER_ID': chat_id})
    rs = []
    for item in result:
        rs.append(item)
    group = rs[0] if len(rs) > 0 else {}
    if group:
        groupInfo = json.dumps(group)
        redis.set(GroupPrefix + str(chat_id), groupInfo,ex=21600)
        return group
    else:
        return None

def saveUser(chat_id,adress ,user_name,inviter,coin):
    ctime = int(time.time() * 1000)
    result = COLLECTION_USER.insert_one({
        '_id':chat_id,
        'USER_ID': chat_id,
        'ADRESS': adress,
        'USER_NAME': user_name,
        'INVITER': inviter,
        'COIN': coin,
        'INVITER_NUMBER': 0,
        'CTIME': ctime
    })
    redis.delete(userId + str(chat_id))
    return result

def getUser(chat_id):
    userInfo = redis.get(userId + str(chat_id))
    if userInfo:
        return json.loads(userInfo)
    result = COLLECTION_USER.find({'_id':chat_id})
    rs = []
    for item in result:
        rs.append(item)
    user = rs[0] if len(rs) > 0 else {}
    if user:
        userInfo = json.dumps(user)
        redis.set(userId + str(chat_id),userInfo,ex=21600)
        return user
    else:
        return None

def checkAdress(adress):
    result = COLLECTION_USER.find({'ADRESS': adress}).limit(1)
    rs = []
    for item in result:
        rs.append(item)
    return rs[0] if len(rs) > 0 else {}


def updateAdress(chat_id, adress):
    token = checkAdress(adress)
    if token:
        bot.sendMessage(chat_id, settings.repeatHint)
    else:
        result =COLLECTION_USER.update_one({'_id': chat_id}, {'$set': {'ADRESS': adress}})
        num = result.matched_count
        if num == 1:
            redis.delete(userId + str(chat_id))
            redis.set(updateId + str(chat_id),1,ex=86400)
            bot.sendMessage(chat_id, settings.bindingHint.format(adress))
        else:
            app.logger.info('没有找到对应的记录')


def updateInvitorNumber(chat_id):
    inviterNumber = 0
    users = COLLECTION_USER.find({'_id': chat_id})
    if users:
        for item in users:
             inviterNumber = item["INVITER_NUMBER"]
             break
        increaseInveterNum=1+inviterNumber
        whiteList = settings.whiteList
        is_whiltUser = whiteList.split(",").__contains__(str(chat_id))
        if is_whiltUser:
            if increaseInveterNum > 2:
                coin = 10 + 30 * increaseInveterNum
                if coin < 90000:
                    COLLECTION_USER.update_one({'_id': chat_id}, {'$set': {'INVITER_NUMBER': increaseInveterNum,"COIN":coin}})
                    sendMessage(chat_id, settings.sendYeeHintBig3.format(coin,increaseInveterNum))
                    redis.delete(userId + str(chat_id))
                else:
                    COLLECTION_USER.update_one({'_id': chat_id},{'$set': {'INVITER_NUMBER': increaseInveterNum, "COIN": 90000}})
                    redis.delete(userId + str(chat_id))
                    logging.info("用户获得YEE大于3000不发送提示")
            else:
                COLLECTION_USER.update_one({'_id': chat_id}, {'$set': {'INVITER_NUMBER': increaseInveterNum, "COIN": 10}})
                sendMessage(chat_id, settings.sendYeeHintSmall3.format(increaseInveterNum,3-increaseInveterNum))
                redis.delete(userId + str(chat_id))
        else:
            if increaseInveterNum > 2:
                coin = 10 + 30 * increaseInveterNum
                if coin < 3000:
                    COLLECTION_USER.update_one({'_id': chat_id},{'$set': {'INVITER_NUMBER': increaseInveterNum, "COIN": coin}})
                    sendMessage(chat_id, settings.sendYeeHintBig3.format(coin, increaseInveterNum))
                    redis.delete(userId + str(chat_id))
                else:
                    logging.info("用户获得YEE大于3000不发送提示")
            else:
                COLLECTION_USER.update_one({'_id': chat_id},
                                           {'$set': {'INVITER_NUMBER': increaseInveterNum, "COIN": 10}})
                sendMessage(chat_id, settings.sendYeeHintSmall3.format(increaseInveterNum, 3 - increaseInveterNum))
                redis.delete(userId + str(chat_id))


def getInvitor(token):
    result = COLLECTION_INVITER.find({'TOKEN': token})
    rs = []
    for item in result:
        rs.append(item)
    return rs[0] if len(rs) > 0 else {}


def checkToken(token):
    length = len(token)
    if length == 42:
        return True
    else:
        return False


def handle(chat_id,content_type,msg):
    app.logger.info('received msg:chatId:%s,%s',chat_id,msg)
    tokens = tokenBucket.get_tokens()
    if content_type == 'text':
        if tokens>0:
            tokenBucket.consume(1)
            chatId = int(chat_id)
            flag = False
            if chatId > 0:
                flag = handlerOperationRquest(chat_id, msg=msg)
            if not flag:
                handlerOperationMsg(chat_id, msg=msg)
        else:
            sendMessage(chat_id,settings.busyHint)
    elif content_type == 'new_chat_member':
        tokenBucket.consume(1)
        if str(chat_id) == settings.groupId:
            groupInfoList = []
            ctime = int(time.time() * 1000)
            try:
                for item in msg['new_chat_members']:
                    id = str(item['id'])
                    groupInfo = {}
                    groupInfo['_id'] = id
                    groupInfo['USER_ID'] = id
                    if 'first_name' in item.keys():
                         groupInfo['FIRST_NAME'] = item['first_name']
                    if 'last_name' in item.keys():
                         groupInfo['LAST_NAME'] = item['last_name']
                    if 'is_bot' in item.keys():
                         groupInfo['IS_BOT'] = item['is_bot']
                    groupInfo['GROUP_ID'] = chat_id
                    groupInfo['CTIME'] = ctime
                    groupInfoList.append(groupInfo)
            except Exception as e:
                app.logger.error('解析群成员信息出错:%s',e)
            saveGroup(groupInfoList)
            flag = redis.get("new_chat_member_msg_event")
            if flag:
                app.logger.info("触发了进群事件，但是上次发送消息不到1分钟，这次不发送欢迎消息")
            else:
                sendMessage(chat_id, settings.welcomeHint)
                app.logger.info("发送欢迎消息成功!")
                redis.set("new_chat_member_msg_event", 1, ex=40)
        else:
            app.logger.info('在非指定群进行了邀请事件')
    elif content_type == 'left_chat_member':
        tokenBucket.consume(1)
        removeGroup(chat_id)
    else:
        app.logger.info('不关注的操作')



def handlerOperationRquest(chat_id,msg):
    matched=True;
    if msg['text'] == '/help':
        redis.delete(AdressPrefix + str(chat_id))
        sendMessage(chat_id, settings.helpHint)
    elif msg['text'] == '/set_address':
        user = getUser(chat_id)
        if user == None:
            bot.sendMessage(chat_id, settings.setAdressHint)
            redis.set(AdressPrefix + str(chat_id), '1',ex=300)
        else:
            adress = user.get("ADRESS")
            sendMessage(chat_id, settings.bindingHint.format(adress))
    elif msg['text'] == '/update_address':
        user = getUser(chat_id)
        if user:
            sendMessage(chat_id, settings.updateAdressHint)
            redis.set(AdressPrefix + str(chat_id), '2',ex=300)
        else:
            sendMessage(chat_id, settings.pleaseBind)
            redis.delete(AdressPrefix + str(chat_id))
    elif msg['text'] == '/my_address':
        redis.delete(AdressPrefix + str(chat_id))
        user = getUser(chat_id)
        if user:
            adress = user.get("ADRESS")
            sendMessage(chat_id, settings.bindingHint.format(adress))
        else:
            sendMessage(chat_id, settings.pleaseBind)
    elif msg['text'] == '/my_token':
        redis.delete(AdressPrefix + str(chat_id))
        # redis.delete(userId + str(chat_id))
        user = getUser(chat_id)
        if user:
            coin = user.get("COIN")
            invitorNumber = user.get("INVITER_NUMBER")
            whiteList = settings.whiteList
            is_whiltUser = whiteList.split(",").__contains__(str(chat_id))
            if is_whiltUser:
                if invitorNumber < 3:
                    sendMessage(chat_id, settings.showCoinHintSmall3.format(invitorNumber, 3 - invitorNumber))
                elif invitorNumber >= 3 and invitorNumber < 3000:
                    sendMessage(chat_id, settings.showCoinHintBig3.format(coin, invitorNumber))
                else:
                    sendMessage(chat_id, settings.showCoinHintbig90000)
            else:
                if invitorNumber<3:
                    sendMessage(chat_id, settings.showCoinHintSmall3.format(invitorNumber,3-invitorNumber))
                elif invitorNumber>=3 and invitorNumber <100:
                    sendMessage(chat_id, settings.showCoinHintBig3.format(coin,invitorNumber))
                else:
                    sendMessage(chat_id, settings.showCoinHintbig3000)
        else:
            sendMessage(chat_id, settings.pleaseBind)
    elif msg['text'] == '/my_referral_link':
        redis.delete(AdressPrefix + str(chat_id))
        user = getUser(chat_id)
        if user:
            idEncodeStr = str(chat_id)
            idBase64 = base64.b64encode(bytes(idEncodeStr, encoding = "utf8"))
            sendMessage(chat_id, settings.copyConnect)
            connect = settings.activity_url.format(idBase64.decode('utf-8'))
            sendMessage(chat_id, settings.ConnectUrl.format(connect))
        else:
            sendMessage(chat_id, settings.pleaseBind)
    else:
        matched=False
    return matched

def handlerOperationMsg(chat_id,msg):
    group_flag = redis.get(AdressPrefix + str(chat_id))
    group = getGroup(chat_id)
    if group_flag and int(group_flag) == 1 and group:
        result = checkToken(msg['text'])
        if result:
            Invitor = getInvitor(msg['text']);
            if Invitor:
                try:
                    saveUser(chat_id, msg['text'], msg.get('from').get('username'), Invitor.get("INVITER"), 10)
                    # 给邀请人的邀请数＋1,重新核算邀请人YEE币
                    updateInvitorNumber(Invitor.get("INVITER"))
                    sendMessage(chat_id, settings.bindingHint.format(msg['text']))
                    # 删除缓存
                    redis.delete(AdressPrefix + str(chat_id))
                    app.logger.info("user :{} 设置设置钱包成功，邀请人：{}".format(chat_id,Invitor))
                    # 打印日志
                    saveInfo = {}
                    saveInfo['USER_ID'] = chat_id
                    saveInfo['TOKEN'] = msg['text']
                    saveInfo['USER_NAME'] = msg.get('from').get('username')
                    saveInfo['INVITER'] = Invitor.get("INVITER")
                    app.logger.info(saveInfo)
                except:
                    sendMessage(chat_id, settings.errorHint)
            else:
                saveUser(chat_id, msg['text'], msg.get('from').get('username'), 0, 10)
                sendMessage(chat_id, settings.bindingHint.format(msg['text']))
                redis.delete(AdressPrefix + str(chat_id))
                app.logger.info("user :{} 设置设置钱包成功.".format(chat_id))
                # 打印日志
                saveInfo = {}
                saveInfo['USER_ID'] = chat_id
                saveInfo['TOKEN'] = msg['text']
                saveInfo['USER_NAME'] = msg.get('from').get('username')
                app.logger.info(saveInfo)
        else:
            sendMessage(chat_id, settings.errorHint)
    elif group_flag and int(group_flag) == 2 and group:
        update = redis.get(updateId + str(chat_id))
        if update:
            sendMessage(chat_id, settings.overupdatelimit)
        else:
            result = checkToken(msg['text'])
            if result:
                updateAdress(chat_id, msg['text'])
                redis.delete(AdressPrefix + str(chat_id))
                #打印日志
                updateInfo = {}
                updateInfo['USER_ID'] = chat_id
                updateInfo['TOKEN'] = msg['text']
                app.logger.info(updateInfo)
            else:
                sendMessage(chat_id, settings.errorHint)
    else:
        if group:
            sendMessage(chat_id, settings.helpHint)
        else:
            if str(chat_id) == settings.groupId:
                sendMessage(chat_id, settings.welcomeHint)
            else:
                sendMessage(chat_id, settings.groupInviteHint)

def sendMessage(chat_id,msg):
    try:
        bot.sendMessage(chat_id, msg)
    except Exception as e:
        logging.error('send message error:%s',e)

def main():
    print(bot.getChatMember(-259029693, 513659816));


if __name__ == '__main__':
    main()