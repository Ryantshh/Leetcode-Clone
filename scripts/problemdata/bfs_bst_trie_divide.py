"""Problem data for the breadth-first search, BST, trie and divide-and-conquer group.

Exposes PROBLEMS, the list of problem specs consumed by scripts/build_problems.py.
Every solver reads a whole stdin payload and returns the whole stdout payload.
"""

from __future__ import annotations

import heapq
from collections import deque
from typing import Any

TREE_ENCODING_NOTE = """The tree is given on one line as level-order (breadth-first) tokens.
The first token is the root value. Every node already placed then consumes two
tokens in the order the nodes appear: its left child, then its right child. The
token `null` means that child is absent, and trailing `null` tokens are left out.

For example `3 9 20 null null 15 7` is the tree whose root is 3, whose root's
children are 9 and 20, where 9 has no children and 20 has children 15 and 7.
"""


class TreeNode:
    """Binary tree node holding an integer value and two optional children.

    Attributes
    ----------
    value : int
        Value stored at this node.
    left : TreeNode | None
        Left child, or None.
    right : TreeNode | None
        Right child, or None.
    """

    def __init__(self, value: int) -> None:
        """Create a childless node.

        Parameters
        ----------
        value : int
            Value stored at this node.
        """
        self.value = value
        self.left: TreeNode | None = None
        self.right: TreeNode | None = None


class QuadNode:
    """Quad tree node, either a leaf carrying a bit or an internal node with four children.

    Attributes
    ----------
    is_leaf : bool
        True when the node covers a uniform region.
    value : int
        Region value for a leaf; meaningless for an internal node.
    children : list[QuadNode]
        Top-left, top-right, bottom-left and bottom-right children, empty for a leaf.
    """

    def __init__(self, is_leaf: bool, value: int) -> None:
        """Create a node with no children attached.

        Parameters
        ----------
        is_leaf : bool
            True when the node covers a uniform region.
        value : int
            Region value for a leaf.
        """
        self.is_leaf = is_leaf
        self.value = value
        self.children: list[QuadNode] = []


def read_lines(stdin_text: str) -> list[str]:
    """Split a stdin payload into stripped lines.

    Parameters
    ----------
    stdin_text : str
        Whole stdin payload.

    Returns
    -------
    list[str]
        One stripped string per input line.
    """
    return [line.strip() for line in stdin_text.strip().split("\n")]


def parse_tree(encoded_line: str) -> TreeNode | None:
    """Rebuild a binary tree from one line of level-order tokens.

    Parameters
    ----------
    encoded_line : str
        Level-order tokens separated by spaces, with `null` for a missing child.

    Returns
    -------
    TreeNode | None
        Root of the rebuilt tree, or None when the encoding is empty.
    """
    tokens = encoded_line.split()
    if not tokens or tokens[0] == "null":
        return None
    root = TreeNode(int(tokens[0]))
    waiting = deque([root])
    token_index = 1
    while waiting and token_index < len(tokens):
        node = waiting.popleft()
        if token_index < len(tokens):
            token = tokens[token_index]
            token_index += 1
            if token != "null":
                node.left = TreeNode(int(token))
                waiting.append(node.left)
        if token_index < len(tokens):
            token = tokens[token_index]
            token_index += 1
            if token != "null":
                node.right = TreeNode(int(token))
                waiting.append(node.right)
    return root


def encode_tree(root: TreeNode | None) -> str:
    """Serialize a binary tree into one line of level-order tokens.

    Parameters
    ----------
    root : TreeNode | None
        Root of the tree.

    Returns
    -------
    str
        Space separated tokens with `null` for missing children and trailing nulls dropped.
    """
    if root is None:
        return "null"
    tokens: list[str] = []
    waiting: deque[TreeNode | None] = deque([root])
    while waiting:
        node = waiting.popleft()
        if node is None:
            tokens.append("null")
            continue
        tokens.append(str(node.value))
        waiting.append(node.left)
        waiting.append(node.right)
    while tokens and tokens[-1] == "null":
        tokens.pop()
    return " ".join(tokens)


def collect_levels_by_depth(root: TreeNode | None) -> list[list[int]]:
    """Group node values by depth using recursion.

    Parameters
    ----------
    root : TreeNode | None
        Root of the tree.

    Returns
    -------
    list[list[int]]
        Values at depth 0, depth 1 and so on, left to right within each depth.
    """
    levels: list[list[int]] = []

    def visit(node: TreeNode | None, depth: int) -> None:
        if node is None:
            return
        if depth == len(levels):
            levels.append([])
        levels[depth].append(node.value)
        visit(node.left, depth + 1)
        visit(node.right, depth + 1)

    visit(root, 0)
    return levels


def collect_values(root: TreeNode | None) -> list[int]:
    """Collect every node value in breadth-first order.

    Parameters
    ----------
    root : TreeNode | None
        Root of the tree.

    Returns
    -------
    list[int]
        Node values.
    """
    values: list[int] = []
    waiting: deque[TreeNode] = deque()
    if root is not None:
        waiting.append(root)
    while waiting:
        node = waiting.popleft()
        values.append(node.value)
        if node.left is not None:
            waiting.append(node.left)
        if node.right is not None:
            waiting.append(node.right)
    return values


def inorder_values(root: TreeNode | None) -> list[int]:
    """Collect node values in in-order using an explicit stack.

    Parameters
    ----------
    root : TreeNode | None
        Root of the tree.

    Returns
    -------
    list[int]
        Node values in left, node, right order.
    """
    values: list[int] = []
    stack: list[TreeNode] = []
    current = root
    while stack or current is not None:
        while current is not None:
            stack.append(current)
            current = current.left
        current = stack.pop()
        values.append(current.value)
        current = current.right
    return values


# --------------------------------------------------------------------------- #
# Binary Tree Right Side View
# --------------------------------------------------------------------------- #


def solve_binary_tree_right_side_view(stdin_text: str) -> str:
    """Report the rightmost value of every depth, found by level-order sweep.

    Parameters
    ----------
    stdin_text : str
        One line of level-order tokens.

    Returns
    -------
    str
        Rightmost values from the shallowest depth down, space separated.
    """
    root = parse_tree(read_lines(stdin_text)[0])
    visible: list[str] = []
    current_level: list[TreeNode] = [root] if root is not None else []
    while current_level:
        visible.append(str(current_level[-1].value))
        next_level: list[TreeNode] = []
        for node in current_level:
            if node.left is not None:
                next_level.append(node.left)
            if node.right is not None:
                next_level.append(node.right)
        current_level = next_level
    return " ".join(visible)


def brute_binary_tree_right_side_view(stdin_text: str) -> str:
    """Report the rightmost value of every depth, found by right-first recursion.

    Parameters
    ----------
    stdin_text : str
        One line of level-order tokens.

    Returns
    -------
    str
        Rightmost values from the shallowest depth down, space separated.
    """
    root = parse_tree(read_lines(stdin_text)[0])
    first_seen_per_depth: dict[int, int] = {}

    def visit(node: TreeNode | None, depth: int) -> None:
        if node is None:
            return
        if depth not in first_seen_per_depth:
            first_seen_per_depth[depth] = node.value
        visit(node.right, depth + 1)
        visit(node.left, depth + 1)

    visit(root, 0)
    return " ".join(str(first_seen_per_depth[depth]) for depth in sorted(first_seen_per_depth))


# --------------------------------------------------------------------------- #
# Average of Levels in Binary Tree
# --------------------------------------------------------------------------- #


