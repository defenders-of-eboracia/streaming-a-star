#!/usr/bin/env python3

class Endpoint(object):
	def __init__(self, latency, nCaches):
		self.latency = latency
		self.nCaches = nCaches
		self.cacheServers = []

	def addCacheServer(self, cID, latency):
		self.cacheServers.append((cID, latency))

	def check(self):
		assert(self.nCaches == len(self.cacheServers))

	def __str__(self):
		return self.__repr__()

	def __repr__(self):
		return ",".join("%d: latency=%d" % (cID, latency) for (cID, latency) in self.cacheServers)

class FileReader(object):

	def parseFile(self):
		firstLine = self.file.readline()
		(self.nVideos, self.nEndoints, self.nReqDescs, self.nCaches, self.cacheCapacty) = [int(x) for x in firstLine.split(" ")]
		print("Videos: %d, Endpoints: %d, Request Descriptions: %d, Caches: %d, Cache Capacity: %d" % (self.nVideos, self.nEndoints, self.nReqDescs, self.nCaches, self.cacheCapacty))
		self.videoSizes = [int(x) for x in self.file.readline().split(" ")]
		# Parse endpoints
		self.endpoints = []
		for e in range(self.nEndoints):
			latency, numCaches = [int(x) for x in self.file.readline().split(" ")]
			thisEndpoint = Endpoint(latency, numCaches)
			for c in range(numCaches):
				(cID, latency) = [int(x) for x in self.file.readline().split(" ")]
				thisEndpoint.addCacheServer(cID, latency)
			thisEndpoint.check()
			self.endpoints.append(thisEndpoint)
		self.requests = []
		for r in range(self.nReqDescs):
			vID, eID, latency = [int(x) for x in self.file.readline().split(" ")]
			self.requests.append((vID, eID, latency))

	def __init__(self, filename):
		self.filename = filename
		self.file = open(self.filename, "r")
		self.parseFile()

if __name__ == "__main__":
	testfile = "trivialExample.in"
	inputData = FileReader(testfile)
	print("Video Sizes: %r" % (inputData.videoSizes))
	print("Endpoints:\n\t%s" % ("\n\t".join([str(e) for e in inputData.endpoints])))
	print("Requests: %r" % ([r for r in inputData.requests]))
