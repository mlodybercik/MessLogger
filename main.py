from getpass import getpass
from Logger.logger import Logger
from fbchat import FBchatException, FBchatUserError
import json

if __name__ == "__main__":
	cookies = None
	try:
		with open("session", "r") as file:
			cookies = json.loads(file.read())
	except:
		pass
	try:
		try:
			if cookies:
				try:
					client = Logger("0", "0", session_cookies=cookies, max_tries=1)
				except FBchatUserError:
					client = Logger(input("Login: "), getpass("Password: "), max_tries=1)
			else:
				client = Logger(input("Login: "), getpass("Password: "), max_tries=1)
		except FBchatException:
			raise(Exception("Error during logging in, wrong password/bad cookies?"))
		client.listen()
	except:
		try:
			client.logout()
		except:
			raise(Exception("Error during logging out. Did you even log in?"))
		else:
			client.dumpContents()
