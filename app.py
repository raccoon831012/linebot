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
