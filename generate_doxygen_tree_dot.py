import os
import argparse
from anytree import Node
from anytree.exporter import DotExporter

def build_tree(path):
    root_name = os.path.basename(os.path.abspath(path)) or os.path.abspath(path)
    root = Node(root_name)
    nodes = {os.path.abspath(path): root}

    for parent, dirs, files in os.walk(path):
        parent = os.path.abspath(parent)
        parent_node = nodes[parent]

        for d in dirs:
            full = os.path.abspath(os.path.join(parent, d))
            nodes[full] = Node(d, parent=parent_node)

        for f in files:
            Node(f, parent=parent_node)

    from anytree import RenderTree
    for pre, fill, node in RenderTree(root):
        print("%s%s" % (pre, node.name))

    return root

def main():
    parser = argparse.ArgumentParser(description="Generate a DOT file of a directory tree.")
    parser.add_argument("directory", help="Path to the root directory.")
    parser.add_argument("-o", "--output", default="tree.dot", help="Output DOT filename (default: tree.dot).")
    args = parser.parse_args()

    root = build_tree(args.directory)
    DotExporter(root).to_dotfile(args.output)
    print(f"DOT file written to {args.output}")

if __name__ == "__main__":
    main()
