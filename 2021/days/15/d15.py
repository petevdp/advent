import math
from typing import NamedTuple
from dataclasses import dataclass


class Coords(NamedTuple):
    x: int
    y: int


class Vertex:

    def __init__(self, risk, dist, coords):
        self.risk = risk
        self.dist = dist
        self.coords = coords

        self.prev = None
        self.edges = []


def main():
    start, destination, vertexes = parse_input()
    for vertex in vertexes.values():
        print(vertex.coords, [v.coords for v in vertex.edges])

    print(dijkstra(vertexes, start, destination))


def dijkstra(vertexes, source, destination):
    unvisited = {**vertexes}

    current_node = unvisited[source.coords]
    while unvisited:
        if len(unvisited) % 100 == 0:
            print('unvisited: ', len(unvisited))
        # first element is always starting vertex
        for neighbor in current_node.edges:
            if neighbor.coords not in unvisited:
                continue
            new_dist = current_node.dist + neighbor.risk
            if new_dist < neighbor.dist:
                neighbor.dist = new_dist

        del unvisited[current_node.coords]
        if destination.coords not in unvisited:
            return destination.dist
        current_node = unvisited[min(unvisited.keys(), key=lambda v: unvisited[v].dist)]
    print(unvisited)


def parse_input(path="./input"):
    neighbor_edges = {Coords(-1, 0), Coords(0, -1)}
    with open(path) as f:
        lines = f.read().strip().split()

    coords = [Coords(x, y) for y in range(len(lines)) for x in range(len(lines[0]))]
    vertexes = {}
    for y in range(len(lines)):
        for x in range(len(lines[0])):
            # no risk added for starting node
            vertex_coords = Coords(x, y)

            if x == 0 and y == 0:
                risk = 0
                dist = 0
                vertex = Vertex(risk, dist, vertex_coords)
            else:
                risk = int(lines[y][x])
                dist = math.inf
                vertex = Vertex(risk, dist, vertex_coords)
            vertexes[vertex_coords] = vertex

            for dx, dy in neighbor_edges:
                edge_coords = Coords(x + dx, y + dy)
                if edge_coords in coords:
                    vertexes[edge_coords].edges.append(vertex)
                    vertex.edges.append(vertexes[edge_coords])
    start = vertexes[Coords(0, 0)]
    destination = vertexes[Coords(len(lines[0]) - 1, len(lines) - 1)]
    return start, destination, vertexes


if __name__ == '__main__':
    main()
