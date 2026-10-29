"""Problem specs for the graphs and backtracking study group.

Each entry pairs a markdown statement with a reference solver that maps one
stdin payload to the exact stdout text the judge expects, plus an independently
written cross-check used at build time.
"""

from __future__ import annotations

import heapq
import itertools
from collections import deque
from typing import Any

CARDINAL_STEPS: tuple[tuple[int, int], ...] = ((-1, 0), (1, 0), (0, -1), (0, 1))
PHONE_LETTERS: dict[str, str] = {
    "2": "abc",
    "3": "def",
    "4": "ghi",
    "5": "jkl",
    "6": "mno",
    "7": "pqrs",
    "8": "tuv",
    "9": "wxyz",
}
EMPTY_RESULT_TOKEN = "none"


def _read_lines(stdin_text: str) -> list[str]:
    """Split a stdin payload into stripped lines.

    Parameters
    ----------
    stdin_text : str
        Full stdin payload.

    Returns
    -------
    list[str]
        Lines with surrounding whitespace removed from the payload as a whole.
    """
    return stdin_text.strip("\n").split("\n")


def _parse_character_grid(stdin_text: str) -> tuple[list[list[str]], list[str]]:
    """Read a rows/columns header plus that many rows of space separated cells.

    Parameters
    ----------
    stdin_text : str
        Full stdin payload.

    Returns
    -------
    tuple[list[list[str]], list[str]]
        The grid, and the lines that follow it.
    """
    lines = _read_lines(stdin_text)
    row_count, column_count = (int(value) for value in lines[0].split())
    grid = [lines[row_index + 1].split()[:column_count] for row_index in range(row_count)]
    return grid, lines[row_count + 1 :]


def _find_root(parent: dict[tuple[int, int], tuple[int, int]], cell: tuple[int, int]) -> tuple[int, int]:
    """Resolve the representative of a cell in a disjoint set forest.

    Parameters
    ----------
    parent : dict[tuple[int, int], tuple[int, int]]
        Parent pointer per cell, mutated in place by path halving.
    cell : tuple[int, int]
        Cell whose set representative is wanted.

    Returns
    -------
    tuple[int, int]
        The representative cell of the set containing cell.
    """
    while parent[cell] != cell:
        parent[cell] = parent[parent[cell]]
        cell = parent[cell]
    return cell


# ---------------------------------------------------------------- Number of Islands


def solve_number_of_islands(stdin_text: str) -> str:
    """Count connected groups of land cells with breadth-first search.

    Parameters
    ----------
    stdin_text : str
        Grid header followed by the grid rows.

    Returns
    -------
    str
        The island count.
    """
    grid, _ = _parse_character_grid(stdin_text)
    row_count = len(grid)
    column_count = len(grid[0]) if row_count else 0
    visited = [[False] * column_count for _ in range(row_count)]
    island_count = 0
    for start_row in range(row_count):
        for start_column in range(column_count):
            if grid[start_row][start_column] != "1" or visited[start_row][start_column]:
                continue
            island_count += 1
            visited[start_row][start_column] = True
            queue = deque([(start_row, start_column)])
            while queue:
                row, column = queue.popleft()
                for row_step, column_step in CARDINAL_STEPS:
                    next_row = row + row_step
                    next_column = column + column_step
                    is_inside = 0 <= next_row < row_count and 0 <= next_column < column_count
                    if not is_inside or visited[next_row][next_column]:
                        continue
                    if grid[next_row][next_column] == "1":
                        visited[next_row][next_column] = True
                        queue.append((next_row, next_column))
    return str(island_count)


def brute_number_of_islands(stdin_text: str) -> str:
    """Count land groups by unioning every adjacent pair of land cells.

    Parameters
    ----------
    stdin_text : str
        Grid header followed by the grid rows.

    Returns
    -------
    str
        The island count.
    """
    grid, _ = _parse_character_grid(stdin_text)
    parent: dict[tuple[int, int], tuple[int, int]] = {}
    for row_index, row in enumerate(grid):
        for column_index, cell in enumerate(row):
            if cell == "1":
                parent[(row_index, column_index)] = (row_index, column_index)
    for row_index, column_index in list(parent):
        below = (row_index + 1, column_index)
        right = (row_index, column_index + 1)
        for neighbour in (below, right):
            if neighbour not in parent:
                continue
            left_root = _find_root(parent, (row_index, column_index))
            right_root = _find_root(parent, neighbour)
            if left_root != right_root:
                parent[right_root] = left_root
    return str(len({_find_root(parent, cell) for cell in parent}))


# ---------------------------------------------------------------- Surrounded Regions


def solve_surrounded_regions(stdin_text: str) -> str:
    """Flip every O region that does not touch the border, keeping the rest.

    Parameters
    ----------
    stdin_text : str
        Grid header followed by the grid rows of X and O cells.

    Returns
    -------
    str
        The resulting grid, one row per line of space separated cells.
    """
    grid, _ = _parse_character_grid(stdin_text)
    row_count = len(grid)
    column_count = len(grid[0])
    is_safe = [[False] * column_count for _ in range(row_count)]
    queue: deque[tuple[int, int]] = deque()
    for row in range(row_count):
        for column in range(column_count):
            is_on_border = row in (0, row_count - 1) or column in (0, column_count - 1)
            if is_on_border and grid[row][column] == "O":
                is_safe[row][column] = True
                queue.append((row, column))
    while queue:
        row, column = queue.popleft()
        for row_step, column_step in CARDINAL_STEPS:
            next_row = row + row_step
            next_column = column + column_step
            is_inside = 0 <= next_row < row_count and 0 <= next_column < column_count
            if not is_inside or is_safe[next_row][next_column]:
                continue
            if grid[next_row][next_column] == "O":
                is_safe[next_row][next_column] = True
                queue.append((next_row, next_column))
    rendered_rows = []
    for row in range(row_count):
        cells = [
            "O" if grid[row][column] == "O" and is_safe[row][column] else "X"
            for column in range(column_count)
        ]
        rendered_rows.append(" ".join(cells))
    return "\n".join(rendered_rows)


def _can_reach_border(grid: list[list[str]], start_row: int, start_column: int) -> bool:
    """Test whether an O cell reaches the grid border through O cells only.

    Parameters
    ----------
    grid : list[list[str]]
        Grid of X and O cells.
    start_row : int
        Row of the starting cell.
    start_column : int
        Column of the starting cell.

    Returns
    -------
    bool
        True when the border is reachable from the starting cell.
    """
    row_count = len(grid)
    column_count = len(grid[0])
    stack = [(start_row, start_column)]
    seen = {(start_row, start_column)}
    while stack:
        row, column = stack.pop()
        is_on_border = row in (0, row_count - 1) or column in (0, column_count - 1)
        if is_on_border:
            return True
        for row_step, column_step in CARDINAL_STEPS:
            next_cell = (row + row_step, column + column_step)
            if next_cell in seen:
                continue
            if grid[next_cell[0]][next_cell[1]] == "O":
                seen.add(next_cell)
                stack.append(next_cell)
    return False


def brute_surrounded_regions(stdin_text: str) -> str:
    """Decide each O cell on its own by searching for a path to the border.

    Parameters
    ----------
    stdin_text : str
        Grid header followed by the grid rows of X and O cells.

    Returns
    -------
    str
        The resulting grid, one row per line of space separated cells.
    """
    grid, _ = _parse_character_grid(stdin_text)
    rendered_rows = []
    for row_index, row in enumerate(grid):
        cells = []
        for column_index, cell in enumerate(row):
            keeps_open = cell == "O" and _can_reach_border(grid, row_index, column_index)
            cells.append("O" if keeps_open else "X")
        rendered_rows.append(" ".join(cells))
    return "\n".join(rendered_rows)


# ---------------------------------------------------------------- Clone Graph


class _GraphNode:
    """Undirected graph node carrying a label and its neighbour objects.

    Attributes
    ----------
    label : int
        1-indexed node label.
    neighbours : list[_GraphNode]
        Adjacent node objects.
    """

    def __init__(self, label: int) -> None:
        """Create a node with an empty neighbour list.

        Parameters
        ----------
        label : int
            1-indexed node label.
        """
        self.label = label
        self.neighbours: list[_GraphNode] = []


def _build_graph_nodes(stdin_text: str) -> list[_GraphNode]:
    """Build the original node objects from the adjacency payload.

    Parameters
    ----------
    stdin_text : str
        Node count followed by one degree-prefixed adjacency line per node.

    Returns
    -------
    list[_GraphNode]
        Nodes in label order.
    """
    lines = _read_lines(stdin_text)
    node_count = int(lines[0])
    nodes = [_GraphNode(label) for label in range(1, node_count + 1)]
    for offset in range(node_count):
        values = [int(value) for value in lines[offset + 1].split()]
        degree = values[0]
        for neighbour_label in values[1 : degree + 1]:
            nodes[offset].neighbours.append(nodes[neighbour_label - 1])
    return nodes


