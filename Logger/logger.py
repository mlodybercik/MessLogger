from fbchat import Client, Message, ThreadType, ImageAttachment
from .lenArray import LenArray
import time

default = {
# Max length of given thread history.
"LENGTH": 1000,

# Translate from uid to name, DISCLAIMER: translating seems kinda buggy
"TRANSLATE_NAMES": False,

# Log to file
"LOG": True,

# Log to console current messages
"LOG_TO_CONSOLE": True,

# Dump contents of LenArray to thread files after logout
"DUMP_CONTENTS": True,

# Import knwon names to knownUsers from a file
"IMPORT_KNOWN_NAMES": False}

# TODO:
# log to file not to stdout
# import known names
# add daemon capabilities
# add way of logging to file
# add something to distinguish thread types

class Logger(Client):
	arr = {}
	knownUsers = {}

	def __init__(self, *args, **kwargs):
		super(Logger, self).__init__(*args, **kwargs)
		# I hate doing that, but I hate having to look at useless space more
		# good code > clean code (imo lol)
		try:
			for key in kwargs["params"]:
				setattr(self, key, params[key])
			del kwargs["params"]
		except:
			for key in default:
				setattr(self, key, default[key])
		self.logToConsole("[I] Defining all useless functions...")
		for funct in allFunctions:
			setattr(self, funct, lambda *args, **kwargs: None)
		self.logToConsole("[I] Listening...")

	def logToConsole(self, text):
		if(self.LOG_TO_CONSOLE):
			print(text)

	def dumpContents(self, folder="history/"):
		if(self.DUMP_CONTENTS):
			self.logToConsole("[I] Dumping contents...")
			try:
				import os
				fname = time.strftime("%m_%d-%H_%M_%S")
				for history in self.arr.keys():
					try:
						os.mkdir(folder + history)
					except FileExistsError:
						pass
					try:
						dump = self.arr[history].dumpArray()
						with open(folder + history + "/" + fname, "w") as file:
							for line in dump:
								file.write(line[2] + ": " + line[1] + "\r\n")
					except Exception as e:
						with open(folder + "/exceptions", "wa") as file:
							file.write(str(e) + "\n")
						continue
						
			except Exception as e:
				self.logToConsole("[E] Something went wrong when dumping to file. " + e)


	def translateName(self, author_id, threadType):
		if self.TRANSLATE_NAMES:
			if author_id in self.knownUsers.keys():
				return self.knownUsers[author_id]
			else:
				name = self.fetchUserInfo(author_id)[author_id].name
				self.knownUsers[author_id] = name
				return name
		else:
			return author_id


	def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
		# exit in chat to "self" to exut
		if message_object.text == "exit" and author_id == self.uid:
			self.logout()

		# create empty LenArray for user who sent you a message
		if(thread_id not in self.arr.keys()):
			self.arr[thread_id] = LenArray(self.LENGTH)

		# if has text add text to previously created LenArray
		if message_object.text:
			self.logToConsole("[M] {} in {}: {}".format(self.translateName(author_id, thread_type), thread_id, message_object.text))
			self.arr[thread_id].append([message_object.uid, message_object.text, author_id])
		# else propably is an attachment, add all URLs to array
		elif len(message_object.attachments) > 0:
			for i in message_object.attachments:
				if isinstance(i, ImageAttachment):
					self.logToConsole("[M] {} in {}: {}".format(self.translateName(author_id, thread_type), thread_id, i.large_preview_url))
					self.arr[thread_id].append([message_object.uid, i.large_preview_url, author_id])


	def onMessageUnsent(self, mid, author_id, thread_id, thread_type, ts, msg, **kwargs):
		mess = self.arr[thread_id].find(func=lambda a: True if a[0] == mid else False)
		if mess == None:
			self.logToConsole("[E] Couldnt resolve deleted message. {}".format(mid))
		else:
			self.logToConsole("[D] {} in {} deleted message: {}".format(self.translateName(author_id, thread_type), thread_id, mess[1]))


### END OF USED FUNCTIONS ###
# Definition on all useless (for now) functions
allFunctions = [ "onLoggingIn", "onMessageSeen",
"onLoggedIn","onListening","onListenError","onColorChange","onEmojiChange",
"onTitleChange","onImageChange","onNicknameChange","onAdminAdded","onAdminRemoved",
"onApprovalModeChange","onMessageDelivered","onMarkedSeen","onPeopleAdded","onPersonRemoved",
"onFriendRequest","onInbox","onTyping","onReactionAdded","onReactionRemoved","onBlock",
"onUnblock","onLiveLocation","onQprimer","onUnknownMesssageType","onMessageError",
"onCallStarted","onCallEnded","onUserJoinedCall","onPollCreated","onPollVoted",
"onPlanCreated","onPlanEnded","onPlanEdited","onPlanDeleted","onPlanParticipation"]
