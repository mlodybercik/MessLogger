from getpass import getpass
from Logger.logger import Logger, logToConsole
from fbchat import FBchatException

if __name__ == "__main__":
	try:
		try:
			client = Logger(input("Login: "), getpass("Password: "))
		except FBchatException:
			raise(Exception("Error during logging in, wrong password?"))
		client.listen()
	except:
		try:
			client.logout()
		except:
			raise(Exception("Error during logging out. Did you even log in?"))
		else:
			logToConsole("[I] Succesful logout.")
		client.dumpContents()
