"""Problem specs for the binary tree group of the study plan.

Every spec is a self-contained stdin-to-stdout task: trees travel as a single
line of level-order tokens, so a solution needs no node class of its own.
"""

from __future__ import annotations

from collections import deque
from typing import Any, Callable, Optional


class TreeNode:
    """Binary tree node carrying an extra sibling link.

    Attributes
    ----------
    value : int
        Integer stored at this node.
    left : Optional[TreeNode]
        Left child, or None when absent.
    right : Optional[TreeNode]
        Right child, or None when absent.
    next_right : Optional[TreeNode]
        Neighbour to the right on the same level, or None.
    """

    __slots__ = ("value", "left", "right", "next_right")

    def __init__(self, value: int) -> None:
        """Create a childless node.

        Parameters
        ----------
        value : int
            Integer stored at this node.
        """
        self.value: int = value
        self.left: Optional[TreeNode] = None
        self.right: Optional[TreeNode] = None
        self.next_right: Optional[TreeNode] = None


def read_lines(stdin_text: str) -> list[str]:
    """Split a stdin payload into stripped lines.

    Parameters
    ----------
    stdin_text : str
        Whole stdin payload.

    Returns
    -------
    list[str]
        One stripped string per line.
    """
    return [line.strip() for line in stdin_text.strip().split("\n")]


def parse_level_order(line: str) -> list[Optional[int]]:
    """Turn a line of level-order tokens into values and holes.

    Parameters
    ----------
    line : str
        Whitespace separated integers and `null` tokens.

    Returns
    -------
    list[Optional[int]]
        One entry per token, None for every `null`.
    """
    return [None if token == "null" else int(token) for token in line.split()]


def build_tree(line: str) -> Optional[TreeNode]:
    """Build a tree from a line of level-order tokens.

    Parameters
    ----------
    line : str
        Whitespace separated integers and `null` tokens.

    Returns
    -------
    Optional[TreeNode]
        Root of the tree, or None when the line holds no node.
    """
    tokens = parse_level_order(line)
    if not tokens or tokens[0] is None:
        return None
    root = TreeNode(tokens[0])
    pending: deque[TreeNode] = deque([root])
    cursor = 1
    while pending and cursor < len(tokens):
        parent = pending.popleft()
        if cursor < len(tokens):
            left_value = tokens[cursor]
            cursor += 1
            if left_value is not None:
                parent.left = TreeNode(left_value)
                pending.append(parent.left)
        if cursor < len(tokens):
            right_value = tokens[cursor]
            cursor += 1
            if right_value is not None:
                parent.right = TreeNode(right_value)
                pending.append(parent.right)
    return root


def serialize_tree(root: Optional[TreeNode]) -> str:
    """Render a tree as one line of level-order tokens.

    Parameters
    ----------
    root : Optional[TreeNode]
        Root of the tree.

    Returns
    -------
    str
        Space separated tokens with trailing `null` tokens removed.
    """
    tokens: list[str] = []
    pending: deque[Optional[TreeNode]] = deque([root])
    while pending:
        node = pending.popleft()
        if node is None:
            tokens.append("null")
            continue
        tokens.append(str(node.value))
        pending.append(node.left)
        pending.append(node.right)
    while tokens and tokens[-1] == "null":
        tokens.pop()
    return " ".join(tokens)


def collect_nodes(root: Optional[TreeNode]) -> list[TreeNode]:
    """List every node of a tree in level order.

    Parameters
    ----------
    root : Optional[TreeNode]
        Root of the tree.

    Returns
    -------
    list[TreeNode]
        Nodes in breadth-first order.
    """
    if root is None:
        return []
    nodes: list[TreeNode] = []
    pending: deque[TreeNode] = deque([root])
    while pending:
        node = pending.popleft()
        nodes.append(node)
        if node.left is not None:
            pending.append(node.left)
        if node.right is not None:
            pending.append(node.right)
    return nodes


TREE_INPUT_FORMAT = (
    "The tree arrives as a single line of level-order tokens. Each token is "
    "either an integer or the word `null`, which marks a missing child. The "
    "tokens are read breadth first: the first token is the root, the next two "
    "are the root's children, the next four are those nodes' children, and so "
    "on, where a `null` contributes no children of its own. Trailing `null` "
    "tokens are left out. For instance `3 9 20 null null 15 7` is a root `3` "
    "with children `9` and `20`, where `9` is a leaf and `20` has children "
    "`15` and `7`."
)

TREE_OUTPUT_FORMAT = (
    "Print the resulting tree on one line using the very same level-order "
    "encoding: values and `null` tokens separated by single spaces, with "
    "trailing `null` tokens dropped."
)


# --------------------------------------------------------------------------
# Maximum Depth of Binary Tree
# --------------------------------------------------------------------------


def solve_maximum_depth_of_binary_tree(stdin_text: str) -> str:
    """Report the number of nodes on the longest root-to-leaf path.

    Parameters
    ----------
    stdin_text : str
        One line of level-order tokens.

    Returns
    -------
    str
        The depth as a decimal integer.
    """

    def depth_of(node: Optional[TreeNode]) -> int:
        if node is None:
            return 0
        return 1 + max(depth_of(node.left), depth_of(node.right))

    return str(depth_of(build_tree(read_lines(stdin_text)[0])))


def brute_maximum_depth_of_binary_tree(stdin_text: str) -> str:
    """Count tree levels by walking the tree breadth first.

    Parameters
    ----------
    stdin_text : str
        One line of level-order tokens.

    Returns
    -------
    str
        The depth as a decimal integer.
    """
    root = build_tree(read_lines(stdin_text)[0])
    if root is None:
        return "0"
    level_count = 0
    current_level: list[TreeNode] = [root]
    while current_level:
        level_count += 1
        next_level: list[TreeNode] = []
        for node in current_level:
            if node.left is not None:
                next_level.append(node.left)
            if node.right is not None:
                next_level.append(node.right)
        current_level = next_level
    return str(level_count)


# --------------------------------------------------------------------------
# Same Tree
# --------------------------------------------------------------------------


def solve_same_tree(stdin_text: str) -> str:
    """Decide whether two trees have identical shape and values.

    Parameters
    ----------
    stdin_text : str
        Two lines of level-order tokens, one tree per line.

    Returns
    -------
    str
        "true" when the trees match, otherwise "false".
    """

    def matches(first: Optional[TreeNode], second: Optional[TreeNode]) -> bool:
        if first is None or second is None:
            return first is None and second is None
        if first.value != second.value:
            return False
        return matches(first.left, second.left) and matches(first.right, second.right)

    lines = read_lines(stdin_text)
    first_root = build_tree(lines[0])
    second_root = build_tree(lines[1])
    return "true" if matches(first_root, second_root) else "false"