def _render_clone_adjacency(clones: dict[int, _GraphNode], node_count: int) -> str:
    """Render the cloned graph as one adjacency line per node.

    Parameters
    ----------
    clones : dict[int, _GraphNode]
        Cloned nodes keyed by label.
    node_count : int
        Number of nodes in the graph.

    Returns
    -------
    str
        One line per node: the label, a colon, then neighbour labels ascending.
    """
    lines = []
    for label in range(1, node_count + 1):
        neighbour_labels = sorted(neighbour.label for neighbour in clones[label].neighbours)
        rendered = " ".join(str(value) for value in neighbour_labels)
        lines.append(f"{label}: {rendered or EMPTY_RESULT_TOKEN}")
    return "\n".join(lines)


def solve_clone_graph(stdin_text: str) -> str:
    """Deep copy every component with breadth-first search, then print the copy.

    Parameters
    ----------
    stdin_text : str
        Node count followed by one degree-prefixed adjacency line per node.

    Returns
    -------
    str
        The clone's adjacency list, one line per node.
    """
    original_nodes = _build_graph_nodes(stdin_text)
    clones: dict[int, _GraphNode] = {}
    for start_node in original_nodes:
        if start_node.label in clones:
            continue
        clones[start_node.label] = _GraphNode(start_node.label)
        queue = deque([start_node])
        while queue:
            node = queue.popleft()
            for neighbour in node.neighbours:
                if neighbour.label not in clones:
                    clones[neighbour.label] = _GraphNode(neighbour.label)
                    queue.append(neighbour)
                clones[node.label].neighbours.append(clones[neighbour.label])
    return _render_clone_adjacency(clones, len(original_nodes))


def _clone_depth_first(node: _GraphNode, clones: dict[int, _GraphNode]) -> _GraphNode:
    """Copy a node and everything reachable from it, memoising by label.

    Parameters
    ----------
    node : _GraphNode
        Original node to copy.
    clones : dict[int, _GraphNode]
        Copies built so far, keyed by label and extended in place.

    Returns
    -------
    _GraphNode
        The copy of node.
    """
    if node.label in clones:
        return clones[node.label]
    copy = _GraphNode(node.label)
    clones[node.label] = copy
    for neighbour in node.neighbours:
        copy.neighbours.append(_clone_depth_first(neighbour, clones))
    return copy


def brute_clone_graph(stdin_text: str) -> str:
    """Deep copy every component with recursive depth-first search.

    Parameters
    ----------
    stdin_text : str
        Node count followed by one degree-prefixed adjacency line per node.

    Returns
    -------
    str
        The clone's adjacency list, one line per node.
    """
    original_nodes = _build_graph_nodes(stdin_text)
    clones: dict[int, _GraphNode] = {}
    for node in original_nodes:
        _clone_depth_first(node, clones)
    return _render_clone_adjacency(clones, len(original_nodes))


# ---------------------------------------------------------------- Evaluate Division


def _parse_division_payload(
    stdin_text: str,
) -> tuple[list[tuple[str, str, float]], list[tuple[str, str]]]:
    """Read the equation and query blocks of the division payload.

    Parameters
    ----------
    stdin_text : str
        Counts header, then the equations, then the queries.

    Returns
    -------
    tuple[list[tuple[str, str, float]], list[tuple[str, str]]]
        Equations as numerator, denominator, value, and the query pairs.
    """
    lines = _read_lines(stdin_text)
    equation_count, query_count = (int(value) for value in lines[0].split())
    equations = []
    for offset in range(equation_count):
        numerator, denominator, value = lines[offset + 1].split()
        equations.append((numerator, denominator, float(value)))
    queries = []
    for offset in range(query_count):
        numerator, denominator = lines[equation_count + 1 + offset].split()
        queries.append((numerator, denominator))
    return equations, queries


def solve_evaluate_division(stdin_text: str) -> str:
    """Answer each ratio query by walking the weighted graph of equations.

    Parameters
    ----------
    stdin_text : str
        Counts header, then the equations, then the queries.

    Returns
    -------
    str
        One answer per query, five decimal places, -1.00000 when unanswerable.
    """
    equations, queries = _parse_division_payload(stdin_text)
    ratios: dict[str, list[tuple[str, float]]] = {}
    for numerator, denominator, value in equations:
        ratios.setdefault(numerator, []).append((denominator, value))
        ratios.setdefault(denominator, []).append((numerator, 1.0 / value))
    answers = []
    for source, target in queries:
        if source not in ratios or target not in ratios:
            answers.append("-1.00000")
            continue
        found = None
        visited = {source}
        queue = deque([(source, 1.0)])
        while queue and found is None:
            variable, product = queue.popleft()
            if variable == target:
                found = product
                break
            for neighbour, weight in ratios[variable]:
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append((neighbour, product * weight))
        answers.append("-1.00000" if found is None else f"{found:.5f}")
    return "\n".join(answers)


def brute_evaluate_division(stdin_text: str) -> str:
    """Answer the queries from an all-pairs ratio table built by relaxation.

    Parameters
    ----------
    stdin_text : str
        Counts header, then the equations, then the queries.

    Returns
    -------
    str
        One answer per query, five decimal places, -1.00000 when unanswerable.
    """
    equations, queries = _parse_division_payload(stdin_text)
    variables: list[str] = []
    for numerator, denominator, _ in equations:
        for name in (numerator, denominator):
            if name not in variables:
                variables.append(name)
    table: dict[tuple[str, str], float] = {(name, name): 1.0 for name in variables}
    for numerator, denominator, value in equations:
        table[(numerator, denominator)] = value
        table[(denominator, numerator)] = 1.0 / value
    for middle in variables:
        for source in variables:
            for target in variables:
                left = table.get((source, middle))
                right = table.get((middle, target))
                if left is not None and right is not None and (source, target) not in table:
                    table[(source, target)] = left * right
    answers = []
    for source, target in queries:
        value = table.get((source, target))
        answers.append("-1.00000" if value is None else f"{value:.5f}")
    return "\n".join(answers)


# ---------------------------------------------------------------- Course Schedule


def _parse_course_payload(stdin_text: str) -> tuple[int, list[tuple[int, int]]]:
    """Read the course count and the prerequisite pairs.

    Parameters
    ----------
    stdin_text : str
        Counts header followed by one prerequisite pair per line.

    Returns
    -------
    tuple[int, list[tuple[int, int]]]
        Course count, and pairs of course then required prerequisite.
    """
    lines = _read_lines(stdin_text)
    course_count, pair_count = (int(value) for value in lines[0].split())
    pairs = []
    for offset in range(pair_count):
        course, prerequisite = (int(value) for value in lines[offset + 1].split())
        pairs.append((course, prerequisite))
    return course_count, pairs


def solve_course_schedule(stdin_text: str) -> str:
    """Decide whether every course can be taken, using indegree peeling.

    Parameters
    ----------
    stdin_text : str
        Counts header followed by one prerequisite pair per line.

    Returns
    -------
    str
        "true" when an order exists, otherwise "false".
    """
    course_count, pairs = _parse_course_payload(stdin_text)
    followers: dict[int, list[int]] = {course: [] for course in range(course_count)}
    indegrees = [0] * course_count
    for course, prerequisite in pairs:
        followers[prerequisite].append(course)
        indegrees[course] += 1
    queue = deque(course for course in range(course_count) if indegrees[course] == 0)
    taken_count = 0
    while queue:
        course = queue.popleft()
        taken_count += 1
        for follower in followers[course]:
            indegrees[follower] -= 1
            if indegrees[follower] == 0:
                queue.append(follower)
    return "true" if taken_count == course_count else "false"


def brute_course_schedule(stdin_text: str) -> str:
    """Decide the same question by hunting for a cycle with coloured search.

    Parameters
    ----------
    stdin_text : str
        Counts header followed by one prerequisite pair per line.

    Returns
    -------
    str
        "true" when an order exists, otherwise "false".
    """
    course_count, pairs = _parse_course_payload(stdin_text)
    prerequisites: dict[int, list[int]] = {course: [] for course in range(course_count)}
    for course, prerequisite in pairs:
        prerequisites[course].append(prerequisite)
    UNSEEN, ON_PATH, DONE = 0, 1, 2
    colours = [UNSEEN] * course_count
    for start_course in range(course_count):
        if colours[start_course] != UNSEEN:
            continue
        stack = [(start_course, iter(prerequisites[start_course]))]
        colours[start_course] = ON_PATH
        while stack:
            course, pending = stack[-1]
            next_course = next(pending, None)
            if next_course is None:
                colours[course] = DONE
                stack.pop()
                continue
            if colours[next_course] == ON_PATH:
                return "false"
            if colours[next_course] == UNSEEN:
                colours[next_course] = ON_PATH
                stack.append((next_course, iter(prerequisites[next_course])))
    return "true"