def solve_average_of_levels_in_binary_tree(stdin_text: str) -> str:
    """Average each depth of the tree using a level-order sweep.

    Parameters
    ----------
    stdin_text : str
        One line of level-order tokens.

    Returns
    -------
    str
        One average per line, shallowest depth first, fixed to five decimals.
    """
    root = parse_tree(read_lines(stdin_text)[0])
    averages: list[str] = []
    current_level: list[TreeNode] = [root] if root is not None else []
    while current_level:
        level_total = sum(node.value for node in current_level)
        averages.append(f"{level_total / len(current_level):.5f}")
        next_level: list[TreeNode] = []
        for node in current_level:
            if node.left is not None:
                next_level.append(node.left)
            if node.right is not None:
                next_level.append(node.right)
        current_level = next_level
    return "\n".join(averages)


def brute_average_of_levels_in_binary_tree(stdin_text: str) -> str:
    """Average each depth of the tree after grouping values recursively.

    Parameters
    ----------
    stdin_text : str
        One line of level-order tokens.

    Returns
    -------
    str
        One average per line, shallowest depth first, fixed to five decimals.
    """
    levels = collect_levels_by_depth(parse_tree(read_lines(stdin_text)[0]))
    return "\n".join(f"{sum(level) / len(level):.5f}" for level in levels)


# --------------------------------------------------------------------------- #
# Binary Tree Level Order Traversal
# --------------------------------------------------------------------------- #


def solve_binary_tree_level_order_traversal(stdin_text: str) -> str:
    """List every depth of the tree using a queue.

    Parameters
    ----------
    stdin_text : str
        One line of level-order tokens.

    Returns
    -------
    str
        One depth per line, values space separated left to right.
    """
    root = parse_tree(read_lines(stdin_text)[0])
    lines: list[str] = []
    waiting: deque[TreeNode] = deque()
    if root is not None:
        waiting.append(root)
    while waiting:
        level_size = len(waiting)
        level_values: list[str] = []
        for _ in range(level_size):
            node = waiting.popleft()
            level_values.append(str(node.value))
            if node.left is not None:
                waiting.append(node.left)
            if node.right is not None:
                waiting.append(node.right)
        lines.append(" ".join(level_values))
    return "\n".join(lines)


def brute_binary_tree_level_order_traversal(stdin_text: str) -> str:
    """List every depth of the tree using depth-indexed recursion.

    Parameters
    ----------
    stdin_text : str
        One line of level-order tokens.

    Returns
    -------
    str
        One depth per line, values space separated left to right.
    """
    levels = collect_levels_by_depth(parse_tree(read_lines(stdin_text)[0]))
    return "\n".join(" ".join(str(value) for value in level) for level in levels)


# --------------------------------------------------------------------------- #
# Binary Tree Zigzag Level Order Traversal
# --------------------------------------------------------------------------- #


def solve_binary_tree_zigzag_level_order_traversal(stdin_text: str) -> str:
    """List every depth of the tree with alternating direction, filling a deque.

    Parameters
    ----------
    stdin_text : str
        One line of level-order tokens.

    Returns
    -------
    str
        One depth per line, left to right on even depths and right to left on odd ones.
    """
    root = parse_tree(read_lines(stdin_text)[0])
    lines: list[str] = []
    waiting: deque[TreeNode] = deque()
    if root is not None:
        waiting.append(root)
    is_left_to_right = True
    while waiting:
        level_values: deque[str] = deque()
        for _ in range(len(waiting)):
            node = waiting.popleft()
            if is_left_to_right:
                level_values.append(str(node.value))
            else:
                level_values.appendleft(str(node.value))
            if node.left is not None:
                waiting.append(node.left)
            if node.right is not None:
                waiting.append(node.right)
        lines.append(" ".join(level_values))
        is_left_to_right = not is_left_to_right
    return "\n".join(lines)


def brute_binary_tree_zigzag_level_order_traversal(stdin_text: str) -> str:
    """List every depth of the tree with alternating direction, reversing odd depths.

    Parameters
    ----------
    stdin_text : str
        One line of level-order tokens.

    Returns
    -------
    str
        One depth per line, left to right on even depths and right to left on odd ones.
    """
    levels = collect_levels_by_depth(parse_tree(read_lines(stdin_text)[0]))
    lines: list[str] = []
    for depth, level in enumerate(levels):
        ordered = level if depth % 2 == 0 else level[::-1]
        lines.append(" ".join(str(value) for value in ordered))
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# Minimum Absolute Difference in BST
# --------------------------------------------------------------------------- #


def solve_minimum_absolute_difference_in_bst(stdin_text: str) -> str:
    """Find the smallest gap between two values by scanning the in-order sequence.

    Parameters
    ----------
    stdin_text : str
        One line of level-order tokens describing a binary search tree.

    Returns
    -------
    str
        Smallest absolute difference between any two node values.
    """
    sorted_values = inorder_values(parse_tree(read_lines(stdin_text)[0]))
    smallest_gap = min(
        sorted_values[position + 1] - sorted_values[position]
        for position in range(len(sorted_values) - 1)
    )
    return str(smallest_gap)


def brute_minimum_absolute_difference_in_bst(stdin_text: str) -> str:
    """Find the smallest gap between two values by comparing every pair.

    Parameters
    ----------
    stdin_text : str
        One line of level-order tokens describing a binary search tree.

    Returns
    -------
    str
        Smallest absolute difference between any two node values.
    """
    values = collect_values(parse_tree(read_lines(stdin_text)[0]))
    smallest_gap = min(
        abs(values[first] - values[second])
        for first in range(len(values))
        for second in range(first + 1, len(values))
    )
    return str(smallest_gap)


# --------------------------------------------------------------------------- #
# Kth Smallest Element in a BST
# --------------------------------------------------------------------------- #


def solve_kth_smallest_element_in_a_bst(stdin_text: str) -> str:
    """Find the kth smallest value by walking in-order and stopping early.

    Parameters
    ----------
    stdin_text : str
        Level-order tokens on the first line, k on the second.

    Returns
    -------
    str
        The kth smallest node value.
    """
    lines = read_lines(stdin_text)
    root = parse_tree(lines[0])
    wanted_rank = int(lines[1])
    stack: list[TreeNode] = []
    current = root
    seen_count = 0
    while stack or current is not None:
        while current is not None:
            stack.append(current)
            current = current.left
        current = stack.pop()
        seen_count += 1
        if seen_count == wanted_rank:
            return str(current.value)
        current = current.right
    raise ValueError("k exceeds the number of nodes")


def brute_kth_smallest_element_in_a_bst(stdin_text: str) -> str:
    """Find the kth smallest value by sorting every node value.

    Parameters
    ----------
    stdin_text : str
        Level-order tokens on the first line, k on the second.

    Returns
    -------
    str
        The kth smallest node value.
    """
    lines = read_lines(stdin_text)
    values = sorted(collect_values(parse_tree(lines[0])))
    wanted_rank = int(lines[1])
    return str(values[wanted_rank - 1])


# --------------------------------------------------------------------------- #
# Validate Binary Search Tree
# --------------------------------------------------------------------------- #


def solve_validate_binary_search_tree(stdin_text: str) -> str:
    """Decide whether a tree is a binary search tree by passing value bounds down.

    Parameters
    ----------
    stdin_text : str
        One line of level-order tokens.

    Returns
    -------
    str
        "true" when every node obeys the search-tree ordering, else "false".
    """
    root = parse_tree(read_lines(stdin_text)[0])

    def is_within_bounds(node: TreeNode | None, lower: int | None, upper: int | None) -> bool:
        if node is None:
            return True
        if lower is not None and node.value <= lower:
            return False
        if upper is not None and node.value >= upper:
            return False
        return is_within_bounds(node.left, lower, node.value) and is_within_bounds(
            node.right, node.value, upper
        )

    return "true" if is_within_bounds(root, None, None) else "false"


