class Tree:
    def __init__(self, root):
        self.root = root
        self.list_of_nodes = []
        self.list_of_nodes.append(self.root)

    def get_childes(self, parent):
        childes = []
        for node in self.list_of_nodes:
            # check that the length of child be grater than the parent
            # and the path of parent exactly repeated at the first of child's path
            if (len(node.path) == len(parent.path)+1) and (parent.path == node.path[:-1]):
                childes.append(node)
        return childes

    def get_leafs(self):
        leafs = []
        for node in self.list_of_nodes:
            if node.leaf_flag:
                leafs.append(node)
        return leafs