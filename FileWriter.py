class FileWriter(object):

	def __init__(self, filename):
		self.filename = filename

	"""write outputData to file, outputData is a dict where the
		cache ID is the key and the values are lists of video IDs
	"""
	def writeData(self, outputData):
		file = open(self.filename, "w+")
		file.write("%d\n" % (len(outputData)))
		for cID, vidList in outputData.items():
			file.write("%d %s\n" % (cID, " ".join("%d" % (x) for x in vidList)))
		file.close()
