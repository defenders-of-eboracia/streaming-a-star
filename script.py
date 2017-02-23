from FileReader import FileReader
from mcts.mcts import MCTS
from mcts.tree_policies import UCB1
from mcts.default_policies import immediate_reward
from mcts.backups import monte_carlo
from mcts.graph import StateNode


# Read the input file
from graph import MazeState, MazeAction

testfile = "trivialExample.in"
problem = FileReader(testfile)
print("Video Sizes: %r" % (problem.videoSizes,))
print("Endpoints:\n\t%s" % ("\n\t".join([str(e) for e in problem.endpoints])))
print("Requests: %r" % ([r for r in problem.requests]))

# Generate initial state
initial_contents = list([(0, []) for _ in range(problem.nCaches)])
initial_score = 0
initial_state = MazeState(caches_contents=initial_contents, score=initial_score,
                          problem=problem)

# Generate the optimal end state
mcts = MCTS(tree_policy=UCB1(c=1.41),
            default_policy=immediate_reward,
            backup=monte_carlo)

root = StateNode(parent=None, state=initial_state)
best_action = mcts(root)
print(best_action)
