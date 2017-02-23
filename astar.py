class AStar:
    """
    A-Star implementation adapted from @jrialland's version at
    https://github.com/jrialland/python-astar/blob/master/astar.py
    """

    def heuristic_cost_estimate(self, start, goal):
        # return self.average_min_pies_cost * (start.last_day - start.current_day)
        raise NotImplementedError

    def _yield_path(self, came_from, last):
        yield last
        current = came_from[last]
        while True:
            yield current
            if current in came_from:
                current = came_from[current]
            else:
                break

    def _reconstruct_path(self, came_from, last):
        return list(reversed([p for p in self._yield_path(came_from, last)]))

    def calculate_total_cost(self, the_path):
        node = the_path[0]
        next = the_path[1]
        total = 0
        while True:
            children = node.options(self.available_pies_cost)
            if not children:
                return total
            for cost, node in children:
                if node == next:
                    total += cost
                    break
            the_path = the_path[1:]
            try:
                node = the_path[0]
                next = the_path[1]
            except IndexError:
                return total

    def astar(self, start, goal):
        """applies the a-star path searching algorithm in order to find a route between a 'start' node and a 'root' node"""
        closedset = set([])    # The set of nodes already evaluated.
        # The set of tentative nodes to be evaluated, initially containing the
        # start node
        openset = set([start])
        came_from = {}    # The map of navigated nodes.

        g_score = {}
        g_score[start] = 0   # Cost from start along best known path.

        # Estimated total cost from start to goal through y.
        f_score = {}
        f_score[start] = self.heuristic_cost_estimate(start, goal)

        while len(openset) > 0:
            # the node in openset having the lowest f_score[] value
            current = min(f_score, key=f_score.get)
            if current == goal:
                path = self._reconstruct_path(came_from, goal)
                return path
            openset.discard(current)  # remove current from openset
            del f_score[current]
            closedset.add(current)  # add current to closedset

            for cost, neighbor in current.options():
                if neighbor in closedset:
                    continue
                tentative_g_score = g_score[current] + cost
                if (neighbor not in openset) or (tentative_g_score < g_score[neighbor]):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + \
                        self.heuristic_cost_estimate(neighbor, goal)
                    openset.add(neighbor)
        return None