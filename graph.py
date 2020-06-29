from collections import deque
from random import choice

class Vertex(object):
    """
    Defines a single vertex and its neighbors.
    """

    def __init__(self, vertex_id):
        """
        Initialize a vertex and its neighbors dictionary.
        
        Parameters:
        vertex_id (string): A unique identifier to identify this vertex.
        """
        self.__id = vertex_id
        self.__neighbors_dict = {} # id -> object

    def add_neighbor(self, vertex_obj):
        """
        Add a neighbor by storing it in the neighbors dictionary.

        Parameters:
        vertex_obj (Vertex): An instance of Vertex to be stored as a neighbor.
        """
        self.__neighbors_dict[vertex_obj.get_id()] = vertex_obj

    def __str__(self):
        """Output the list of neighbors of this vertex."""
        neighbor_ids = list(self.__neighbors_dict.keys())
        return f'{self.__id} adjacent to {neighbor_ids}'

    def __repr__(self):
        """Output the list of neighbors of this vertex."""
        return self.__str__()

    def get_neighbors(self):
        """Return the neighbors of this vertex."""
        return list(self.__neighbors_dict.values())

    def get_id(self):
        """Return the id of this vertex."""
        return self.__id


class Graph:
    """ Graph Class
    Represents a directed or undirected graph.
    """
    def __init__(self, is_directed=True):
        """
        Initialize a graph object with an empty vertex dictionary.

        Parameters:
        is_directed (boolean): Whether the graph is directed (edges go in only one direction).
        """
        self.__vertex_dict = {} # id -> object
        self.__is_directed = is_directed

    def add_vertex(self, vertex_id):
        """
        Add a new vertex object to the graph with the given key and return the vertex.
        
        Parameters:
        vertex_id (string): The unique identifier for the new vertex.

        Returns:
        Vertex: The new vertex object.
        """
        self.__vertex_dict[vertex_id] = Vertex(vertex_id)
        return self.__vertex_dict.get(vertex_id)

    def get_vertex(self, vertex_id):
        """Return the vertex if it exists."""
        if vertex_id not in self.__vertex_dict:
            return None

        vertex_obj = self.__vertex_dict[vertex_id]
        return vertex_obj

    def add_edge(self, vertex_id1, vertex_id2):
        """
        Add an edge from vertex with id `vertex_id1` to vertex with id `vertex_id2`.

        Parameters:
        vertex_id1 (string): The unique identifier of the first vertex.
        vertex_id2 (string): The unique identifier of the second vertex.
        """
        if self.get_vertex(vertex_id1) is None:
            self.add_vertex(vertex_id1)

        if self.get_vertex(vertex_id2) is None:
            self.add_vertex(vertex_id2)
        
        self.__vertex_dict[vertex_id1].add_neighbor(self.__vertex_dict[vertex_id2])

        if not self.__is_directed:
            self.__vertex_dict[vertex_id2].add_neighbor(self.__vertex_dict[vertex_id1])
        
    def get_vertices(self):
        """
        Return all vertices in the graph.
        
        Returns:
        List<Vertex>: The vertex objects contained in the graph.
        """
        return list(self.__vertex_dict.values())

    def contains_id(self, vertex_id):
        return vertex_id in self.__vertex_dict

    def __str__(self):
        """Return a string representation of the graph."""
        return f'Graph with vertices: {self.get_vertices()}'

    def __repr__(self):
        """Return a string representation of the graph."""
        return self.__str__()

    def bfs_traversal(self, start_id):
        """
        Traverse the graph using breadth-first search.
        """
        if not self.contains_id(start_id):
            raise KeyError("One or both vertices are not in the graph!")

        # Keep a set to denote which vertices we've seen before
        seen = set()
        seen.add(start_id)

        # Keep a queue so that we visit vertices in the appropriate order
        queue = deque()
        queue.append(self.get_vertex(start_id))

        while queue:
            current_vertex_obj = queue.popleft()
            current_vertex_id = current_vertex_obj.get_id()

            # Process current node
            print('Processing vertex {}'.format(current_vertex_id))

            # Add its neighbors to the queue
            for neighbor in current_vertex_obj.get_neighbors():
                if neighbor.get_id() not in seen:
                    seen.add(neighbor.get_id())
                    queue.append(neighbor)

        return # everything has been processed

    def find_shortest_path(self, start_id, target_id):
        """
        Find and return the shortest path from start_id to target_id.

        Parameters:
        start_id (string): The id of the start vertex.
        target_id (string): The id of the target (end) vertex.

        Returns:
        list<string>: A list of all vertex ids in the shortest path, from start to end.
        """
        if not self.contains_id(start_id) or not self.contains_id(target_id):
            raise KeyError("One or both vertices are not in the graph!")

        # vertex keys we've seen before and their paths from the start vertex
        vertex_id_to_path = {
            start_id: [start_id] # only one thing in the path
        }

        # queue of vertices to visit next
        queue = deque() 
        queue.append(self.get_vertex(start_id))

        # while queue is not empty
        while queue:
            current_vertex_obj = queue.pop() # vertex obj to visit next
            current_vertex_id = current_vertex_obj.get_id()

            # found target, can stop the loop early
            if current_vertex_id == target_id:
                break

            neighbors = current_vertex_obj.get_neighbors()
            for neighbor in neighbors:
                if neighbor.get_id() not in vertex_id_to_path:
                    current_path = vertex_id_to_path[current_vertex_id]
                    # extend the path by 1 vertex
                    next_path = current_path + [neighbor.get_id()]
                    vertex_id_to_path[neighbor.get_id()] = next_path
                    queue.append(neighbor)
                    # print(vertex_id_to_path)

        if target_id not in vertex_id_to_path: # path not found
            return None

        return vertex_id_to_path[target_id]

    def find_vertices_n_away(self, start_id, target_distance):
        """
        Find and return all vertices n distance away.
        
        Arguments:
        start_id (string): The id of the start vertex.
        target_distance (integer): The distance from the start vertex we are looking for

        Returns:
        list<string>: All vertex ids that are `target_distance` away from the start vertex
        """
        visited = set()
        target_vertices = []

        queue = deque()
        queue.append((start_id, 0))
        visited.add(start_id)

        while queue:
            x = queue.pop()

            current_vertex_id = x[0]
            vertex_distance = x[1]

            if vertex_distance == target_distance:
                target_vertices.append(current_vertex_id)

            neighbors = self.get_vertex(current_vertex_id).get_neighbors()

            for neighbor in neighbors:
                if neighbor.get_id() not in visited:
                    queue.append((neighbor.get_id(), vertex_distance + 1))
                    visited.add(neighbor.get_id())
            
        return target_vertices

    def get_connected(self, start_id, visit):
        """
        Helper function that performs bfs and returns a list of connected components
        """
        visited = set()
        queue = deque()
        queue.append(start_id)
        visited.add(start_id)

        while queue:
            v = self.get_vertex(queue.popleft())

            for _, vertex in enumerate(v.get_neighbors()):
                if vertex.get_id() not in visited:
                    queue.append((vertex.get_id()))
                    visited.add(vertex.get_id())
                    visit(vertex.get_id())

        return list(visited)
    
    def is_bipartite(self):
        """
        Return True if the graph is bipartite, and False otherwise.
        """
        queue = deque()
        visited = {}
        current_color = 0

        current_vertex_id = choice(list(self.__vertex_dict.keys()))

        queue.append(current_vertex_id)
        visited[current_vertex_id] = current_color

        while queue:
            current_color ^= 1

            current_vertex_id = queue.popleft()

            neighbors = self.get_vertex(current_vertex_id).get_neighbors()

            for neighbor in neighbors:
                if neighbor.get_id() not in visited.keys():
                    visited[neighbor.get_id()] = current_color

                    queue.append(neighbor.get_id())
                else:
                    if visited[current_vertex_id] == visited[neighbor.get_id()]:
                        return False
        return True

    def find_connected_components(self):
        """
        Return a list of all connected components, with each connected component
        represented as a list of vertex ids.
        """
        vertices = set(self.__vertex_dict.keys())
        components = []

        while vertices:
            component = []
            queue = []
            
            start_id = vertices.pop()

            queue.append(start_id)
            component.append(start_id)

            while queue:
                current_id = queue.pop()
                current_vertex = self.get_vertex(current_id)

                for neighbor in current_vertex.get_neighbors():
                    neighbor_id = neighbor.get_id()
                    
                    if neighbor_id in vertices:
                        vertices.remove(neighbor_id)

                    if neighbor_id not in component:
                        queue.append(neighbor_id)
                        component.append(neighbor_id)

            components.append(component)

        return components
    
    def find_path_dfs_iter(self, start_id, target_id):
        """
        Use DFS with a stack to find a path from start_id to target_id.
        """
        if not self.contains_id(start_id) or not self.contains_id(target_id):
            raise KeyError("One or both vertices are not in the graph!")

        stack = deque()
        stack.append(self.get_vertex(start_id))
        
        paths = {
            start_id: [start_id]
        }

        while stack:
            current_vertex_obj = stack.pop()
            current_vertex_id = current_vertex_obj.get_id()

            if current_vertex_id == target_id:
                break

            neighbors = current_vertex_obj.get_neighbors()

            for neighbor in neighbors:
                if neighbor.get_id() not in paths:
                    stack.append(neighbor)
                    current_path = paths[current_vertex_id]
                    next_path = current_path + [neighbor.get_id()]
                    paths[neighbor.get_id()] = next_path
                    
        if target_id not in paths:
            return None

        return paths[target_id]

    def dfs_traversal(self, start_id):
        """Visit each vertex, starting with start_id, in DFS order."""

        visited = set() # set of vertices we've visited so far

        def dfs_traversal_recursive(start_vertex):
            print(f'Visiting vertex {start_vertex.get_id()}')

            # recurse for each vertex in neighbors
            for neighbor in start_vertex.get_neighbors():
                if neighbor.get_id() not in visited:
                    visited.add(neighbor.get_id())
                    dfs_traversal_recursive(neighbor)
            return

        visited.add(start_id)
        start_vertex = self.get_vertex(start_id)
        dfs_traversal_recursive(start_vertex)
    
    def contains_cycle(self):
        """
        Return True if the directed graph contains a cycle, False otherwise.
        """
        def dfs_cycle(vertex, visited, recursion_stack):
            v_id = vertex.get_id()
            visited.append(v_id)
            neighbors = vertex.get_neighbors()
            for n in neighbors:
                n_id = n.get_id()
                if n_id in visited:
                    recursion_stack.append(True)
                    return
                else:
                    recursion_stack.append(False)
                    dfs_cycle(n, visited, recursion_stack)
            return recursion_stack[-1]
        
        start_id = list(self.__vertex_dict.keys())[0]
        start_obj = self.get_vertex(start_id)
        visited, recursion_stack = [start_id], []
        is_cycle = dfs_cycle(start_obj, visited, recursion_stack)
        return is_cycle
    
    def bfs_calculate_depth(self, start_id):
        """
        Traverse the graph using breadth-first search.
        """
        seen = set()
        seen.add(start_id)
        max_depth = 0

        queue = deque()
        queue.append((self.get_vertex(start_id), 0))

        while queue:
            current_vertex_obj = queue.popleft()
            current_depth = current_vertex_obj[1]
            current_vertex_id = current_vertex_obj[0].get_id()
            if current_depth > max_depth:
                max_depth = current_depth

            for neighbor in current_vertex_obj[0].get_neighbors():
                if neighbor.get_id() not in seen:
                    seen.add(neighbor.get_id())
                    queue.append((neighbor, current_depth + 1))

        return max_depth

    def topological_sort(self):
        """
        Return a valid ordering of vertices in a directed acyclic graph.
        If the graph contains a cycle, throw a ValueError.
        """
        stack = []
        visited = set()
        
        if self.contains_cycle():
            raise ValueError('Graph not DAG')

        def dfs_topological_sort(vertex):
            visited.add(vertex.get_id())
            
            for neighbor in vertex.get_neighbors():
                if neighbor.get_id() not in visited:
                    dfs_topological_sort(neighbor)

            stack.append(vertex.get_id())

        for vertex in list(self.__vertex_dict.values()):
            if vertex.get_id() not in visited:
                dfs_topological_sort(vertex)

        return stack[::-1]