from deap import gp
import pygraphviz as pgv


def replace_labels(labels,old,new):
    indices = [i for i, value in enumerate(list(labels.values())) if value == old]
    for i in indices:
        labels[i]=new
    return labels

def plot_tree(expr, name: str = "tree"):
    nodes, edges, labels = gp.graph(expr)
    labels = replace_labels(labels, 'or_','OR')
    labels = replace_labels(labels, 'and_','AND')
    labels = replace_labels(labels, 'gt','>')

    g = pgv.AGraph(strict=False, directed=False)
    g.add_nodes_from(nodes)
    g.add_edges_from(edges)
    g.graph_attr["ranksep"] = "0.1"

    # Improve node and label spacing and change the node shape to "box"
    for i in nodes:
        n = g.get_node(i)
        n.attr["label"] = labels[i]
        n.attr["fontsize"] = "10"  # Adjust font size for better readability
        n.attr["fontname"] = "Arial Bold" 
        n.attr["width"] = "0.5"    # Adjust node width
        n.attr["height"] = "0.05"   # Adjust node height
        n.attr["margin"] = "0.1"   # Add margin to prevent label overlap within nodes
        n.attr["shape"] = "box"    # Set the shape of the node to "box" to encapsulate in a block
        n.attr["style"] = "rounded" # Optional: Use rounded corners for the box
    for e in edges:
        edge = g.get_edge(e[0], e[1])
        edge.attr["arrowhead"] = "none"  # Remove arrows, making it a line
        edge.attr["penwidth"] = "1" 


    g.layout(prog="dot")

    # Save the tree as an image
    g.draw(rf"./trees/{name}.png")