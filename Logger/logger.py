from fbchat import Client, Message, ThreadType, ImageAttachment
from .lenArray import LenArray
from .enums import LogType
import os
import time
import traceback

default = {
# Max length of given thread history.
"LENGTH": 1000,

# Log to arr
"LOG": False,

# Log to console current messages
"LOG_TO_CONSOLE": False,

# Dump contents of LenArray to thread files after logout
"DUMP_CONTENTS": False,

# Live logging to file, useful when leaving it over longer span of time
"LIVE_LOG": True,

# Add timestamp to logs
"TIMESTAMP": True
}

# TODO:
# add daemon capabilities
# add way to manipulate way how log is formatted, eg. "%u %i %t %m" => some processing => "<uid> <threadid> <timestamp> <message>"
# liveLog = "%t %u %i %m"
# consoleLog = "%u in %i said: %m"

class Logger(Client):
	# dict to save message history
	arr = {}
	# live file streams
	liveStreams = {}

	def __init__(self, *args, **kwargs):
		super(Logger, self).__init__(*args, **kwargs)
		# I hate doing that, but I hate having to look at useless space more
		# good code > clean code (imo lol)

		# Defining flags
		try:
			for key in kwargs["params"]:
				setattr(self, key, params[key])
			del kwargs["params"]
		except:
			for key in default:
				setattr(self, key, default[key])
		# Defining useless functions
		self.logToConsole("[I] Defining all useless functions...")
		for funct in allFunctions:
			setattr(self, funct, lambda *args, **kwargs: None)
		self.logToConsole("[I] Listening...")

	def logToFile(self, userID, content, threadID, folder="history/", end="\r\n", live=False):
		def createStream(threadID, folder, fname, buffering=1):
			try:
				os.mkdir(folder + threadID)
			except FileExistsError:
				pass
			return open(folder + threadID + "/" + fname, "a", buffering=buffering)

		if live:
			fname = time.strftime("%m_%d-" + str(threadID))
			if threadID not in self.liveStreams:
				self.liveStreams[threadID] = createStream(threadID, folder, fname)
			self.liveStreams[threadID].write(content + end)
		else:
			fname = time.strftime("%m_%d-%H_%M_%S")
			for user in content:
				with createStream(userID, folder, fname) as file:
					file.write(user[3] + " " + user[2] + ": " + user[1] + "\r\n", buffering=-1)

	def logToConsole(self, text):
		print(text)

	def findMessage(self, threadID, query):
		if threadID not in self.arr.keys():
			return None
		_ = self.arr[threadID].find(func=lambda a: True if a[0] == query else False)
		if _:
			return _[1]
		else:
			return None

	def log(self, logType=LogType.NONE, delete=False, **kwargs):
		# LOG = logging to lenArray
		# LOG_TO_CONSOLE = logging to console output TODO: changing stdout
		# LIVE_LOG = live logging to file
		# DUMP_CONTENTS = dump lenArray to file after exit
		if isinstance(logType, list):
			for log in logType:
				self.log(log, delete, **kwargs)

		authorID = kwargs["authorID"]
		threadID = kwargs["threadID"]

		if self.LOG and logType == LogType.TEXT:
			messID = kwargs["messID"]
			text = kwargs["text"]

			if threadID not in self.arr:
				self.arr[threadID] = LenArray(self.LENGTH)
			if self.TIMESTAMP:
				self.arr[threadID].append([messID, text, authorID, kwargs["timestamp"]])
			else:
				self.arr[threadID].append([messID, text, authorID])

		if self.LOG_TO_CONSOLE and logType == LogType.LOG_TO_CONSOLE:
			# If deleted is set and log is on, find the message
			if delete and self.LOG:
				text = self.findMessage(threadID, kwargs["messID"])
				if text is None:
					self.logToConsole("[D] Couldn't resolve deleted message. ID: {} in {}".format(text, threadID))
					return
			# If logging to array is turned off, return message ID
			elif delete:
				text = kwargs["messID"]
			else:
				text = kwargs["text"]

			if delete:
				if self.TIMESTAMP:
					self.logToConsole("[D] {}: {} in {} deleted: {}".format(time.time(), authorID, threadID, text))
				else:
					self.logToConsole("[D] {} in {} deleted: {}".format(authorID, threadID, text))
			else:
				if self.TIMESTAMP:
					self.logToConsole("[M] {}: {} in {}: {}".format(kwargs["timestamp"], authorID, threadID, text))
				else:
					self.logToConsole("[M] {} in {}: {}".format(authorID, threadID, text))
			return

		if self.LIVE_LOG and logType == LogType.LIVE_LOG:
			# If deleted is set and log is on, find the message
			if delete and self.LOG:
				text = self.findMessage(threadID, kwargs["messID"])
				if text is None:
					return
			# If logging to array is turned off, return message ID
			elif delete:
				text = kwargs["messID"]
			text = kwargs["text"]
			content = "{} {}: {}".format(kwargs["timestamp"], authorID, text)
			self.logToFile(authorID, content, threadID, live=True)
			return

		if self.DUMP_CONTENTS and self.LOG and logType == LogType.DUMP_CONTENTS:
			for thread in self.arr.keys():
				self.logToFile(thread, self.arr[thread].dumpArray())

	def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
		# exit in chat to "self" to exut
		if message_object.text == "exit" and author_id == self.uid:
			self.logout(True)

		# if has text add text to previously created LenArray
		if message_object.text:
			try:
				self.log([LogType.TEXT, LogType.LOG_TO_CONSOLE, LogType.LIVE_LOG], authorID = author_id, threadID = thread_id, text = message_object.text, messID = message_object.uid, timestamp = message_object.timestamp)
			except Exception as E:
				traceback.print_exc()
		# else propably is an attachment, add all URLs to array
		elif len(message_object.attachments) > 0:
			for i in message_object.attachments:
				if isinstance(i, ImageAttachment):
					try:
						self.log([LogType.TEXT, LogType.LOG_TO_CONSOLE, LogType.LIVE_LOG], authorID = author_id, threadID = thread_id, text = i.large_preview_url, messID = message_object.uid, timestamp = message_object.timestamp)
					except Exception as E:
						traceback.print_exc()

	def onMessageUnsent(self, mid, author_id, thread_id, thread_type, ts, msg, **kwargs):
		try:
			self.log(LogType.LOG_TO_CONSOLE, delete=True, authorID = author_id, threadID = thread_id, messID=mid)
		except:
			traceback.print_exc()

	def logout(self, cookies=False):
		if not cookies:
			super(Logger, self).logout()
		try:
			self.log(logType = LogType.DUMP_CONTENTS, authorID="", threadID="")
		except Exception:
			traceback.print_exc()
		for stream in liveStreams.keys():
			liveStrams[stream].close()

### END OF USED FUNCTIONS ###
# Definition on all useless (for now) functions
allFunctions = ["onLoggingIn", "onMessageSeen",
	"onLoggedIn","onListening","onListenError","onColorChange","onEmojiChange",
	"onTitleChange","onImageChange","onNicknameChange","onAdminAdded",
	"onAdminRemoved", "onApprovalModeChange","onMessageDelivered",
	"onMarkedSeen","onPeopleAdded","onPersonRemoved","onFriendRequest",
	"onInbox", "onTyping","onReactionAdded","onReactionRemoved","onBlock",
	"onUnblock", "onLiveLocation","onQprimer","onUnknownMesssageType",
	"onMessageError", "onCallStarted","onCallEnded","onUserJoinedCall",
	"onPollCreated","onPollVoted","onPlanCreated","onPlanEnded","onPlanEdited",
	"onPlanDeleted","onPlanParticipation"
]
