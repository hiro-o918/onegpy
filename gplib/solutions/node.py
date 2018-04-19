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
            n_children: int, the number of children of this function.
            eval: function, function of node to evaluate.
    """

    def __init__(self, n_children, f_eval=None):
        self.n_children = n_children
        self.f_eval = f_eval

    def __call__(self, x):
        return self.f_eval(x)


def build_func(f_eval, n_children):
    def eval_func(x):
        return f_eval(x)

    func = Function(n_children, f_eval=eval_func)

    return func


def set_id(node, func_id):
    """function for setting id to node object.

            # Arguments
                node: Node object, target node.
                id: int, id of node.
    """
    _node_checker(node)
    _func_id_checker(func_id)
    node.func_id = func_id


def get_n_children(func_id, function_dict):
    _func_id_checker(func_id)
    func = function_dict[func_id]

    return func.n_children


def set_children(node, children):
    """ TODO: implement a method to check follows:
              the number of children of node = len(children)
    """
    _nodes_checker(node)
    _children_checker(children)

    node.children = children


def get_parent_node(root, target_node):
    """function for searching parent node of target node.

        # Arguments
            root: Node object, root node.
            target_node: Node object, target node.

        # Returns
            Position of target_node in parent node and node object of parent node.
    """

    def find_parent_node(current_node):
        if current_node.children is None:
            return

        children = current_node.children
        p = None
        for i, c in enumerate(children):
            if c is target_node:
                return i, current_node
            else:
                p = p or find_parent_node(c)

        return p

    _nodes_checker(root, target_node)
    if target_node is root:
        msg = 'There is no parent of root.'
        raise ValueError(msg)

    pos, parent = find_parent_node(root) or (None, None)

    if pos is None or parent is None:
        msg = 'Invalid arguments: cannot find parent.'
        raise ValueError(msg)

    return pos, parent


def get_all_node(root):
    """
    function for getting all node in the solution

    :param root: Node object. root node of target solution.
    :return: list of Node object. All node in the solution
    """

    _node_checker(root)
    nodes = [root]

    def add_children_to_nodes(current_node):
        children = current_node.children
        nonlocal nodes
        if children is None:
            return
        for c in children:
            nodes.append(c)
            add_children_to_nodes(c)

    add_children_to_nodes(root)

    return nodes


def _func_id_checker(func_id):
    if not isinstance(func_id, int):
        typ = TypeError
        msg = 'Expected type: {} not {}.'.format(int, type(func_id))
    elif func_id < 0:
        typ = ValueError
        msg = 'Expected condition: func_id >= 0.'
    else:
        return

    raise typ(msg)


def _node_checker(node):
    if not isinstance(node, Node):
        typ = TypeError
        msg = 'Expected type: {} not {}.'.format(Node, type(node))
    else:
        return

    raise typ(msg)


def _nodes_checker(*nodes):
    for node in nodes:
        _node_checker(node)


def _children_checker(children):
    if not isinstance(children, list):
        raise TypeError('Expected type: {}'.format(list))

    _nodes_checker(*children)
