import math
from typing import NamedTuple


class Coords(NamedTuple):
    x: int
    y: int


class Vertex:

    def __init__(self, id):
        self.id = id
        self.prev = None
        self.edges = []


class Edge(NamedTuple):
    weight: int
    vtx: Vertex


neighbor_edges = {Coords(-1, 0), Coords(0, -1)}


def main():
    risk_coords, tile_width, tile_height = parse_input('./test')
    num_tiles_x = 5
    num_tiles_y = 5

    start = Coords(0, 0)
    end = Coords((tile_width * num_tiles_x) - 1, (tile_height * num_tiles_y) - 1)

    vertexes = get_graph(risk_coords, tile_height, tile_width, num_tiles_x, num_tiles_y)
    print('num nodes: ', len(vertexes))
    total_risk = dijkstra(vertexes, vertexes[start], vertexes[end])
    print(total_risk)


# noinspection DuplicatedCode
class PriorityQueue:

    def __init__(self, starting_elts):
        self.tree = {}
        self.dist_map = {}
        self.processed = set()
        for node_id, priority in starting_elts:
            self.push(node_id, priority)

    def empty(self):
        return len(self.processed) == len(self.dist_map)

    def remove_id(self, node_id, node, parent):
        node['ids'].remove(node_id)
        self.processed.add(node_id)
        if not node['ids']:
            self.delete_node(node, parent)

    def modify_priority(self, node_id, new_priority):
        prev_priority = self.dist_map[node_id]
        parent = None
        curr_node = self.tree
        while True:
            if curr_node['priority'] == prev_priority:
                self.remove_id(node_id, curr_node, parent)
                break
            parent = curr_node
            if curr_node['priority'] < prev_priority:
                curr_node = curr_node['less']
            if curr_node['priority'] > prev_priority:
                curr_node = curr_node['more']

        self.push(node_id, new_priority)

    def push(self, node_id, priority):
        self.dist_map[node_id] = priority
        num_left = (len(self.dist_map) - len(self.processed))
        if num_left % 1000 == 0:
            print(f'dist_map={num_left}')
        curr_node = self.tree
        if 'priority' not in curr_node:
            curr_node['priority'] = priority
            curr_node['ids'] = []
        while True:
            if curr_node['priority'] == priority:
                curr_node['ids'].append(node_id)
                break
            if curr_node['priority'] > priority:
                if 'less' not in curr_node:
                    next_node = {'priority': priority, 'ids': []}
                    curr_node['less'] = next_node
                else:
                    next_node = curr_node['less']
            if curr_node['priority'] < priority:
                if 'more' not in curr_node:
                    next_node = {'priority': priority, 'ids': []}
                    curr_node['more'] = next_node
                else:
                    next_node = curr_node['more']
            curr_node = next_node

    def delete_node(self, node_to_delete, parent):
        children = []
        if 'less' in node_to_delete:
            children.append(node_to_delete['less'])
        if 'more' in node_to_delete:
            children.append(node_to_delete['more'])

        if len(children) == 2:
            new_node, new_child = sorted(children,
                                         key=lambda child: math.abs(child['priority'] - node_to_delete['priority']))
            if node_to_delete['less'] == new_node:
                c_node = new_node
                while 'more' in c_node:
                    c_node = c_node['more']
                c_node['more'] = new_child
            else:
                c_node = new_node
                while 'less' in c_node:
                    c_node = c_node['less']
                c_node['less'] = new_child

        if len(children) == 1:
            new_node = children[0]

        if parent:
            if len(children) == 0:
                del parent['less']
            else:
                parent['less'] = new_node
        else:
            if len(children) == 0:
                self.tree = {}
            else:
                self.tree = new_node

    def pop_min(self):
        parent = None
        curr_node = self.tree
        while 'less' in curr_node:
            parent = curr_node
            curr_node = curr_node['less']

        node_id = curr_node['ids'][0]
        self.remove_id(node_id, curr_node, parent)

        return node_id


def dijkstra(vertexes, source, destination):
    dists = {k: math.inf for k in vertexes.keys()}

    # starting node guaranteed to be smallest
    dists[source.id] = 0
    queue = PriorityQueue([*dists.items()])
    while not queue.empty():
        current_node = vertexes[queue.pop_min()]

        for weight, neighbor in current_node.edges:
            if neighbor.id in queue.processed:
                continue
            curr_neighbor_dist = queue.dist_map[neighbor.id]
            new_dist = queue.dist_map[current_node.id] + weight

            if new_dist < curr_neighbor_dist:
                queue.modify_priority(neighbor.id, new_dist)

            if destination.id in queue.processed:
                return queue.dist_map[destination.id]
    raise "destination not in vertexes"


def get_graph(risk_coords, tile_height, tile_width, num_tiles_x, num_tiles_y):
    vertexes = {}

    def calc_risk(coords):
        risk = risk_coords[Coords(coords.y % tile_height, coords.x % tile_width)]
        tile_coords = Coords(coords.x // tile_width, coords.y // tile_height)
        risk += tile_coords.x + tile_coords.y
        while risk > 9:
            risk -= 9
        return risk

    for y in range(num_tiles_y * tile_height):
        for x in range(num_tiles_x * tile_width):
            # no risk added for starting node
            vertex_coords = Coords(x, y)
            curr_vtx_risk = calc_risk(vertex_coords)
            vertex = Vertex(vertex_coords)
            vertexes[vertex_coords] = vertex

            for dx, dy in neighbor_edges:
                edge_coords = Coords(x + dx, y + dy)
                if edge_coords in vertexes:
                    vertexes[edge_coords].edges.append(Edge(curr_vtx_risk, vertex))
                    vertex.edges.append(Edge(calc_risk(edge_coords), vertexes[edge_coords]))
    return vertexes


def in_bounds(coord, bx, by):
    return bx[0] <= coord.x < bx[1] and by[0] <= coord.y < by[1]


def parse_input(path="./input"):
    with open(path) as f:
        lines = f.read().strip().split()

    risk_coords = {Coords(x, y): int(lines[y][x]) for y in range(len(lines)) for x in range(len(lines[0]))}
    return risk_coords, len(lines), len(lines[0])


if __name__ == '__main__':
    main()
