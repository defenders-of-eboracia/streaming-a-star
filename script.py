from FileReader import FileReader
from mcts.mcts import MCTS
from mcts.tree_policies import UCB1
from mcts.default_policies import immediate_reward
from mcts.backups import monte_carlo
from mcts.graph import StateNode


# Read the input file
from FileWriter import FileWriter
from graph import TreeState, TreeAction, _clean_solution

testfile = "trivialExample.in"
problem = FileReader(testfile)
print("Video Sizes: %r" % (problem.videoSizes,))
print("Endpoints:\n\t%s" % ("\n\t".join([str(e) for e in problem.endpoints])))
print("Requests: %r" % ([r for r in problem.requests]))

# Generate initial state
initial_contents = list([(0, []) for _ in range(problem.nCaches)])
initial_score = 0
initial_state = TreeState(caches_contents=initial_contents, score=initial_score,
                          problem=problem)

# Generate the optimal end state
mcts = MCTS(tree_policy=UCB1(c=1.41),
            default_policy=immediate_reward,
            backup=monte_carlo)

node = StateNode(parent=None, state=initial_state)

while True:
    if node.state.is_terminal():
        print("Terminal node reached.")
        break
    print("Finding best action")
    best_action = mcts(node)
    print("Performing action")
    node = StateNode(parent=None, state=node.state.perform(best_action))
    print("Score now is: %d" % node.state.score)

print("Saving output")
print(node.state.caches_contents)

contents = node.state.caches_contents
contents = _clean_solution(contents)
dictionary = {i: e for i, e in enumerate(contents) if e}

writer = FileWriter('output.txt')
writer.writeData(dictionary)
