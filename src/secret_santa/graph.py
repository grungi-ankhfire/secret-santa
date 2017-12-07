class Vertex(object):
    def __init__(self, node, item, nodelist):
        self.i = node
        self.item = item
        self.nodelist = nodelist

    def __hash__(self):
        return self.i

    def reaches(self, vertex):
        if isinstance(vertex, int):
            return vertex in self.nodelist

        return self.reaches(vertex.i)

    def __str__(self):
        return str(self.item)

    def __repr__(self):
        return self.__str__()


class Graph(object):
    def __init__(self):
        self.vlist = {}

    def add(self, node, item, *nodelist):
        vertex = Vertex(node, item, *nodelist)
        self.vlist[node] = vertex

    def hamiltonian(self, current=None, pending=None, destiny=None):
        if pending is None:
            pending = self.vlist.values()

        result = None

        if current is None:
            for current in pending:
                result = self.hamiltonian(
                    current, [x for x in pending if x is not current], current)
                if result is not None:
                    break
        else:
            if pending == []:
                if current.reaches(destiny):
                    return [current]
                else:
                    return None

            for x in [self.vlist[v] for v in current.nodelist]:
                if x in pending:
                    result = self.hamiltonian(
                        x, [y for y in pending if y is not x], destiny)
                    if result is not None:
                        result = [current] + result
                        break

        return result