def brute_same_tree(stdin_text: str) -> str:
    """Compare two trees through their canonical level-order encodings.

    Parameters
    ----------
    stdin_text : str
        Two lines of level-order tokens, one tree per line.

    Returns
    -------
    str
        "true" when the trees match, otherwise "false".
    """
    lines = read_lines(stdin_text)
    first_encoding = serialize_tree(build_tree(lines[0]))
    second_encoding = serialize_tree(build_tree(lines[1]))
    return "true" if first_encoding == second_encoding else "false"


# --------------------------------------------------------------------------
# Invert Binary Tree
# --------------------------------------------------------------------------


def solve_invert_binary_tree(stdin_text: str) -> str:
    """Mirror a tree left to right, recursively.

    Parameters
    ----------
    stdin_text : str
        One line of level-order tokens.

    Returns
    -------
    str
        The mirrored tree in the level-order encoding.
    """

    def invert(node: Optional[TreeNode]) -> Optional[TreeNode]:
        if node is None:
            return None
        node.left, node.right = invert(node.right), invert(node.left)
        return node

    return serialize_tree(invert(build_tree(read_lines(stdin_text)[0])))


def brute_invert_binary_tree(stdin_text: str) -> str:
    """Mirror a tree left to right with an explicit stack.

    Parameters
    ----------
    stdin_text : str
        One line of level-order tokens.

    Returns
    -------
    str
        The mirrored tree in the level-order encoding.
    """
    root = build_tree(read_lines(stdin_text)[0])
    stack: list[TreeNode] = [] if root is None else [root]
    while stack:
        node = stack.pop()
        node.left, node.right = node.right, node.left
        if node.left is not None:
            stack.append(node.left)
        if node.right is not None:
            stack.append(node.right)
    return serialize_tree(root)


# --------------------------------------------------------------------------
# Symmetric Tree
# --------------------------------------------------------------------------


def solve_symmetric_tree(stdin_text: str) -> str:
    """Decide whether a tree is its own mirror image.

    Parameters
    ----------
    stdin_text : str
        One line of level-order tokens.

    Returns
    -------
    str
        "true" when the tree is symmetric, otherwise "false".
    """

    def mirrors(left: Optional[TreeNode], right: Optional[TreeNode]) -> bool:
        if left is None or right is None:
            return left is None and right is None
        if left.value != right.value:
            return False
        return mirrors(left.left, right.right) and mirrors(left.right, right.left)

    root = build_tree(read_lines(stdin_text)[0])
    if root is None:
        return "true"
    return "true" if mirrors(root.left, root.right) else "false"


def brute_symmetric_tree(stdin_text: str) -> str:
    """Compare a tree against a separately built mirrored copy.

    Parameters
    ----------
    stdin_text : str
        One line of level-order tokens.

    Returns
    -------
    str
        "true" when the tree is symmetric, otherwise "false".
    """
    line = read_lines(stdin_text)[0]
    original_encoding = serialize_tree(build_tree(line))

    def mirrored_copy(node: Optional[TreeNode]) -> Optional[TreeNode]:
        if node is None:
            return None
        copy = TreeNode(node.value)
        copy.left = mirrored_copy(node.right)
        copy.right = mirrored_copy(node.left)
        return copy

    mirrored_encoding = serialize_tree(mirrored_copy(build_tree(line)))
    return "true" if original_encoding == mirrored_encoding else "false"


# --------------------------------------------------------------------------
# Construct Binary Tree from Preorder and Inorder Traversal
# --------------------------------------------------------------------------


def solve_construct_binary_tree_from_preorder_and_inorder_traversal(stdin_text: str) -> str:
    """Rebuild a tree from its preorder and inorder traversals.

    Parameters
    ----------
    stdin_text : str
        A count line, then the preorder line, then the inorder line.

    Returns
    -------
    str
        The rebuilt tree in the level-order encoding.
    """
    lines = read_lines(stdin_text)
    node_count = int(lines[0])
    preorder = [int(token) for token in lines[1].split()][:node_count]
    inorder = [int(token) for token in lines[2].split()][:node_count]
    position_by_value = {value: index for index, value in enumerate(inorder)}
    preorder_cursor = 0

    def build(low: int, high: int) -> Optional[TreeNode]:
        nonlocal preorder_cursor
        if low > high:
            return None
        value = preorder[preorder_cursor]
        preorder_cursor += 1
        node = TreeNode(value)
        split = position_by_value[value]
        node.left = build(low, split - 1)
        node.right = build(split + 1, high)
        return node

    return serialize_tree(build(0, node_count - 1))


def brute_construct_binary_tree_from_preorder_and_inorder_traversal(stdin_text: str) -> str:
    """Rebuild a tree from preorder and inorder by slicing both lists.

    Parameters
    ----------
    stdin_text : str
        A count line, then the preorder line, then the inorder line.

    Returns
    -------
    str
        The rebuilt tree in the level-order encoding.
    """
    lines = read_lines(stdin_text)
    node_count = int(lines[0])
    preorder = [int(token) for token in lines[1].split()][:node_count]
    inorder = [int(token) for token in lines[2].split()][:node_count]

    def build(preorder_part: list[int], inorder_part: list[int]) -> Optional[TreeNode]:
        if not preorder_part:
            return None
        root_value = preorder_part[0]
        split = inorder_part.index(root_value)
        node = TreeNode(root_value)
        node.left = build(preorder_part[1 : split + 1], inorder_part[:split])
        node.right = build(preorder_part[split + 1 :], inorder_part[split + 1 :])
        return node

    return serialize_tree(build(preorder, inorder))


# --------------------------------------------------------------------------
# Construct Binary Tree from Inorder and Postorder Traversal
# --------------------------------------------------------------------------


def solve_construct_binary_tree_from_inorder_and_postorder_traversal(stdin_text: str) -> str:
    """Rebuild a tree from its inorder and postorder traversals.

    Parameters
    ----------
    stdin_text : str
        A count line, then the inorder line, then the postorder line.

    Returns
    -------
    str
        The rebuilt tree in the level-order encoding.
    """
    lines = read_lines(stdin_text)
    node_count = int(lines[0])
    inorder = [int(token) for token in lines[1].split()][:node_count]
    postorder = [int(token) for token in lines[2].split()][:node_count]
    position_by_value = {value: index for index, value in enumerate(inorder)}
    postorder_cursor = node_count - 1

    def build(low: int, high: int) -> Optional[TreeNode]:
        nonlocal postorder_cursor
        if low > high:
            return None
        value = postorder[postorder_cursor]
        postorder_cursor -= 1
        node = TreeNode(value)
        split = position_by_value[value]
        node.right = build(split + 1, high)
        node.left = build(low, split - 1)
        return node

    return serialize_tree(build(0, node_count - 1))


