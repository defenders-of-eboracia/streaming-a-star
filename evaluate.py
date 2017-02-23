from FileReader import FileReader
def score(problem, solution):
    """
    Get the score given the problem definition and the solution.

    This function ASSUMES the solution is valid (i.e. there are no too many videos on the cache servers!).

    :param problem: A `FileReader` object.
    :param solution: A list of lists of video IDs. solution[i] is the list of video IDs stored in cache i.
    :return:
    """

    savings = 0
    total_requests_no = 0

    for video_id, endpoint_id, requests_no in problem.requests:

        endpoint = problem.endpoints[endpoint_id]
        baseline_latency = endpoint.latency

        total_requests_no += requests_no

        all_caches = endpoint.cacheServers.copy()
        for available_cache_id, available_cache in all_caches.copy().items():
            if video_id not in solution[available_cache_id]:
                del all_caches[available_cache_id]

        # If there are no caches left
        if not all_caches:
            # No savings!
            continue

        # best_cache = min(all_caches, key=all_caches.get)
        best_cache_latency = min(all_caches.values())

        # Calculate the saving
        saving = baseline_latency - best_cache_latency
        saving *= requests_no

        savings += saving

    savings /= total_requests_no
    savings *= 1000

    return savings


if __name__ == "__main__":

    problem = FileReader('trivialExample.in')

    trivialSolution = [[2],[3,1],[0,1]]
    testSolution = [[2,3],[1],[0,1]]

    assert score(problem, trivialSolution), 462500
    assert score(problem, testSolution), 537500