def brute_validate_binary_search_tree(stdin_text: str) -> str:
    """Decide whether a tree is a binary search tree by checking the in-order sequence.

    Parameters
    ----------
    stdin_text : str
        One line of level-order tokens.

    Returns
    -------
    str
        "true" when the in-order sequence strictly increases, else "false".
    """
    values = inorder_values(parse_tree(read_lines(stdin_text)[0]))
    is_strictly_increasing = all(
        values[position] < values[position + 1] for position in range(len(values) - 1)
    )
    return "true" if is_strictly_increasing else "false"


# --------------------------------------------------------------------------- #
# Implement Trie (Prefix Tree)
# --------------------------------------------------------------------------- #

WORD_END_MARKER = "$"


def solve_implement_trie_prefix_tree(stdin_text: str) -> str:
    """Answer trie commands using nested dictionaries of child letters.

    Parameters
    ----------
    stdin_text : str
        Operation count on the first line, then one operation per line.

    Returns
    -------
    str
        "true" or "false" per search and startsWith command, one per line.
    """
    lines = read_lines(stdin_text)
    operation_count = int(lines[0])
    root: dict[str, Any] = {}
    answers: list[str] = []
    for line in lines[1 : 1 + operation_count]:
        command, argument = line.split()
        if command == "insert":
            node = root
            for letter in argument:
                node = node.setdefault(letter, {})
            node[WORD_END_MARKER] = True
            continue
        node = root
        has_path = True
        for letter in argument:
            if letter not in node:
                has_path = False
                break
            node = node[letter]
        if command == "search":
            answers.append("true" if has_path and WORD_END_MARKER in node else "false")
        else:
            answers.append("true" if has_path else "false")
    return "\n".join(answers)


def brute_implement_trie_prefix_tree(stdin_text: str) -> str:
    """Answer trie commands by rescanning the list of inserted words.

    Parameters
    ----------
    stdin_text : str
        Operation count on the first line, then one operation per line.

    Returns
    -------
    str
        "true" or "false" per search and startsWith command, one per line.
    """
    lines = read_lines(stdin_text)
    operation_count = int(lines[0])
    inserted_words: list[str] = []
    answers: list[str] = []
    for line in lines[1 : 1 + operation_count]:
        command, argument = line.split()
        if command == "insert":
            inserted_words.append(argument)
        elif command == "search":
            answers.append("true" if argument in inserted_words else "false")
        else:
            has_prefix = any(word.startswith(argument) for word in inserted_words)
            answers.append("true" if has_prefix else "false")
    return "\n".join(answers)


# --------------------------------------------------------------------------- #
# Design Add and Search Words Data Structure
# --------------------------------------------------------------------------- #


def solve_design_add_and_search_words_data_structure(stdin_text: str) -> str:
    """Answer wildcard word queries with a trie walked by recursive descent.

    Parameters
    ----------
    stdin_text : str
        Operation count on the first line, then one operation per line.

    Returns
    -------
    str
        "true" or "false" per search command, one per line.
    """
    lines = read_lines(stdin_text)
    operation_count = int(lines[0])
    root: dict[str, Any] = {}
    answers: list[str] = []

    def matches(node: dict[str, Any], pattern: str, position: int) -> bool:
        if position == len(pattern):
            return WORD_END_MARKER in node
        letter = pattern[position]
        if letter == ".":
            for key, child in node.items():
                if key != WORD_END_MARKER and matches(child, pattern, position + 1):
                    return True
            return False
        child = node.get(letter)
        return child is not None and matches(child, pattern, position + 1)

    for line in lines[1 : 1 + operation_count]:
        command, argument = line.split()
        if command == "addWord":
            node = root
            for letter in argument:
                node = node.setdefault(letter, {})
            node[WORD_END_MARKER] = True
            continue
        answers.append("true" if matches(root, argument, 0) else "false")
    return "\n".join(answers)


def brute_design_add_and_search_words_data_structure(stdin_text: str) -> str:
    """Answer wildcard word queries by comparing each stored word position by position.

    Parameters
    ----------
    stdin_text : str
        Operation count on the first line, then one operation per line.

    Returns
    -------
    str
        "true" or "false" per search command, one per line.
    """
    lines = read_lines(stdin_text)
    operation_count = int(lines[0])
    stored_words: list[str] = []
    answers: list[str] = []
    for line in lines[1 : 1 + operation_count]:
        command, argument = line.split()
        if command == "addWord":
            stored_words.append(argument)
            continue
        has_match = False
        for word in stored_words:
            if len(word) != len(argument):
                continue
            if all(
                pattern_letter in (".", word_letter)
                for pattern_letter, word_letter in zip(argument, word)
            ):
                has_match = True
                break
        answers.append("true" if has_match else "false")
    return "\n".join(answers)


# --------------------------------------------------------------------------- #
# Word Search II
# --------------------------------------------------------------------------- #

GRID_STEPS = ((-1, 0), (1, 0), (0, -1), (0, 1))


def parse_word_search(stdin_text: str) -> tuple[list[list[str]], list[str]]:
    """Read the grid and the word list of a Word Search II payload.

    Parameters
    ----------
    stdin_text : str
        Dimensions line, grid rows, word count line, then the words.

    Returns
    -------
    tuple[list[list[str]], list[str]]
        Grid as rows of single letters, and the words to look for.
    """
    lines = read_lines(stdin_text)
    row_count = int(lines[0].split()[0])
    grid = [list(lines[1 + row_index].replace(" ", "")) for row_index in range(row_count)]
    word_count = int(lines[1 + row_count])
    words = [lines[2 + row_count + offset] for offset in range(word_count)]
    return grid, words


def solve_word_search_ii(stdin_text: str) -> str:
    """Find every listed word in the grid with one trie-guided walk per starting cell.

    Parameters
    ----------
    stdin_text : str
        Dimensions line, grid rows, word count line, then the words.

    Returns
    -------
    str
        Found words sorted lexicographically, one per line, or "none".
    """
    grid, words = parse_word_search(stdin_text)
    row_count = len(grid)
    column_count = len(grid[0])
    root: dict[str, Any] = {}
    for word in words:
        node = root
        for letter in word:
            node = node.setdefault(letter, {})
        node[WORD_END_MARKER] = word
    found: set[str] = set()

    def walk(row: int, column: int, node: dict[str, Any]) -> None:
        letter = grid[row][column]
        child = node.get(letter)
        if child is None:
            return
        complete_word = child.get(WORD_END_MARKER)
        if complete_word is not None:
            found.add(complete_word)
        grid[row][column] = "#"
        for row_step, column_step in GRID_STEPS:
            next_row = row + row_step
            next_column = column + column_step
            if 0 <= next_row < row_count and 0 <= next_column < column_count:
                walk(next_row, next_column, child)
        grid[row][column] = letter

    for row in range(row_count):
        for column in range(column_count):
            walk(row, column, root)
    if not found:
        return "none"
    return "\n".join(sorted(found))


def brute_word_search_ii(stdin_text: str) -> str:
    """Find every listed word by backtracking the grid separately for each word.

    Parameters
    ----------
    stdin_text : str
        Dimensions line, grid rows, word count line, then the words.

    Returns
    -------
    str
        Found words sorted lexicographically, one per line, or "none".
    """
    grid, words = parse_word_search(stdin_text)
    row_count = len(grid)
    column_count = len(grid[0])

    def backtrack(row: int, column: int, word: str, position: int) -> bool:
        if grid[row][column] != word[position]:
            return False
        if position == len(word) - 1:
            return True
        letter = grid[row][column]
        grid[row][column] = "#"
        for row_step, column_step in GRID_STEPS:
            next_row = row + row_step
            next_column = column + column_step
            is_inside = 0 <= next_row < row_count and 0 <= next_column < column_count
            if is_inside and backtrack(next_row, next_column, word, position + 1):
                grid[row][column] = letter
                return True
        grid[row][column] = letter
        return False

    found: list[str] = []
    for word in words:
        is_present = any(
            backtrack(row, column, word, 0)
            for row in range(row_count)
            for column in range(column_count)
        )
        if is_present and word not in found:
            found.append(word)
    if not found:
        return "none"
    return "\n".join(sorted(found))


