from FileReader import FileReader


# Read the input file
from graph import Node

testfile = "small.in"
problem = FileReader(testfile)
print("Video Sizes: %r" % (problem.videoSizes,))
print("Endpoints:\n\t%s" % ("\n\t".join([str(e) for e in problem.endpoints])))
print("Requests: %r" % ([r for r in problem.requests]))

# Generate initial state
initial_contents = list([(0, []) for _ in range(problem.nCaches)])
initial_score = 0
initial_state = Node(caches_contents=initial_contents, score=initial_score)

# Generate the optimal end state

# TODO A-Star needs end-node!! Fuck!!