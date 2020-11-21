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
    print(form)
    for key in form:
        if form[key] == 'on':
            i, j = map(int, key)
            matrix[i*width + j] = 1
            obstacles.append([i, j])

    return matrix, numpy.array(obstacles)

class Node:
    def __init__(self, point: tuple):
        self.x = point[0]
        self.y = point[1]
        self.parent = None
        self.H = 0
        self.G = 0

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y
    
    def __hash__(self) -> int:
        return (hash(self.x) ^ hash(self.y))

def manhattan_distance(a: Node, b: Node) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)

def walkable(node: Node, grid: list[list]) -> bool:
    if node.x >= 0 and node.y >= 0 and node.x < len(grid[0]) and node.y < len(grid):
        return grid[node.y][node.x] == 0
    else:
        return False

def retrace(node: Node) -> list[tuple]:
    path, current = [], node
    
    while current.parent:
        path.append(current)
        current = current.parent
    return [(p.y, p.x) for p in path]

def astar(
    grid: list[list], 
    start: tuple=(0, 0), 
    end: tuple=(9, 9)) -> list[tuple]:
    
    start = Node(start)
    end = Node(end)
    
    if start == end:
        return
    
    open_set, closed_set = set(), set()
    open_set.add(start)

    while open_set:
        c = min(open_set, key=lambda node: node.G + node.H)
        
        if c == end:
            return retrace(c)
        
        open_set.remove(c)
        closed_set.add(c)
        
        neighbors = []
        
        for x, y in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            neighbors.append(Node((c.x + x, c.y + y)))
            
        for neighbor in neighbors:
            if neighbor not in closed_set and walkable(neighbor, grid):
                if neighbor in open_set:
                    new_G = c.G + 1
                    
                    if neighbor.G > new_G:
                        neighbor.G = new_G
                        neighbor.parent = c
                else:
                    neighbor.G = c.G + 1
                    neighbor.H = manhattan_distance(neighbor, end)
                    neighbor.parent = c
                    open_set.add(neighbor)
                    
    return None