# --------------------------------------------------------------------------- #
# Convert Sorted Array to Binary Search Tree
# --------------------------------------------------------------------------- #


def solve_convert_sorted_array_to_binary_search_tree(stdin_text: str) -> str:
    """Build the left-biased balanced search tree by recursive halving.

    Parameters
    ----------
    stdin_text : str
        Element count on the first line, the sorted values on the second.

    Returns
    -------
    str
        Level-order encoding of the built tree.
    """
    lines = read_lines(stdin_text)
    element_count = int(lines[0])
    values = [int(part) for part in lines[1].split()][:element_count]

    def build(low: int, high: int) -> TreeNode | None:
        if low > high:
            return None
        middle = (low + high) // 2
        node = TreeNode(values[middle])
        node.left = build(low, middle - 1)
        node.right = build(middle + 1, high)
        return node

    return encode_tree(build(0, element_count - 1))


def brute_convert_sorted_array_to_binary_search_tree(stdin_text: str) -> str:
    """Build the left-biased balanced search tree with an explicit range stack.

    Parameters
    ----------
    stdin_text : str
        Element count on the first line, the sorted values on the second.

    Returns
    -------
    str
        Level-order encoding of the built tree.
    """
    lines = read_lines(stdin_text)
    element_count = int(lines[0])
    values = [int(part) for part in lines[1].split()][:element_count]
    root_index = (element_count - 1) // 2
    root = TreeNode(values[root_index])
    pending: list[tuple[int, int, TreeNode, bool]] = [
        (0, root_index - 1, root, True),
        (root_index + 1, element_count - 1, root, False),
    ]
    while pending:
        low, high, parent, is_left_child = pending.pop()
        if low > high:
            continue
        middle = (low + high) // 2
        child = TreeNode(values[middle])
        if is_left_child:
            parent.left = child
        else:
            parent.right = child
        pending.append((low, middle - 1, child, True))
        pending.append((middle + 1, high, child, False))
    return encode_tree(root)


# --------------------------------------------------------------------------- #
# Sort List
# --------------------------------------------------------------------------- #


def solve_sort_list(stdin_text: str) -> str:
    """Sort the sequence with a top-down merge sort.

    Parameters
    ----------
    stdin_text : str
        Element count on the first line, the values on the second.

    Returns
    -------
    str
        Sorted values on one line, space separated.
    """
    lines = read_lines(stdin_text)
    element_count = int(lines[0])
    values = [int(part) for part in lines[1].split()][:element_count]

    def merge_sort(items: list[int]) -> list[int]:
        if len(items) <= 1:
            return items
        middle = len(items) // 2
        left_half = merge_sort(items[:middle])
        right_half = merge_sort(items[middle:])
        merged: list[int] = []
        left_position = 0
        right_position = 0
        while left_position < len(left_half) and right_position < len(right_half):
            if left_half[left_position] <= right_half[right_position]:
                merged.append(left_half[left_position])
                left_position += 1
            else:
                merged.append(right_half[right_position])
                right_position += 1
        merged.extend(left_half[left_position:])
        merged.extend(right_half[right_position:])
        return merged

    return " ".join(str(value) for value in merge_sort(values))


def brute_sort_list(stdin_text: str) -> str:
    """Sort the sequence with an insertion sort.

    Parameters
    ----------
    stdin_text : str
        Element count on the first line, the values on the second.

    Returns
    -------
    str
        Sorted values on one line, space separated.
    """
    lines = read_lines(stdin_text)
    element_count = int(lines[0])
    values = [int(part) for part in lines[1].split()][:element_count]
    sorted_values: list[int] = []
    for value in values:
        insert_at = len(sorted_values)
        for position, placed_value in enumerate(sorted_values):
            if value < placed_value:
                insert_at = position
                break
        sorted_values.insert(insert_at, value)
    return " ".join(str(value) for value in sorted_values)


# --------------------------------------------------------------------------- #
# Construct Quad Tree
# --------------------------------------------------------------------------- #


def parse_binary_grid(stdin_text: str) -> list[list[int]]:
    """Read the size line and the binary rows of a quad tree payload.

    Parameters
    ----------
    stdin_text : str
        Grid size on the first line, then that many rows of 0 and 1 characters.

    Returns
    -------
    list[list[int]]
        Grid values as integers.
    """
    lines = read_lines(stdin_text)
    size = int(lines[0])
    return [
        [int(character) for character in lines[1 + row_index].replace(" ", "")]
        for row_index in range(size)
    ]


def solve_construct_quad_tree(stdin_text: str) -> str:
    """Build the quad tree bottom-up, merging four equal leaves, then walk it in preorder.

    Parameters
    ----------
    stdin_text : str
        Grid size on the first line, then that many rows of 0 and 1 characters.

    Returns
    -------
    str
        Preorder walk, one node per line, as "leaf <value>" or "internal".
    """
    grid = parse_binary_grid(stdin_text)

    def build(top_row: int, left_column: int, length: int) -> QuadNode:
        if length == 1:
            return QuadNode(True, grid[top_row][left_column])
        half = length // 2
        children = [
            build(top_row, left_column, half),
            build(top_row, left_column + half, half),
            build(top_row + half, left_column, half),
            build(top_row + half, left_column + half, half),
        ]
        values_seen = {child.value for child in children}
        if all(child.is_leaf for child in children) and len(values_seen) == 1:
            return QuadNode(True, children[0].value)
        internal = QuadNode(False, 1)
        internal.children = children
        return internal

    lines: list[str] = []

    def describe(node: QuadNode) -> None:
        if node.is_leaf:
            lines.append(f"leaf {node.value}")
            return
        lines.append("internal")
        for child in node.children:
            describe(child)

    describe(build(0, 0, len(grid)))
    return "\n".join(lines)


def brute_construct_quad_tree(stdin_text: str) -> str:
    """Emit the quad tree preorder directly, testing each region for uniformity with a stack.

    Parameters
    ----------
    stdin_text : str
        Grid size on the first line, then that many rows of 0 and 1 characters.

    Returns
    -------
    str
        Preorder walk, one node per line, as "leaf <value>" or "internal".
    """
    grid = parse_binary_grid(stdin_text)
    lines: list[str] = []
    pending: list[tuple[int, int, int]] = [(0, 0, len(grid))]
    while pending:
        top_row, left_column, length = pending.pop()
        first_value = grid[top_row][left_column]
        region_values = {
            grid[row][column]
            for row in range(top_row, top_row + length)
            for column in range(left_column, left_column + length)
        }
        if len(region_values) == 1:
            lines.append(f"leaf {first_value}")
            continue
        lines.append("internal")
        half = length // 2
        # Pushed in reverse so the children pop in topLeft, topRight, bottomLeft, bottomRight order.
        pending.append((top_row + half, left_column + half, half))
        pending.append((top_row + half, left_column, half))
        pending.append((top_row, left_column + half, half))
        pending.append((top_row, left_column, half))
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# Merge k Sorted Lists
# --------------------------------------------------------------------------- #


def parse_sorted_lists(stdin_text: str) -> list[list[int]]:
    """Read the list count and each list's length-prefixed values.

    Parameters
    ----------
    stdin_text : str
        List count on the first line, then one line per list holding its length then its values.

    Returns
    -------
    list[list[int]]
        The input lists, each already sorted.
    """
    lines = read_lines(stdin_text)
    list_count = int(lines[0])
    lists: list[list[int]] = []
    for line_index in range(1, 1 + list_count):
        numbers = [int(part) for part in lines[line_index].split()]
        length = numbers[0]
        lists.append(numbers[1 : 1 + length])
    return lists


