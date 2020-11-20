import yaml, os, flask, numpy

def get_configs(path='configs') -> dict:
    result = dict()
    
    for config in os.listdir(path):
        if config.endswith('yaml'):
            with open(os.path.join(path, config), 'r') as f:
                tmp = yaml.load(f, Loader=yaml.FullLoader)
                if tmp is not None:
                    result |= tmp

    return result

def create_app(key: str) -> flask.Flask:
    app = flask.Flask(__name__)
    app.config['SECRET_KEY'] = key

    return app

def checkCorrectness(height: str, width: str) -> bool:
    for number in (height, width):
        if not number.isdigit():
            return False

        if '.' in number or '-' in number:
            return False

        if int(number) < 2:
            return False

    return True

def matrixFromDict(height: int, width: int, form: dict) -> tuple[numpy.array]:
    matrix = numpy.zeros(height*width, dtype=numpy.int)
    obstacles = []

    for key in form:
        if form[key] == 'on':
            i, j = map(int, key)
            matrix[i*height + j] = 1
            obstacles.append([i, j])

    return matrix, numpy.array(obstacles)

class Node:
    def __init__(self, parent: tuple=None, position: tuple=None):
        self.position = position
        self.parent = parent

        self.f = 0
        self.g = 0
        self.h = 0

    def __eq__(self, other: tuple) -> bool:
        return self.position == other.position

    def __str__(self) -> bool:
        return f'({self.position[0]}, {self.position[1]})'

def astar(maze: list[list], start: tuple, end: tuple) -> list[tuple]:

    start_node = Node(None, start)
    end_node = Node(None, end)

    open_nodes = [start_node]
    closed_nodes = []

    while open_nodes:
        current_node = open_nodes[0]
        current_idx = 0
        for idx, node in enumerate(open_nodes):
            if node.f < current_node.f:
                current_node = node
                current_idx = idx

        open_nodes.pop(current_idx)
        closed_nodes.append(current_node)

        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]

        children = []
        allowed_moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for x, y in allowed_moves:
            new_x = (current_node.position[0] + x)
            new_y = (current_node.position[1] + y)

            if (new_x > (len(maze) - 1) or new_x < 0 or
               (new_y > len(maze[new_x]) - 1) or new_y < 0):
               continue

            if maze[new_x][new_y] != 0:
                continue

            new_node = Node(current_node, (new_x, new_y))
            children.append(new_node)

        for child in children:
            if child in closed_nodes: continue

            child.g = current_node.g + 1
            child.h = (((child.position[0] - child.position[0]) ** 2) +
                       ((child.position[1] - child.position[1]) ** 2))
            child.f = child.g + child.h

            try:
                found_node = open_nodes[open_nodes.index(child)]
                if child.g > found_node.g:
                    continue
            except ValueError:
                pass

            open_nodes.append(child)
