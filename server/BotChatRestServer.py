from flask import request
from flask import Flask
import json
from robots import BotChatHandler
from concurrent.futures import ThreadPoolExecutor
import logging,settings
import multiprocessing
executor = ThreadPoolExecutor(multiprocessing.cpu_count()*2+1)
app = Flask(__name__)
gunicorn_error_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.INFO)
app.logger.info('start server!')

@app.route('/chat/msg', methods=['POST'])
def chatMessage():
    try:
        jsondata = request.form['msg']
        chat_id =  request.form['chat_id']
        content_type = request.form['content_type']
        msg = json.loads(jsondata)
        executor.submit(BotChatHandler.handle(chat_id,content_type,msg=msg))
    except Exception as e:
        app.logger.error("handler msg error:%s",e)
    result="ok"
    return json.dumps(result)

if __name__ == '__main__':
    #app.run(host=settings.FLASK_SERVER_IP,port=settings.FLASK_SERVER_PORT,debug=True)
    app.run(debug=True)