def solve_merge_k_sorted_lists(stdin_text: str) -> str:
    """Merge the sorted lists with a heap holding one candidate per list.

    Parameters
    ----------
    stdin_text : str
        List count on the first line, then one line per list holding its length then its values.

    Returns
    -------
    str
        Merged values in non-decreasing order on one line, space separated.
    """
    lists = parse_sorted_lists(stdin_text)
    heap: list[tuple[int, int, int]] = []
    for list_index, values in enumerate(lists):
        if values:
            heap.append((values[0], list_index, 0))
    heapq.heapify(heap)
    merged: list[str] = []
    while heap:
        value, list_index, position = heapq.heappop(heap)
        merged.append(str(value))
        next_position = position + 1
        if next_position < len(lists[list_index]):
            heapq.heappush(heap, (lists[list_index][next_position], list_index, next_position))
    return " ".join(merged)


def brute_merge_k_sorted_lists(stdin_text: str) -> str:
    """Merge the sorted lists by folding them together two at a time.

    Parameters
    ----------
    stdin_text : str
        List count on the first line, then one line per list holding its length then its values.

    Returns
    -------
    str
        Merged values in non-decreasing order on one line, space separated.
    """
    lists = parse_sorted_lists(stdin_text)
    merged: list[int] = []
    for values in lists:
        combined: list[int] = []
        left_position = 0
        right_position = 0
        while left_position < len(merged) and right_position < len(values):
            if merged[left_position] <= values[right_position]:
                combined.append(merged[left_position])
                left_position += 1
            else:
                combined.append(values[right_position])
                right_position += 1
        combined.extend(merged[left_position:])
        combined.extend(values[right_position:])
        merged = combined
    return " ".join(str(value) for value in merged)