def brute_construct_binary_tree_from_inorder_and_postorder_traversal(stdin_text: str) -> str:
    """Rebuild a tree from inorder and postorder by slicing both lists.

    Parameters
    ----------
    stdin_text : str
        A count line, then the inorder line, then the postorder line.

    Returns
    -------
    str
        The rebuilt tree in the level-order encoding.
    """
    lines = read_lines(stdin_text)
    node_count = int(lines[0])
    inorder = [int(token) for token in lines[1].split()][:node_count]
    postorder = [int(token) for token in lines[2].split()][:node_count]

    def build(inorder_part: list[int], postorder_part: list[int]) -> Optional[TreeNode]:
        if not postorder_part:
            return None
        root_value = postorder_part[-1]
        split = inorder_part.index(root_value)
        node = TreeNode(root_value)
        node.left = build(inorder_part[:split], postorder_part[:split])
        node.right = build(inorder_part[split + 1 :], postorder_part[split:-1])
        return node

    return serialize_tree(build(inorder, postorder))


# --------------------------------------------------------------------------
# Populating Next Right Pointers in Each Node II
# --------------------------------------------------------------------------


def solve_populating_next_right_pointers_in_each_node_ii(stdin_text: str) -> str:
    """Wire every node to its right neighbour, then read the levels back.

    Parameters
    ----------
    stdin_text : str
        One line of level-order tokens.

    Returns
    -------
    str
        One line per level, values separated by single spaces.
    """
    root = build_tree(read_lines(stdin_text)[0])
    level_head = root
    while level_head is not None:
        placeholder = TreeNode(0)
        tail = placeholder
        node: Optional[TreeNode] = level_head
        while node is not None:
            if node.left is not None:
                tail.next_right = node.left
                tail = node.left
            if node.right is not None:
                tail.next_right = node.right
                tail = node.right
            node = node.next_right
        level_head = placeholder.next_right

    lines: list[str] = []
    level_head = root
    while level_head is not None:
        values: list[str] = []
        node = level_head
        while node is not None:
            values.append(str(node.value))
            node = node.next_right
        lines.append(" ".join(values))
        next_head: Optional[TreeNode] = None
        node = level_head
        while node is not None and next_head is None:
            next_head = node.left if node.left is not None else node.right
            node = node.next_right
        level_head = next_head
    return "\n".join(lines)


def brute_populating_next_right_pointers_in_each_node_ii(stdin_text: str) -> str:
    """List the nodes of each level by plain breadth-first traversal.

    Parameters
    ----------
    stdin_text : str
        One line of level-order tokens.

    Returns
    -------
    str
        One line per level, values separated by single spaces.
    """
    root = build_tree(read_lines(stdin_text)[0])
    lines: list[str] = []
    current_level: list[TreeNode] = [] if root is None else [root]
    while current_level:
        lines.append(" ".join(str(node.value) for node in current_level))
        next_level: list[TreeNode] = []
        for node in current_level:
            if node.left is not None:
                next_level.append(node.left)
            if node.right is not None:
                next_level.append(node.right)
        current_level = next_level
    return "\n".join(lines)


# --------------------------------------------------------------------------
# Flatten Binary Tree to Linked List
# --------------------------------------------------------------------------


def solve_flatten_binary_tree_to_linked_list(stdin_text: str) -> str:
    """Flatten a tree into a right-hand chain in place, then read it off.

    Parameters
    ----------
    stdin_text : str
        One line of level-order tokens.

    Returns
    -------
    str
        The chain values on one line, separated by single spaces.
    """
    root = build_tree(read_lines(stdin_text)[0])
    node = root
    while node is not None:
        if node.left is not None:
            rightmost = node.left
            while rightmost.right is not None:
                rightmost = rightmost.right
            rightmost.right = node.right
            node.right = node.left
            node.left = None
        node = node.right

    values: list[str] = []
    node = root
    while node is not None:
        values.append(str(node.value))
        node = node.right
    return " ".join(values)


def brute_flatten_binary_tree_to_linked_list(stdin_text: str) -> str:
    """Collect the preorder values with an explicit stack.

    Parameters
    ----------
    stdin_text : str
        One line of level-order tokens.

    Returns
    -------
    str
        The chain values on one line, separated by single spaces.
    """
    root = build_tree(read_lines(stdin_text)[0])
    values: list[str] = []
    stack: list[TreeNode] = [] if root is None else [root]
    while stack:
        node = stack.pop()
        values.append(str(node.value))
        if node.right is not None:
            stack.append(node.right)
        if node.left is not None:
            stack.append(node.left)
    return " ".join(values)


# --------------------------------------------------------------------------
# Path Sum
# --------------------------------------------------------------------------


def solve_path_sum(stdin_text: str) -> str:
    """Decide whether some root-to-leaf path adds up to the target.

    Parameters
    ----------
    stdin_text : str
        A tree line, then a line holding the target sum.

    Returns
    -------
    str
        "true" when such a path exists, otherwise "false".
    """
    lines = read_lines(stdin_text)
    root = build_tree(lines[0])
    target_sum = int(lines[1])

    def reaches(node: Optional[TreeNode], remaining: int) -> bool:
        if node is None:
            return False
        if node.left is None and node.right is None:
            return remaining == node.value
        return reaches(node.left, remaining - node.value) or reaches(
            node.right, remaining - node.value
        )

    return "true" if reaches(root, target_sum) else "false"


def brute_path_sum(stdin_text: str) -> str:
    """Enumerate every root-to-leaf total with an explicit stack.

    Parameters
    ----------
    stdin_text : str
        A tree line, then a line holding the target sum.

    Returns
    -------
    str
        "true" when some total equals the target, otherwise "false".
    """
    lines = read_lines(stdin_text)
    root = build_tree(lines[0])
    target_sum = int(lines[1])
    if root is None:
        return "false"
    stack: list[tuple[TreeNode, int]] = [(root, root.value)]
    while stack:
        node, running_total = stack.pop()
        if node.left is None and node.right is None and running_total == target_sum:
            return "true"
        if node.left is not None:
            stack.append((node.left, running_total + node.left.value))
        if node.right is not None:
            stack.append((node.right, running_total + node.right.value))
    return "false"


# --------------------------------------------------------------------------
# Sum Root to Leaf Numbers
# --------------------------------------------------------------------------


