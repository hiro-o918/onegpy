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


def get_parent_node(parent_node, target_node):
    """function for searching parent node of target node.

        # Arguments
            parent_node: Node object, current node.
            target_node: Node object, target node.

        # Returns
            Node object of parent node.
    """
    children = parent_node.children
    for i, c in enumerate(children):
        if c is target_node:
            return i, parent_node
        else:
            return get_parent_node(c, target_node)


def get_all_node(root, list = []):
    """
    function for getting all node in the solution

    :param root: Node object. root node of target solution.
    :return: list of Node object. All node in the solution
    """

    children = root.children
    for n in enumerate(children):
        list.append(n)
        get_all_node(n, list)

    return list