PROBLEMS: list[dict[str, Any]] = [
    {
        "title": "Binary Tree Right Side View",
        "level": "Medium",
        "topics": "Tree, Breadth-First Search, Depth-First Search, Binary Tree",
        "companies": "Amazon, Microsoft, Bloomberg, Meta",
        "description": (
            "Imagine standing to the right of a binary tree and looking at it straight on. "
            "At every depth you can only see the node that sits furthest to the right. "
            "Report those visible values from the top of the tree downwards.\n\n"
            "**Input**\n\n"
            "A single line.\n\n" + TREE_ENCODING_NOTE + "\n"
            "**Output**\n\n"
            "One line holding the visible value of each depth, shallowest first, "
            "separated by single spaces.\n\n"
        ),
        "examples": (
            "**Example 1**\n\n"
            "```\n"
            "Input\n"
            "1 2 3 null 5 null 4\n"
            "Output\n"
            "1 3 4\n"
            "```\n\n"
            "At depth 0 only 1 is visible, at depth 1 the rightmost node is 3, "
            "and at depth 2 the only node is 4.\n\n"
            "**Example 2**\n\n"
            "```\n"
            "Input\n"
            "1 2 null 3 null 4\n"
            "Output\n"
            "1 2 3 4\n"
            "```\n\n"
            "Every depth of this left-leaning chain has exactly one node, so all of them are "
            "visible.\n\n"
        ),
        "constraints": (
            "- The tree holds between 1 and 100 nodes.\n"
            "- Each node value fits in the range -100 to 100.\n"
            "- The input is always a single line of level-order tokens.\n\n"
        ),
        "inputs": [
            "1 2 3 null 5 null 4",
            "3 9 20 null null 15 7",
            "1",
            "1 2 null 3 null 4",
            "1 null 2 null 3",
            "5 3 8 2 4 7 9",
        ],
        "solve": solve_binary_tree_right_side_view,
        "brute": brute_binary_tree_right_side_view,
    },
    {
        "title": "Average of Levels in Binary Tree",
        "level": "Easy",
        "topics": "Tree, Breadth-First Search, Binary Tree",
        "companies": "Facebook, Amazon, Adobe",
        "description": (
            "For every depth of a binary tree, work out the average of the values stored at "
            "that depth, then report the averages from the top of the tree downwards.\n\n"
            "**Input**\n\n"
            "A single line.\n\n" + TREE_ENCODING_NOTE + "\n"
            "**Output**\n\n"
            "One average per line, shallowest depth first. Every average is printed with "
            "exactly five digits after the decimal point, so an average of 3 prints as "
            "`3.00000`.\n\n"
        ),
        "examples": (
            "**Example 1**\n\n"
            "```\n"
            "Input\n"
            "3 9 20 null null 15 7\n"
            "Output\n"
            "3.00000\n"
            "14.50000\n"
            "11.00000\n"
            "```\n\n"
            "The depths hold [3], [9, 20] and [15, 7].\n\n"
            "**Example 2**\n\n"
            "```\n"
            "Input\n"
            "1\n"
            "Output\n"
            "1.00000\n"
            "```\n\n"
            "A single node means a single depth.\n\n"
        ),
        "constraints": (
            "- The tree holds between 1 and 10000 nodes.\n"
            "- Each node value fits in the range -2^31 to 2^31 - 1.\n"
            "- Averages must be printed with exactly five decimal places.\n\n"
        ),
        "inputs": [
            "3 9 20 null null 15 7",
            "1",
            "3 9 20 15 7",
            "1 2 null 3 null 4",
            "1 null 2 null 3",
            "5 3 8 2 4 7 9",
        ],
        "solve": solve_average_of_levels_in_binary_tree,
        "brute": brute_average_of_levels_in_binary_tree,
    },
    {
        "title": "Binary Tree Level Order Traversal",
        "level": "Medium",
        "topics": "Tree, Breadth-First Search, Binary Tree",
        "companies": "Amazon, Microsoft, LinkedIn, Bloomberg",
        "description": (
            "Visit a binary tree depth by depth, starting at the root, and report the values "
            "found at each depth from left to right.\n\n"
            "**Input**\n\n"
            "A single line.\n\n" + TREE_ENCODING_NOTE + "\n"
            "**Output**\n\n"
            "One line per depth, shallowest first. Each line holds that depth's values from "
            "left to right, separated by single spaces.\n\n"
        ),
        "examples": (
            "**Example 1**\n\n"
            "```\n"
            "Input\n"
            "3 9 20 null null 15 7\n"
            "Output\n"
            "3\n"
            "9 20\n"
            "15 7\n"
            "```\n\n"
            "**Example 2**\n\n"
            "```\n"
            "Input\n"
            "1 2 3 4 null null 5\n"
            "Output\n"
            "1\n"
            "2 3\n"
            "4 5\n"
            "```\n\n"
            "Node 2 has only a left child and node 3 has only a right child, so the deepest "
            "line holds 4 then 5.\n\n"
        ),
        "constraints": (
            "- The tree holds between 1 and 2000 nodes.\n"
            "- Each node value fits in the range -1000 to 1000.\n"
            "- The input is always a single line of level-order tokens.\n\n"
        ),
        "inputs": [
            "3 9 20 null null 15 7",
            "1 2 3 4 null null 5",
            "1",
            "1 2 null 3 null 4",
            "1 null 2 null 3",
            "5 3 8 2 4 7 9",
        ],
        "solve": solve_binary_tree_level_order_traversal,
        "brute": brute_binary_tree_level_order_traversal,
    },
    {
        "title": "Binary Tree Zigzag Level Order Traversal",
        "level": "Medium",
        "topics": "Tree, Breadth-First Search, Binary Tree",
        "companies": "Amazon, Microsoft, Bloomberg, Apple",
        "description": (
            "Walk a binary tree depth by depth, but change direction on every depth. The root "
            "depth is read left to right, the next depth right to left, the one after that "
            "left to right again, and so on.\n\n"
            "**Input**\n\n"
            "A single line.\n\n" + TREE_ENCODING_NOTE + "\n"
            "**Output**\n\n"
            "One line per depth, shallowest first, values separated by single spaces and "
            "ordered according to that depth's reading direction.\n\n"
        ),
        "examples": (
            "**Example 1**\n\n"
            "```\n"
            "Input\n"
            "3 9 20 null null 15 7\n"
            "Output\n"
            "3\n"
            "20 9\n"
            "15 7\n"
            "```\n\n"
            "Depth 1 is reversed, depth 2 goes back to left-to-right.\n\n"
            "**Example 2**\n\n"
            "```\n"
            "Input\n"
            "1 2 3 4 null null 5\n"
            "Output\n"
            "1\n"
            "3 2\n"
            "4 5\n"
            "```\n\n"
        ),
        "constraints": (
            "- The tree holds between 1 and 2000 nodes.\n"
            "- Each node value fits in the range -100 to 100.\n"
            "- The root depth is always read left to right.\n\n"
        ),
        "inputs": [
            "3 9 20 null null 15 7",
            "1 2 3 4 null null 5",
            "1",
            "1 2 null 3 null 4",
            "1 null 2 null 3",
            "5 3 8 2 4 7 9",
        ],
        "solve": solve_binary_tree_zigzag_level_order_traversal,
        "brute": brute_binary_tree_zigzag_level_order_traversal,
    },
    {
        "title": "Minimum Absolute Difference in BST",
        "level": "Easy",
        "topics": "Tree, Depth-First Search, Binary Search Tree, Binary Tree",
        "companies": "Google, Amazon, Adobe",
        "description": (
            "A binary search tree keeps every value in its left subtree smaller than the node "
            "and every value in its right subtree larger. Given such a tree, find the smallest "
            "absolute difference between any two different nodes' values.\n\n"
            "**Input**\n\n"
            "A single line.\n\n" + TREE_ENCODING_NOTE + "\n"
            "**Output**\n\n"
            "One line holding the smallest absolute difference as an integer.\n\n"
        ),
        "examples": (
            "**Example 1**\n\n"
            "```\n"
            "Input\n"
            "4 2 6 1 3\n"
            "Output\n"
            "1\n"
            "```\n\n"
            "The values in order are 1, 2, 3, 4, 6, and the closest neighbours differ by 1.\n\n"
            "**Example 2**\n\n"
            "```\n"
            "Input\n"
            "236 104 701 null 227 null 911\n"
            "Output\n"
            "9\n"
            "```\n\n"
            "The values in order are 104, 227, 236, 701, 911, and 236 - 227 is the smallest gap.\n\n"
        ),
        "constraints": (
            "- The tree holds between 2 and 10000 nodes.\n"
            "- Each node value fits in the range 0 to 10^5.\n"
            "- The input is always a valid binary search tree with distinct values.\n\n"
        ),
        "inputs": [
            "4 2 6 1 3",
            "236 104 701 null 227 null 911",
            "1 null 5",
            "90 69 null 49 89 null 52",
            "10 5 15",
        ],
        "solve": solve_minimum_absolute_difference_in_bst,
        "brute": brute_minimum_absolute_difference_in_bst,
    },
    {
        "title": "Kth Smallest Element in a BST",
        "level": "Medium",
        "topics": "Tree, Depth-First Search, Binary Search Tree, Binary Tree",
        "companies": "Amazon, Google, Uber, Bloomberg",
        "description": (
            "A binary search tree keeps every value in its left subtree smaller than the node "
            "and every value in its right subtree larger. Given such a tree and a rank k, "
            "report the kth smallest value stored in it, counting from 1.\n\n"
            "**Input**\n\n"
            "Two lines.\n\n" + TREE_ENCODING_NOTE + "\n"
            "The second line holds the integer k.\n\n"
            "**Output**\n\n"
            "One line holding the kth smallest value.\n\n"
        ),
        "examples": (
            "**Example 1**\n\n"
            "```\n"
            "Input\n"
            "3 1 4 null 2\n"
            "1\n"
            "Output\n"
            "1\n"
            "```\n\n"
            "The values in order are 1, 2, 3, 4, so the smallest is 1.\n\n"
            "**Example 2**\n\n"
            "```\n"
            "Input\n"
            "5 3 6 2 4 null null 1\n"
            "3\n"
            "Output\n"
            "3\n"
            "```\n\n"
            "The values in order are 1, 2, 3, 4, 5, 6, and the third of those is 3.\n\n"
        ),
        "constraints": (
            "- The tree holds between 1 and 10000 nodes.\n"
            "- 1 <= k <= number of nodes.\n"
            "- Each node value fits in the range 0 to 10^4.\n\n"
        ),
        "inputs": [
            "3 1 4 null 2\n1",
            "5 3 6 2 4 null null 1\n3",
            "1\n1",
            "1 null 2 null 3\n3",
            "2 1\n2",
            "8 3 10 1 6 null 14 null null 4 7\n5",
        ],
        "solve": solve_kth_smallest_element_in_a_bst,
        "brute": brute_kth_smallest_element_in_a_bst,
    },
    {
        "title": "Validate Binary Search Tree",
        "level": "Medium",
        "topics": "Tree, Depth-First Search, Binary Search Tree, Binary Tree",
        "companies": "Amazon, Microsoft, Meta, Bloomberg",
        "description": (
            "Decide whether a binary tree is a valid binary search tree. It is valid when, for "
            "every node, all values in its left subtree are strictly smaller than the node and "
            "all values in its right subtree are strictly larger. Equal values are never "
            "allowed.\n\n"
            "**Input**\n\n"
            "A single line.\n\n" + TREE_ENCODING_NOTE + "\n"
            "**Output**\n\n"
            "One line holding `true` or `false`, in lower case.\n\n"
        ),
        "examples": (
            "**Example 1**\n\n"
            "```\n"
            "Input\n"
            "2 1 3\n"
            "Output\n"
            "true\n"
            "```\n\n"
            "**Example 2**\n\n"
            "```\n"
            "Input\n"
            "5 1 4 null null 3 6\n"
            "Output\n"
            "false\n"
            "```\n\n"
            "Node 3 sits in the right subtree of 5 but is smaller than 5, so the ordering "
            "breaks.\n\n"
        ),
        "constraints": (
            "- The tree holds between 1 and 10000 nodes.\n"
            "- Each node value fits in the range -2^31 to 2^31 - 1.\n"
            "- Output is exactly `true` or `false` in lower case.\n\n"
        ),
        "inputs": [
            "2 1 3",
            "5 1 4 null null 3 6",
            "1",
            "10 5 15 null null 6 20",
            "2 2 2",
            "5 1 7 null null 6 8",
        ],
        "solve": solve_validate_binary_search_tree,
        "brute": brute_validate_binary_search_tree,
    },
    {
        "title": "Implement Trie (Prefix Tree)",
        "level": "Medium",
        "topics": "Design, Trie, Hash Table, String",
        "companies": "Google, Amazon, Microsoft, Twitter",
        "description": (
            "Build a prefix tree that stores lower case words and answers three commands:\n\n"
            "- `insert word` stores a word and reports nothing.\n"
            "- `search word` reports whether that exact word was stored before.\n"
            "- `startsWith prefix` reports whether any stored word begins with that prefix.\n\n"
            "**Input**\n\n"
            "The first line holds q, the number of commands. Each of the next q lines holds one "
            "command: the command name, a single space, then its word or prefix.\n\n"
            "**Output**\n\n"
            "One line for every `search` and `startsWith` command, in the order the commands "
            "appear, holding `true` or `false` in lower case. `insert` prints nothing.\n\n"
        ),
        "examples": (
            "**Example 1**\n\n"
            "```\n"
            "Input\n"
            "6\n"
            "insert apple\n"
            "search apple\n"
            "search app\n"
            "startsWith app\n"
            "insert app\n"
            "search app\n"
            "Output\n"
            "true\n"
            "false\n"
            "true\n"
            "true\n"
            "```\n\n"
            "`app` is only a prefix of `apple` until it is inserted in its own right.\n\n"
            "**Example 2**\n\n"
            "```\n"
            "Input\n"
            "3\n"
            "search a\n"
            "startsWith a\n"
            "insert a\n"
            "Output\n"
            "false\n"
            "false\n"
            "```\n\n"
            "Both queries run against an empty trie.\n\n"
        ),
        "constraints": (
            "- 1 <= q <= 30000.\n"
            "- Words and prefixes hold 1 to 2000 lower case English letters.\n"
            "- Every input holds at least one `search` or `startsWith` command.\n\n"
        ),
        "inputs": [
            "6\ninsert apple\nsearch apple\nsearch app\nstartsWith app\ninsert app\nsearch app",
            "3\nsearch a\nstartsWith a\ninsert a",
            "4\ninsert banana\nsearch ban\nstartsWith ban\nstartsWith bananas",
            "7\ninsert dog\ninsert deer\ninsert deal\nsearch dog\nsearch doge\n"
            "startsWith de\nstartsWith z",
            "2\ninsert a\nsearch a",
        ],
        "solve": solve_implement_trie_prefix_tree,
        "brute": brute_implement_trie_prefix_tree,
    },
    {
        "title": "Design Add and Search Words Data Structure",
        "level": "Medium",
        "topics": "Design, Trie, Depth-First Search, String",
        "companies": "Meta, Amazon, Google, Microsoft",
        "description": (
            "Build a word store that supports two commands:\n\n"
            "- `addWord word` stores a word of lower case letters and reports nothing.\n"
            "- `search pattern` reports whether any stored word matches the pattern. A pattern "
            "may contain the character `.`, which stands for exactly one letter of any kind. A "
            "match requires the same length and agreement at every position.\n\n"
            "**Input**\n\n"
            "The first line holds q, the number of commands. Each of the next q lines holds one "
            "command: the command name, a single space, then its word or pattern.\n\n"
            "**Output**\n\n"
            "One line for every `search` command, in the order the commands appear, holding "
            "`true` or `false` in lower case. `addWord` prints nothing.\n\n"
        ),
        "examples": (
            "**Example 1**\n\n"
            "```\n"
            "Input\n"
            "6\n"
            "addWord bad\n"
            "addWord dad\n"
            "addWord mad\n"
            "search pad\n"
            "search bad\n"
            "search .ad\n"
            "Output\n"
            "false\n"
            "true\n"
            "true\n"
            "```\n\n"
            "`pad` was never stored, while `.ad` matches all three stored words.\n\n"
            "**Example 2**\n\n"
            "```\n"
            "Input\n"
            "5\n"
            "addWord bad\n"
            "search b..\n"
            "search ...\n"
            "search ....\n"
            "search ..\n"
            "Output\n"
            "true\n"
            "true\n"
            "false\n"
            "false\n"
            "```\n\n"
            "A pattern only matches words of exactly its own length.\n\n"
        ),
        "constraints": (
            "- 1 <= q <= 10000.\n"
            "- Words hold 1 to 25 lower case English letters.\n"
            "- Patterns hold 1 to 25 characters, each a lower case letter or `.`.\n"
            "- Every input holds at least one `search` command.\n\n"
        ),
        "inputs": [
            "6\naddWord bad\naddWord dad\naddWord mad\nsearch pad\nsearch bad\nsearch .ad",
            "5\naddWord bad\nsearch b..\nsearch ...\nsearch ....\nsearch ..",
            "3\nsearch a\naddWord a\nsearch .",
            "4\naddWord ab\naddWord abc\nsearch ab\nsearch a.c",
            "5\naddWord cat\naddWord car\nsearch c.t\nsearch c..\nsearch ca.s",
        ],
        "solve": solve_design_add_and_search_words_data_structure,
        "brute": brute_design_add_and_search_words_data_structure,
    },
    {
        "title": "Word Search II",
        "level": "Hard",
        "topics": "Trie, Backtracking, Matrix, Depth-First Search",
        "companies": "Amazon, Google, Microsoft, Uber",
        "description": (
            "A grid of lower case letters is given together with a list of candidate words. A "
            "word is present when it can be spelled by stepping from cell to neighbouring cell, "
            "where neighbours share an edge up, down, left or right. A single cell may not be "
            "used twice within one word. Report which candidate words are present.\n\n"
            "**Input**\n\n"
            "The first line holds two integers, the number of rows and the number of columns, "
            "separated by a space. The next rows lines each hold one grid row as a run of lower "
            "case letters with no spaces. The line after the grid holds w, the number of "
            "candidate words, and the final w lines each hold one word.\n\n"
            "**Output**\n\n"
            "The words that are present, sorted lexicographically, one per line. When no word "
            "is present, print the single line `none`.\n\n"
        ),
        "examples": (
            "**Example 1**\n\n"
            "```\n"
            "Input\n"
            "4 4\n"
            "oaan\n"
            "etae\n"
            "ihkr\n"
            "iflv\n"
            "4\n"
            "oath\n"
            "pea\n"
            "eat\n"
            "rain\n"
            "Output\n"
            "eat\n"
            "oath\n"
            "```\n\n"
            "`oath` is spelled by the o and a of the top row, then the t and h below them. "
            "`eat` starts at the e that ends the second row. Neither `pea` nor `rain` has a "
            "path, and the two found words are printed in alphabetical order.\n\n"
            "**Example 2**\n\n"
            "```\n"
            "Input\n"
            "2 2\n"
            "ab\n"
            "cd\n"
            "2\n"
            "abcd\n"
            "dcba\n"
            "Output\n"
            "none\n"
            "```\n\n"
            "Neither word has a path through edge-sharing cells.\n\n"
        ),
        "constraints": (
            "- 1 <= rows, columns <= 12.\n"
            "- 1 <= w <= 30000.\n"
            "- Grid letters and word letters are lower case English letters.\n"
            "- Words hold 1 to 10 letters and are all different.\n\n"
        ),
        "inputs": [
            "4 4\noaan\netae\nihkr\niflv\n4\noath\npea\neat\nrain",
            "2 2\nab\ncd\n2\nabcd\ndcba",
            "1 1\na\n2\na\naa",
            "3 3\nabc\ndef\nghi\n3\nabc\nadg\nceg",
            "2 3\naaa\naaa\n3\naaaaaa\naaaaaaa\naa",
        ],
        "solve": solve_word_search_ii,
        "brute": brute_word_search_ii,
    },
    {
        "title": "Convert Sorted Array to Binary Search Tree",
        "level": "Easy",
        "topics": "Divide and Conquer, Binary Search Tree, Tree, Array",
        "companies": "Amazon, Microsoft, Airbnb",
        "description": (
            "Turn a sorted array of distinct integers into a height-balanced binary search "
            "tree. Many balanced trees fit the same array, so the shape is pinned down by one "
            "rule: for the index range low to high, the root of that range is always the "
            "element at index `(low + high) // 2`. When the range holds an even number of "
            "elements, that rule picks the left of the two middle elements. Elements before the "
            "chosen index build the left subtree and elements after it build the right subtree, "
            "by the same rule.\n\n"
            "**Input**\n\n"
            "The first line holds n, the number of elements. The second line holds the n "
            "elements in increasing order, separated by spaces.\n\n"
            "**Output**\n\n"
            "One line holding the resulting tree in level-order (breadth-first) encoding: the "
            "root value first, then two tokens for every node already placed, its left child "
            "then its right child, with `null` for a missing child and trailing `null` tokens "
            "omitted.\n\n"
        ),
        "examples": (
            "**Example 1**\n\n"
            "```\n"
            "Input\n"
            "7\n"
            "-10 -3 0 5 9 12 20\n"
            "Output\n"
            "5 -3 12 -10 0 9 20\n"
            "```\n\n"
            "Indices 0 to 6 pick index 3, the value 5, as the root.\n\n"
            "**Example 2**\n\n"
            "```\n"
            "Input\n"
            "4\n"
            "1 2 3 4\n"
            "Output\n"
            "2 1 3 null null null 4\n"
            "```\n\n"
            "Indices 0 to 3 pick index 1, so the root is 2 rather than 3.\n\n"
        ),
        "constraints": (
            "- 1 <= n <= 10000.\n"
            "- Elements are distinct and given in strictly increasing order.\n"
            "- Each element fits in the range -10^4 to 10^4.\n\n"
        ),
        "inputs": [
            "7\n-10 -3 0 5 9 12 20",
            "4\n1 2 3 4",
            "1\n0",
            "2\n1 3",
            "5\n-5 -2 0 3 8",
            "6\n1 2 3 4 5 6",
        ],
        "solve": solve_convert_sorted_array_to_binary_search_tree,
        "brute": brute_convert_sorted_array_to_binary_search_tree,
    },
    {
        "title": "Sort List",
        "level": "Medium",
        "topics": "Divide and Conquer, Sorting, Merge Sort, Linked List",
        "companies": "Microsoft, Amazon, Bloomberg",
        "description": (
            "Sort a sequence of integers into non-decreasing order. The sequence stands in for "
            "a singly linked list, so the natural approach is a merge sort that splits the "
            "sequence in half, sorts each half, then merges the two halves.\n\n"
            "**Input**\n\n"
            "The first line holds n, the number of values. The second line holds the n values "
            "separated by spaces.\n\n"
            "**Output**\n\n"
            "One line holding the n values in non-decreasing order, separated by single "
            "spaces.\n\n"
        ),
        "examples": (
            "**Example 1**\n\n"
            "```\n"
            "Input\n"
            "4\n"
            "4 2 1 3\n"
            "Output\n"
            "1 2 3 4\n"
            "```\n\n"
            "**Example 2**\n\n"
            "```\n"
            "Input\n"
            "5\n"
            "-1 5 3 4 0\n"
            "Output\n"
            "-1 0 3 4 5\n"
            "```\n\n"
        ),
        "constraints": (
            "- 1 <= n <= 50000.\n"
            "- Each value fits in the range -10^5 to 10^5.\n"
            "- Values may repeat.\n\n"
        ),
        "inputs": [
            "4\n4 2 1 3",
            "5\n-1 5 3 4 0",
            "1\n7",
            "2\n2 1",
            "6\n5 5 1 1 3 3",
            "8\n8 7 6 5 4 3 2 1",
        ],
        "solve": solve_sort_list,
        "brute": brute_sort_list,
    },
    {
        "title": "Construct Quad Tree",
        "level": "Medium",
        "topics": "Divide and Conquer, Tree, Matrix, Depth-First Search",
        "companies": "Google, Amazon, Apple",
        "description": (
            "A quad tree describes a square grid of zeros and ones. Each node covers one square "
            "region. If every cell in the region holds the same value, the node is a leaf "
            "carrying that value. Otherwise the node is internal and the region is cut into "
            "four equal squares, described in the order top-left, top-right, bottom-left, "
            "bottom-right. Build the quad tree of the given grid and print it.\n\n"
            "**Input**\n\n"
            "The first line holds n, the side length of the grid, which is always a power of "
            "two. Each of the next n lines holds one grid row as a run of n characters, each "
            "either `0` or `1`.\n\n"
            "**Output**\n\n"
            "A preorder walk of the quad tree, one node per line. A node is visited before its "
            "children, and children are visited in the order top-left, top-right, bottom-left, "
            "bottom-right. A leaf prints `leaf ` followed by its value, so `leaf 0` or "
            "`leaf 1`. An internal node prints `internal`.\n\n"
        ),
        "examples": (
            "**Example 1**\n\n"
            "```\n"
            "Input\n"
            "2\n"
            "01\n"
            "10\n"
            "Output\n"
            "internal\n"
            "leaf 0\n"
            "leaf 1\n"
            "leaf 1\n"
            "leaf 0\n"
            "```\n\n"
            "The whole grid is mixed, so the root is internal and each of the four single cells "
            "becomes a leaf.\n\n"
            "**Example 2**\n\n"
            "```\n"
            "Input\n"
            "4\n"
            "1111\n"
            "1111\n"
            "1100\n"
            "1100\n"
            "Output\n"
            "internal\n"
            "leaf 1\n"
            "leaf 1\n"
            "leaf 1\n"
            "leaf 0\n"
            "```\n\n"
            "Three of the four quadrants are all ones and the bottom-right quadrant is all "
            "zeros, so each quadrant collapses into a single leaf.\n\n"
        ),
        "constraints": (
            "- n is a power of two with 1 <= n <= 64.\n"
            "- Every grid character is `0` or `1`.\n"
            "- Each grid row holds exactly n characters.\n\n"
        ),
        "inputs": [
            "2\n01\n10",
            "4\n1111\n1111\n1100\n1100",
            "1\n1",
            "4\n0000\n0000\n0000\n0000",
            "4\n1011\n0111\n1111\n1111",
            "2\n11\n11",
        ],
        "solve": solve_construct_quad_tree,
        "brute": brute_construct_quad_tree,
    },
    {
        "title": "Merge k Sorted Lists",
        "level": "Hard",
        "topics": "Divide and Conquer, Heap, Merge Sort, Linked List",
        "companies": "Amazon, Google, Microsoft, Meta",
        "description": (
            "Several sequences are each already sorted in non-decreasing order. Combine all of "
            "their values into one sequence that is also sorted in non-decreasing order.\n\n"
            "**Input**\n\n"
            "The first line holds k, the number of sequences. Each of the next k lines describes "
            "one sequence: its length first, then that many values, all separated by spaces. A "
            "sequence of length 0 is written as a line holding just `0`.\n\n"
            "**Output**\n\n"
            "One line holding every value from every sequence in non-decreasing order, separated "
            "by single spaces. Repeated values are all kept.\n\n"
        ),
        "examples": (
            "**Example 1**\n\n"
            "```\n"
            "Input\n"
            "3\n"
            "3 1 4 5\n"
            "3 1 3 4\n"
            "2 2 6\n"
            "Output\n"
            "1 1 2 3 4 4 5 6\n"
            "```\n\n"
            "The first number on each sequence line is its length, so the three sequences are "
            "[1, 4, 5], [1, 3, 4] and [2, 6].\n\n"
            "**Example 2**\n\n"
            "```\n"
            "Input\n"
            "2\n"
            "0\n"
            "1 5\n"
            "Output\n"
            "5\n"
            "```\n\n"
            "The first sequence is empty and contributes nothing.\n\n"
        ),
        "constraints": (
            "- 1 <= k <= 10000.\n"
            "- Each sequence holds 0 to 500 values and is already sorted.\n"
            "- Each value fits in the range -10^4 to 10^4.\n"
            "- At least one value is present across all sequences.\n\n"
        ),
        "inputs": [
            "3\n3 1 4 5\n3 1 3 4\n2 2 6",
            "2\n0\n1 5",
            "1\n3 1 2 3",
            "4\n1 -5\n2 -3 0\n0\n3 1 1 2",
            "2\n2 1 2\n2 1 2",
        ],
        "solve": solve_merge_k_sorted_lists,
        "brute": brute_merge_k_sorted_lists,
    },
]