# ---------------------------------------------------------------- Course Schedule II


def solve_course_schedule_ii(stdin_text: str) -> str:
    """Produce the lexicographically smallest course order with a min-heap.

    Parameters
    ----------
    stdin_text : str
        Counts header followed by one prerequisite pair per line.

    Returns
    -------
    str
        The order as space separated course numbers, or "none" when impossible.
    """
    course_count, pairs = _parse_course_payload(stdin_text)
    followers: dict[int, list[int]] = {course: [] for course in range(course_count)}
    indegrees = [0] * course_count
    for course, prerequisite in pairs:
        followers[prerequisite].append(course)
        indegrees[course] += 1
    available = [course for course in range(course_count) if indegrees[course] == 0]
    heapq.heapify(available)
    order: list[int] = []
    while available:
        course = heapq.heappop(available)
        order.append(course)
        for follower in followers[course]:
            indegrees[follower] -= 1
            if indegrees[follower] == 0:
                heapq.heappush(available, follower)
    if len(order) != course_count:
        return EMPTY_RESULT_TOKEN
    return " ".join(str(course) for course in order)


def brute_course_schedule_ii(stdin_text: str) -> str:
    """Build the same order by rescanning for the smallest unblocked course.

    Parameters
    ----------
    stdin_text : str
        Counts header followed by one prerequisite pair per line.

    Returns
    -------
    str
        The order as space separated course numbers, or "none" when impossible.
    """
    course_count, pairs = _parse_course_payload(stdin_text)
    prerequisites: dict[int, set[int]] = {course: set() for course in range(course_count)}
    for course, prerequisite in pairs:
        prerequisites[course].add(prerequisite)
    taken: set[int] = set()
    order: list[int] = []
    for _ in range(course_count):
        chosen = None
        for course in range(course_count):
            if course in taken:
                continue
            if prerequisites[course] <= taken:
                chosen = course
                break
        if chosen is None:
            return EMPTY_RESULT_TOKEN
        taken.add(chosen)
        order.append(chosen)
    return " ".join(str(course) for course in order)


# ---------------------------------------------------------------- Snakes and Ladders


def _parse_snakes_board(stdin_text: str) -> list[list[int]]:
    """Read the board size and the board rows.

    Parameters
    ----------
    stdin_text : str
        Board size followed by that many rows of that many integers.

    Returns
    -------
    list[list[int]]
        Board rows top to bottom.
    """
    lines = _read_lines(stdin_text)
    board_size = int(lines[0])
    return [
        [int(value) for value in lines[row_index + 1].split()[:board_size]]
        for row_index in range(board_size)
    ]


def _square_to_cell(board_size: int, square: int) -> tuple[int, int]:
    """Map a square number to its cell in the boustrophedon layout.

    Parameters
    ----------
    board_size : int
        Side length of the board.
    square : int
        Square number from 1 to board_size squared.

    Returns
    -------
    tuple[int, int]
        Row and column of the square.
    """
    quotient, remainder = divmod(square - 1, board_size)
    row = board_size - 1 - quotient
    column = remainder if quotient % 2 == 0 else board_size - 1 - remainder
    return row, column


def solve_snakes_and_ladders(stdin_text: str) -> str:
    """Find the fewest dice moves to the last square with breadth-first search.

    Parameters
    ----------
    stdin_text : str
        Board size followed by that many rows of that many integers.

    Returns
    -------
    str
        Fewest moves, or -1 when the last square cannot be reached.
    """
    board = _parse_snakes_board(stdin_text)
    board_size = len(board)
    final_square = board_size * board_size
    visited = {1}
    queue = deque([(1, 0)])
    while queue:
        square, moves = queue.popleft()
        if square == final_square:
            return str(moves)
        for roll in range(1, 7):
            next_square = square + roll
            if next_square > final_square:
                break
            row, column = _square_to_cell(board_size, next_square)
            jump = board[row][column]
            destination = next_square if jump == -1 else jump
            if destination not in visited:
                visited.add(destination)
                queue.append((destination, moves + 1))
    return "-1"


def brute_snakes_and_ladders(stdin_text: str) -> str:
    """Find the fewest dice moves by relaxing every move until nothing improves.

    Parameters
    ----------
    stdin_text : str
        Board size followed by that many rows of that many integers.

    Returns
    -------
    str
        Fewest moves, or -1 when the last square cannot be reached.
    """
    board = _parse_snakes_board(stdin_text)
    board_size = len(board)
    final_square = board_size * board_size
    unreachable = final_square + 1
    best_moves = [unreachable] * (final_square + 1)
    best_moves[1] = 0
    has_changed = True
    while has_changed:
        has_changed = False
        for square in range(1, final_square + 1):
            if best_moves[square] == unreachable:
                continue
            for roll in range(1, 7):
                next_square = square + roll
                if next_square > final_square:
                    break
                row, column = _square_to_cell(board_size, next_square)
                jump = board[row][column]
                destination = next_square if jump == -1 else jump
                if best_moves[square] + 1 < best_moves[destination]:
                    best_moves[destination] = best_moves[square] + 1
                    has_changed = True
    return "-1" if best_moves[final_square] == unreachable else str(best_moves[final_square])


# ---------------------------------------------------------------- Minimum Genetic Mutation


def _parse_gene_payload(stdin_text: str) -> tuple[str, str, list[str]]:
    """Read the start gene, the end gene and the bank.

    Parameters
    ----------
    stdin_text : str
        Start gene, end gene, bank size, then that many bank genes.

    Returns
    -------
    tuple[str, str, list[str]]
        Start gene, end gene and bank genes.
    """
    lines = _read_lines(stdin_text)
    start_gene = lines[0].strip()
    end_gene = lines[1].strip()
    bank_size = int(lines[2])
    bank = [lines[3 + offset].strip() for offset in range(bank_size)]
    return start_gene, end_gene, bank


def _differs_by_one(left: str, right: str) -> bool:
    """Test whether two equal-length strings differ at exactly one position.

    Parameters
    ----------
    left : str
        First string.
    right : str
        Second string.

    Returns
    -------
    bool
        True when exactly one position differs.
    """
    difference_count = sum(1 for pair in zip(left, right) if pair[0] != pair[1])
    return difference_count == 1


def solve_minimum_genetic_mutation(stdin_text: str) -> str:
    """Count the fewest single-character mutations with breadth-first search.

    Parameters
    ----------
    stdin_text : str
        Start gene, end gene, bank size, then that many bank genes.

    Returns
    -------
    str
        Fewest mutations, or -1 when the end gene cannot be produced.
    """
    start_gene, end_gene, bank = _parse_gene_payload(stdin_text)
    if start_gene == end_gene:
        return "0"
    available = set(bank)
    if end_gene not in available:
        return "-1"
    queue = deque([(start_gene, 0)])
    available.discard(start_gene)
    while queue:
        gene, mutations = queue.popleft()
        for candidate in [item for item in available if _differs_by_one(gene, item)]:
            if candidate == end_gene:
                return str(mutations + 1)
            available.discard(candidate)
            queue.append((candidate, mutations + 1))
    return "-1"


def brute_minimum_genetic_mutation(stdin_text: str) -> str:
    """Count the fewest mutations from an all-pairs distance table.

    Parameters
    ----------
    stdin_text : str
        Start gene, end gene, bank size, then that many bank genes.

    Returns
    -------
    str
        Fewest mutations, or -1 when the end gene cannot be produced.
    """
    start_gene, end_gene, bank = _parse_gene_payload(stdin_text)
    if start_gene == end_gene:
        return "0"
    if end_gene not in bank:
        return "-1"
    genes: list[str] = [start_gene]
    for gene in bank:
        if gene not in genes:
            genes.append(gene)
    unreachable = len(genes) + 1
    distances = [[unreachable] * len(genes) for _ in genes]
    for left_index, left_gene in enumerate(genes):
        distances[left_index][left_index] = 0
        for right_index, right_gene in enumerate(genes):
            if _differs_by_one(left_gene, right_gene):
                distances[left_index][right_index] = 1
    for middle in range(len(genes)):
        for source in range(len(genes)):
            for target in range(len(genes)):
                through = distances[source][middle] + distances[middle][target]
                if through < distances[source][target]:
                    distances[source][target] = through
    total = distances[0][genes.index(end_gene)]
    return "-1" if total >= unreachable else str(total)


# ---------------------------------------------------------------- Word Ladder


def _parse_word_ladder_payload(stdin_text: str) -> tuple[str, str, list[str]]:
    """Read the begin word, the end word and the word list.

    Parameters
    ----------
    stdin_text : str
        Begin word, end word, list size, then that many words.

    Returns
    -------
    tuple[str, str, list[str]]
        Begin word, end word and the word list.
    """
    lines = _read_lines(stdin_text)
    begin_word = lines[0].strip()
    end_word = lines[1].strip()
    word_count = int(lines[2])
    words = [lines[3 + offset].strip() for offset in range(word_count)]
    return begin_word, end_word, words


