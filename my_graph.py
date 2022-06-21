from graph import Graph
if __name__ == '__main__':
    g = Graph()

    g.add_vertex('A')
    g.add_vertex('B')
    g.add_vertex('C')
    g.add_vertex('D')
    g.add_vertex('E')

    g.add_edge('A','B',15)
    g.add_edge('A','C',12)
    g.add_edge('B','E',5)
    g.add_edge('B','D',13)
    g.add_edge('B','C',6)
    g.add_edge('D','C',6)



    print(g.kruscal())