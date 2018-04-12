class Node(object):
    """Node object.

        # Attribute
            id: int, symbolic id for Function. This id is not assigned for each node object.
            children: list of Node object, children of this node.
    """
    def __init__(self, func_id=-1):
        self.func_id = func_id
        self.children = None


class Function(object):
    """Function object.

        # Attribute
            n_childen: int, the number of children of this function.
            eval: function, function of node to evaluate.
    """
    def __init__(self, n_children, eval=None):
        self.n_children = n_children
        self.eval = eval


def set_id(node, func_id):
    """function for setting id to node object.

            # Arguments
                node: Node object, target node.
                id: int, id of node.
    """
    # TODO implement a method to check if id is correct type and range
    node.func_id = func_id


def get_n_children(func_id, function_dict):

    # TODO implement a method to check if id is correct type
    func = function_dict[func_id]
    return func.n_children


def set_children(node, children):
    """ TODO: implement a method to check follows:
              the number of children of node = len(children)
              children is list
    """
    node.children = children


def get_parent_node(root, target_node):
    """function for searching parent node of target node.

        # Arguments
            root: Node object, root node.
            target_node: Node object, target node.

        # Returns
            Position of target_node in parent node and node object of parent node.
    """

    def find_parent_node(current_node, target_node):
        children = current_node.children
        if children is None:
            raise ValueError('current_node is a terminal node')

        for i, c in enumerate(children):
            if c is target_node:
                return i, current_node
            else:
                return find_parent_node(c, target_node)

    if target_node is root:
        raise ValueError('There is no parent of root.')

    try:
        pos, parent = find_parent_node(root, target_node)
    except ValueError:
        raise ValueError('root and target_node are not in the same tree.')

    return pos, parent


def get_all_node(root):
    """
    function for getting all node in the solution

    :param root: Node object. root node of target solution.
    :return: list of Node object. All node in the solution
    """

    def add_children(current_node, nodes=[]):
        children = current_node.children

        if children is None:
            return
        for c in children:
            nodes.append(c)
            add_children(c, nodes)

    nodes = []
    add_children(root, nodes)

    return nodes

