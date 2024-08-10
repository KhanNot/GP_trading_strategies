from deap import gp
import pygraphviz as pgv


def plot_tree(expr, name:str = "tree"):
    nodes, edges, labels = gp.graph(expr)

    ### Graphviz Section ###

    g = pgv.AGraph()
    g.add_nodes_from(nodes)
    g.add_edges_from(edges)
    g.layout(prog="dot")

    for i in nodes:
        n = g.get_node(i)
        n.attr["label"] = labels[i]

    g.draw(rf"./trees/{name}.png")