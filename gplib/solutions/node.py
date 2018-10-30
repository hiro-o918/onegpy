import copy


class Node(object):
    """Node object.

        # Attribute
            id: int, symbolic id for Function. This id is not assigned for each node object.
            children: list of Node object, children of this node.
    """

    def __init__(self, func_id=-1):
        self.func_id = func_id
        self.children = []

    @property
    def is_terminal(self):
        return not self.children


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


def set_id(node, func_id):
    """function for setting id to node object.

            # Arguments
                node: Node object, target node.
                id: int, id of node.
    """
    node_checker(node)
    func_id_checker(func_id)
    node.func_id = func_id


def get_n_children(func_id, function_dict):
    func_id_checker(func_id)
    func = function_dict[func_id]

    return func.n_children


def set_children(node, children):
    """ TODO: implement a method to check follows:
              the number of children of node = len(children)
    """
    node_checker(node)
    children_checker(children)

    node.children = children


def copy_node(node, deep=False):
    if not deep:
        new_node = node.__class__(node.func_id)
        if node.children:
            new_node.children = [copy.copy(c) for c in node.children]

        return new_node
    else:
        return copy.deepcopy(node)


def copy_nodes_along_graph(graph):
    """
    Copy node object from ``root`` to the target node based on ``graph''
    This method differs from deepcopy(root) in that it copies only the nodes along ``graph''.
    :param graph: list of ``(i, Node object)'' where ``i'' is the index of the next node of graph
    and ``Node object'' is the parent node. This graph is obtained by using ``get_parent_node''.
    :return: the index of target node node in the parent, copied the target node object and copied root object.
    """
    previous_pos = None
    current_node = None
    root = None
    for pos, node in graph:
        copied_node = copy_node(node)
        if previous_pos is None:
            root = copied_node
        else:
            current_node.children[previous_pos] = copied_node
        current_node = copied_node
        previous_pos = pos

    return previous_pos, current_node, root


def get_parent_node(root, target_node):
    """function for searching parent node of target node.

        :param root: Node object, root node.
        :param target_node: Node object, target node.

        :return Position of target_node in parent node, node object of parent node
    """

    def find_parent_node(current_node):
        if current_node.is_terminal:
            return

        children = current_node.children
        p = None
        for i, c in enumerate(children):
            if c is target_node:
                return i, current_node
            else:
                p = p or find_parent_node(c)

                if p is not None:
                    break
        return p

    nodes_checker([root, target_node])
    if target_node is root:
        msg = 'There is no parent of root.'
        raise ValueError(msg)

    pos, parent = find_parent_node(root) or (None, None)
    if pos is None or parent is None:
        msg = 'Invalid arguments: cannot find parent.'
        raise ValueError(msg)

    return pos, parent


def get_graph_to_target(root, target_node):
    """function for searching a graph from root node to a target node.

        :param root: Node object, root node.
        :param target_node: Node object, target node.

        :return Graph from ``root'' to ``target_node''
    """
    graph = []

    def find_parent_node(current_node):
        nonlocal graph
        if current_node.is_terminal:
            return

        children = current_node.children
        p = None
        for i, c in enumerate(children):
            graph.append((i, current_node))
            if c is target_node:
                return i, current_node
            p = p or find_parent_node(c)
            if p is None:
                graph.pop()
            else:
                break

        return p

    nodes_checker([root, target_node])
    if target_node is root:
        msg = 'There is no parent of root.'
        raise ValueError(msg)

    pos, parent = find_parent_node(root) or (None, None)
    if pos is None or parent is None:
        msg = 'Invalid arguments: cannot find parent.'
        raise ValueError(msg)

    return graph


