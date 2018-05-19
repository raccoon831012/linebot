#encoding=utf-8
import jieba
import pandas as pd
dicts = {  
    "責任制": 1,
    "平日": 0.987,
    "打卡": 0.981,
    "制": 0.979,
    "假日": 0.977,
    "國定": 0.974,
    "時數": 0.973,
    "上下班": 0.968,
    "工時": 0.968,
    "強迫": 0.966,
    "規定": 0.962,
    "準時": 0.961,
    "給付": 0.960,
    "加班": 0.958
}
from flask import Flask, request, abort

from linebot import (
	LineBotApi, WebhookHandler
)
from linebot.exceptions import (
	InvalidSignatureError
)
from linebot.models import (
	MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('mY06TCg4DZyWnD71hPlukDrlI6riga2MXOtx+N8u5ruWhej2rstxbTUPLEi/tjxBaKq2RGfWijres4PAZYcCVkrDJquvsg7KgPo0ZotOygez8F48XM/w996FvoOZkO3IxrBR0At7cWLGJhRrvJJKzgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('6ba525a97245df4d1bf56a55d9ef5d1d')

@app.route("/callback", methods=['POST'])
def callback():
	signature = request.headers['X-Line-Signature']
	body = request.get_data(as_text=True)
	words = jieba.cut(body, cut_all=False)
	sum = 0
	i = 0
	for word in words:
    i = i+1
    try:
        sum = dicts[word]
    except KeyError:
        sum +=0;
	sum = sum/i
	body = "你評論該公司有"+str(sum)+"可能性違法勞基法"
	app.logger.info("Request body: " + body)
	try:
		handler.handle(body, signature)
	except InvalidSignatureError:
		abort(400)
	return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
	line_bot_api.reply_message(
		event.reply_token,
		TextSendMessage(text=event.message.text))
if __name__ == "__main__":
	app.run()
