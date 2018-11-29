# -*- coding: utf-8 -*-

# Scrapy settings for RichFunVideoSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# LOG
#LOG_FILE = '../logs/serverrobot.log'
LOG_FILE = '/data/home/work/ChatRobot/server/logs/serverrobot.log'
#LOG_FILE = '../logs/clientrobot.log'
LOG_LEVEL = 'DEBUG'


#mysql configuration
DB_HOST='xxxxxxxxxxx'
DB_PORT=3306
DB_NAME='TESTDB'
DB_USER='testuser'
DB_PWD='test123'
DB_CHAR='utf8'

#mongo
mghost="",
mgport=27027,
mguser ="",
mgpassword="",
mgdatabase="",

# urls queue
REDIS_HOST = ''
REDIS_PORT = 6379

#mongod
MONGO_DB = ""
MONGO_HOST = ""
MONGO_PORT = 27027
MONGO_USER = ""
MONGO_PASS = ""
#MONGO_URI = 'mongodb://%s:%s@%s:%s/%s' % (MONGO_USER, MONGO_PASS, MONGO_HOST, MONGO_PORT, MONGO_DB)
MONGO_URI = 'mongodb://xxxxxxxxxxxxx:xxxxxxxxxxxxxxxxxxxxxx@xxxxxxxxxxxx:27027,xxxxxxxxxx:27027/xxxxxxity?readPreference=nearest'
# Specify the full Redis URL for connecting (optional).
# If set, this takes precedence over the REDIS_HOST and REDIS_PORT settings.
# REDIS_URL = 'redis://127.0.0.1:6379'

# Custom redis client parameters (i.e.: socket timeout, etc.)
REDIS_PARAMS = {}
# Use custom redis client class.
REDIS_PARAMS['redis_cls'] = 'ChatRobot.database.redis.RedisClient.RedisClient'

# If True, it uses redis' ``spop`` operation. This could be useful if you
# want to avoid duplicates in your start urls list. In this cases, urls must
# be added via ``sadd`` command or you will get a type error from redis.
REDIS_START_URLS_AS_SET = True

# How many start urls to fetch at once.
REDIS_START_URLS_BATCH_SIZE = 16

HANDLER_SERVERS=['xxxxxxxxxxxx:6990','xxxxxxxxxxxxx:6990']

activity_url = "https://xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxe?u={}"

token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

groupId = 'xxxxxxxxxxxxxx' 
#welcomeHint = 'Welcome join Yee Official Telegram group. Please tap my profile and register your ETH wallet address before share your referral link.'
#helpHint = 'YeeBot is very happy to help you. Instruction: :\n /help - FAQ \n /set_address - Register your ETH wallet address \n /my_address - check your current ETH wallet address\n /update_address -  update your current ETH wallet address\n /my_coin - check my Bitcoin rewards\n /my_connect - Get my referral link'
#setAdressHint = 'Please sent me your ETH wallet address and make sure the address is correct'
#updateAdressHint = 'Please sent me your new ETH wallet address and make sure the address is correct.'
#errorHint = 'The ETH wallet address you sent is not right. Please send me a correct ETH wallet address.'
#repeatHint = 'The ETH wallet address you sent is already register. You can copy your referral link to invite now.'
#bindingHint = "Your ETH wallet address is: \n {} Successfully registered. \n Share referral link to get more Bitcoin for FREE!"
#showCoinHint = "Check how many Bitcoin I earned：{}。Share referral link to get more Bitcoin for FREE!"
#pleaseBind = "Please register your ETH wallet address first"
#copyConnect = "Please copy below and share your friends. Invite more to get more Bitcoin."
#overvisit = "Check too frequently. The maximum checking time is 10 times per min."
#overupdatelimit = "You can only change your ETH wallet address once every day"
#sendYeeHint = "Get your extra 90 Bitcoin by successfully inviting 3 friends joining Yee Official Telegram group. ( If you successfully invited more than 3 friends, for every friend you invited, get 30 Bitcoin for FREE ) Invite more📈 to get more📈 Copy referral link to invite now😊"
#busyHint="System is busing, please try again later!"