def solve_word_ladder(stdin_text: str) -> str:
    """Measure the shortest transformation chain with wildcard bucket search.

    Parameters
    ----------
    stdin_text : str
        Begin word, end word, list size, then that many words.

    Returns
    -------
    str
        Number of words in the shortest chain, or 0 when there is none.
    """
    begin_word, end_word, words = _parse_word_ladder_payload(stdin_text)
    word_set = set(words)
    if end_word not in word_set:
        return "0"
    buckets: dict[str, list[str]] = {}
    for word in word_set | {begin_word}:
        for position in range(len(word)):
            pattern = word[:position] + "*" + word[position + 1 :]
            buckets.setdefault(pattern, []).append(word)
    visited = {begin_word}
    queue = deque([(begin_word, 1)])
    while queue:
        word, length = queue.popleft()
        if word == end_word:
            return str(length)
        for position in range(len(word)):
            pattern = word[:position] + "*" + word[position + 1 :]
            for neighbour in buckets.get(pattern, []):
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append((neighbour, length + 1))
    return "0"


def brute_word_ladder(stdin_text: str) -> str:
    """Measure the shortest chain from an all-pairs distance table.

    Parameters
    ----------
    stdin_text : str
        Begin word, end word, list size, then that many words.

    Returns
    -------
    str
        Number of words in the shortest chain, or 0 when there is none.
    """
    begin_word, end_word, words = _parse_word_ladder_payload(stdin_text)
    if end_word not in words:
        return "0"
    nodes: list[str] = [begin_word]
    for word in words:
        if word not in nodes:
            nodes.append(word)
    unreachable = len(nodes) + 1
    distances = [[unreachable] * len(nodes) for _ in nodes]
    for left_index, left_word in enumerate(nodes):
        distances[left_index][left_index] = 0
        for right_index, right_word in enumerate(nodes):
            if _differs_by_one(left_word, right_word):
                distances[left_index][right_index] = 1
    for middle in range(len(nodes)):
        for source in range(len(nodes)):
            for target in range(len(nodes)):
                through = distances[source][middle] + distances[middle][target]
                if through < distances[source][target]:
                    distances[source][target] = through
    steps = distances[0][nodes.index(end_word)]
    return "0" if steps >= unreachable else str(steps + 1)


# ---------------------------------------------------------------- Letter Combinations


def _collect_letter_combinations(digits: str, position: int, prefix: str, found: list[str]) -> None:
    """Grow one letter choice per digit, recording every finished string.

    Parameters
    ----------
    digits : str
        Digit string being mapped.
    position : int
        Index of the digit to expand next.
    prefix : str
        Letters chosen so far.
    found : list[str]
        Completed combinations, extended in place.

    Returns
    -------
    None
    """
    if position == len(digits):
        found.append(prefix)
        return
    for letter in PHONE_LETTERS[digits[position]]:
        _collect_letter_combinations(digits, position + 1, prefix + letter, found)


def _parse_digit_line(stdin_text: str) -> str:
    """Read the digit string, mapping the empty sentinel to an empty string.

    Parameters
    ----------
    stdin_text : str
        Single line holding the digits or the word empty.

    Returns
    -------
    str
        The digit string, possibly empty.
    """
    line = _read_lines(stdin_text)[0].strip()
    return "" if line == "empty" else line


def solve_letter_combinations_of_a_phone_number(stdin_text: str) -> str:
    """List every letter string a digit sequence can spell, sorted.

    Parameters
    ----------
    stdin_text : str
        Single line holding the digits or the word empty.

    Returns
    -------
    str
        One combination per line in lexicographic order, or "none".
    """
    digits = _parse_digit_line(stdin_text)
    if not digits:
        return EMPTY_RESULT_TOKEN
    found: list[str] = []
    _collect_letter_combinations(digits, 0, "", found)
    return "\n".join(sorted(found))


def brute_letter_combinations_of_a_phone_number(stdin_text: str) -> str:
    """List the same strings as the cartesian product of the digit alphabets.

    Parameters
    ----------
    stdin_text : str
        Single line holding the digits or the word empty.

    Returns
    -------
    str
        One combination per line in lexicographic order, or "none".
    """
    digits = _parse_digit_line(stdin_text)
    if not digits:
        return EMPTY_RESULT_TOKEN
    alphabets = [PHONE_LETTERS[digit] for digit in digits]
    found = ["".join(letters) for letters in itertools.product(*alphabets)]
    return "\n".join(sorted(found))


# ---------------------------------------------------------------- Combinations


def _collect_combinations(
    highest: int, size: int, next_value: int, chosen: list[int], found: list[tuple[int, ...]]
) -> None:
    """Extend an ascending selection until it reaches the wanted size.

    Parameters
    ----------
    highest : int
        Largest selectable number.
    size : int
        Wanted selection size.
    next_value : int
        Smallest number still allowed.
    chosen : list[int]
        Numbers picked so far.
    found : list[tuple[int, ...]]
        Completed selections, extended in place.

    Returns
    -------
    None
    """
    if len(chosen) == size:
        found.append(tuple(chosen))
        return
    for value in range(next_value, highest + 1):
        chosen.append(value)
        _collect_combinations(highest, size, value + 1, chosen, found)
        chosen.pop()


def _render_number_tuples(found: list[tuple[int, ...]]) -> str:
    """Sort tuples ascending and render one per line.

    Parameters
    ----------
    found : list[tuple[int, ...]]
        Tuples of numbers.

    Returns
    -------
    str
        One tuple per line as space separated numbers, or "none" when empty.
    """
    if not found:
        return EMPTY_RESULT_TOKEN
    lines = [" ".join(str(value) for value in item) for item in sorted(found)]
    return "\n".join(lines)


def solve_combinations(stdin_text: str) -> str:
    """List every ascending selection of k numbers from 1 to n.

    Parameters
    ----------
    stdin_text : str
        Single line holding n and k.

    Returns
    -------
    str
        One selection per line in ascending tuple order, or "none".
    """
    highest, size = (int(value) for value in _read_lines(stdin_text)[0].split())
    found: list[tuple[int, ...]] = []
    _collect_combinations(highest, size, 1, [], found)
    return _render_number_tuples(found)


def brute_combinations(stdin_text: str) -> str:
    """List the same selections straight from the standard library.

    Parameters
    ----------
    stdin_text : str
        Single line holding n and k.

    Returns
    -------
    str
        One selection per line in ascending tuple order, or "none".
    """
    highest, size = (int(value) for value in _read_lines(stdin_text)[0].split())
    if size > highest or size < 0:
        return EMPTY_RESULT_TOKEN
    found = list(itertools.combinations(range(1, highest + 1), size))
    return _render_number_tuples(found)


# ---------------------------------------------------------------- Permutations


def _parse_number_list(stdin_text: str) -> list[int]:
    """Read a count line followed by a line of that many integers.

    Parameters
    ----------
    stdin_text : str
        Count line then the values line.

    Returns
    -------
    list[int]
        The values in input order.
    """
    lines = _read_lines(stdin_text)
    value_count = int(lines[0])
    return [int(value) for value in lines[1].split()[:value_count]]


def _collect_permutations(
    remaining: list[int], chosen: list[int], found: list[tuple[int, ...]]
) -> None:
    """Take one unused number at a time until none are left.

    Parameters
    ----------
    remaining : list[int]
        Numbers not yet placed.
    chosen : list[int]
        Numbers placed so far.
    found : list[tuple[int, ...]]
        Completed arrangements, extended in place.

    Returns
    -------
    None
    """
    if not remaining:
        found.append(tuple(chosen))
        return
    for position, value in enumerate(remaining):
        shorter = remaining[:position] + remaining[position + 1 :]
        _collect_permutations(shorter, chosen + [value], found)


def solve_permutations(stdin_text: str) -> str:
    """List every arrangement of the given distinct numbers.

    Parameters
    ----------
    stdin_text : str
        Count line then the values line.

    Returns
    -------
    str
        One arrangement per line in ascending tuple order.
    """
    values = _parse_number_list(stdin_text)
    found: list[tuple[int, ...]] = []
    _collect_permutations(values, [], found)
    return _render_number_tuples(found)


def brute_permutations(stdin_text: str) -> str:
    """List the same arrangements straight from the standard library.

    Parameters
    ----------
    stdin_text : str
        Count line then the values line.

    Returns
    -------
    str
        One arrangement per line in ascending tuple order.
    """
    values = _parse_number_list(stdin_text)
    found = list(itertools.permutations(values))
    return _render_number_tuples(found)


# ---------------------------------------------------------------- Combination Sum


