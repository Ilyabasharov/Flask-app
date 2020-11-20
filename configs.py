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

def matrixFromDict(height: int, width: int, form: dict) -> numpy.array:
    matrix = numpy.zeros(height*width, dtype=numpy.int)

    for key in form:
        if form[key] == 'on':
            i, j = key
            matrix[int(i)*height + int(j)] = 1

    return matrix

class Node():
    def __init__(self, parent: tuple=None, position: tuple=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other: tuple) -> bool:
        return self.position == other.position

def manhattan(a: tuple, b: tuple) -> float:
    return ((a[0] - b[0]) ** 2) + ((a[1] - b[1]) ** 2)

def astar(matrix: list[list], start: tuple, end: tuple) -> list[tuple]:

    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    open_list, closed_list = [], []

    open_list.append(start_node)

    while len(open_list) > 0:

        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        open_list.pop(current_index)
        closed_list.append(current_node)

        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]

        children = []
        for new_position in [
        (0, -1), (0, 1),(-1, 0), (1, 0),
        (-1, -1), (-1, 1), (1, -1), (1, 1)]:

            node_position = (
                current_node.position[0] + new_position[0], 
                current_node.position[1] + new_position[1])

            if node_position[0] > (len(matrix) - 1) \
            or node_position[0] < 0 \
            or node_position[1] > (len(matrix[len(matrix) - 1]) - 1) \
            or node_position[1] < 0:
                continue

            if matrix[node_position[0]][node_position[1]] != 0:
                continue

            new_node = Node(current_node, node_position)
            children.append(new_node)

        for child in children:
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            child.g = current_node.g + 1
            child.h = manhattan(child.position, end_node.position)
            child.f = child.g + child.h

            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            open_list.append(child)
