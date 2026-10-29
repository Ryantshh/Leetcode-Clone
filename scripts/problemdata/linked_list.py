"""Linked list problem specs for the study-plan seeder.

Every problem is a stdin-to-stdout task: the editor hands the user no scaffold,
so each statement spells out the text format of the list instead of assuming a
node class.
"""

from __future__ import annotations

from typing import Any, Optional

EMPTY_LIST_TOKEN = "empty"


class ListNode:
    """Singly linked list node carrying an optional arbitrary second pointer.

    Parameters
    ----------
    value : int
        Stored integer.

    Attributes
    ----------
    value : int
        Stored integer.
    next_node : Optional[ListNode]
        Following node, or None at the end of the list.
    random_node : Optional[ListNode]
        Arbitrary node of the same list, or None.
    """

    def __init__(self, value: int) -> None:
        self.value: int = value
        self.next_node: Optional[ListNode] = None
        self.random_node: Optional[ListNode] = None


class DoublyLinkedCacheNode:
    """Cache entry inside a recency-ordered doubly linked list.

    Parameters
    ----------
    key : int
        Cache key.
    value : int
        Cached value.

    Attributes
    ----------
    key : int
        Cache key.
    value : int
        Cached value.
    previous_node : Optional[DoublyLinkedCacheNode]
        Neighbour towards the least recently used end.
    next_node : Optional[DoublyLinkedCacheNode]
        Neighbour towards the most recently used end.
    """

    def __init__(self, key: int, value: int) -> None:
        self.key: int = key
        self.value: int = value
        self.previous_node: Optional[DoublyLinkedCacheNode] = None
        self.next_node: Optional[DoublyLinkedCacheNode] = None