def solve_sum_root_to_leaf_numbers(stdin_text: str) -> str:
    """Add up the numbers spelled out by every root-to-leaf path.

    Parameters
    ----------
    stdin_text : str
        One line of level-order tokens holding single digits.

    Returns
    -------
    str
        The total as a decimal integer.
    """
    root = build_tree(read_lines(stdin_text)[0])

    def total_below(node: Optional[TreeNode], number_so_far: int) -> int:
        if node is None:
            return 0
        number_so_far = number_so_far * 10 + node.value
        if node.left is None and node.right is None:
            return number_so_far
        return total_below(node.left, number_so_far) + total_below(node.right, number_so_far)

    return str(total_below(root, 0))


def brute_sum_root_to_leaf_numbers(stdin_text: str) -> str:
    """Collect each root-to-leaf digit string, then add the numbers.

    Parameters
    ----------
    stdin_text : str
        One line of level-order tokens holding single digits.

    Returns
    -------
    str
        The total as a decimal integer.
    """
    root = build_tree(read_lines(stdin_text)[0])
    if root is None:
        return "0"
    total = 0
    stack: list[tuple[TreeNode, str]] = [(root, str(root.value))]
    while stack:
        node, digits = stack.pop()
        if node.left is None and node.right is None:
            total += int(digits)
            continue
        if node.left is not None:
            stack.append((node.left, digits + str(node.left.value)))
        if node.right is not None:
            stack.append((node.right, digits + str(node.right.value)))
    return str(total)


# --------------------------------------------------------------------------
# Binary Tree Maximum Path Sum
# --------------------------------------------------------------------------


def solve_binary_tree_maximum_path_sum(stdin_text: str) -> str:
    """Find the largest sum over any connected path in the tree.

    Parameters
    ----------
    stdin_text : str
        One line of level-order tokens.

    Returns
    -------
    str
        The best path sum as a decimal integer.
    """
    root = build_tree(read_lines(stdin_text)[0])
    best_total = -(10**18)

    def best_downward(node: Optional[TreeNode]) -> int:
        nonlocal best_total
        if node is None:
            return 0
        left_gain = max(best_downward(node.left), 0)
        right_gain = max(best_downward(node.right), 0)
        best_total = max(best_total, node.value + left_gain + right_gain)
        return node.value + max(left_gain, right_gain)

    best_downward(root)
    return str(best_total)


def brute_binary_tree_maximum_path_sum(stdin_text: str) -> str:
    """Walk every path of the tree read as an undirected graph.

    Parameters
    ----------
    stdin_text : str
        One line of level-order tokens.

    Returns
    -------
    str
        The best path sum as a decimal integer.
    """
    root = build_tree(read_lines(stdin_text)[0])
    nodes = collect_nodes(root)
    if not nodes:
        return "0"
    neighbours: dict[TreeNode, list[TreeNode]] = {node: [] for node in nodes}
    for node in nodes:
        for child in (node.left, node.right):
            if child is not None:
                neighbours[node].append(child)
                neighbours[child].append(node)

    best_total = -(10**18)

    def walk(node: TreeNode, came_from: Optional[TreeNode], running_total: int) -> None:
        nonlocal best_total
        best_total = max(best_total, running_total)
        for neighbour in neighbours[node]:
            if neighbour is not came_from:
                walk(neighbour, node, running_total + neighbour.value)

    for start in nodes:
        walk(start, None, start.value)
    return str(best_total)


# --------------------------------------------------------------------------
# Binary Search Tree Iterator
# --------------------------------------------------------------------------


def solve_binary_search_tree_iterator(stdin_text: str) -> str:
    """Answer iterator queries from the fully materialised inorder sequence.

    Parameters
    ----------
    stdin_text : str
        A tree line, an operation count line, then that many operation lines.

    Returns
    -------
    str
        One line per operation: a value, `none`, `true` or `false`.
    """
    lines = read_lines(stdin_text)
    root = build_tree(lines[0])
    operation_count = int(lines[1])
    operations = lines[2 : 2 + operation_count]

    sorted_values: list[int] = []

    def visit(node: Optional[TreeNode]) -> None:
        if node is None:
            return
        visit(node.left)
        sorted_values.append(node.value)
        visit(node.right)

    visit(root)

    answers: list[str] = []
    cursor = 0
    for operation in operations:
        if operation == "hasNext":
            answers.append("true" if cursor < len(sorted_values) else "false")
        elif cursor < len(sorted_values):
            answers.append(str(sorted_values[cursor]))
            cursor += 1
        else:
            answers.append("none")
    return "\n".join(answers)


def brute_binary_search_tree_iterator(stdin_text: str) -> str:
    """Answer iterator queries with a lazy stack of pending nodes.

    Parameters
    ----------
    stdin_text : str
        A tree line, an operation count line, then that many operation lines.

    Returns
    -------
    str
        One line per operation: a value, `none`, `true` or `false`.
    """
    lines = read_lines(stdin_text)
    root = build_tree(lines[0])
    operation_count = int(lines[1])
    operations = lines[2 : 2 + operation_count]

    pending: list[TreeNode] = []

    def push_left_spine(node: Optional[TreeNode]) -> None:
        while node is not None:
            pending.append(node)
            node = node.left

    push_left_spine(root)

    answers: list[str] = []
    for operation in operations:
        if operation == "hasNext":
            answers.append("true" if pending else "false")
        elif pending:
            node = pending.pop()
            push_left_spine(node.right)
            answers.append(str(node.value))
        else:
            answers.append("none")
    return "\n".join(answers)


# --------------------------------------------------------------------------
# Count Complete Tree Nodes
# --------------------------------------------------------------------------


def solve_count_complete_tree_nodes(stdin_text: str) -> str:
    """Count the nodes of a complete tree using perfect-subtree shortcuts.

    Parameters
    ----------
    stdin_text : str
        One line of level-order tokens describing a complete tree.

    Returns
    -------
    str
        The node count as a decimal integer.
    """
    root = build_tree(read_lines(stdin_text)[0])

    def leftmost_height(node: Optional[TreeNode]) -> int:
        height = 0
        while node is not None:
            height += 1
            node = node.left
        return height

    def count(node: Optional[TreeNode]) -> int:
        if node is None:
            return 0
        left_height = leftmost_height(node.left)
        right_height = leftmost_height(node.right)
        if left_height == right_height:
            return 1 + (2**left_height - 1) + count(node.right)
        return 1 + count(node.left) + (2**right_height - 1)

    return str(count(root))


def brute_count_complete_tree_nodes(stdin_text: str) -> str:
    """Count the nodes by visiting every one of them.

    Parameters
    ----------
    stdin_text : str
        One line of level-order tokens describing a complete tree.

    Returns
    -------
    str
        The node count as a decimal integer.
    """
    return str(len(collect_nodes(build_tree(read_lines(stdin_text)[0]))))