welcomeHint = "👋  Hey, if you would like to join our airdrop event, please 📲 talk to @YeeRobot PRIVATELY! 🙏  DO NOT spam or paste your referral link in group, otherwise admin will ban you 😐"
helpHint = "Welcome! I am very happy to help you! If you would like to join our airdrop event, please tap 'start' and follow the below steps. \n\n►Step 1: 👉 /set_address - Set your ETH wallet address with me \n►Step 2: 👉 /my_referral_link - Get referral link and share to invite friends \n►Step 3: Wait to get your Bitcoin tokens. You can always check how much you get via 👉 /my_token\n\nIf you need check or update your ETH/Bitcoin wallet address,\n👉 /my_address - check your current ETH/Bitcoin wallet address \n👉 /update_address - update your current ETH/Bitcoin wallet address\nPlease don't check or update your ETH/Bitcoin wallet address too frequently, it may cause losing data.\n\n【Important】\n►The maximum Bitcoin one user in telegram group could get through this airdrop event is 3000 Bitcoin\n\n►We will ONLY delivery airdrops no less than 100 Bitcoin (In order to meet that requirement, you need to AT LEAST SUCCESSFULLY invite 3 friends to telegram group and stay in telegram group.\n\nMore detail rules can be found at https://goo.gl/fbmu8t\n\nEnjoy and good luck!😊"
setAdressHint = "📮 Please send me your ETH/Bitcoin wallet address (Format should be 0x + 40 character hexadecimal) Please check CAREFULLY before submitting"
pleaseBind = "ETH/Bitcoin wallet address not set. 👉 Tap /set_address to set your ETH/Bitcoin wallet address first"
errorHint = "The ETH/Bitcoin wallet address you sent is invaild. The correct format should be 0x + 40 character hexadecimal. Please check CAREFULLY and send again"
bindingHint = "Your ETH/Bitcoin wallet address is: \n {} \n\n Successfully set. \n\n Tap /my_referral_link get your unique referral link. \n\nCopy to share to friends. Get Bitcoin token for FREE now!🚀"
copyConnect = "🚀Please COPY the message below and share to your friends. Get Bitcoin token for FREE now!👇👇👇👇👇"
ConnectUrl = "💥ATTENTION💥 Bitcointoken airdrop event is live🍭🍭🍭  Join telegram to get 10 Bitcoin for FREE. Invite 3 friends to join to get extra 90 Bitcoin. <Invite more📈 to get more📈> Event ending soon⏳  Get Free 100+ Bitcoin now👉{}"
showCoinHintSmall3 = "😍Congratulations! You successfully invited {} friends. You already got 10 Bitcoin. Invite {} more to get extra 90 Bitcoin. \n\n👉 Tap /my_referral_link to get your unique referral link. Copy to share to friends. Earn more Bitcoin now🚀 \n\n►The maximum Bitcoin one user in telegram group could get through this airdrop event is 3000 Bitcoin\n\n►We will ONLY delivery airdrops no less than 100 Bitcoin (In order to meet that requirement, you need to AT LEAST SUCCESSFULLY invite 3 friends to telegram group and stay in telegram group\n\nMore detail rules can be found at https://goo.gl/fbmu8t"
showCoinHintBig3 = "😍Congratulations! You earned {} Bitcoin. Successfully invited {} friends\n\n Get 30 Bitcoin for every additional friend you referred. \n\n👉 Tap /my_referral_link get your unique referral link. Copy to share to friends. Earn more Bitcoin now🚀 \n\n►The maximum Bitcoin one user in telegram group could get through this airdrop event is 3000 Bitcoin\n\nMore detail rules can be found at https://goo.gl/fbmu8t"
showCoinHintbig3000 = "😍Congratulations! You earned 3000 Bitcoin🚀  \n\n►The maximum Bitcoin one user in telegram group could get through this airdrop event is 3000 Bitcoin\n\nMore detail rules can be found at https://goo.gl/fbmu8t"

updateAdressHint = "📮 Please send me your new ETH/Bitcoin wallet address (Format should be 0x + 40 character hexadecimal)\n\n You can only update your ETH/Bitcoin wallet address once every day, so please check CAREFULLY before submitting"
overupdatelimit = "🙊You can only update your ETH/Bitcoin wallet address once every day"
overvisit = "🙊Check too frequently. The maximum checking time is 10 times per min."
repeatHint = '🙊 The ETH/Bitcoin wallet address you sent is already set before. \n 👉Tap /my_referral_link get your unique referral link. Copy to share to friends. Get Bitcoin token for FREE now🚀!'
groupInviteHint="Hello! We have a Bitcoin token airdrop now😍  If you would like to join the event, you have to join https://t.me/xxxxxxxxxxxxxxxp first🚀!"

sendYeeHintSmall3 = "😍Congratulations! You successfully invited {} friends. You already got 10 Bitcoin. Invite {} more to get extra 90 Bitcoin. \n\n👉 Tap /my_referral_link to get your unique referral link. Copy to share to friends. Earn more Bitcoin now🚀\n\n►The maximum Bitcoin one user in telegram group could get through this airdrop event is 3000 Bitcoin\n\n►We will ONLY delivery airdrops no less than 100 Bitcoin (In order to meet that requirement, you need to AT LEAST SUCCESSFULLY invite 3 friends to telegram group and stay in telegram group\n\nMore detail rules can be found at https://goo.gl/fbmu8t"
sendYeeHintBig3 = "😍Congratulations! You earned {} Bitcoin\n Successfully invited {} friends\n\n Get 30 Bitcoin for every additional friend you referred. \n\n👉 Tap /my_referral_link get your unique referral link. Copy to share to friends. Earn more Bitcoin now🚀 \n\n►The maximum Bitcoin one user in telegram group could get through this airdrop event is 3000 Bitcoin\n\nMore detail rules can be found at https://goo.gl/fbmu8t"

sendYeeHintBig3000="😍Congratulations! You earned xxxxxxxE🚀"
busyHint="🙊 System is busing, please try again later!"
whiteList='da'
showCoinHintbig90000 = "😍Congratulations! You earned xxxxxxxBitcoin🚀 \n\n►The maximum Bitcoin one user in telegram group could get through this airdrop event is 3000 Bitcoin\n\nMore detail rules can be found at https://goo.gl/fbmu8t"

whiteList=''
showCoinHintbig90000 = "😍Congratulations! You earned 90,000 Bitcoin🚀 \n\n►The maximum Bitcoin one user in telegram group could get through this airdrop event is 3000 Bitcoin\n\nMore detail rules can be found at https://goo.gl/fbmu8t"

MAX_TOKEN=2000
FILL_RATE=1000

FLASK_SERVER_IP="172.32.27.238"
FLASK_SERVER_PORT=6990

getYeeHint = "you hava {} Yee"
