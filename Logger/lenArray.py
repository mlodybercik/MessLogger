class LenArray():
	__array__ = []
	__index__ = 0

	def __init__(self, max_len):
		self.maxLen = max_len

	def __replace__(self, index, obj):
		del self.__array__[index]
		self.__array__.insert(index, obj)

	def __getitem__(self, i):
		return self.__array__[i]

	def append(self, obj):
		if len(self.__array__) > self.maxLen-1:
			self.__replace__(self.__index__ % self.maxLen, obj)
			self.__index__ += 1
		else:
			self.__array__.append(obj)
			self.__index__ += 1

	def getLen(self):
		return maxLen

	def dumpArray(self):
		if len(self.__array__) < self.maxLen:
			return self.__array__
		else:
			return [self.__array__[x % self.maxLen] for x in range(self.__index__, self.__index__ + self.maxLen)]

	def find(self, func=lambda a: True):
		for item in self.__array__:
			if(func(item)):
				return item
				break
		return None