# --------------------------------------------------------------------------
# Lowest Common Ancestor of a Binary Tree
# --------------------------------------------------------------------------


def solve_lowest_common_ancestor_of_a_binary_tree(stdin_text: str) -> str:
    """Find the deepest node that has both query values below it.

    Parameters
    ----------
    stdin_text : str
        A tree line, then a line holding the two node values.

    Returns
    -------
    str
        The ancestor's value as a decimal integer.
    """
    lines = read_lines(stdin_text)
    root = build_tree(lines[0])
    first_value, second_value = (int(token) for token in lines[1].split())

    def lowest_ancestor(node: Optional[TreeNode]) -> Optional[TreeNode]:
        if node is None or node.value in (first_value, second_value):
            return node
        from_left = lowest_ancestor(node.left)
        from_right = lowest_ancestor(node.right)
        if from_left is not None and from_right is not None:
            return node
        return from_left if from_left is not None else from_right

    ancestor = lowest_ancestor(root)
    return str(ancestor.value) if ancestor is not None else "-1"


def brute_lowest_common_ancestor_of_a_binary_tree(stdin_text: str) -> str:
    """Compare the two root-to-node paths and take their last shared value.

    Parameters
    ----------
    stdin_text : str
        A tree line, then a line holding the two node values.

    Returns
    -------
    str
        The ancestor's value as a decimal integer.
    """
    lines = read_lines(stdin_text)
    root = build_tree(lines[0])
    first_value, second_value = (int(token) for token in lines[1].split())

    def path_to(node: Optional[TreeNode], target: int, trail: list[int]) -> bool:
        if node is None:
            return False
        trail.append(node.value)
        if node.value == target:
            return True
        if path_to(node.left, target, trail) or path_to(node.right, target, trail):
            return True
        trail.pop()
        return False

    first_path: list[int] = []
    second_path: list[int] = []
    if not path_to(root, first_value, first_path) or not path_to(root, second_value, second_path):
        return "-1"
    shared = "-1"
    for left_step, right_step in zip(first_path, second_path):
        if left_step != right_step:
            break
        shared = str(left_step)
    return shared


