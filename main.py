from getpass import getpass
from Logger.logger import Logger, logToConsole
from fbchat import FBchatException

if __name__ == "__main__":
	try:
		try:
			client = Logger(input("Login: "), getpass("Password: "))
		except FBchatException:
			raise(Exception("Error during loggin, wrong password?"))
		client.listen()
	except:
		try:
			client.logout()
		except:
			raise(Exception("Error during logging out."))
		logToConsole("[I] Succesful logout.")
		client.dumpContents()
