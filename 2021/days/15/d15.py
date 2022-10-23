import math
from typing import NamedTuple
import heapq


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
    risk_coords, tile_width, tile_height = parse_input()
    num_tiles_x = 5
    num_tiles_y = 5

    start = Coords(0, 0)
    end = Coords((tile_width * num_tiles_x) - 1, (tile_height * num_tiles_y) - 1)

    vertexes = get_graph(risk_coords, tile_height, tile_width, num_tiles_x, num_tiles_y)
    print('num nodes: ', len(vertexes))
    total_risk = dijkstra(vertexes, vertexes[start], vertexes[end])
    print(total_risk)


def dijkstra(vertexes, source, destination):
    # starting node guaranteed to be smallest
    processed = {}
    queue = [(math.inf, key) for key in vertexes.keys()]
    queue.insert(0, (0, source.id))
    heapq.heapify(queue)
    dists = {k: v for v, k in queue}
    while queue:
        curr_node_dist, vtx_id = heapq.heappop(queue)
        current_node = vertexes[vtx_id]
        processed[vtx_id] = curr_node_dist

        for weight, neighbor in current_node.edges:
            if neighbor.id in processed:
                continue
            neighbor_dist = dists[neighbor.id]
            new_dist = curr_node_dist + weight
            if new_dist < neighbor_dist:
                dists[neighbor.id] = new_dist
                heapq.heappush(queue, (new_dist, neighbor.id))

        if destination.id in processed:
            return processed[destination.id]
    raise "destination not in vertexes"


# we could do a straight coords lookup instead of creating this graph
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
