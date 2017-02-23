

class Node:
    """
    Represent a node in the state of the game.
    """

    def __init__(self, score, caches_contents):
        """
        Represent the a possible state, given the state of the caches.
        :param caches_contents: A list of tuples (cache_current_size, [video_id,...])
        """
        self.caches_contents = caches_contents
        self.score = score

    def options(self, problem):
        """
        Get options after having added a single
        :param problem: The problem descriptor.
        :return: A list of (cost, node).
        """

        # The max capacity of each cache server
        max_capacity = problem.cacheCapacity

        options = []

        # For each of the caches
        for cache_id, (cache_current_size, cache_videos) in enumerate(self.caches_contents):

            # For each video we can add
            for video_id, video_size in enumerate(problem.videoSizes):

                if video_size + video_size > max_capacity:
                    continue

                cost_function = lambda problem, solution: -1

                # Create a copy of this node with the cache having this video in it.
                contents = self.caches_contents
                contents[cache_id][0] += video_size
                contents[cache_id][1].append(video_id)
                score = cost_function(problem, contents)
                node = Node(contents, score)

                # The weight of the connection is the difference in score (negative, as obj. is minimisation)
                weight = -(score - self.score)
                option = (weight, node)

                options.append(option)

        return options

    def __hash__(self):
        return hash(self.__repr__())