PROBLEMS: list[dict[str, Any]] = [
    {
        "title": "Maximum Depth of Binary Tree",
        "level": "Easy",
        "topics": "Tree, Depth-First Search, Breadth-First Search, Binary Tree",
        "companies": "Amazon, Google, Microsoft, Apple",
        "description": (
            "The depth of a binary tree is the number of nodes you pass through on "
            "the longest walk from the root down to a leaf. Read one tree and report "
            "that number.\n\n"
            f"{TREE_INPUT_FORMAT}\n\n"
            "Print a single line holding the depth as a decimal integer.\n\n"
        ),
        "examples": (
            "```\n"
            "Input:\n"
            "3 9 20 null null 15 7\n"
            "Output:\n"
            "3\n"
            "```\n\n"
            "```\n"
            "Input:\n"
            "1 2 null 3 null 4 null 5\n"
            "Output:\n"
            "5\n"
            "```\n\n"
        ),
        "constraints": (
            "- The tree holds between 1 and 2000 nodes.\n"
            "- Each value fits in the range -1000 to 1000.\n"
            "- Only the word `null` stands for a missing child.\n\n"
        ),
        "inputs": [
            "3 9 20 null null 15 7",
            "1",
            "1 2 null 3 null 4 null 5",
            "1 null 2 null 3 null 4",
            "5 4 8 11 null 13 4 7 2 null null null 1",
            "-1 -2 -3 null -4",
        ],
        "solve": solve_maximum_depth_of_binary_tree,
        "brute": brute_maximum_depth_of_binary_tree,
    },
    {
        "title": "Same Tree",
        "level": "Easy",
        "topics": "Tree, Depth-First Search, Breadth-First Search, Binary Tree",
        "companies": "Amazon, Bloomberg, Microsoft, Adobe",
        "description": (
            "Two binary trees count as the same when they have exactly the same "
            "shape and the matching positions hold the same values. Read two trees "
            "and say whether they are the same.\n\n"
            f"{TREE_INPUT_FORMAT}\n\n"
            "The input is two such lines: the first tree on line one, the second "
            "tree on line two.\n\n"
            "Print a single line holding `true` or `false`, in lower case.\n\n"
        ),
        "examples": (
            "```\n"
            "Input:\n"
            "1 2 3\n"
            "1 2 3\n"
            "Output:\n"
            "true\n"
            "```\n\n"
            "```\n"
            "Input:\n"
            "1 2\n"
            "1 null 2\n"
            "Output:\n"
            "false\n"
            "```\n\n"
        ),
        "constraints": (
            "- Each tree holds between 1 and 100 nodes.\n"
            "- Each value fits in the range -10000 to 10000.\n"
            "- Both lines use the same level-order encoding.\n\n"
        ),
        "inputs": [
            "1 2 3\n1 2 3",
            "1 2\n1 null 2",
            "1 2 1\n1 1 2",
            "1\n1",
            "1 2 3 4 5\n1 2 3 4 null",
            "-1 -2 -3\n-1 -2 -3",
        ],
        "solve": solve_same_tree,
        "brute": brute_same_tree,
    },
    {
        "title": "Invert Binary Tree",
        "level": "Easy",
        "topics": "Tree, Depth-First Search, Breadth-First Search, Binary Tree",
        "companies": "Google, Amazon, Meta, Uber",
        "description": (
            "Inverting a binary tree means swapping the left and right child of "
            "every node, so the whole tree ends up mirrored. Read one tree, invert "
            "it, and print the result.\n\n"
            f"{TREE_INPUT_FORMAT}\n\n"
            f"{TREE_OUTPUT_FORMAT}\n\n"
        ),
        "examples": (
            "```\n"
            "Input:\n"
            "4 2 7 1 3 6 9\n"
            "Output:\n"
            "4 7 2 9 6 3 1\n"
            "```\n\n"
            "```\n"
            "Input:\n"
            "1 2 null 3\n"
            "Output:\n"
            "1 null 2 null 3\n"
            "```\n\n"
        ),
        "constraints": (
            "- The tree holds between 1 and 100 nodes.\n"
            "- Each value fits in the range -100 to 100.\n"
            "- The printed line drops trailing `null` tokens.\n\n"
        ),
        "inputs": [
            "4 2 7 1 3 6 9",
            "2 1 3",
            "1",
            "1 2 null 3",
            "1 null 2 null 3",
            "-5 -3 -8 null -1",
        ],
        "solve": solve_invert_binary_tree,
        "brute": brute_invert_binary_tree,
    },
    {
        "title": "Symmetric Tree",
        "level": "Easy",
        "topics": "Tree, Depth-First Search, Breadth-First Search, Binary Tree",
        "companies": "Amazon, Microsoft, LinkedIn, Bloomberg",
        "description": (
            "A binary tree is symmetric when its left half is the mirror image of "
            "its right half, both in shape and in values. Read one tree and say "
            "whether it is symmetric.\n\n"
            f"{TREE_INPUT_FORMAT}\n\n"
            "Print a single line holding `true` or `false`, in lower case.\n\n"
        ),
        "examples": (
            "```\n"
            "Input:\n"
            "1 2 2 3 4 4 3\n"
            "Output:\n"
            "true\n"
            "```\n\n"
            "```\n"
            "Input:\n"
            "1 2 2 null 3 null 3\n"
            "Output:\n"
            "false\n"
            "```\n\n"
        ),
        "constraints": (
            "- The tree holds between 1 and 1000 nodes.\n"
            "- Each value fits in the range -100 to 100.\n"
            "- A one-node tree is symmetric.\n\n"
        ),
        "inputs": [
            "1 2 2 3 4 4 3",
            "1 2 2 null 3 null 3",
            "1",
            "1 2 2 null 3 3 null",
            "2 3 3 4 5 5 7",
            "-1 -2 -2",
        ],
        "solve": solve_symmetric_tree,
        "brute": brute_symmetric_tree,
    },
    {
        "title": "Construct Binary Tree from Preorder and Inorder Traversal",
        "level": "Medium",
        "topics": "Array, Hash Table, Divide and Conquer, Tree, Binary Tree",
        "companies": "Amazon, Microsoft, Bloomberg, Google",
        "description": (
            "A preorder traversal lists a node before its two subtrees; an inorder "
            "traversal lists the left subtree, then the node, then the right "
            "subtree. Given both traversals of the same tree, and with every value "
            "distinct, exactly one tree fits. Rebuild it.\n\n"
            "The input is three lines:\n\n"
            "1. an integer `n`, the number of nodes;\n"
            "2. the `n` preorder values, separated by spaces;\n"
            "3. the `n` inorder values, separated by spaces.\n\n"
            f"{TREE_OUTPUT_FORMAT}\n\n"
        ),
        "examples": (
            "```\n"
            "Input:\n"
            "5\n"
            "3 9 20 15 7\n"
            "9 3 15 20 7\n"
            "Output:\n"
            "3 9 20 null null 15 7\n"
            "```\n\n"
            "```\n"
            "Input:\n"
            "4\n"
            "1 2 3 4\n"
            "4 3 2 1\n"
            "Output:\n"
            "1 2 null 3 null 4\n"
            "```\n\n"
        ),
        "constraints": (
            "- 1 <= n <= 3000.\n"
            "- Each value fits in the range -3000 to 3000.\n"
            "- All values are distinct, and the two traversals describe one tree.\n\n"
        ),
        "inputs": [
            "3\n3 9 20\n9 3 20",
            "1\n1\n1",
            "5\n3 9 20 15 7\n9 3 15 20 7",
            "4\n1 2 3 4\n4 3 2 1",
            "4\n1 2 3 4\n1 2 3 4",
            "5\n-10 -9 -20 -15 -7\n-9 -10 -15 -20 -7",
        ],
        "solve": solve_construct_binary_tree_from_preorder_and_inorder_traversal,
        "brute": brute_construct_binary_tree_from_preorder_and_inorder_traversal,
    },
    {
        "title": "Construct Binary Tree from Inorder and Postorder Traversal",
        "level": "Medium",
        "topics": "Array, Hash Table, Divide and Conquer, Tree, Binary Tree",
        "companies": "Amazon, Microsoft, Apple, Bloomberg",
        "description": (
            "An inorder traversal lists the left subtree, then the node, then the "
            "right subtree; a postorder traversal lists both subtrees before the "
            "node. Given both traversals of the same tree, and with every value "
            "distinct, exactly one tree fits. Rebuild it.\n\n"
            "The input is three lines:\n\n"
            "1. an integer `n`, the number of nodes;\n"
            "2. the `n` inorder values, separated by spaces;\n"
            "3. the `n` postorder values, separated by spaces.\n\n"
            f"{TREE_OUTPUT_FORMAT}\n\n"
        ),
        "examples": (
            "```\n"
            "Input:\n"
            "5\n"
            "9 3 15 20 7\n"
            "9 15 7 20 3\n"
            "Output:\n"
            "3 9 20 null null 15 7\n"
            "```\n\n"
            "```\n"
            "Input:\n"
            "4\n"
            "1 2 3 4\n"
            "4 3 2 1\n"
            "Output:\n"
            "1 null 2 null 3 null 4\n"
            "```\n\n"
        ),
        "constraints": (
            "- 1 <= n <= 3000.\n"
            "- Each value fits in the range -3000 to 3000.\n"
            "- All values are distinct, and the two traversals describe one tree.\n\n"
        ),
        "inputs": [
            "3\n9 3 15\n9 15 3",
            "1\n1\n1",
            "5\n9 3 15 20 7\n9 15 7 20 3",
            "4\n4 3 2 1\n4 3 2 1",
            "4\n1 2 3 4\n4 3 2 1",
            "5\n-9 -3 -15 -20 -7\n-9 -15 -7 -20 -3",
        ],
        "solve": solve_construct_binary_tree_from_inorder_and_postorder_traversal,
        "brute": brute_construct_binary_tree_from_inorder_and_postorder_traversal,
    },
    {
        "title": "Populating Next Right Pointers in Each Node II",
        "level": "Medium",
        "topics": "Linked List, Tree, Depth-First Search, Breadth-First Search, Binary Tree",
        "companies": "Microsoft, Amazon, Meta, Bloomberg",
        "description": (
            "Give every node a `next` pointer aimed at the node immediately to its "
            "right on the same level, and aimed at nothing when the node is the "
            "last on its level. The tree may have any shape: a level can have gaps, "
            "so the neighbour to the right is not always a sibling.\n\n"
            f"{TREE_INPUT_FORMAT}\n\n"
            "Print one line per level, from the root level downwards. A line holds "
            "the values met by starting at the leftmost node of that level and "
            "following `next` pointers to the end of the level, separated by single "
            "spaces.\n\n"
        ),
        "examples": (
            "```\n"
            "Input:\n"
            "1 2 3 4 5 null 7\n"
            "Output:\n"
            "1\n"
            "2 3\n"
            "4 5 7\n"
            "```\n\n"
            "```\n"
            "Input:\n"
            "1 2 3 null 4 null 5\n"
            "Output:\n"
            "1\n"
            "2 3\n"
            "4 5\n"
            "```\n\n"
        ),
        "constraints": (
            "- The tree holds between 1 and 6000 nodes.\n"
            "- Each value fits in the range -100 to 100.\n"
            "- Levels are printed top to bottom, values left to right.\n\n"
        ),
        "inputs": [
            "1 2 3 4 5 null 7",
            "1",
            "1 2 3 null 4 null 5",
            "1 2 null 3 null 4",
            "1 null 2 null 3",
            "-1 -2 -3 -4 null null -5",
        ],
        "solve": solve_populating_next_right_pointers_in_each_node_ii,
        "brute": brute_populating_next_right_pointers_in_each_node_ii,
    },
    {
        "title": "Flatten Binary Tree to Linked List",
        "level": "Medium",
        "topics": "Linked List, Stack, Tree, Depth-First Search, Binary Tree",
        "companies": "Microsoft, Amazon, Google, Adobe",
        "description": (
            "Flattening a binary tree means rearranging it into a chain that only "
            "ever goes right: every node keeps no left child, and its right child "
            "is the node that follows it in preorder. Preorder visits a node first, "
            "then everything in its left subtree, then everything in its right "
            "subtree.\n\n"
            f"{TREE_INPUT_FORMAT}\n\n"
            "Print a single line holding the values of the chain in order, from the "
            "root to the last node, separated by single spaces.\n\n"
        ),
        "examples": (
            "```\n"
            "Input:\n"
            "1 2 5 3 4 null 6\n"
            "Output:\n"
            "1 2 3 4 5 6\n"
            "```\n\n"
            "```\n"
            "Input:\n"
            "5 3 8 1 4 null 9\n"
            "Output:\n"
            "5 3 1 4 8 9\n"
            "```\n\n"
        ),
        "constraints": (
            "- The tree holds between 1 and 2000 nodes.\n"
            "- Each value fits in the range -100 to 100.\n"
            "- The chain always has as many values as the tree had nodes.\n\n"
        ),
        "inputs": [
            "1 2 5 3 4 null 6",
            "1",
            "1 2 null 3 null 4",
            "1 null 2 null 3",
            "5 3 8 1 4 null 9",
            "-1 -2 -3",
        ],
        "solve": solve_flatten_binary_tree_to_linked_list,
        "brute": brute_flatten_binary_tree_to_linked_list,
    },
    {
        "title": "Path Sum",
        "level": "Easy",
        "topics": "Tree, Depth-First Search, Breadth-First Search, Binary Tree",
        "companies": "Amazon, Microsoft, Meta, Bloomberg",
        "description": (
            "Walk from the root down to any leaf, adding the values you pass "
            "through. Say whether at least one such walk reaches a given target. A "
            "leaf is a node with no children, and a path must end at a leaf.\n\n"
            f"{TREE_INPUT_FORMAT}\n\n"
            "The input is two lines: the tree on line one, and the target sum as a "
            "single integer on line two.\n\n"
            "Print a single line holding `true` or `false`, in lower case.\n\n"
        ),
        "examples": (
            "```\n"
            "Input:\n"
            "5 4 8 11 null 13 4 7 2 null null null 1\n"
            "22\n"
            "Output:\n"
            "true\n"
            "```\n\n"
            "```\n"
            "Input:\n"
            "1 2\n"
            "1\n"
            "Output:\n"
            "false\n"
            "```\n\n"
        ),
        "constraints": (
            "- The tree holds between 1 and 5000 nodes.\n"
            "- Each value fits in the range -1000 to 1000, negatives included.\n"
            "- The target fits in the range -1000000 to 1000000.\n\n"
        ),
        "inputs": [
            "5 4 8 11 null 13 4 7 2 null null null 1\n22",
            "1 2 3\n5",
            "1 2\n1",
            "1\n1",
            "1 null 2 null 3\n6",
            "-5 -3 4 null null -2\n-3",
        ],
        "solve": solve_path_sum,
        "brute": brute_path_sum,
    },
    {
        "title": "Sum Root to Leaf Numbers",
        "level": "Medium",
        "topics": "Tree, Depth-First Search, Binary Tree",
        "companies": "Meta, Amazon, Microsoft, Google",
        "description": (
            "Every node holds a single digit, so each root-to-leaf path spells out "
            "a number, reading the digits from the root downwards. Add up the "
            "numbers spelled by all root-to-leaf paths. A leaf is a node with no "
            "children.\n\n"
            f"{TREE_INPUT_FORMAT}\n\n"
            "Print a single line holding the total as a decimal integer.\n\n"
        ),
        "examples": (
            "```\n"
            "Input:\n"
            "1 2 3\n"
            "Output:\n"
            "25\n"
            "```\n\n"
            "```\n"
            "Input:\n"
            "4 9 0 5 1\n"
            "Output:\n"
            "1026\n"
            "```\n\n"
        ),
        "constraints": (
            "- The tree holds between 1 and 1000 nodes.\n"
            "- Every value is a digit from 0 to 9.\n"
            "- The depth never exceeds 10, so the total fits in a 64-bit integer.\n\n"
        ),
        "inputs": [
            "1 2 3",
            "4 9 0 5 1",
            "1",
            "1 2 null 3 null 4",
            "1 null 2 null 3",
            "9 8 7 6 null null 5",
        ],
        "solve": solve_sum_root_to_leaf_numbers,
        "brute": brute_sum_root_to_leaf_numbers,
    },
    {
        "title": "Binary Tree Maximum Path Sum",
        "level": "Hard",
        "topics": "Dynamic Programming, Tree, Depth-First Search, Binary Tree",
        "companies": "Amazon, Microsoft, Google, DoorDash",
        "description": (
            "A path is any sequence of nodes where each one is joined to the next "
            "by an edge, and no node repeats. A path does not have to touch the "
            "root, it may bend upwards through a node and back down the other side, "
            "and a single node counts as a path on its own. Report the largest "
            "possible sum of the values along one path.\n\n"
            f"{TREE_INPUT_FORMAT}\n\n"
            "Print a single line holding the best sum as a decimal integer, which "
            "may be negative.\n\n"
        ),
        "examples": (
            "```\n"
            "Input:\n"
            "-10 9 20 null null 15 7\n"
            "Output:\n"
            "42\n"
            "```\n\n"
            "```\n"
            "Input:\n"
            "-1 -2 -3 -4 -5\n"
            "Output:\n"
            "-1\n"
            "```\n\n"
        ),
        "constraints": (
            "- The tree holds between 1 and 30000 nodes.\n"
            "- Each value fits in the range -1000 to 1000.\n"
            "- All values may be negative, so the answer may be negative.\n\n"
        ),
        "inputs": [
            "1 2 3",
            "-10 9 20 null null 15 7",
            "-3",
            "2 -1",
            "1 2 null 3 null 4",
            "-1 -2 -3 -4 -5",
        ],
        "solve": solve_binary_tree_maximum_path_sum,
        "brute": brute_binary_tree_maximum_path_sum,
    },
    {
        "title": "Binary Search Tree Iterator",
        "level": "Medium",
        "topics": "Stack, Tree, Design, Binary Search Tree, Binary Tree, Iterator",
        "companies": "Amazon, Microsoft, Meta, Salesforce",
        "description": (
            "Run an iterator that hands back the values of a binary search tree in "
            "increasing order. Two operations exist: `next` returns the smallest "
            "value not yet handed back, and `hasNext` says whether any value is "
            "still waiting.\n\n"
            f"{TREE_INPUT_FORMAT}\n\n"
            "The tree is a binary search tree, so an inorder walk already gives the "
            "values in increasing order.\n\n"
            "After the tree line comes a line holding `q`, the number of "
            "operations, then `q` lines each holding either `next` or `hasNext`, "
            "spelled exactly that way.\n\n"
            "Print one line per operation, in order. For `hasNext` print `true` or "
            "`false` in lower case. For `next` print the value, or `none` when "
            "every value has already been handed back.\n\n"
        ),
        "examples": (
            "```\n"
            "Input:\n"
            "7 3 15 null null 9 20\n"
            "5\n"
            "next\n"
            "next\n"
            "hasNext\n"
            "next\n"
            "hasNext\n"
            "Output:\n"
            "3\n"
            "7\n"
            "true\n"
            "9\n"
            "true\n"
            "```\n\n"
            "```\n"
            "Input:\n"
            "2 1 3\n"
            "5\n"
            "next\n"
            "next\n"
            "next\n"
            "hasNext\n"
            "next\n"
            "Output:\n"
            "1\n"
            "2\n"
            "3\n"
            "false\n"
            "none\n"
            "```\n\n"
        ),
        "constraints": (
            "- The tree holds between 1 and 100000 nodes and is a valid search tree.\n"
            "- Each value fits in the range -1000000 to 1000000.\n"
            "- 1 <= q <= 100000, and every operation line is `next` or `hasNext`.\n\n"
        ),
        "inputs": [
            "7 3 15 null null 9 20\n5\nnext\nnext\nhasNext\nnext\nhasNext",
            "5\n3\nhasNext\nnext\nhasNext",
            "5 4 null 3 null 2\n4\nnext\nnext\nnext\nnext",
            "1 null 2 null 3\n4\nhasNext\nnext\nnext\nnext",
            "2 1 3\n5\nnext\nnext\nnext\nhasNext\nnext",
            "0 -3 8 -5 null 5\n4\nnext\nnext\nnext\nnext",
        ],
        "solve": solve_binary_search_tree_iterator,
        "brute": brute_binary_search_tree_iterator,
    },
    {
        "title": "Count Complete Tree Nodes",
        "level": "Medium",
        "topics": "Binary Search, Bit Manipulation, Tree, Binary Tree",
        "companies": "Google, Amazon, Microsoft, Uber",
        "description": (
            "A complete binary tree has every level full except possibly the last, "
            "and the last level is filled from the left with no gaps. Count the "
            "nodes of such a tree. Visiting them all works, but the shape also "
            "allows a much faster count.\n\n"
            f"{TREE_INPUT_FORMAT}\n\n"
            "The tree on the input line is always complete, so no `null` token ever "
            "appears before a value.\n\n"
            "Print a single line holding the node count as a decimal integer.\n\n"
        ),
        "examples": (
            "```\n"
            "Input:\n"
            "1 2 3 4 5 6\n"
            "Output:\n"
            "6\n"
            "```\n\n"
            "```\n"
            "Input:\n"
            "1 2 3 4 5 6 7 8 9 10 11 12\n"
            "Output:\n"
            "12\n"
            "```\n\n"
        ),
        "constraints": (
            "- The tree holds between 1 and 50000 nodes.\n"
            "- The tree is guaranteed to be complete.\n"
            "- Each value fits in the range 0 to 50000.\n\n"
        ),
        "inputs": [
            "1 2 3 4 5 6",
            "1",
            "1 2 3 4 5 6 7",
            "1 2",
            "1 2 3 4 5 6 7 8 9 10 11 12",
            "1 2 3 4",
        ],
        "solve": solve_count_complete_tree_nodes,
        "brute": brute_count_complete_tree_nodes,
    },
    {
        "title": "Lowest Common Ancestor of a Binary Tree",
        "level": "Medium",
        "topics": "Tree, Depth-First Search, Binary Tree",
        "companies": "Amazon, Meta, Microsoft, LinkedIn",
        "description": (
            "The lowest common ancestor of two nodes is the deepest node that has "
            "both of them somewhere below it, where a node counts as being below "
            "itself. Find it for two given nodes.\n\n"
            f"{TREE_INPUT_FORMAT}\n\n"
            "All values in the tree are distinct, so a value names exactly one "
            "node. After the tree line comes a line holding two of those values, "
            "separated by a space, in any order.\n\n"
            "Print a single line holding the value of the lowest common ancestor.\n\n"
        ),
        "examples": (
            "```\n"
            "Input:\n"
            "3 5 1 6 2 0 8 null null 7 4\n"
            "5 1\n"
            "Output:\n"
            "3\n"
            "```\n\n"
            "```\n"
            "Input:\n"
            "3 5 1 6 2 0 8 null null 7 4\n"
            "5 4\n"
            "Output:\n"
            "5\n"
            "```\n\n"
        ),
        "constraints": (
            "- The tree holds between 2 and 100000 nodes.\n"
            "- Each value fits in the range -1000000000 to 1000000000 and is unique.\n"
            "- The two given values are different and both appear in the tree.\n\n"
        ),
        "inputs": [
            "3 5 1 6 2 0 8 null null 7 4\n5 1",
            "3 5 1 6 2 0 8 null null 7 4\n5 4",
            "1 2\n1 2",
            "1 2 null 3 null 4\n2 4",
            "1 null 2 null 3\n3 1",
            "-1 -2 -3 -4 -5\n-4 -5",
        ],
        "solve": solve_lowest_common_ancestor_of_a_binary_tree,
        "brute": brute_lowest_common_ancestor_of_a_binary_tree,
    },
]