class LeastRecentlyUsedCache:
    """Fixed-capacity key-value cache that evicts the least recently used key.

    Parameters
    ----------
    capacity : int
        Maximum number of keys held at once.

    Attributes
    ----------
    capacity : int
        Maximum number of keys held at once.
    """

    def __init__(self, capacity: int) -> None:
        self.capacity: int = capacity
        self.nodes_by_key: dict[int, DoublyLinkedCacheNode] = {}
        self.least_recent_sentinel = DoublyLinkedCacheNode(0, 0)
        self.most_recent_sentinel = DoublyLinkedCacheNode(0, 0)
        self.least_recent_sentinel.next_node = self.most_recent_sentinel
        self.most_recent_sentinel.previous_node = self.least_recent_sentinel

    def detach_node(self, node: DoublyLinkedCacheNode) -> None:
        """Unlink a node from the recency list.

        Parameters
        ----------
        node : DoublyLinkedCacheNode
            Node currently linked between two neighbours.

        Returns
        -------
        None
        """
        previous_node = node.previous_node
        next_node = node.next_node
        if previous_node is not None:
            previous_node.next_node = next_node
        if next_node is not None:
            next_node.previous_node = previous_node
        node.previous_node = None
        node.next_node = None

    def insert_as_most_recent(self, node: DoublyLinkedCacheNode) -> None:
        """Link a detached node just before the most-recent sentinel.

        Parameters
        ----------
        node : DoublyLinkedCacheNode
            Node with both pointers cleared.

        Returns
        -------
        None
        """
        previous_node = self.most_recent_sentinel.previous_node
        node.previous_node = previous_node
        node.next_node = self.most_recent_sentinel
        if previous_node is not None:
            previous_node.next_node = node
        self.most_recent_sentinel.previous_node = node

    def get(self, key: int) -> int:
        """Read a key and mark it most recently used.

        Parameters
        ----------
        key : int
            Key to look up.

        Returns
        -------
        int
            Stored value, or -1 when the key is absent.
        """
        node = self.nodes_by_key.get(key)
        if node is None:
            return -1
        self.detach_node(node)
        self.insert_as_most_recent(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        """Store a key, evicting the least recently used key when full.

        Parameters
        ----------
        key : int
            Key to store.
        value : int
            Value to associate with the key.

        Returns
        -------
        None
        """
        existing_node = self.nodes_by_key.get(key)
        if existing_node is not None:
            existing_node.value = value
            self.detach_node(existing_node)
            self.insert_as_most_recent(existing_node)
            return
        if len(self.nodes_by_key) >= self.capacity:
            evicted_node = self.least_recent_sentinel.next_node
            if evicted_node is not None and evicted_node is not self.most_recent_sentinel:
                self.detach_node(evicted_node)
                del self.nodes_by_key[evicted_node.key]
        fresh_node = DoublyLinkedCacheNode(key, value)
        self.nodes_by_key[key] = fresh_node
        self.insert_as_most_recent(fresh_node)


def split_input_lines(stdin_text: str) -> list[str]:
    """Split a stdin payload into its lines.

    Parameters
    ----------
    stdin_text : str
        Raw stdin payload.

    Returns
    -------
    list[str]
        Lines of the payload.
    """
    return stdin_text.split("\n")


def read_count_and_values(lines: list[str], start_index: int) -> tuple[list[int], int]:
    """Read a count line followed by its space-separated values line.

    Parameters
    ----------
    lines : list[str]
        All stdin lines.
    start_index : int
        Index of the count line.

    Returns
    -------
    tuple[list[int], int]
        The values and the index of the line after this section.
    """
    count = int(lines[start_index].strip())
    values_line = lines[start_index + 1] if start_index + 1 < len(lines) else ""
    values = [int(token) for token in values_line.split()][:count]
    return values, start_index + 2


def build_linked_list(values: list[int]) -> Optional[ListNode]:
    """Chain values into a singly linked list.

    Parameters
    ----------
    values : list[int]
        Node values in order.

    Returns
    -------
    Optional[ListNode]
        Head of the list, or None when there are no values.
    """
    head: Optional[ListNode] = None
    previous_node: Optional[ListNode] = None
    for value in values:
        node = ListNode(value)
        if previous_node is None:
            head = node
        else:
            previous_node.next_node = node
        previous_node = node
    return head


def collect_values(head: Optional[ListNode]) -> list[int]:
    """Walk a singly linked list and collect its values.

    Parameters
    ----------
    head : Optional[ListNode]
        First node, or None for an empty list.

    Returns
    -------
    list[int]
        Values in list order.
    """
    values: list[int] = []
    node = head
    while node is not None:
        values.append(node.value)
        node = node.next_node
    return values


def format_value_line(values: list[int]) -> str:
    """Render list values as one output line.

    Parameters
    ----------
    values : list[int]
        Values to render.

    Returns
    -------
    str
        Space-separated values, or the empty-list token when there are none.
    """
    if not values:
        return EMPTY_LIST_TOKEN
    return " ".join(str(value) for value in values)


def link_nodes_in_order(values: list[int]) -> list[ListNode]:
    """Create one node per value and chain them front to back.

    Parameters
    ----------
    values : list[int]
        Node values in order.

    Returns
    -------
    list[ListNode]
        Nodes indexed by position, already linked.
    """
    nodes = [ListNode(value) for value in values]
    for position in range(len(nodes) - 1):
        nodes[position].next_node = nodes[position + 1]
    return nodes


def solve_linked_list_cycle(stdin_text: str) -> str:
    """Detect a cycle with one slow and one fast walker.

    Parameters
    ----------
    stdin_text : str
        Count line, values line, then the tail target index.

    Returns
    -------
    str
        "true" when the list cycles, otherwise "false".
    """
    lines = split_input_lines(stdin_text)
    values, next_index = read_count_and_values(lines, 0)
    cycle_index = int(lines[next_index].strip())
    nodes = link_nodes_in_order(values)
    if cycle_index >= 0:
        nodes[-1].next_node = nodes[cycle_index]

    slow_node: Optional[ListNode] = nodes[0]
    fast_node: Optional[ListNode] = nodes[0]
    while fast_node is not None and fast_node.next_node is not None:
        slow_node = slow_node.next_node if slow_node is not None else None
        fast_node = fast_node.next_node.next_node
        if slow_node is fast_node:
            return "true"
    return "false"


def brute_linked_list_cycle(stdin_text: str) -> str:
    """Detect a cycle by remembering every node already visited.

    Parameters
    ----------
    stdin_text : str
        Count line, values line, then the tail target index.

    Returns
    -------
    str
        "true" when the list cycles, otherwise "false".
    """
    lines = split_input_lines(stdin_text)
    values, next_index = read_count_and_values(lines, 0)
    cycle_index = int(lines[next_index].strip())
    nodes = link_nodes_in_order(values)
    if cycle_index >= 0:
        nodes[-1].next_node = nodes[cycle_index]

    visited_node_ids: set[int] = set()
    node: Optional[ListNode] = nodes[0]
    while node is not None:
        if id(node) in visited_node_ids:
            return "true"
        visited_node_ids.add(id(node))
        node = node.next_node
    return "false"


def solve_add_two_numbers(stdin_text: str) -> str:
    """Add two reversed digit lists node by node with a carry.

    Parameters
    ----------
    stdin_text : str
        Two count-and-values sections holding reversed decimal digits.

    Returns
    -------
    str
        Sum digits in reverse order, space separated.
    """
    lines = split_input_lines(stdin_text)
    first_values, next_index = read_count_and_values(lines, 0)
    second_values, _ = read_count_and_values(lines, next_index)

    first_node = build_linked_list(first_values)
    second_node = build_linked_list(second_values)
    result_sentinel = ListNode(0)
    tail_node = result_sentinel
    carry = 0
    while first_node is not None or second_node is not None or carry > 0:
        column_total = carry
        if first_node is not None:
            column_total += first_node.value
            first_node = first_node.next_node
        if second_node is not None:
            column_total += second_node.value
            second_node = second_node.next_node
        carry, digit = divmod(column_total, 10)
        tail_node.next_node = ListNode(digit)
        tail_node = tail_node.next_node
    return format_value_line(collect_values(result_sentinel.next_node))


def brute_add_two_numbers(stdin_text: str) -> str:
    """Add two reversed digit lists by converting them to integers.

    Parameters
    ----------
    stdin_text : str
        Two count-and-values sections holding reversed decimal digits.

    Returns
    -------
    str
        Sum digits in reverse order, space separated.
    """
    lines = split_input_lines(stdin_text)
    first_values, next_index = read_count_and_values(lines, 0)
    second_values, _ = read_count_and_values(lines, next_index)

    first_number = int("".join(str(digit) for digit in reversed(first_values)))
    second_number = int("".join(str(digit) for digit in reversed(second_values)))
    total_digits = [int(character) for character in reversed(str(first_number + second_number))]
    return format_value_line(total_digits)


def solve_merge_two_sorted_lists(stdin_text: str) -> str:
    """Splice two sorted lists together by relinking nodes.

    Parameters
    ----------
    stdin_text : str
        Two count-and-values sections, each already sorted ascending.

    Returns
    -------
    str
        Merged values ascending, space separated.
    """
    lines = split_input_lines(stdin_text)
    first_values, next_index = read_count_and_values(lines, 0)
    second_values, _ = read_count_and_values(lines, next_index)

    first_node = build_linked_list(first_values)
    second_node = build_linked_list(second_values)
    merged_sentinel = ListNode(0)
    tail_node = merged_sentinel
    while first_node is not None and second_node is not None:
        if first_node.value <= second_node.value:
            tail_node.next_node = first_node
            first_node = first_node.next_node
        else:
            tail_node.next_node = second_node
            second_node = second_node.next_node
        tail_node = tail_node.next_node
    tail_node.next_node = first_node if first_node is not None else second_node
    return format_value_line(collect_values(merged_sentinel.next_node))


def brute_merge_two_sorted_lists(stdin_text: str) -> str:
    """Merge two sorted lists by concatenating and sorting the values.

    Parameters
    ----------
    stdin_text : str
        Two count-and-values sections, each already sorted ascending.

    Returns
    -------
    str
        Merged values ascending, space separated.
    """
    lines = split_input_lines(stdin_text)
    first_values, next_index = read_count_and_values(lines, 0)
    second_values, _ = read_count_and_values(lines, next_index)
    return format_value_line(sorted(first_values + second_values))


def solve_copy_list_with_random_pointer(stdin_text: str) -> str:
    """Deep copy a list with random pointers, then report the copy.

    Parameters
    ----------
    stdin_text : str
        Count line, values line, then the random target indices.

    Returns
    -------
    str
        One line per copied node holding its value and random index.
    """
    lines = split_input_lines(stdin_text)
    values, next_index = read_count_and_values(lines, 0)
    random_line = lines[next_index] if next_index < len(lines) else ""
    random_indices = [int(token) for token in random_line.split()][: len(values)]

    original_nodes = link_nodes_in_order(values)
    for position, random_index in enumerate(random_indices):
        if random_index >= 0:
            original_nodes[position].random_node = original_nodes[random_index]

    copies_by_original_id: dict[int, ListNode] = {}
    original_cursor: Optional[ListNode] = original_nodes[0]
    while original_cursor is not None:
        copies_by_original_id[id(original_cursor)] = ListNode(original_cursor.value)
        original_cursor = original_cursor.next_node

    original_cursor = original_nodes[0]
    while original_cursor is not None:
        copied_node = copies_by_original_id[id(original_cursor)]
        if original_cursor.next_node is not None:
            copied_node.next_node = copies_by_original_id[id(original_cursor.next_node)]
        if original_cursor.random_node is not None:
            copied_node.random_node = copies_by_original_id[id(original_cursor.random_node)]
        original_cursor = original_cursor.next_node

    copied_nodes: list[ListNode] = []
    copy_cursor: Optional[ListNode] = copies_by_original_id[id(original_nodes[0])]
    while copy_cursor is not None:
        copied_nodes.append(copy_cursor)
        copy_cursor = copy_cursor.next_node

    index_by_copy_id = {id(copied_node): position for position, copied_node in enumerate(copied_nodes)}
    output_lines: list[str] = []
    for copied_node in copied_nodes:
        random_target = -1
        if copied_node.random_node is not None:
            random_target = index_by_copy_id[id(copied_node.random_node)]
        output_lines.append(f"{copied_node.value} {random_target}")
    return "\n".join(output_lines)


def brute_copy_list_with_random_pointer(stdin_text: str) -> str:
    """Report the copied list straight from the parsed value and index arrays.

    Parameters
    ----------
    stdin_text : str
        Count line, values line, then the random target indices.

    Returns
    -------
    str
        One line per copied node holding its value and random index.
    """
    lines = split_input_lines(stdin_text)
    values, next_index = read_count_and_values(lines, 0)
    random_line = lines[next_index] if next_index < len(lines) else ""
    random_indices = [int(token) for token in random_line.split()][: len(values)]
    return "\n".join(
        f"{value} {random_index}" for value, random_index in zip(values, random_indices)
    )


def solve_reverse_linked_list_ii(stdin_text: str) -> str:
    """Reverse one stretch of a list by relinking its nodes in place.

    Parameters
    ----------
    stdin_text : str
        Count line, values line, then the 1-based left and right positions.

    Returns
    -------
    str
        Resulting values, space separated.
    """
    lines = split_input_lines(stdin_text)
    values, next_index = read_count_and_values(lines, 0)
    left_text, right_text = lines[next_index].split()
    left_position = int(left_text)
    right_position = int(right_text)

    head_sentinel = ListNode(0)
    head_sentinel.next_node = build_linked_list(values)
    node_before_segment = head_sentinel
    for _ in range(left_position - 1):
        if node_before_segment.next_node is None:
            break
        node_before_segment = node_before_segment.next_node

    segment_start = node_before_segment.next_node
    previous_node: Optional[ListNode] = None
    current_node = segment_start
    for _ in range(right_position - left_position + 1):
        if current_node is None:
            break
        following_node = current_node.next_node
        current_node.next_node = previous_node
        previous_node = current_node
        current_node = following_node

    node_before_segment.next_node = previous_node
    if segment_start is not None:
        segment_start.next_node = current_node
    return format_value_line(collect_values(head_sentinel.next_node))


def brute_reverse_linked_list_ii(stdin_text: str) -> str:
    """Reverse one stretch of a list with plain list slicing.

    Parameters
    ----------
    stdin_text : str
        Count line, values line, then the 1-based left and right positions.

    Returns
    -------
    str
        Resulting values, space separated.
    """
    lines = split_input_lines(stdin_text)
    values, next_index = read_count_and_values(lines, 0)
    left_text, right_text = lines[next_index].split()
    left_position = int(left_text)
    right_position = int(right_text)

    prefix = values[: left_position - 1]
    middle = values[left_position - 1 : right_position]
    suffix = values[right_position:]
    return format_value_line(prefix + middle[::-1] + suffix)


def solve_reverse_nodes_in_k_group(stdin_text: str) -> str:
    """Reverse every full group of k nodes by relinking them in place.

    Parameters
    ----------
    stdin_text : str
        Count line, values line, then the group size k.

    Returns
    -------
    str
        Resulting values, space separated.
    """
    lines = split_input_lines(stdin_text)
    values, next_index = read_count_and_values(lines, 0)
    group_size = int(lines[next_index].strip())

    head_sentinel = ListNode(0)
    head_sentinel.next_node = build_linked_list(values)
    node_before_group: ListNode = head_sentinel
    while True:
        group_end: Optional[ListNode] = node_before_group
        remaining_steps = group_size
        while remaining_steps > 0 and group_end is not None:
            group_end = group_end.next_node
            remaining_steps -= 1
        if group_end is None:
            break

        node_after_group = group_end.next_node
        previous_node: Optional[ListNode] = node_after_group
        current_node = node_before_group.next_node
        while current_node is not node_after_group and current_node is not None:
            following_node = current_node.next_node
            current_node.next_node = previous_node
            previous_node = current_node
            current_node = following_node

        new_node_before_group = node_before_group.next_node
        node_before_group.next_node = group_end
        if new_node_before_group is None:
            break
        node_before_group = new_node_before_group
    return format_value_line(collect_values(head_sentinel.next_node))


def brute_reverse_nodes_in_k_group(stdin_text: str) -> str:
    """Reverse every full group of k values by chunking a plain list.

    Parameters
    ----------
    stdin_text : str
        Count line, values line, then the group size k.

    Returns
    -------
    str
        Resulting values, space separated.
    """
    lines = split_input_lines(stdin_text)
    values, next_index = read_count_and_values(lines, 0)
    group_size = int(lines[next_index].strip())

    rearranged: list[int] = []
    for start in range(0, len(values), group_size):
        chunk = values[start : start + group_size]
        rearranged.extend(chunk[::-1] if len(chunk) == group_size else chunk)
    return format_value_line(rearranged)


def solve_remove_nth_node_from_end_of_list(stdin_text: str) -> str:
    """Drop the nth node counted from the end using two spaced walkers.

    Parameters
    ----------
    stdin_text : str
        Count line, values line, then the position n counted from the end.

    Returns
    -------
    str
        Remaining values, or the empty-list token.
    """
    lines = split_input_lines(stdin_text)
    values, next_index = read_count_and_values(lines, 0)
    position_from_end = int(lines[next_index].strip())

    head_sentinel = ListNode(0)
    head_sentinel.next_node = build_linked_list(values)
    leading_node: Optional[ListNode] = head_sentinel
    for _ in range(position_from_end):
        if leading_node is None:
            break
        leading_node = leading_node.next_node

    trailing_node = head_sentinel
    while leading_node is not None and leading_node.next_node is not None:
        leading_node = leading_node.next_node
        if trailing_node.next_node is None:
            break
        trailing_node = trailing_node.next_node

    doomed_node = trailing_node.next_node
    if doomed_node is not None:
        trailing_node.next_node = doomed_node.next_node
    return format_value_line(collect_values(head_sentinel.next_node))


def brute_remove_nth_node_from_end_of_list(stdin_text: str) -> str:
    """Drop the nth value counted from the end of a plain list.

    Parameters
    ----------
    stdin_text : str
        Count line, values line, then the position n counted from the end.

    Returns
    -------
    str
        Remaining values, or the empty-list token.
    """
    lines = split_input_lines(stdin_text)
    values, next_index = read_count_and_values(lines, 0)
    position_from_end = int(lines[next_index].strip())

    remaining = list(values)
    del remaining[len(remaining) - position_from_end]
    return format_value_line(remaining)


def solve_remove_duplicates_from_sorted_list_ii(stdin_text: str) -> str:
    """Drop every run of repeated values by skipping whole runs of nodes.

    Parameters
    ----------
    stdin_text : str
        Count line then the sorted values line.

    Returns
    -------
    str
        Remaining values, or the empty-list token.
    """
    lines = split_input_lines(stdin_text)
    values, _ = read_count_and_values(lines, 0)

    head_sentinel = ListNode(0)
    head_sentinel.next_node = build_linked_list(values)
    last_kept_node = head_sentinel
    current_node = head_sentinel.next_node
    while current_node is not None:
        run_end_node = current_node
        while run_end_node.next_node is not None and run_end_node.next_node.value == current_node.value:
            run_end_node = run_end_node.next_node
        if run_end_node is current_node:
            last_kept_node.next_node = current_node
            last_kept_node = current_node
        current_node = run_end_node.next_node
    last_kept_node.next_node = None
    return format_value_line(collect_values(head_sentinel.next_node))


def brute_remove_duplicates_from_sorted_list_ii(stdin_text: str) -> str:
    """Keep only the values that occur exactly once, counted on a plain list.

    Parameters
    ----------
    stdin_text : str
        Count line then the sorted values line.

    Returns
    -------
    str
        Remaining values, or the empty-list token.
    """
    lines = split_input_lines(stdin_text)
    values, _ = read_count_and_values(lines, 0)
    kept = [value for value in values if values.count(value) == 1]
    return format_value_line(kept)


def solve_rotate_list(stdin_text: str) -> str:
    """Rotate a list right by k by closing it into a ring and cutting it.

    Parameters
    ----------
    stdin_text : str
        Count line, values line, then the rotation amount k.

    Returns
    -------
    str
        Resulting values, space separated.
    """
    lines = split_input_lines(stdin_text)
    values, next_index = read_count_and_values(lines, 0)
    rotation_amount = int(lines[next_index].strip())

    head = build_linked_list(values)
    if head is None:
        return format_value_line([])

    length = 1
    tail_node = head
    while tail_node.next_node is not None:
        tail_node = tail_node.next_node
        length += 1

    effective_shift = rotation_amount % length
    if effective_shift == 0:
        return format_value_line(collect_values(head))

    new_tail_node = head
    for _ in range(length - effective_shift - 1):
        if new_tail_node.next_node is None:
            break
        new_tail_node = new_tail_node.next_node
    new_head = new_tail_node.next_node
    new_tail_node.next_node = None
    tail_node.next_node = head
    return format_value_line(collect_values(new_head))


def brute_rotate_list(stdin_text: str) -> str:
    """Rotate a plain list right by k with slicing.

    Parameters
    ----------
    stdin_text : str
        Count line, values line, then the rotation amount k.

    Returns
    -------
    str
        Resulting values, space separated.
    """
    lines = split_input_lines(stdin_text)
    values, next_index = read_count_and_values(lines, 0)
    rotation_amount = int(lines[next_index].strip())

    if not values:
        return format_value_line([])
    cut_point = len(values) - rotation_amount % len(values)
    return format_value_line(values[cut_point:] + values[:cut_point])


def solve_partition_list(stdin_text: str) -> str:
    """Split a list around x by building two node chains and joining them.

    Parameters
    ----------
    stdin_text : str
        Count line, values line, then the pivot value x.

    Returns
    -------
    str
        Resulting values, space separated.
    """
    lines = split_input_lines(stdin_text)
    values, next_index = read_count_and_values(lines, 0)
    pivot_value = int(lines[next_index].strip())

    smaller_sentinel = ListNode(0)
    smaller_tail = smaller_sentinel
    larger_sentinel = ListNode(0)
    larger_tail = larger_sentinel
    current_node = build_linked_list(values)
    while current_node is not None:
        following_node = current_node.next_node
        current_node.next_node = None
        if current_node.value < pivot_value:
            smaller_tail.next_node = current_node
            smaller_tail = current_node
        else:
            larger_tail.next_node = current_node
            larger_tail = current_node
        current_node = following_node
    smaller_tail.next_node = larger_sentinel.next_node
    return format_value_line(collect_values(smaller_sentinel.next_node))


def brute_partition_list(stdin_text: str) -> str:
    """Split a plain list around x with two order-preserving passes.

    Parameters
    ----------
    stdin_text : str
        Count line, values line, then the pivot value x.

    Returns
    -------
    str
        Resulting values, space separated.
    """
    lines = split_input_lines(stdin_text)
    values, next_index = read_count_and_values(lines, 0)
    pivot_value = int(lines[next_index].strip())

    smaller = [value for value in values if value < pivot_value]
    larger = [value for value in values if value >= pivot_value]
    return format_value_line(smaller + larger)


def solve_lru_cache(stdin_text: str) -> str:
    """Replay cache operations against a dict plus a recency linked list.

    Parameters
    ----------
    stdin_text : str
        Capacity and operation count, then one operation per line.

    Returns
    -------
    str
        One line per get operation.
    """
    lines = split_input_lines(stdin_text)
    capacity_text, operation_count_text = lines[0].split()
    cache = LeastRecentlyUsedCache(int(capacity_text))
    operation_count = int(operation_count_text)

    output_lines: list[str] = []
    for operation_line in lines[1 : 1 + operation_count]:
        tokens = operation_line.split()
        if tokens[0] == "get":
            output_lines.append(str(cache.get(int(tokens[1]))))
        else:
            cache.put(int(tokens[1]), int(tokens[2]))
    return "\n".join(output_lines)


def brute_lru_cache(stdin_text: str) -> str:
    """Replay cache operations against a dict plus a scanned recency list.

    Parameters
    ----------
    stdin_text : str
        Capacity and operation count, then one operation per line.

    Returns
    -------
    str
        One line per get operation.
    """
    lines = split_input_lines(stdin_text)
    capacity_text, operation_count_text = lines[0].split()
    capacity = int(capacity_text)
    operation_count = int(operation_count_text)

    values_by_key: dict[int, int] = {}
    recency_order: list[int] = []
    output_lines: list[str] = []
    for operation_line in lines[1 : 1 + operation_count]:
        tokens = operation_line.split()
        key = int(tokens[1])
        if tokens[0] == "get":
            if key not in values_by_key:
                output_lines.append("-1")
                continue
            recency_order.remove(key)
            recency_order.append(key)
            output_lines.append(str(values_by_key[key]))
            continue
        if key in values_by_key:
            recency_order.remove(key)
        elif len(values_by_key) >= capacity:
            del values_by_key[recency_order.pop(0)]
        values_by_key[key] = int(tokens[2])
        recency_order.append(key)
    return "\n".join(output_lines)


PROBLEMS: list[dict[str, Any]] = [
    {
        "title": "Linked List Cycle",
        "level": "Easy",
        "topics": "Linked List, Two Pointers, Hash Table",
        "companies": "Amazon, Microsoft, Bloomberg, Adobe",
        "description": """Decide whether a singly linked list loops back on itself. You are given the
node values in order plus the index of the node that the last node points at,
so you build the list yourself and then report whether walking it forever would
ever revisit a node.

Input, read from standard input:

1. A line with one integer `n`, the number of nodes.
2. A line with `n` space-separated integers, the node values in order.
3. A line with one integer `pos`: the 0-based index of the node that the last
   node links to, or `-1` when the last node links to nothing.

Output, written to standard output: a single line holding `true` when the list
contains a cycle, or `false` when it does not.

""",
        "examples": """```
Input
4
3 2 0 -4
1

Output
true
```

```
Input
5
1 2 3 4 5
-1

Output
false
```

```
Input
1
7
0

Output
true
```

""",
        "constraints": """- `1 <= n <= 10000`
- `-100000 <= value <= 100000`
- `pos` is `-1`, or an integer in `[0, n - 1]`

""",
        "inputs": [
            "4\n3 2 0 -4\n1",
            "2\n1 2\n0",
            "1\n1\n-1",
            "5\n1 2 3 4 5\n-1",
            "1\n7\n0",
            "3\n1 2 3\n2",
        ],
        "solve": solve_linked_list_cycle,
        "brute": brute_linked_list_cycle,
    },
    {
        "title": "Add Two Numbers",
        "level": "Medium",
        "topics": "Linked List, Math, Recursion",
        "companies": "Amazon, Microsoft, Bloomberg, Apple, Meta",
        "description": """Two non-negative integers are stored one decimal digit per node, with the
least significant digit first. Add them and report the sum stored the same way.

Input, read from standard input:

1. A line with one integer `n1`, the number of digits in the first number.
2. A line with `n1` space-separated digits of the first number, least
   significant digit first.
3. A line with one integer `n2`, the number of digits in the second number.
4. A line with `n2` space-separated digits of the second number, least
   significant digit first.

Output, written to standard output: a single line with the digits of the sum,
space separated, least significant digit first. The sum carries no leading
zeros, which means its last printed digit is never `0` unless the sum is `0`.

""",
        "examples": """```
Input
3
2 4 3
3
5 6 4

Output
7 0 8
```

```
Input
7
9 9 9 9 9 9 9
4
9 9 9 9

Output
8 9 9 9 0 0 0 1
```

```
Input
1
0
1
0

Output
0
```

""",
        "constraints": """- `1 <= n1, n2 <= 100`
- Every digit is in `[0, 9]`
- Neither number has a leading zero, except the number `0` itself

""",
        "inputs": [
            "3\n2 4 3\n3\n5 6 4",
            "1\n0\n1\n0",
            "7\n9 9 9 9 9 9 9\n4\n9 9 9 9",
            "1\n5\n1\n5",
            "4\n1 2 3 4\n1\n9",
            "3\n9 9 9\n1\n1",
        ],
        "solve": solve_add_two_numbers,
        "brute": brute_add_two_numbers,
    },
    {
        "title": "Merge Two Sorted Lists",
        "level": "Easy",
        "topics": "Linked List, Two Pointers, Recursion",
        "companies": "Amazon, Microsoft, Apple, Adobe",
        "description": """Two sorted lists of integers arrive separately. Combine them into one list
that is still sorted from smallest to largest, keeping every value, duplicates
included.

Input, read from standard input:

1. A line with one integer `n1`, the length of the first list.
2. A line with `n1` space-separated integers in non-decreasing order. The line
   is blank when `n1` is `0`.
3. A line with one integer `n2`, the length of the second list.
4. A line with `n2` space-separated integers in non-decreasing order. The line
   is blank when `n2` is `0`.

Output, written to standard output: a single line with every value in
non-decreasing order, space separated.

""",
        "examples": """```
Input
3
1 2 4
3
1 3 4

Output
1 1 2 3 4 4
```

```
Input
0

1
0

Output
0
```

```
Input
4
-10 -3 0 5
2
-7 9

Output
-10 -7 -3 0 5 9
```

""",
        "constraints": """- `0 <= n1, n2 <= 1000`
- `n1 + n2 >= 1`, so the answer is never an empty line
- `-1000 <= value <= 1000`
- Each input list is already sorted in non-decreasing order

""",
        "inputs": [
            "3\n1 2 4\n3\n1 3 4",
            "0\n\n1\n0",
            "1\n5\n1\n5",
            "4\n-10 -3 0 5\n2\n-7 9",
            "2\n1 100\n3\n2 3 4",
        ],
        "solve": solve_merge_two_sorted_lists,
        "brute": brute_merge_two_sorted_lists,
    },
    {
        "title": "Copy List with Random Pointer",
        "level": "Medium",
        "topics": "Linked List, Hash Table",
        "companies": "Amazon, Microsoft, Bloomberg, Meta",
        "description": """Every node of a list holds a value, a link to the next node, and a second
"random" link that may point at any node of the same list or at nothing. Build a
completely separate copy of the list: fresh nodes only, with the same values and
the same shape of links, and leave the original list untouched.

Input, read from standard input:

1. A line with one integer `n`, the number of nodes.
2. A line with `n` space-separated integers, the node values in order.
3. A line with `n` space-separated integers, the random targets. Entry `i` is
   the 0-based index of the node that node `i` points at with its random link,
   or `-1` when that link points at nothing.

Output, written to standard output: `n` lines, one per node of the copied list
in order. Each line holds the node's value, a single space, and the 0-based
index inside the copied list of the node its random link points at, or `-1`
when it points at nothing.

""",
        "examples": """```
Input
5
7 13 11 10 1
-1 0 4 2 0

Output
7 -1
13 0
11 4
10 2
1 0
```

```
Input
2
1 2
1 1

Output
1 1
2 1
```

```
Input
1
1
-1

Output
1 -1
```

""",
        "constraints": """- `1 <= n <= 1000`
- `-10000 <= value <= 10000`
- Each random target is `-1`, or an integer in `[0, n - 1]`

""",
        "inputs": [
            "5\n7 13 11 10 1\n-1 0 4 2 0",
            "1\n1\n-1",
            "1\n3\n0",
            "2\n1 2\n1 1",
            "3\n-1 -2 -3\n-1 -1 -1",
            "4\n5 5 5 5\n3 2 1 0",
        ],
        "solve": solve_copy_list_with_random_pointer,
        "brute": brute_copy_list_with_random_pointer,
    },
    {
        "title": "Reverse Linked List II",
        "level": "Medium",
        "topics": "Linked List, Two Pointers",
        "companies": "Amazon, Microsoft, Bloomberg, Uber",
        "description": """Reverse one stretch of a list and leave the rest alone. The stretch runs from
position `left` to position `right`, counting positions from `1` at the front of
the list, and both ends are included.

Input, read from standard input:

1. A line with one integer `n`, the number of nodes.
2. A line with `n` space-separated integers, the node values in order.
3. A line with two space-separated integers `left` and `right`.

Output, written to standard output: a single line with the values of the
resulting list in order, space separated.

""",
        "examples": """```
Input
5
1 2 3 4 5
2 4

Output
1 4 3 2 5
```

```
Input
6
10 20 30 40 50 60
1 3

Output
30 20 10 40 50 60
```

```
Input
4
1 2 3 4
3 3

Output
1 2 3 4
```

""",
        "constraints": """- `1 <= n <= 500`
- `-500 <= value <= 500`
- `1 <= left <= right <= n`

""",
        "inputs": [
            "5\n1 2 3 4 5\n2 4",
            "1\n5\n1 1",
            "5\n1 2 3 4 5\n1 5",
            "4\n1 2 3 4\n3 3",
            "6\n10 20 30 40 50 60\n1 3",
            "3\n1 2 3\n2 3",
        ],
        "solve": solve_reverse_linked_list_ii,
        "brute": brute_reverse_linked_list_ii,
    },
    {
        "title": "Reverse Nodes in k-Group",
        "level": "Hard",
        "topics": "Linked List, Recursion",
        "companies": "Amazon, Microsoft, Meta, Google",
        "description": """Walk a list from the front and reverse the nodes `k` at a time. If fewer than
`k` nodes are left at the end, that final short run stays in its original order.

Input, read from standard input:

1. A line with one integer `n`, the number of nodes.
2. A line with `n` space-separated integers, the node values in order.
3. A line with one integer `k`, the group size.

Output, written to standard output: a single line with the values of the
resulting list in order, space separated.

""",
        "examples": """```
Input
5
1 2 3 4 5
2

Output
2 1 4 3 5
```

```
Input
5
1 2 3 4 5
3

Output
3 2 1 4 5
```

```
Input
7
1 2 3 4 5 6 7
5

Output
5 4 3 2 1 6 7
```

""",
        "constraints": """- `1 <= n <= 5000`
- `0 <= value <= 1000`
- `1 <= k <= n`

""",
        "inputs": [
            "5\n1 2 3 4 5\n2",
            "5\n1 2 3 4 5\n3",
            "4\n1 2 3 4\n4",
            "1\n1\n1",
            "6\n1 2 3 4 5 6\n1",
            "7\n1 2 3 4 5 6 7\n5",
        ],
        "solve": solve_reverse_nodes_in_k_group,
        "brute": brute_reverse_nodes_in_k_group,
    },
    {
        "title": "Remove Nth Node From End of List",
        "level": "Medium",
        "topics": "Linked List, Two Pointers",
        "companies": "Amazon, Microsoft, Bloomberg, Meta",
        "description": """Delete one node from a list, named by its distance from the back: `nth` equal
to `1` means the last node, `2` means the one before it, and so on.

Input, read from standard input:

1. A line with one integer `n`, the number of nodes.
2. A line with `n` space-separated integers, the node values in order.
3. A line with one integer `nth`, the position counted from the end.

Output, written to standard output: a single line with the values of the
resulting list in order, space separated. When the deletion leaves no nodes at
all, print the single word `empty` instead.

""",
        "examples": """```
Input
5
1 2 3 4 5
2

Output
1 2 3 5
```

```
Input
1
1
1

Output
empty
```

```
Input
4
9 8 7 6
4

Output
8 7 6
```

""",
        "constraints": """- `1 <= n <= 1000`
- `-1000 <= value <= 1000`
- `1 <= nth <= n`

""",
        "inputs": [
            "5\n1 2 3 4 5\n2",
            "1\n1\n1",
            "2\n1 2\n1",
            "2\n1 2\n2",
            "4\n9 8 7 6\n4",
            "3\n1 2 3\n3",
        ],
        "solve": solve_remove_nth_node_from_end_of_list,
        "brute": brute_remove_nth_node_from_end_of_list,
    },
    {
        "title": "Remove Duplicates from Sorted List II",
        "level": "Medium",
        "topics": "Linked List, Two Pointers",
        "companies": "Amazon, Microsoft, Bloomberg, Adobe",
        "description": """A sorted list may hold repeated values. Delete every value that appears more
than once, keeping only the values that appear exactly once, in their original
order.

Input, read from standard input:

1. A line with one integer `n`, the number of nodes.
2. A line with `n` space-separated integers in non-decreasing order.

Output, written to standard output: a single line with the remaining values in
order, space separated. When nothing remains, print the single word `empty`
instead.

""",
        "examples": """```
Input
7
1 2 3 3 4 4 5

Output
1 2 5
```

```
Input
4
1 1 2 2

Output
empty
```

```
Input
6
-3 -3 -1 0 0 2

Output
-1 2
```

""",
        "constraints": """- `1 <= n <= 1000`
- `-1000 <= value <= 1000`
- The input values are already sorted in non-decreasing order

""",
        "inputs": [
            "7\n1 2 3 3 4 4 5",
            "3\n1 1 2",
            "1\n1",
            "4\n1 1 2 2",
            "6\n-3 -3 -1 0 0 2",
            "5\n1 2 3 4 5",
        ],
        "solve": solve_remove_duplicates_from_sorted_list_ii,
        "brute": brute_remove_duplicates_from_sorted_list_ii,
    },
    {
        "title": "Rotate List",
        "level": "Medium",
        "topics": "Linked List, Two Pointers, Math",
        "companies": "Amazon, Microsoft, LinkedIn, Bloomberg",
        "description": """Shift every node of a list `k` places towards the back, wrapping the nodes
that fall off the end around to the front. `k` may be `0`, and it may be larger
than the list itself.

Input, read from standard input:

1. A line with one integer `n`, the number of nodes.
2. A line with `n` space-separated integers, the node values in order.
3. A line with one integer `k`, the number of places to shift.

Output, written to standard output: a single line with the values of the
resulting list in order, space separated.

""",
        "examples": """```
Input
5
1 2 3 4 5
2

Output
4 5 1 2 3
```

```
Input
3
0 1 2
4

Output
2 0 1
```

```
Input
4
1 2 3 4
4

Output
1 2 3 4
```

""",
        "constraints": """- `1 <= n <= 500`
- `-1000 <= value <= 1000`
- `0 <= k <= 1000000000`

""",
        "inputs": [
            "5\n1 2 3 4 5\n2",
            "3\n0 1 2\n4",
            "1\n1\n0",
            "4\n1 2 3 4\n4",
            "4\n1 2 3 4\n0",
            "6\n1 2 3 4 5 6\n13",
        ],
        "solve": solve_rotate_list,
        "brute": brute_rotate_list,
    },
    {
        "title": "Partition List",
        "level": "Medium",
        "topics": "Linked List, Two Pointers",
        "companies": "Amazon, Microsoft, Bloomberg, Uber",
        "description": """Rearrange a list around a pivot value `x`: every node whose value is smaller
than `x` must come before every node whose value is `x` or larger. Inside each
of those two halves the nodes keep the order they had in the input.

Input, read from standard input:

1. A line with one integer `n`, the number of nodes.
2. A line with `n` space-separated integers, the node values in order.
3. A line with one integer `x`, the pivot value.

Output, written to standard output: a single line with the values of the
resulting list in order, space separated.

""",
        "examples": """```
Input
6
1 4 3 2 5 2
3

Output
1 2 2 4 3 5
```

```
Input
4
4 3 2 1
3

Output
2 1 4 3
```

```
Input
5
5 5 5 5 5
5

Output
5 5 5 5 5
```

""",
        "constraints": """- `1 <= n <= 200`
- `-100 <= value <= 100`
- `-200 <= x <= 200`

""",
        "inputs": [
            "6\n1 4 3 2 5 2\n3",
            "2\n2 1\n2",
            "1\n1\n0",
            "5\n5 5 5 5 5\n5",
            "5\n1 2 3 4 5\n10",
            "4\n4 3 2 1\n3",
        ],
        "solve": solve_partition_list,
        "brute": brute_partition_list,
    },
    {
        "title": "LRU Cache",
        "level": "Medium",
        "topics": "Linked List, Hash Table, Design, Doubly-Linked List",
        "companies": "Amazon, Microsoft, Bloomberg, Google, Meta",
        "description": """Run a cache that holds at most `capacity` keys. Reading a key and writing a
key both count as using it. When a write would push the cache past its capacity,
the key that was used longest ago is thrown out first.

Input, read from standard input:

1. A line with two space-separated integers `capacity` and `q`, the cache size
   and the number of operations.
2. `q` lines, each one of:
   - `put key value` — store `value` under `key`, replacing any earlier value.
   - `get key` — read the value stored under `key`.

Output, written to standard output: one line per `get` operation, in the order
those operations appear, holding the stored value, or `-1` when the key is not
in the cache. Every input contains at least one `get`.

""",
        "examples": """```
Input
2 8
put 1 1
put 2 2
get 1
put 3 3
get 2
put 4 4
get 1
get 3

Output
1
-1
-1
3
```

```
Input
1 4
put 1 10
get 1
put 2 20
get 1

Output
10
-1
```

```
Input
3 7
put 1 1
put 2 2
put 3 3
put 1 100
get 1
get 2
get 3

Output
100
2
3
```

""",
        "constraints": """- `1 <= capacity <= 3000`
- `1 <= q <= 20000`, with at least one `get`
- `0 <= key <= 100000`
- `0 <= value <= 1000000`

""",
        "inputs": [
            "2 8\nput 1 1\nput 2 2\nget 1\nput 3 3\nget 2\nput 4 4\nget 1\nget 3",
            "1 4\nput 1 10\nget 1\nput 2 20\nget 1",
            "2 4\nget 1\nput 1 5\nget 1\nget 2",
            "3 7\nput 1 1\nput 2 2\nput 3 3\nput 1 100\nget 1\nget 2\nget 3",
            "2 6\nput 1 1\nput 2 2\nput 1 11\nput 3 3\nget 1\nget 2",
            "1 3\nput 5 50\nput 5 60\nget 5",
        ],
        "solve": solve_lru_cache,
        "brute": brute_lru_cache,
    },
]
