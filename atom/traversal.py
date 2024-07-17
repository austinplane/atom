from enum import Enum


class SearchState(Enum):
    WHITE = 0
    GRAY = 1
    BLACK = 2


def traverse_descendants(node, callback):
    stop = False

    def stop_func():
        nonlocal stop
        stop = True

    def traverse(curr_node):
        nonlocal stop
        callback(curr_node, stop_func)
        for child in curr_node.children:
            if stop:
                break
            traverse(child)

    traverse(node)


def traverse_ancestors(node, callback):
    stop = False

    def stop_func():
        nonlocal stop
        stop = True

    def traverse(curr_node):
        nonlocal stop
        callback(curr_node, stop_func)
        for parent in curr_node.parents:
            if stop:
                break
            traverse(parent)

    traverse(node)


def dfs(node, callback, directed=True):
    stop = False
    state_by_id = {}

    def stop_func():
        nonlocal stop
        stop = True

    def traverse(curr_node):
        nonlocal stop
        state_by_id[curr_node.id] = SearchState.GRAY

        reachable = curr_node.children
        if not directed:
            reachable = curr_node.parents + curr_node.children

        for r in reachable:
            if stop:
                break

            if r.id in state_by_id:
                callback(r, state_by_id[r.id], stop_func)
            else:
                callback(r, SearchState.WHITE, stop_func)
                traverse(r)

        state_by_id[curr_node.id] = SearchState.BLACK

    callback(node, SearchState.WHITE, stop_func)
    traverse(node)


def depth_first_search(start_node, callback):
    dfs(start_node, callback, True)


def depth_first_search_undirected(start_node, callback):
    dfs(start_node, callback, False)
