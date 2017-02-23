#!/usr/bin/env python3

class Endpoint(object):
	def __init__(self, latency, nCaches):
		self.latency = latency
		self.nCaches = nCaches
		self.cacheServers = {}
		self.requests = {}

	def addCacheServer(self, cID, latency):
		self.cacheServers[cID] = latency

	def addRequests(self, vID, requests):
		if vID not in self.requests:
			self.requests[vID] = requests
			return
		self.requests[vID] += requests

	def check(self):
		assert(self.nCaches == len(self.cacheServers))

	def __str__(self):
		return self.__repr__()

	def __repr__(self):
		return ",".join("%d: latency=%d" % (cID, latency) for (cID, latency) in self.cacheServers.items())

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
			vID, eID, numReqs = [int(x) for x in self.file.readline().split(" ")]
			self.requests.append((vID, eID, numReqs))

	def transFormVideoRequests(self):
		self.videoRequests = {}
		for vID in range(self.nVideos):
			self.videoRequests[vID] = []
		for (vID, eID, numReqs) in self.requests:
			self.videoRequests[vID].append((eID, numReqs))

	def augmentEndpoints(self):
		self.endpointById = {}
		for eID, endPoint in enumerate(self.endpoints):
			endPoint.id = eID
			self.endpointById[eID] = endPoint
		for (vID, eID, numReqs) in self.requests:
			self.endpointById[eID].addRequests(vID, numReqs)

	def __init__(self, filename):
		self.filename = filename
		self.file = open(self.filename, "r")
		self.parseFile()
		self.transFormVideoRequests()
		self.augmentEndpoints()

if __name__ == "__main__":
	testfile = "trivialExample.in"
	inputData = FileReader(testfile)
	print("Video Sizes: %r" % (inputData.videoSizes))
	print("Endpoints:\n\t%s" % ("\n\t".join([str(e) for e in inputData.endpoints])))
	print("Requests: %r" % ([r for r in inputData.requests]))
	print(inputData.videoRequests)
	print(inputData.endpointById)