def get_all_node(root):
    """
    function for getting all node in the solution

    :param root: Node object. root node of target solution.
    :return: list of Node object. All node in the solution
    """

    node_checker(root)
    nodes = [root]

    def add_children_to_nodes(current_node):
        children = current_node.children
        nonlocal nodes
        if current_node.is_terminal:
            return
        for c in children:
            nodes.append(c)
            add_children_to_nodes(c)

    add_children_to_nodes(root)

    return nodes


def calc_node_depth(node):
    d_list = []

    def cal_depth(c_node, depth):
        if not c_node.is_terminal:
            for c in c_node.children:
                cal_depth(c, depth+1)
        else:
            d_list.append(depth)

    cal_depth(node, 0)

    return max(d_list)


def get_all_terminal_nodes(root):
    """
    function for getting all terminal node in the solution

    :param root: Node object. root node of target solution.
    :return: list of Node object. All terminal node in the solution
    """

    node_checker(root)
    terminal_nodes = []

    def add_children_to_nodes(current_node):
        children = current_node.children
        nonlocal terminal_nodes
        if current_node.is_terminal:
            terminal_nodes.append(current_node)
            return
        for c in children:
            add_children_to_nodes(c)

    add_children_to_nodes(root)

    return terminal_nodes


def get_all_nonterminal_nodes(root):
    """
    function for getting all terminal node in the solution

    :param root: Node object. root node of target solution.
    :return: list of Node object. All terminal node in the solution
    """

    node_checker(root)
    nonterminal_nodes = []

    def add_children_to_nodes(current_node):
        children = current_node.children
        nonlocal nonterminal_nodes
        if not current_node.is_terminal:
            nonterminal_nodes.append(current_node)
            for c in children:
                add_children_to_nodes(c)

    add_children_to_nodes(root)

    return nonterminal_nodes


def get_all_terminal_points(root):
    """
    function for getting all terminal points in the solution
    this function is for crossover in MLPS-GP

    :param root: Node object. root node of target solution.
    :return: list of tuple(Node, int). (parent, index of terminal node)
    """

    node_checker(root)
    points = []

    def add_children_to_nodes(current_node):
        children = current_node.children
        nonlocal points
        if current_node.is_terminal:
            return
        for index, c in enumerate(children):
            if c.is_terminal:
                points.append((current_node, index))
            add_children_to_nodes(c)

    add_children_to_nodes(root)

    return points


def node_equal(node_a, node_b, as_tree=False):
    """
    Function for comparing two nodes.
    :param node_a: Node object
    :param node_b: Node object
    :param as_tree: If False, compare the nodes based the node's type and the function id,
                    otherwise based on their tree structures as well as the node's type and the function id.
    :return:  bool
    """
    def func_id_equal(x, y):
        node_type_equal = not(bool(x.children) ^ bool(y.children))
        if x.func_id == y.func_id and node_type_equal:
            return True
        else:
            return False

    nodes_checker([node_a, node_b])
    if not as_tree:
        return func_id_equal(node_a, node_b)

    else:
        for x, y in zip(get_all_node(node_a), get_all_node(node_b)):
            if not func_id_equal(x, y):
                return False
        return True


def node_array_equal(nodes_a, nodes_b):
    for node_a, node_b in zip(nodes_a, nodes_b):
        if not node_equal(node_a, node_b, as_tree=False):
            return False

    return True


def func_id_checker(func_id):
    if not isinstance(func_id, int):
        typ = TypeError
        msg = 'Expected type: {} not {}.'.format(int, type(func_id))
    elif func_id < 0:
        typ = ValueError
        msg = 'Expected condition: func_id >= 0.'
    else:
        return

    raise typ(msg)


def node_checker(node):
    if not isinstance(node, Node):
        typ = TypeError
        msg = 'Expected type: {} not {}.'.format(Node, type(node))
    else:
        return

    raise typ(msg)


def nodes_checker(nodes):
    for node in nodes:
        node_checker(node)


def children_checker(children):
    if not isinstance(children, list):
        raise TypeError('Expected type: {}'.format(list))

    nodes_checker(children)
