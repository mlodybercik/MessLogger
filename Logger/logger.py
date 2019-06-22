from fbchat import Client, Message, ThreadType
from getpass import getpass
from .lenArray import LenArray
import time

# Max length of given thread history.
LENGTH = 1000

# Translate from uid to name, DISCLAIMER: translating seems kinda buggy
TRANSLATE_NAMES = False

# Log to file
LOG = True

# Log to console current messages
LOG_TO_CONSOLE = True

# Dump contents of LenArray to thread files after logout
DUMP_CONTENTS = True

# Import knwon names to knownUsers from a file
IMPORT_KNOWN_NAMES = False

# TODO:
# log to file not to stdout
# import known names
# add daemon capabilities
# add way of logging to file
# add something to distinguish thread types

def logToConsole(text):
	if(LOG_TO_CONSOLE):
		print(text)

class Logger(Client):
	arr = {}
	knownUsers = {}

	def __init__(self, *args, **kwargs):
		super(Logger, self).__init__(*args, **kwargs)
		# I hate doing that, but I hate having to look at useless space
		# good code > clean code (imo lol)
		logToConsole("[I] Defining all useless functions...")
		for funct in allFunctions:
			setattr(self, funct, lambda *args, **kwargs: None)

	def dumpContents(self, folder="history/"):
		if(DUMP_CONTENTS):
			logToConsole("[I] Dumping contents...")
			try:
				import os
				fname = time.strftime("%m_%d-%H_%M_%S")
				for history in self.arr.keys():
					try:
						os.mkdir(folder + history)
					except FileExistsError:
						pass
					dump = self.arr[history].dumpArray()
					print(dump)
					with open(folder + history + "/" + fname, "w") as file:
						for line in dump:
							file.write(line[2] + ": " + line[1] + "\r\n")
			except Exception as e:
				logToConsole("[E] Something went wrong when dupming. " + e)


	def translateName(self, author_id, threadType):
		if TRANSLATE_NAMES:
			if author_id in self.knownUsers.keys():
				return self.knownUsers[author_id]
			else:
				name = self.fetchUserInfo(author_id)[author_id].name
				self.knownUsers[author_id] = name
				return name
		else:
			return author_id


	def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
		if message_object.text == "exit" and author_id == self.uid:
			self.logout()

		logToConsole("[M] {} in {}: {}".format(self.translateName(author_id, thread_type), thread_id, message_object.text))

		if(thread_id not in self.arr.keys()):
			self.arr[thread_id] = LenArray(LENGTH)

		self.arr[thread_id].append([message_object.uid, message_object.text, author_id])


	def onMessageUnsent(self, mid, author_id, thread_id, thread_type, ts, msg, **kwargs):
		mess = self.arr[thread_id].find(func=lambda a: True if a[0] == mid else False)
		if mess == None:
			logToConsole("[E] Couldnt resolve deleted message. {}".format(mid))
		else:
			logToConsole("[D] {} in {} deleted message: {}".format(self.translateName(author_id, thread_type), thread_id, mess[1]))


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