def _parse_combination_sum_payload(stdin_text: str) -> tuple[list[int], int]:
    """Read the candidate count and target, then the candidates.

    Parameters
    ----------
    stdin_text : str
        Counts header then the candidates line.

    Returns
    -------
    tuple[list[int], int]
        Candidates in input order, and the target sum.
    """
    lines = _read_lines(stdin_text)
    candidate_count, target = (int(value) for value in lines[0].split())
    candidates = [int(value) for value in lines[1].split()[:candidate_count]]
    return candidates, target


def _collect_combination_sum(
    candidates: list[int],
    index: int,
    remaining: int,
    chosen: list[int],
    found: list[tuple[int, ...]],
) -> None:
    """Reuse the current candidate or move on, recording exact sums.

    Parameters
    ----------
    candidates : list[int]
        Candidates sorted ascending.
    index : int
        Smallest candidate index still allowed.
    remaining : int
        Amount left to reach.
    chosen : list[int]
        Candidates picked so far.
    found : list[tuple[int, ...]]
        Completed combinations, extended in place.

    Returns
    -------
    None
    """
    if remaining == 0:
        found.append(tuple(chosen))
        return
    if index >= len(candidates) or remaining < candidates[index]:
        return
    chosen.append(candidates[index])
    _collect_combination_sum(candidates, index, remaining - candidates[index], chosen, found)
    chosen.pop()
    _collect_combination_sum(candidates, index + 1, remaining, chosen, found)


def solve_combination_sum(stdin_text: str) -> str:
    """List every multiset of candidates that adds up to the target.

    Parameters
    ----------
    stdin_text : str
        Counts header then the candidates line.

    Returns
    -------
    str
        One combination per line, numbers ascending, or "none".
    """
    candidates, target = _parse_combination_sum_payload(stdin_text)
    found: list[tuple[int, ...]] = []
    _collect_combination_sum(sorted(candidates), 0, target, [], found)
    return _render_number_tuples(found)


