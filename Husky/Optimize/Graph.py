import numpy as np
import heapq

class Graph:
    def __init__(self,vertices=None):
        if vertices is None:
            self.vertices = {}
        else:
            # Need to check data-structure
            self.vertices = vertices

    def addvertex(self,name,edges):
        self.vertices[name] = edges

    def shortestpath(self,start,end):
        '''
        Dijkstras algorithm
        '''
        distances = {}
        previous = {}
        nodes = {}

        for vertex in self.vertices:
            if vertex == start:
                distances[vertex] = 0
                heapq.heappush(nodes,[0,vertex])
            else:
                distances[vertex] = sys.maxsize
                heapq.heappush(nodes,[sys.maxsize,vertex])
            previous[vertex] = None

        while nodes:
            smallest = heapq.heappop(nodes)[1]
            if smallest == end:
                path = []
                while previous[smallest]:
                    path.append(smallest)
                    smallest = previous[smallest]
                return path
            if distances[smallest] == sys.maxsize:
                break

            for neighbor in self.vertices[smallest]:
                alt = distances[smallest] + self.vertices[smallest][neighbor]
                if alt < distances[neighbor]:
                    distances[neighbor] = alt
                    previous[neighbor] = smallest
                    for n in nodes:
                        if n[1] == neighbor:
                            n[0] = alt
                            break
                    heapq.heapify(nodes)

        return distances


    def __str__(self):
        return str(self.vertices)