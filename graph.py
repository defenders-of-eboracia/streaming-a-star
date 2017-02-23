from evaluate import score as get_score


def _get_caches_contents_by_action(state, action):
    contents = state.caches_contents[:]
    current_size, videos = contents[action.cache_id]
    current_size += action.video_size
    videos = videos[:]
    videos.append(action.video_id)
    contents[action.cache_id] = (current_size, videos)
    return contents


def _clean_solution(solution):
    return list([video_ids for (capacity, video_ids) in solution])


class MazeAction(object):
    def __init__(self, cache_id, video_id, video_size):
        self.cache_id = cache_id
        self.video_id = video_id
        self.video_size = video_size
        self.reward = None

    def compute_reward(self, problem, previous_state, base_score):
        contents = _get_caches_contents_by_action(state=previous_state, action=self)
        self.reward = get_score(problem, _clean_solution(contents))

    def __eq__(self, other):
        return self.cache_id == other.cache_id and self.video_id == other.video_id

    def __hash__(self):
        return self.cache_id * 100000 + self.video_id


class MazeState(object):

    def __init__(self, score, caches_contents, problem):
        self.caches_contents = caches_contents
        self.score = score
        self.problem = problem
        self.actions = self._get_actions()

    def _get_actions(self):
        """
        Get options after having added a single
        :return: A list of actions
        """

        # The max capacity of each cache server
        max_capacity = self.problem.cacheCapacity

        options = []

        # For each of the caches
        for cache_id, (cache_current_size, cache_videos) in enumerate(self.caches_contents):

            # For each video we can add
            for video_id, video_size in enumerate(self.problem.videoSizes):

                # Don't overfill the cache (capacity)
                if video_size + video_size > max_capacity:
                    continue

                # Don't duplicate videos in a cache!
                if video_id in self.caches_contents[cache_id][1]:
                    continue

                action = MazeAction(cache_id=cache_id, video_id=video_id,
                                    video_size=video_size)
                action.compute_reward(self.problem, previous_state=self, base_score=self.score)
                options.append(action)

        return options

    def perform(self, action):

        contents = _get_caches_contents_by_action(self, action)
        new_score = self.score + action.reward

        node = MazeState(score=new_score, caches_contents=contents,
                         problem=self.problem)

        return node

    def reward(self, parent, action):
        return action.reward

    def is_terminal(self):
        return len(self.actions) == 0

    def __eq__(self, other):
        return self.caches_contents == other.caches_contents

    def __hash__(self):
        return str(self.caches_contents).__hash__()