def brute_combination_sum(stdin_text: str) -> str:
    """List the same combinations by trying every count of every candidate.

    Parameters
    ----------
    stdin_text : str
        Counts header then the candidates line.

    Returns
    -------
    str
        One combination per line, numbers ascending, or "none".
    """
    candidates, target = _parse_combination_sum_payload(stdin_text)
    ordered = sorted(candidates)
    found: list[tuple[int, ...]] = []
    stack: list[tuple[int, int, tuple[int, ...]]] = [(0, target, ())]
    while stack:
        index, remaining, chosen = stack.pop()
        if remaining == 0:
            found.append(chosen)
            continue
        if index >= len(ordered):
            continue
        candidate = ordered[index]
        for count in range(remaining // candidate + 1):
            taken = chosen + (candidate,) * count
            stack.append((index + 1, remaining - candidate * count, taken))
    return _render_number_tuples(found)


# ---------------------------------------------------------------- N-Queens II


def _count_queen_placements(
    board_size: int, row: int, columns: int, diagonals: int, anti_diagonals: int
) -> int:
    """Count safe completions from a partially filled board.

    Parameters
    ----------
    board_size : int
        Side length of the board.
    row : int
        Row to fill next.
    columns : int
        Bitmask of columns already attacked.
    diagonals : int
        Bitmask of down-right diagonals already attacked, shifted per row.
    anti_diagonals : int
        Bitmask of down-left diagonals already attacked, shifted per row.

    Returns
    -------
    int
        Number of complete safe arrangements.
    """
    if row == board_size:
        return 1
    total = 0
    available = ~(columns | diagonals | anti_diagonals) & ((1 << board_size) - 1)
    while available:
        spot = available & -available
        available -= spot
        total += _count_queen_placements(
            board_size,
            row + 1,
            columns | spot,
            (diagonals | spot) << 1,
            (anti_diagonals | spot) >> 1,
        )
    return total


def solve_n_queens_ii(stdin_text: str) -> str:
    """Count safe queen arrangements with bitmask backtracking.

    Parameters
    ----------
    stdin_text : str
        Single line holding the board size.

    Returns
    -------
    str
        Number of arrangements.
    """
    board_size = int(_read_lines(stdin_text)[0])
    return str(_count_queen_placements(board_size, 0, 0, 0, 0))


def brute_n_queens_ii(stdin_text: str) -> str:
    """Count safe queen arrangements by testing every column permutation.

    Parameters
    ----------
    stdin_text : str
        Single line holding the board size.

    Returns
    -------
    str
        Number of arrangements.
    """
    board_size = int(_read_lines(stdin_text)[0])
    safe_count = 0
    for placement in itertools.permutations(range(board_size)):
        is_safe = True
        for left_row in range(board_size):
            for right_row in range(left_row + 1, board_size):
                column_gap = abs(placement[left_row] - placement[right_row])
                if column_gap == right_row - left_row:
                    is_safe = False
                    break
            if not is_safe:
                break
        if is_safe:
            safe_count += 1
    return str(safe_count)


# ---------------------------------------------------------------- Generate Parentheses


def _collect_parentheses(
    pair_count: int, opened: int, closed: int, prefix: str, found: list[str]
) -> None:
    """Add a bracket at a time, keeping the prefix balanced.

    Parameters
    ----------
    pair_count : int
        Number of bracket pairs to place.
    opened : int
        Opening brackets used so far.
    closed : int
        Closing brackets used so far.
    prefix : str
        String built so far.
    found : list[str]
        Completed strings, extended in place.

    Returns
    -------
    None
    """
    if len(prefix) == 2 * pair_count:
        found.append(prefix)
        return
    if opened < pair_count:
        _collect_parentheses(pair_count, opened + 1, closed, prefix + "(", found)
    if closed < opened:
        _collect_parentheses(pair_count, opened, closed + 1, prefix + ")", found)


def solve_generate_parentheses(stdin_text: str) -> str:
    """List every balanced bracket string of the wanted pair count.

    Parameters
    ----------
    stdin_text : str
        Single line holding the number of pairs.

    Returns
    -------
    str
        One string per line in lexicographic order, or "none".
    """
    pair_count = int(_read_lines(stdin_text)[0])
    if pair_count == 0:
        return EMPTY_RESULT_TOKEN
    found: list[str] = []
    _collect_parentheses(pair_count, 0, 0, "", found)
    return "\n".join(sorted(found))


def brute_generate_parentheses(stdin_text: str) -> str:
    """List the same strings by filtering every bracket string of that length.

    Parameters
    ----------
    stdin_text : str
        Single line holding the number of pairs.

    Returns
    -------
    str
        One string per line in lexicographic order, or "none".
    """
    pair_count = int(_read_lines(stdin_text)[0])
    if pair_count == 0:
        return EMPTY_RESULT_TOKEN
    found: list[str] = []
    for brackets in itertools.product("()", repeat=2 * pair_count):
        depth = 0
        for bracket in brackets:
            depth += 1 if bracket == "(" else -1
            if depth < 0:
                break
        if depth == 0:
            found.append("".join(brackets))
    return "\n".join(sorted(found))


# ---------------------------------------------------------------- Word Search


def _search_word_from(
    grid: list[list[str]], word: str, position: int, row: int, column: int, used: set[tuple[int, int]]
) -> bool:
    """Try to spell the rest of the word starting at one cell.

    Parameters
    ----------
    grid : list[list[str]]
        Letter grid.
    word : str
        Word being spelled.
    position : int
        Index of the letter expected at this cell.
    row : int
        Row of this cell.
    column : int
        Column of this cell.
    used : set[tuple[int, int]]
        Cells already on the current path, mutated in place.

    Returns
    -------
    bool
        True when the remaining letters can be spelled from this cell.
    """
    if grid[row][column] != word[position]:
        return False
    if position == len(word) - 1:
        return True
    used.add((row, column))
    for row_step, column_step in CARDINAL_STEPS:
        next_row = row + row_step
        next_column = column + column_step
        is_inside = 0 <= next_row < len(grid) and 0 <= next_column < len(grid[0])
        if not is_inside or (next_row, next_column) in used:
            continue
        if _search_word_from(grid, word, position + 1, next_row, next_column, used):
            used.discard((row, column))
            return True
    used.discard((row, column))
    return False


def solve_word_search(stdin_text: str) -> str:
    """Decide whether the word can be spelled along a path of adjacent cells.

    Parameters
    ----------
    stdin_text : str
        Grid header, the grid rows, then the word.

    Returns
    -------
    str
        "true" when the word can be spelled, otherwise "false".
    """
    grid, remaining_lines = _parse_character_grid(stdin_text)
    word = remaining_lines[0].strip()
    for row in range(len(grid)):
        for column in range(len(grid[0])):
            if _search_word_from(grid, word, 0, row, column, set()):
                return "true"
    return "false"


def brute_word_search(stdin_text: str) -> str:
    """Decide the same question by expanding every matching path one letter at a time.

    Parameters
    ----------
    stdin_text : str
        Grid header, the grid rows, then the word.

    Returns
    -------
    str
        "true" when the word can be spelled, otherwise "false".
    """
    grid, remaining_lines = _parse_character_grid(stdin_text)
    word = remaining_lines[0].strip()
    row_count = len(grid)
    column_count = len(grid[0])
    paths: list[tuple[tuple[int, int], frozenset[tuple[int, int]]]] = [
        ((row, column), frozenset({(row, column)}))
        for row in range(row_count)
        for column in range(column_count)
        if grid[row][column] == word[0]
    ]
    for letter in word[1:]:
        grown: list[tuple[tuple[int, int], frozenset[tuple[int, int]]]] = []
        for (row, column), visited in paths:
            for row_step, column_step in CARDINAL_STEPS:
                next_row = row + row_step
                next_column = column + column_step
                is_inside = 0 <= next_row < row_count and 0 <= next_column < column_count
                if not is_inside or (next_row, next_column) in visited:
                    continue
                if grid[next_row][next_column] == letter:
                    grown.append(
                        ((next_row, next_column), visited | {(next_row, next_column)})
                    )
        paths = grown
        if not paths:
            return "false"
    return "true" if paths else "false"


PROBLEMS: list[dict[str, Any]] = [
    {
        "title": "Number of Islands",
        "level": "Medium",
        "topics": "Array, Matrix, Depth-First Search, Breadth-First Search, Union Find",
        "companies": "Amazon, Google, Microsoft, Bloomberg, Meta",
        "description": """Land and water are laid out on a rectangular map. A cell holding `1` is land and a cell holding `0` is water. An island is a group of land cells joined through shared edges, counting only the four sides, never the corners. Count the islands.

**Input**

- The first line holds two integers: the number of rows and the number of columns.
- Each of the next rows holds that many cells separated by single spaces, each cell `0` or `1`.

**Output**

- A single line with the number of islands.

""",
        "examples": """**Example 1**

```
Input
4 5
1 1 0 0 0
1 1 0 0 0
0 0 1 0 0
0 0 0 1 1

Output
3
```

**Example 2**

```
Input
3 3
1 0 1
0 1 0
1 0 1

Output
5
```

""",
        "constraints": """- `1 <= rows, cols <= 50`
- Every cell is either `0` or `1`.
- The grid may be entirely water, in which case the answer is `0`.

""",
        "inputs": [
            "4 5\n1 1 0 0 0\n1 1 0 0 0\n0 0 1 0 0\n0 0 0 1 1",
            "1 1\n1",
            "1 1\n0",
            "3 3\n1 0 1\n0 1 0\n1 0 1",
            "3 4\n0 0 0 0\n0 0 0 0\n0 0 0 0",
            "5 5\n1 1 1 1 1\n1 0 0 0 1\n1 0 1 0 1\n1 0 0 0 1\n1 1 1 1 1",
        ],
        "solve": solve_number_of_islands,
        "brute": brute_number_of_islands,
    },
    {
        "title": "Surrounded Regions",
        "level": "Medium",
        "topics": "Array, Matrix, Depth-First Search, Breadth-First Search, Union Find",
        "companies": "Amazon, Microsoft, Google, Uber",
        "description": """A board is filled with the letters `X` and `O`. A region is a group of `O` cells joined through shared edges, counting only the four sides. A region is captured when none of its cells sit on the outer border of the board. Capture every such region by turning its `O` cells into `X`, and leave every region that touches the border untouched.

**Input**

- The first line holds two integers: the number of rows and the number of columns.
- Each of the next rows holds that many cells separated by single spaces, each cell `X` or `O`.

**Output**

- The board after the captures, one row per line, cells separated by single spaces.

""",
        "examples": """**Example 1**

```
Input
4 4
X X X X
X O O X
X X O X
X O X X

Output
X X X X
X X X X
X X X X
X O X X
```

**Example 2**

```
Input
3 3
X X X
X O X
X X X

Output
X X X
X X X
X X X
```

""",
        "constraints": """- `1 <= rows, cols <= 50`
- Every cell is either `X` or `O`.
- On a board of one row or one column every cell sits on the border, so nothing is captured.

""",
        "inputs": [
            "4 4\nX X X X\nX O O X\nX X O X\nX O X X",
            "1 1\nO",
            "1 1\nX",
            "3 3\nO O O\nO O O\nO O O",
            "3 3\nX X X\nX O X\nX X X",
            "4 5\nX O X O X\nO X O X O\nX O X O X\nO X O X O",
        ],
        "solve": solve_surrounded_regions,
        "brute": brute_surrounded_regions,
    },
    {
        "title": "Clone Graph",
        "level": "Medium",
        "topics": "Graph, Hash Table, Depth-First Search, Breadth-First Search",
        "companies": "Meta, Amazon, Google, Pinterest",
        "description": """You are given a connected or disconnected undirected graph whose nodes are labelled `1` to `n`. Build a deep copy of it: a fresh node object per original node, wired to the copies of its neighbours. No copied node may point at an original node, and no original node may be modified. Then print the copy, which is what proves the wiring is right.

**Input**

- The first line holds `n`, the number of nodes.
- Each of the next `n` lines describes one node, in label order starting at `1`: the node's neighbour count, then that many neighbour labels separated by single spaces. A node with no neighbours is the single value `0`.

**Output**

- `n` lines, one per node in label order. Each line holds the label, a colon, a space, then the labels of that node's neighbours **in the copied graph** in ascending order, separated by single spaces. When a node has no neighbours, print the word `none` in their place.

""",
        "examples": """**Example 1**

```
Input
4
2 2 4
2 1 3
2 2 4
2 1 3

Output
1: 2 4
2: 1 3
3: 2 4
4: 1 3
```

**Example 2**

```
Input
1
0

Output
1: none
```

""",
        "constraints": """- `1 <= n <= 100`
- Every neighbour label is between `1` and `n`.
- There are no self loops and no repeated edges.
- Edges are undirected, so each edge appears in both of its endpoints' lines.

""",
        "inputs": [
            "4\n2 2 4\n2 1 3\n2 2 4\n2 1 3",
            "1\n0",
            "2\n0\n0",
            "5\n2 2 3\n1 1\n1 1\n1 5\n1 4",
            "3\n2 2 3\n2 1 3\n2 1 2",
            "2\n1 2\n1 1",
        ],
        "solve": solve_clone_graph,
        "brute": brute_clone_graph,
    },
    {
        "title": "Evaluate Division",
        "level": "Medium",
        "topics": "Graph, Hash Table, Breadth-First Search, Union Find, Shortest Path",
        "companies": "Google, Meta, Amazon, Airbnb",
        "description": """You are given a list of equations of the form `A / B = value`, where `A` and `B` are variable names. Each equation also tells you `B / A`, which is the reciprocal. Answer a list of queries, each asking for the value of `C / D`. A query is unanswerable when either name never appears in the equations, or when no chain of equations connects the two names.

**Input**

- The first line holds two integers: the number of equations and the number of queries.
- Each of the next equation lines holds a numerator name, a denominator name and the value, separated by single spaces.
- Each of the remaining query lines holds the numerator name and the denominator name of one query.

**Output**

- One line per query, in input order, holding the value rounded to exactly five decimal places. Print `-1.00000` for an unanswerable query. A query such as `a a` for a known name `a` answers `1.00000`.

""",
        "examples": """**Example 1**

```
Input
2 4
a b 2.0
b c 3.0
a c
b a
a e
a a

Output
6.00000
0.50000
-1.00000
1.00000
```

**Example 2**

```
Input
2 3
a b 2.0
c d 3.0
a d
c d
b a

Output
-1.00000
3.00000
0.50000
```

""",
        "constraints": """- `1 <= equations <= 20` and `1 <= queries <= 20`
- Variable names are lowercase letters, at most 5 characters.
- Every equation value is greater than `0`.
- The equations never contradict each other.

""",
        "inputs": [
            "2 4\na b 2.0\nb c 3.0\na c\nb a\na e\na a",
            "1 2\nx y 0.5\ny x\nx x",
            "2 3\na b 2.0\nc d 3.0\na d\nc d\nb a",
            "1 1\np q 4.0\nr s",
            "3 3\na b 2.0\nb c 1.5\nc d 4.0\na d\nd a\nb d",
            "2 3\na b 2.0\nb c 3.0\nx x\nc a\nb b",
        ],
        "solve": solve_evaluate_division,
        "brute": brute_evaluate_division,
    },
    {
        "title": "Course Schedule",
        "level": "Medium",
        "topics": "Graph, Topological Sort, Depth-First Search, Breadth-First Search",
        "companies": "Amazon, Google, Microsoft, Bloomberg",
        "description": """A degree has `numCourses` courses, numbered `0` to `numCourses - 1`. A prerequisite pair `a b` means course `b` has to be finished before course `a` can be taken. Decide whether all the courses can be finished.

**Input**

- The first line holds two integers: `numCourses` and the number of prerequisite pairs.
- Each of the next lines holds one pair `a b`, meaning `b` comes before `a`.

**Output**

- A single line holding `true` when every course can be finished, otherwise `false`.

""",
        "examples": """**Example 1**

```
Input
2 1
1 0

Output
true
```

**Example 2**

```
Input
2 2
1 0
0 1

Output
false
```

""",
        "constraints": """- `1 <= numCourses <= 2000`
- `0 <= pairs <= 5000`
- `0 <= a, b < numCourses` and `a != b`
- No pair is repeated.

""",
        "inputs": [
            "2 1\n1 0",
            "2 2\n1 0\n0 1",
            "1 0",
            "4 4\n1 0\n2 1\n3 2\n1 3",
            "5 3\n1 0\n2 0\n4 3",
            "3 3\n0 1\n1 2\n2 0",
        ],
        "solve": solve_course_schedule,
        "brute": brute_course_schedule,
    },
    {
        "title": "Course Schedule II",
        "level": "Medium",
        "topics": "Graph, Topological Sort, Heap (Priority Queue), Breadth-First Search",
        "companies": "Amazon, Google, Microsoft, Uber",
        "description": """A degree has `numCourses` courses, numbered `0` to `numCourses - 1`. A prerequisite pair `a b` means course `b` has to be finished before course `a` can be taken. Produce an order in which all the courses can be taken.

Many orders are usually valid, so exactly one is accepted: the **lexicographically smallest** one. Read the order as a sequence of course numbers and compare sequences position by position; the accepted answer is the smallest under that comparison. In practice this means that whenever several courses have all their prerequisites met, the one with the smallest number is taken next.

**Input**

- The first line holds two integers: `numCourses` and the number of prerequisite pairs.
- Each of the next lines holds one pair `a b`, meaning `b` comes before `a`.

**Output**

- A single line holding the course numbers in order, separated by single spaces. When no order exists, print the word `none` instead.

""",
        "examples": """**Example 1**

```
Input
4 4
1 0
2 0
3 1
3 2

Output
0 1 2 3
```

**Example 2**

```
Input
4 2
0 3
1 3

Output
2 3 0 1
```

""",
        "constraints": """- `1 <= numCourses <= 2000`
- `0 <= pairs <= 5000`
- `0 <= a, b < numCourses` and `a != b`
- No pair is repeated.

""",
        "inputs": [
            "4 4\n1 0\n2 0\n3 1\n3 2",
            "4 2\n0 3\n1 3",
            "1 0",
            "2 2\n0 1\n1 0",
            "3 0",
            "6 4\n2 5\n0 5\n1 2\n3 1",
        ],
        "solve": solve_course_schedule_ii,
        "brute": brute_course_schedule_ii,
    },
    {
        "title": "Snakes and Ladders",
        "level": "Medium",
        "topics": "Array, Matrix, Breadth-First Search, Shortest Path",
        "companies": "Amazon, Google, Microsoft",
        "description": """An `n` by `n` board is numbered from `1` to `n * n` in boustrophedon order: numbering starts in the bottom left corner, runs right along the bottom row, then turns and runs left along the row above it, alternating direction on every row.

A turn works like this. From square `s` you may move to any of `s + 1` through `s + 6`, as long as the number does not pass `n * n`. If the square you land on carries a snake or ladder, you are moved to its destination immediately. You never take a second snake or ladder in the same turn, even when the destination carries one. Find the fewest turns needed to land exactly on square `n * n`.

**Input**

- The first line holds `n`.
- Each of the next `n` lines holds `n` integers separated by single spaces, given top row first. A value of `-1` means the square is plain; any other value is the destination square of the snake or ladder on that square.

**Output**

- A single line with the fewest turns, or `-1` when the last square cannot be reached.

""",
        "examples": """**Example 1**

```
Input
6
-1 -1 -1 -1 -1 -1
-1 -1 -1 -1 -1 -1
-1 -1 -1 -1 -1 -1
-1 35 -1 -1 13 -1
-1 -1 -1 -1 -1 -1
-1 15 -1 -1 -1 -1

Output
4
```

**Example 2**

```
Input
3
1 -1 -1
1 1 1
-1 1 1

Output
-1
```

""",
        "constraints": """- `2 <= n <= 20`, plus the degenerate `n = 1` board, where the answer is `0`.
- Each value is `-1` or a square number between `1` and `n * n`.
- A snake or ladder never starts on square `1` or on square `n * n`.

""",
        "inputs": [
            "6\n-1 -1 -1 -1 -1 -1\n-1 -1 -1 -1 -1 -1\n-1 -1 -1 -1 -1 -1\n-1 35 -1 -1 13 -1\n-1 -1 -1 -1 -1 -1\n-1 15 -1 -1 -1 -1",
            "1\n-1",
            "2\n-1 -1\n-1 -1",
            "3\n1 -1 -1\n1 1 1\n-1 1 1",
            "4\n-1 -1 -1 -1\n-1 -1 -1 -1\n-1 -1 -1 -1\n-1 -1 -1 16",
            "6\n-1 -1 -1 -1 -1 -1\n-1 -1 -1 -1 -1 -1\n-1 -1 -1 -1 -1 -1\n-1 -1 -1 -1 -1 -1\n-1 -1 -1 -1 -1 -1\n-1 -1 -1 -1 -1 -1",
        ],
        "solve": solve_snakes_and_ladders,
        "brute": brute_snakes_and_ladders,
    },
    {
        "title": "Minimum Genetic Mutation",
        "level": "Medium",
        "topics": "Graph, Hash Table, Breadth-First Search, String",
        "companies": "Amazon, Google, Microsoft",
        "description": """A gene is a string of the characters `A`, `C`, `G` and `T`, all genes here having the same length. One mutation changes exactly one character of the gene. A mutation is only allowed when the gene it produces appears in the gene bank. Starting from the start gene, count the fewest mutations that turn it into the end gene.

The start gene itself does not have to be in the bank. When the start gene already equals the end gene the answer is `0`, whatever the bank holds.

**Input**

- The first line holds the start gene.
- The second line holds the end gene.
- The third line holds the number of genes in the bank.
- Each of the next lines holds one bank gene.

**Output**

- A single line with the fewest mutations, or `-1` when the end gene cannot be reached.

""",
        "examples": """**Example 1**

```
Input
AACCGGTT
AAACGGTA
3
AACCGGTA
AACCGCTA
AAACGGTA

Output
2
```

**Example 2**

```
Input
AACCGGTT
AAACGGTA
2
AACCGGTA
AACCGCTA

Output
-1
```

""",
        "constraints": """- Every gene is 8 characters long and uses only `A`, `C`, `G` and `T`.
- `0 <= bank size <= 10`
- The bank may be empty, in which case only the start equals end case answers anything but `-1`.

""",
        "inputs": [
            "AACCGGTT\nAACCGGTA\n1\nAACCGGTA",
            "AACCGGTT\nAAACGGTA\n3\nAACCGGTA\nAACCGCTA\nAAACGGTA",
            "AACCGGTT\nAACCGGTT\n0",
            "AACCGGTT\nAAACGGTA\n2\nAACCGGTA\nAACCGCTA",
            "AACCGGTT\nAACCGGTA\n0",
            "AAAAAAAA\nCCCCCCCC\n3\nAAAAAAAC\nAAAAAACC\nCCCCCCCC",
        ],
        "solve": solve_minimum_genetic_mutation,
        "brute": brute_minimum_genetic_mutation,
    },
    {
        "title": "Word Ladder",
        "level": "Hard",
        "topics": "Graph, Hash Table, Breadth-First Search, String",
        "companies": "Amazon, Google, Meta, Microsoft, LinkedIn",
        "description": """You are given a begin word, an end word and a word list. All the words have the same length. A transformation chain starts at the begin word and ends at the end word, changes exactly one letter per step, and every word after the first has to be in the word list. Find the shortest such chain and report how many words it contains, counting both ends.

**Input**

- The first line holds the begin word.
- The second line holds the end word.
- The third line holds the number of words in the list.
- Each of the next lines holds one word from the list.

**Output**

- A single line with the number of words in the shortest chain, or `0` when no chain exists. In particular the answer is `0` whenever the end word is missing from the word list.

""",
        "examples": """**Example 1**

```
Input
hit
cog
6
hot
dot
dog
lot
log
cog

Output
5
```

**Example 2**

```
Input
hit
cog
5
hot
dot
dog
lot
log

Output
0
```

""",
        "constraints": """- `1 <= word length <= 10`, every word lowercase letters only.
- `1 <= list size <= 100`, all words distinct.
- The begin word and the end word are different, and the begin word need not be in the list.

""",
        "inputs": [
            "hit\ncog\n6\nhot\ndot\ndog\nlot\nlog\ncog",
            "hit\ncog\n5\nhot\ndot\ndog\nlot\nlog",
            "hit\nhot\n1\nhot",
            "hit\ncog\n3\nhot\ndot\ncog",
            "a\nc\n3\na\nb\nc",
            "red\ntax\n5\nted\ntex\ntax\nden\nrex",
        ],
        "solve": solve_word_ladder,
        "brute": brute_word_ladder,
    },
    {
        "title": "Letter Combinations of a Phone Number",
        "level": "Medium",
        "topics": "Backtracking, String, Hash Table",
        "companies": "Amazon, Google, Meta, Uber, Dropbox",
        "description": """On an old telephone keypad each digit from `2` to `9` prints a group of letters: `2` prints `abc`, `3` prints `def`, `4` prints `ghi`, `5` prints `jkl`, `6` prints `mno`, `7` prints `pqrs`, `8` prints `tuv` and `9` prints `wxyz`. Given a string of such digits, list every letter string it could spell by picking one letter per digit.

**Input**

- A single line holding the digits, each one between `2` and `9`. When there are no digits at all the line holds the word `empty` instead.

**Output**

- One combination per line, every combination the same length as the digit string, and the whole list sorted lexicographically, meaning ordinary alphabetical string order. When the digit string is empty there are no combinations, so print the word `none` instead.

""",
        "examples": """**Example 1**

```
Input
23

Output
ad
ae
af
bd
be
bf
cd
ce
cf
```

**Example 2**

```
Input
empty

Output
none
```

""",
        "constraints": """- `0 <= number of digits <= 4`
- Every digit is between `2` and `9`; `0` and `1` never appear.
- The line is exactly `empty` when the digit string is empty.

""",
        "inputs": ["23", "2", "empty", "79", "234", "9"],
        "solve": solve_letter_combinations_of_a_phone_number,
        "brute": brute_letter_combinations_of_a_phone_number,
    },
    {
        "title": "Combinations",
        "level": "Medium",
        "topics": "Backtracking, Combinatorics",
        "companies": "Amazon, Google, Microsoft, Adobe",
        "description": """Given two integers `n` and `k`, list every way of choosing `k` different numbers out of `1` to `n`. The order within a choice does not matter, so each choice is listed once.

**Input**

- A single line holding `n` and `k`, separated by a space.

**Output**

- One choice per line, its numbers in ascending order and separated by single spaces.
- The lines are sorted by comparing the choices as number sequences, position by position, smallest first. Compare numbers as numbers, not as text, so `2` comes before `10`.
- When no choice is possible, print the word `none` instead.

""",
        "examples": """**Example 1**

```
Input
4 2

Output
1 2
1 3
1 4
2 3
2 4
3 4
```

**Example 2**

```
Input
3 4

Output
none
```

""",
        "constraints": """- `1 <= n <= 12`
- `1 <= k <= 12`; `k` may exceed `n`, in which case there is no choice at all.

""",
        "inputs": ["4 2", "1 1", "3 4", "5 5", "11 1", "5 3"],
        "solve": solve_combinations,
        "brute": brute_combinations,
    },
    {
        "title": "Permutations",
        "level": "Medium",
        "topics": "Backtracking, Array",
        "companies": "Amazon, Google, Microsoft, LinkedIn",
        "description": """Given a list of distinct integers, list every possible arrangement of all of them.

**Input**

- The first line holds `m`, how many numbers follow.
- The second line holds the `m` numbers, separated by single spaces.

**Output**

- One arrangement per line, its numbers separated by single spaces.
- The lines are sorted by comparing the arrangements as number sequences, position by position, smallest first. Compare numbers as numbers, not as text, so `2` comes before `10` and `-1` comes before both.

""",
        "examples": """**Example 1**

```
Input
3
1 2 3

Output
1 2 3
1 3 2
2 1 3
2 3 1
3 1 2
3 2 1
```

**Example 2**

```
Input
3
10 2 1

Output
1 2 10
1 10 2
2 1 10
2 10 1
10 1 2
10 2 1
```

""",
        "constraints": """- `1 <= m <= 6`
- `-10 <= each number <= 10`, and all the numbers are distinct.

""",
        "inputs": [
            "3\n1 2 3",
            "1\n7",
            "2\n-1 5",
            "4\n1 2 3 4",
            "3\n10 2 1",
            "3\n-5 0 5",
        ],
        "solve": solve_permutations,
        "brute": brute_permutations,
    },
    {
        "title": "Combination Sum",
        "level": "Medium",
        "topics": "Backtracking, Array",
        "companies": "Amazon, Google, Microsoft, Bloomberg",
        "description": """Given a list of distinct positive integers and a target, list every group of them that adds up exactly to the target. A number may be used as many times as you like, and two groups count as the same group when they use the same numbers the same number of times.

**Input**

- The first line holds two integers: how many candidate numbers follow, and the target.
- The second line holds the candidate numbers, separated by single spaces.

**Output**

- One group per line, its numbers in ascending order and separated by single spaces.
- The lines are sorted by comparing the groups as number sequences, position by position, smallest first; when one group is a prefix of another, the shorter one comes first.
- When nothing adds up to the target, print the word `none` instead.

""",
        "examples": """**Example 1**

```
Input
4 7
2 3 6 7

Output
2 2 3
7
```

**Example 2**

```
Input
2 9
2 4

Output
none
```

""",
        "constraints": """- `1 <= candidates <= 8`, all distinct.
- `2 <= each candidate <= 40`
- `1 <= target <= 40`

""",
        "inputs": [
            "4 7\n2 3 6 7",
            "3 8\n2 3 5",
            "1 1\n2",
            "1 5\n5",
            "2 9\n2 4",
            "3 10\n2 3 4",
        ],
        "solve": solve_combination_sum,
        "brute": brute_combination_sum,
    },
    {
        "title": "N-Queens II",
        "level": "Hard",
        "topics": "Backtracking, Bit Manipulation",
        "companies": "Amazon, Google, Microsoft, Apple",
        "description": """Count the ways of putting `n` queens on an `n` by `n` chessboard so that no two of them attack each other. Two queens attack each other when they share a row, a column, or a diagonal in either direction.

**Input**

- A single line holding `n`.

**Output**

- A single line with the number of arrangements. It is `0` when no arrangement exists.

""",
        "examples": """**Example 1**

```
Input
4

Output
2
```

**Example 2**

```
Input
2

Output
0
```

""",
        "constraints": """- `1 <= n <= 9`

""",
        "inputs": ["4", "1", "2", "3", "6", "8"],
        "solve": solve_n_queens_ii,
        "brute": brute_n_queens_ii,
    },
    {
        "title": "Generate Parentheses",
        "level": "Medium",
        "topics": "Backtracking, String, Dynamic Programming",
        "companies": "Amazon, Google, Meta, Microsoft, Uber",
        "description": """Given a number of bracket pairs, list every well formed string built from them. A string is well formed when every opening bracket is closed later and no closing bracket ever comes before the opening bracket it belongs to.

**Input**

- A single line holding `n`, the number of bracket pairs.

**Output**

- One string per line, each of length `2 * n`, and the whole list sorted lexicographically, meaning ordinary string order where `(` sorts before `)`.
- When `n` is `0` there is nothing to list, so print the word `none` instead.

""",
        "examples": """**Example 1**

```
Input
3

Output
((()))
(()())
(())()
()(())
()()()
```

**Example 2**

```
Input
0

Output
none
```

""",
        "constraints": """- `0 <= n <= 8`

""",
        "inputs": ["3", "1", "0", "2", "4", "5"],
        "solve": solve_generate_parentheses,
        "brute": brute_generate_parentheses,
    },
    {
        "title": "Word Search",
        "level": "Medium",
        "topics": "Backtracking, Array, Matrix, Depth-First Search",
        "companies": "Amazon, Microsoft, Google, Bloomberg, Meta",
        "description": """A grid is filled with single uppercase letters. A word is present when its letters can be read along a path of cells where each step moves to a cell sharing an edge with the previous one, counting only the four sides. No cell may be used twice in the same path. Decide whether the word is present.

**Input**

- The first line holds two integers: the number of rows and the number of columns.
- Each of the next rows holds that many letters separated by single spaces.
- The last line holds the word.

**Output**

- A single line holding `true` when the word is present, otherwise `false`.

""",
        "examples": """**Example 1**

```
Input
3 4
A B C E
S F C S
A D E E
ABCCED

Output
true
```

**Example 2**

```
Input
3 4
A B C E
S F C S
A D E E
ABCB

Output
false
```

""",
        "constraints": """- `1 <= rows, cols <= 6`
- `1 <= word length <= 15`
- The grid cells and the word use uppercase letters only.

""",
        "inputs": [
            "3 4\nA B C E\nS F C S\nA D E E\nABCCED",
            "3 4\nA B C E\nS F C S\nA D E E\nSEE",
            "3 4\nA B C E\nS F C S\nA D E E\nABCB",
            "1 1\nA\nA",
            "1 1\nA\nB",
            "3 3\nA A A\nA A A\nA A A\nAAAAAAAAAA",
        ],
        "solve": solve_word_search,
        "brute": brute_word_search,
    },
]
