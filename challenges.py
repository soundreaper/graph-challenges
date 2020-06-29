from graph import Graph, Vertex

def numIslands(grid):
    """Take in a grid of 1s (land) and 0s (water) and return the number of islands."""

    graph = Graph(is_directed=False)

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            # position of the item as well as id
            pos = len(grid[i]) * i + j

            if grid[i][j] == 1:
                # add vertex to graph
                graph.add_vertex(pos)

                # look up, bounds and check connection
                if i > 0 and grid[i - 1][j] == 1:
                    adjPos = len(grid[i - 1]) * (i - 1) + j
                    graph.add_edge(pos, adjPos)

                # look left, bounds and check connection
                if j > 0 and grid[i][j - 1] == 1:
                    adjPos = len(grid[i]) * i + (j - 1)
                    graph.add_edge(pos, adjPos)

    return len(graph.find_connected_components())

def timeToRot(grid):
    """
    Take in a grid of numbers, where 0 is an empty space, 1 is a fresh orange, and 2 is a rotten
    orange. Each minute, a rotten orange contaminates its 4-directional neighbors. Return the number
    of minutes until all oranges rot.
    """

    graph = Graph(is_directed=False)
    rotten = list()
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pos = len(grid[i]) * i + j

            if grid[i][j] > 0:
                graph.add_vertex(pos)

                if grid[i][j] == 2:
                    rotten.append(pos)

                if i > 0 and grid[i - 1][j] > 0:
                    adjPos = len(grid[i - 1]) * (i - 1) + j
                    graph.add_edge(pos, adjPos)

                if j > 0 and grid[i][j - 1] > 0:
                    adjPos = len(grid[i]) * i + (j - 1)
                    graph.add_edge(pos, adjPos)

    if len(graph.find_connected_components()) > 1:
        return -1

    max_depth = 0
    for _, pos in enumerate(rotten):
        depth = graph.bfs_calculate_depth(pos)

        if depth > max_depth:
            max_depth = depth
    return max_depth


def courseOrder(numCourses, prerequisites):
    """Return a course schedule according to the prerequisites provided."""

    graph = Graph(is_directed=True)

    for _, req in enumerate(prerequisites):

        if not graph.contains_id(req[0]):
            graph.add_vertex(req[0])

        if not graph.contains_id(req[1]):
            graph.add_vertex(req[1])

        graph.add_edge(req[1], req[0])

    visited = set()
    return graph.get_connected(0, visited.add)