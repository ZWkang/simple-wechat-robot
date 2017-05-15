# -*- coding: utf-8 -*-：
#author:周文康
from wxpy import *
import requests
import re
import time
import logging
bot = Bot(cache_path=True)

KEY = '3090e0829a6c4c04aa6b7b7d88714bfe'
girl_friend = bot.friends().search('girlfirend')[0]
def get_response(msg):
	apiUrl = 'http://www.tuling123.com/openapi/api'
	data = {
		'key'    : KEY,
		'info'   : msg,
		'userid' : 'wechat-robot',
		}
	try:
		r = requests.post(apiUrl, data=data).json()
		return r.get('text')
	except:
		return

# group = bot.groups()
# friend = bot.friends()

# 注册好友请求类消息

@bot.register(msg_types=FRIENDS)
# 自动接受验证信息中包含 'wxpy' 的好友请求
def auto_accept_friends(msg):
    # 判断好友请求中的验证文本
	if 'zwk' in msg.text.lower():
    #     # 接受好友 (msg.card 为该请求的用户对象)
		new_friend = bot.accept_friend(msg.card)
    #     # 或 new_friend = msg.card.accept()
    #     # 向新的好友发送消息
		new_friend.send('请求已经接受咯')
	print(msg)



@bot.register(Group,TEXT,except_self=False)
#接入图灵机器人
def message_set(msg):

	tuling = Tuling(api_key='3090e0829a6c4c04aa6b7b7d88714bfe')
	output = open('D:/data.txt', 'a+',encoding='UTF-8')
	times = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
	output.write((times+'   '+msg.chat.name+'   '+msg.member.name+'  '+msg.text+'\r\n'))
	output.close()
	# 聊天记录写入文件
	print('{}  {}  {}   {}'.format(times,msg.chat.name,msg.member.name,msg.text))
	
	

	## 同理可以过滤一些群做操作
	if(msg.chat.name=='机器人大战群'):
		return '@{} {}'.format(msg.member.name,get_response(msg.text.replace(' ','')))
	if(msg.is_at):
		if('stop' in msg.text):
			return
		mess,num = re .subn(r'@(.+?)\s', '', msg.text)
		#群聊指令 @我 添加好友==谁
		if('添加好友==' in mess):
			arr = mess.split('添加好友==')

			fire = ensure_one(bot.groups().search(msg.chat.name)[0].search(arr[1]))
			if(fire.is_friend==False):
				fire.add('我是xxx')
			else:
				return '我们已经是好基友了'
		else:
			testmain = msg.sender
			# tuling.do_reply(msg,True)
			return '@{} {} '.format(msg.member.name,get_response(mess.replace(' ','')))

#监听群组内的名片 如果有就进行添加
@bot.register(Group,msg_types='Card',except_self=False)
def card_get(msg):
	if(msg.card):
		bot.add_friend(msg.card)



@bot.register(Friend,TEXT)
def message_set(msg):
	if('通过了你的朋友验证请求' in msg.text):
		return
	times = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
	print('{}   {}'.format(times,msg.text))
	#模拟私聊指令
	if('前端开发讨论组' in msg.text):
		bot.groups().search('前端开发讨论组')[0].add_members(msg.sender,True)
		return
	mess = get_response(msg.text) 
	if mess !='':
		return '{}'.format(mess)
	else:
		return '机器人离开了'


@bot.register(girl_friend)
def ignore(msg):
	return

@bot.register(NOTE)
def ignores(msg):
	return

logging.basicConfig(level=logging.DEBUG)
#开启debug模式
embed()
