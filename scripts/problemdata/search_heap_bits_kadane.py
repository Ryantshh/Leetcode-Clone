"""Problem specs for the binary search, heap, bit manipulation and Kadane group.

Every solver reads a whole stdin payload as a single string and returns the exact
stdout text the judge compares against.
"""

from __future__ import annotations

import heapq
import math
from collections import Counter

UNSIGNED_32_BIT_WIDTH = 32
UNSIGNED_32_BIT_MASK = (1 << UNSIGNED_32_BIT_WIDTH) - 1


def read_lines(stdin_text: str) -> list[str]:
    """Split a stdin payload into individual lines with surrounding spaces removed.

    Parameters
    ----------
    stdin_text : str
        Whole stdin payload.

    Returns
    -------
    list[str]
        One entry per line.
    """
    return [line.strip() for line in stdin_text.strip().split("\n")]


def read_integers(line: str) -> list[int]:
    """Parse a whitespace separated line of integers.

    Parameters
    ----------
    line : str
        Line holding zero or more integers.

    Returns
    -------
    list[int]
        Parsed integers in their original order.
    """
    return [int(token) for token in line.split()]


# ---------------------------------------------------------------------------
# Maximum Subarray
# ---------------------------------------------------------------------------


def solve_maximum_subarray(stdin_text: str) -> str:
    """Return the largest sum of a contiguous non-empty subarray via Kadane's scan.

    Parameters
    ----------
    stdin_text : str
        Count line followed by the values line.

    Returns
    -------
    str
        The maximum subarray sum.
    """
    lines = read_lines(stdin_text)
    values = read_integers(lines[1])
    best_total = values[0]
    running_total = values[0]
    for value in values[1:]:
        running_total = max(value, running_total + value)
        best_total = max(best_total, running_total)
    return str(best_total)


def brute_maximum_subarray(stdin_text: str) -> str:
    """Return the largest contiguous subarray sum by checking every start and end.

    Parameters
    ----------
    stdin_text : str
        Count line followed by the values line.

    Returns
    -------
    str
        The maximum subarray sum.
    """
    lines = read_lines(stdin_text)
    values = read_integers(lines[1])
    best_total = values[0]
    for start_index in range(len(values)):
        window_total = 0
        for end_index in range(start_index, len(values)):
            window_total += values[end_index]
            if window_total > best_total:
                best_total = window_total
    return str(best_total)


# ---------------------------------------------------------------------------
# Maximum Sum Circular Subarray
# ---------------------------------------------------------------------------


def solve_maximum_sum_circular_subarray(stdin_text: str) -> str:
    """Return the largest circular subarray sum from the best and worst linear runs.

    Parameters
    ----------
    stdin_text : str
        Count line followed by the values line.

    Returns
    -------
    str
        The maximum circular subarray sum.
    """
    lines = read_lines(stdin_text)
    values = read_integers(lines[1])
    best_total = values[0]
    worst_total = values[0]
    running_best = values[0]
    running_worst = values[0]
    for value in values[1:]:
        running_best = max(value, running_best + value)
        best_total = max(best_total, running_best)
        running_worst = min(value, running_worst + value)
        worst_total = min(worst_total, running_worst)
    # A wrapping window is the complement of the worst run, which is empty when
    # every value is negative.
    if best_total < 0:
        return str(best_total)
    wrapping_total = sum(values) - worst_total
    return str(max(best_total, wrapping_total))


def brute_maximum_sum_circular_subarray(stdin_text: str) -> str:
    """Return the largest circular subarray sum by summing every start and length.

    Parameters
    ----------
    stdin_text : str
        Count line followed by the values line.

    Returns
    -------
    str
        The maximum circular subarray sum.
    """
    lines = read_lines(stdin_text)
    values = read_integers(lines[1])
    count = len(values)
    best_total = values[0]
    for start_index in range(count):
        window_total = 0
        for offset in range(count):
            window_total += values[(start_index + offset) % count]
            if window_total > best_total:
                best_total = window_total
    return str(best_total)


# ---------------------------------------------------------------------------
# Search Insert Position
# ---------------------------------------------------------------------------


def solve_search_insert_position(stdin_text: str) -> str:
    """Return the index of the target, or its insertion point, by binary search.

    Parameters
    ----------
    stdin_text : str
        Count line, sorted values line, target line.

    Returns
    -------
    str
        Index at which the target is or would be placed.
    """
    lines = read_lines(stdin_text)
    values = read_integers(lines[1])
    target = int(lines[2])
    low_index = 0
    high_index = len(values)
    while low_index < high_index:
        middle_index = (low_index + high_index) // 2
        if values[middle_index] < target:
            low_index = middle_index + 1
        else:
            high_index = middle_index
    return str(low_index)


def brute_search_insert_position(stdin_text: str) -> str:
    """Return the insertion index for the target by walking the values in order.

    Parameters
    ----------
    stdin_text : str
        Count line, sorted values line, target line.

    Returns
    -------
    str
        Index at which the target is or would be placed.
    """
    lines = read_lines(stdin_text)
    values = read_integers(lines[1])
    target = int(lines[2])
    for index, value in enumerate(values):
        if value >= target:
            return str(index)
    return str(len(values))


# ---------------------------------------------------------------------------
# Search a 2D Matrix
# ---------------------------------------------------------------------------


def solve_search_a_2d_matrix(stdin_text: str) -> str:
    """Report whether the target sits in the matrix, searching it as one sorted run.

    Parameters
    ----------
    stdin_text : str
        Dimensions line, the matrix rows, then the target line.

    Returns
    -------
    str
        "true" when the target is present, otherwise "false".
    """
    lines = read_lines(stdin_text)
    row_count, column_count = read_integers(lines[0])
    rows = [read_integers(lines[1 + row_index]) for row_index in range(row_count)]
    target = int(lines[1 + row_count])
    low_index = 0
    high_index = row_count * column_count - 1
    while low_index <= high_index:
        middle_index = (low_index + high_index) // 2
        middle_value = rows[middle_index // column_count][middle_index % column_count]
        if middle_value == target:
            return "true"
        if middle_value < target:
            low_index = middle_index + 1
        else:
            high_index = middle_index - 1
    return "false"


def brute_search_a_2d_matrix(stdin_text: str) -> str:
    """Report whether the target sits in the matrix by inspecting every cell.

    Parameters
    ----------
    stdin_text : str
        Dimensions line, the matrix rows, then the target line.

    Returns
    -------
    str
        "true" when the target is present, otherwise "false".
    """
    lines = read_lines(stdin_text)
    row_count, _ = read_integers(lines[0])
    target = int(lines[1 + row_count])
    for row_index in range(row_count):
        for value in read_integers(lines[1 + row_index]):
            if value == target:
                return "true"
    return "false"


# ---------------------------------------------------------------------------
# Find Peak Element
# ---------------------------------------------------------------------------


def solve_find_peak_element(stdin_text: str) -> str:
    """Return the smallest peak index as the end of the first ascending run.

    Parameters
    ----------
    stdin_text : str
        Count line followed by the values line.

    Returns
    -------
    str
        Smallest index whose value exceeds both neighbours.
    """
    lines = read_lines(stdin_text)
    values = read_integers(lines[1])
    count = len(values)
    peak_index = 0
    while peak_index + 1 < count and values[peak_index] < values[peak_index + 1]:
        peak_index += 1
    return str(peak_index)


def brute_find_peak_element(stdin_text: str) -> str:
    """Return the smallest peak index by testing every index against padded edges.

    Parameters
    ----------
    stdin_text : str
        Count line followed by the values line.

    Returns
    -------
    str
        Smallest index whose value exceeds both neighbours.
    """
    lines = read_lines(stdin_text)
    values = read_integers(lines[1])
    padded = [-math.inf, *values, -math.inf]
    peak_indices = [
        index
        for index in range(len(values))
        if padded[index] < padded[index + 1] > padded[index + 2]
    ]
    return str(min(peak_indices))


# ---------------------------------------------------------------------------
# Search in Rotated Sorted Array
# ---------------------------------------------------------------------------


def solve_search_in_rotated_sorted_array(stdin_text: str) -> str:
    """Locate the target in a rotated sorted array with a single binary search.

    Parameters
    ----------
    stdin_text : str
        Count line, values line, target line.

    Returns
    -------
    str
        Index of the target, or "-1" when it is absent.
    """
    lines = read_lines(stdin_text)
    values = read_integers(lines[1])
    target = int(lines[2])
    low_index = 0
    high_index = len(values) - 1
    while low_index <= high_index:
        middle_index = (low_index + high_index) // 2
        if values[middle_index] == target:
            return str(middle_index)
        is_left_half_sorted = values[low_index] <= values[middle_index]
        if is_left_half_sorted:
            is_target_in_left_half = values[low_index] <= target < values[middle_index]
            if is_target_in_left_half:
                high_index = middle_index - 1
            else:
                low_index = middle_index + 1
        else:
            is_target_in_right_half = values[middle_index] < target <= values[high_index]
            if is_target_in_right_half:
                low_index = middle_index + 1
            else:
                high_index = middle_index - 1
    return "-1"


def brute_search_in_rotated_sorted_array(stdin_text: str) -> str:
    """Locate the target in a rotated sorted array by scanning every position.

    Parameters
    ----------
    stdin_text : str
        Count line, values line, target line.

    Returns
    -------
    str
        Index of the target, or "-1" when it is absent.
    """
    lines = read_lines(stdin_text)
    values = read_integers(lines[1])
    target = int(lines[2])
    for index, value in enumerate(values):
        if value == target:
            return str(index)
    return "-1"


# ---------------------------------------------------------------------------
# Find First and Last Position of Element in Sorted Array
# ---------------------------------------------------------------------------


def solve_find_first_and_last_position_of_element_in_sorted_array(stdin_text: str) -> str:
    """Return the target's first and last index using two boundary binary searches.

    Parameters
    ----------
    stdin_text : str
        Count line, sorted values line, target line.

    Returns
    -------
    str
        First and last index separated by a space, or "-1 -1" when absent.
    """
    lines = read_lines(stdin_text)
    values = read_integers(lines[1])
    target = int(lines[2])
    count = len(values)

    low_index, high_index = 0, count
    while low_index < high_index:
        middle_index = (low_index + high_index) // 2
        if values[middle_index] < target:
            low_index = middle_index + 1
        else:
            high_index = middle_index
    first_index = low_index

    low_index, high_index = 0, count
    while low_index < high_index:
        middle_index = (low_index + high_index) // 2
        if values[middle_index] <= target:
            low_index = middle_index + 1
        else:
            high_index = middle_index
    last_index = low_index - 1

    if first_index > last_index:
        return "-1 -1"
    return f"{first_index} {last_index}"


def brute_find_first_and_last_position_of_element_in_sorted_array(stdin_text: str) -> str:
    """Return the target's first and last index by collecting every matching index.

    Parameters
    ----------
    stdin_text : str
        Count line, sorted values line, target line.

    Returns
    -------
    str
        First and last index separated by a space, or "-1 -1" when absent.
    """
    lines = read_lines(stdin_text)
    values = read_integers(lines[1])
    target = int(lines[2])
    matching_indices = [index for index, value in enumerate(values) if value == target]
    if not matching_indices:
        return "-1 -1"
    return f"{matching_indices[0]} {matching_indices[-1]}"


# ---------------------------------------------------------------------------
# Find Minimum in Rotated Sorted Array
# ---------------------------------------------------------------------------


def solve_find_minimum_in_rotated_sorted_array(stdin_text: str) -> str:
    """Return the smallest value of a rotated sorted array by binary search.

    Parameters
    ----------
    stdin_text : str
        Count line followed by the values line.

    Returns
    -------
    str
        The smallest value.
    """
    lines = read_lines(stdin_text)
    values = read_integers(lines[1])
    low_index = 0
    high_index = len(values) - 1
    while low_index < high_index:
        middle_index = (low_index + high_index) // 2
        if values[middle_index] > values[high_index]:
            low_index = middle_index + 1
        else:
            high_index = middle_index
    return str(values[low_index])


def brute_find_minimum_in_rotated_sorted_array(stdin_text: str) -> str:
    """Return the smallest value of a rotated sorted array by a full scan.

    Parameters
    ----------
    stdin_text : str
        Count line followed by the values line.

    Returns
    -------
    str
        The smallest value.
    """
    lines = read_lines(stdin_text)
    values = read_integers(lines[1])
    smallest_value = values[0]
    for value in values:
        if value < smallest_value:
            smallest_value = value
    return str(smallest_value)


# ---------------------------------------------------------------------------
# Median of Two Sorted Arrays
# ---------------------------------------------------------------------------


def solve_median_of_two_sorted_arrays(stdin_text: str) -> str:
    """Return the median of two sorted arrays by binary searching the split point.

    Parameters
    ----------
    stdin_text : str
        First count line, first values line, second count line, second values line.

    Returns
    -------
    str
        The median rounded to five decimal places.

    Raises
    ------
    ValueError
        If no valid split exists, which means an input array is not sorted.
    """
    lines = read_lines(stdin_text)
    shorter = read_integers(lines[1])
    longer = read_integers(lines[3])
    if len(shorter) > len(longer):
        shorter, longer = longer, shorter
    shorter_length = len(shorter)
    longer_length = len(longer)
    total_length = shorter_length + longer_length
    left_half_size = (total_length + 1) // 2

    low_count = 0
    high_count = shorter_length
    while low_count <= high_count:
        taken_from_shorter = (low_count + high_count) // 2
        taken_from_longer = left_half_size - taken_from_shorter
        shorter_left = shorter[taken_from_shorter - 1] if taken_from_shorter > 0 else -math.inf
        shorter_right = (
            shorter[taken_from_shorter] if taken_from_shorter < shorter_length else math.inf
        )
        longer_left = longer[taken_from_longer - 1] if taken_from_longer > 0 else -math.inf
        longer_right = longer[taken_from_longer] if taken_from_longer < longer_length else math.inf
        is_split_valid = shorter_left <= longer_right and longer_left <= shorter_right
        if is_split_valid:
            left_maximum = max(shorter_left, longer_left)
            if total_length % 2 == 1:
                return f"{float(left_maximum):.5f}"
            right_minimum = min(shorter_right, longer_right)
            return f"{(left_maximum + right_minimum) / 2:.5f}"
        if shorter_left > longer_right:
            high_count = taken_from_shorter - 1
        else:
            low_count = taken_from_shorter + 1
    raise ValueError("no valid split found; input arrays must be sorted")


def brute_median_of_two_sorted_arrays(stdin_text: str) -> str:
    """Return the median of two sorted arrays by merging them completely.

    Parameters
    ----------
    stdin_text : str
        First count line, first values line, second count line, second values line.

    Returns
    -------
    str
        The median rounded to five decimal places.
    """
    lines = read_lines(stdin_text)
    merged = sorted(read_integers(lines[1]) + read_integers(lines[3]))
    middle_index = len(merged) // 2
    if len(merged) % 2 == 1:
        return f"{float(merged[middle_index]):.5f}"
    return f"{(merged[middle_index - 1] + merged[middle_index]) / 2:.5f}"


# ---------------------------------------------------------------------------
# Kth Largest Element in an Array
# ---------------------------------------------------------------------------


def solve_kth_largest_element_in_an_array(stdin_text: str) -> str:
    """Return the kth largest value using a bounded min-heap of the top k values.

    Parameters
    ----------
    stdin_text : str
        Count line, values line, k line.

    Returns
    -------
    str
        The kth largest value.
    """
    lines = read_lines(stdin_text)
    values = read_integers(lines[1])
    wanted_rank = int(lines[2])
    top_values: list[int] = []
    for value in values:
        heapq.heappush(top_values, value)
        if len(top_values) > wanted_rank:
            heapq.heappop(top_values)
    return str(top_values[0])


def brute_kth_largest_element_in_an_array(stdin_text: str) -> str:
    """Return the kth largest value by sorting the whole array downwards.

    Parameters
    ----------
    stdin_text : str
        Count line, values line, k line.

    Returns
    -------
    str
        The kth largest value.
    """
    lines = read_lines(stdin_text)
    values = read_integers(lines[1])
    wanted_rank = int(lines[2])
    descending = sorted(values, reverse=True)
    return str(descending[wanted_rank - 1])


# ---------------------------------------------------------------------------
# IPO
# ---------------------------------------------------------------------------


def solve_ipo(stdin_text: str) -> str:
    """Return the final capital after greedily taking the richest affordable projects.

    Parameters
    ----------
    stdin_text : str
        k line, w line, count line, profits line, capital line.

    Returns
    -------
    str
        Capital held after at most k projects.
    """
    lines = read_lines(stdin_text)
    allowed_projects = int(lines[0])
    capital_held = int(lines[1])
    profits = read_integers(lines[3])
    requirements = read_integers(lines[4])
    by_requirement = sorted(zip(requirements, profits))
    affordable_profits: list[int] = []
    next_project_index = 0
    for _ in range(allowed_projects):
        while (
            next_project_index < len(by_requirement)
            and by_requirement[next_project_index][0] <= capital_held
        ):
            heapq.heappush(affordable_profits, -by_requirement[next_project_index][1])
            next_project_index += 1
        if not affordable_profits:
            break
        capital_held += -heapq.heappop(affordable_profits)
    return str(capital_held)


def brute_ipo(stdin_text: str) -> str:
    """Return the final capital by rescanning every unused project on each round.

    Parameters
    ----------
    stdin_text : str
        k line, w line, count line, profits line, capital line.

    Returns
    -------
    str
        Capital held after at most k projects.
    """
    lines = read_lines(stdin_text)
    allowed_projects = int(lines[0])
    capital_held = int(lines[1])
    profits = read_integers(lines[3])
    requirements = read_integers(lines[4])
    is_used = [False] * len(profits)
    for _ in range(allowed_projects):
        best_index = -1
        for index in range(len(profits)):
            is_available = not is_used[index] and requirements[index] <= capital_held
            if is_available and (best_index == -1 or profits[index] > profits[best_index]):
                best_index = index
        if best_index == -1:
            break
        is_used[best_index] = True
        capital_held += profits[best_index]
    return str(capital_held)


# ---------------------------------------------------------------------------
# Find K Pairs with Smallest Sums
# ---------------------------------------------------------------------------


def solve_find_k_pairs_with_smallest_sums(stdin_text: str) -> str:
    """Emit the k smallest pairs in sum order using a heap over the row frontier.

    Parameters
    ----------
    stdin_text : str
        First count line, first values line, second count line, second values line,
        k line.

    Returns
    -------
    str
        One "u v" line per pair, ordered by sum then u then v.
    """
    lines = read_lines(stdin_text)
    first_values = read_integers(lines[1])
    second_values = read_integers(lines[3])
    wanted_pairs = min(int(lines[4]), len(first_values) * len(second_values))
    frontier = [
        (first_value + second_values[0], first_value, 0) for first_value in first_values
    ]
    heapq.heapify(frontier)
    emitted: list[str] = []
    while len(emitted) < wanted_pairs:
        _, first_value, second_index = heapq.heappop(frontier)
        emitted.append(f"{first_value} {second_values[second_index]}")
        if second_index + 1 < len(second_values):
            next_second = second_values[second_index + 1]
            heapq.heappush(frontier, (first_value + next_second, first_value, second_index + 1))
    return "\n".join(emitted)


def brute_find_k_pairs_with_smallest_sums(stdin_text: str) -> str:
    """Emit the k smallest pairs by forming every pair and sorting them.

    Parameters
    ----------
    stdin_text : str
        First count line, first values line, second count line, second values line,
        k line.

    Returns
    -------
    str
        One "u v" line per pair, ordered by sum then u then v.
    """
    lines = read_lines(stdin_text)
    first_values = read_integers(lines[1])
    second_values = read_integers(lines[3])
    wanted_pairs = int(lines[4])
    all_pairs: list[tuple[int, int, int]] = []
    for first_value in first_values:
        for second_value in second_values:
            all_pairs.append((first_value + second_value, first_value, second_value))
    all_pairs.sort()
    return "\n".join(
        f"{first_value} {second_value}"
        for _, first_value, second_value in all_pairs[:wanted_pairs]
    )


# ---------------------------------------------------------------------------
# Find Median from Data Stream
# ---------------------------------------------------------------------------


def solve_find_median_from_data_stream(stdin_text: str) -> str:
    """Answer every findMedian query using a low max-heap and a high min-heap.

    Parameters
    ----------
    stdin_text : str
        Operation count line followed by that many operation lines.

    Returns
    -------
    str
        One median per findMedian query, each to five decimal places.
    """
    lines = read_lines(stdin_text)
    operation_count = int(lines[0])
    negated_lower_half: list[int] = []
    upper_half: list[int] = []
    answers: list[str] = []
    for operation_index in range(1, operation_count + 1):
        parts = lines[operation_index].split()
        if parts[0] == "addNum":
            heapq.heappush(negated_lower_half, -int(parts[1]))
            heapq.heappush(upper_half, -heapq.heappop(negated_lower_half))
            if len(upper_half) > len(negated_lower_half):
                heapq.heappush(negated_lower_half, -heapq.heappop(upper_half))
        else:
            if len(negated_lower_half) > len(upper_half):
                answers.append(f"{float(-negated_lower_half[0]):.5f}")
            else:
                answers.append(f"{(-negated_lower_half[0] + upper_half[0]) / 2:.5f}")
    return "\n".join(answers)


def brute_find_median_from_data_stream(stdin_text: str) -> str:
    """Answer every findMedian query by re-sorting the values seen so far.

    Parameters
    ----------
    stdin_text : str
        Operation count line followed by that many operation lines.

    Returns
    -------
    str
        One median per findMedian query, each to five decimal places.
    """
    lines = read_lines(stdin_text)
    operation_count = int(lines[0])
    seen_values: list[int] = []
    answers: list[str] = []
    for operation_index in range(1, operation_count + 1):
        parts = lines[operation_index].split()
        if parts[0] == "addNum":
            seen_values.append(int(parts[1]))
        else:
            ordered = sorted(seen_values)
            middle_index = len(ordered) // 2
            if len(ordered) % 2 == 1:
                answers.append(f"{float(ordered[middle_index]):.5f}")
            else:
                answers.append(f"{(ordered[middle_index - 1] + ordered[middle_index]) / 2:.5f}")
    return "\n".join(answers)


# ---------------------------------------------------------------------------
# Add Binary
# ---------------------------------------------------------------------------


def solve_add_binary(stdin_text: str) -> str:
    """Add two binary strings column by column.

    Parameters
    ----------
    stdin_text : str
        First binary string line, second binary string line.

    Returns
    -------
    str
        The sum in binary with no leading zeros.
    """
    lines = read_lines(stdin_text)
    first_digits = lines[0]
    second_digits = lines[1]
    first_index = len(first_digits) - 1
    second_index = len(second_digits) - 1
    carry = 0
    result_digits: list[str] = []
    while first_index >= 0 or second_index >= 0 or carry:
        column_total = carry
        if first_index >= 0:
            column_total += int(first_digits[first_index])
            first_index -= 1
        if second_index >= 0:
            column_total += int(second_digits[second_index])
            second_index -= 1
        result_digits.append(str(column_total % 2))
        carry = column_total // 2
    joined = "".join(reversed(result_digits)).lstrip("0")
    return joined or "0"


def brute_add_binary(stdin_text: str) -> str:
    """Add two binary strings through integer conversion.

    Parameters
    ----------
    stdin_text : str
        First binary string line, second binary string line.

    Returns
    -------
    str
        The sum in binary with no leading zeros.
    """
    lines = read_lines(stdin_text)
    total = int(lines[0], 2) + int(lines[1], 2)
    return format(total, "b")


# ---------------------------------------------------------------------------
# Reverse Bits
# ---------------------------------------------------------------------------


def solve_reverse_bits(stdin_text: str) -> str:
    """Reverse the 32 bits of an unsigned integer by shifting bits out and in.

    Parameters
    ----------
    stdin_text : str
        Single line holding the unsigned 32-bit value.

    Returns
    -------
    str
        The reversed value in decimal.
    """
    original_value = int(read_lines(stdin_text)[0])
    reversed_value = 0
    for _ in range(UNSIGNED_32_BIT_WIDTH):
        reversed_value = (reversed_value << 1) | (original_value & 1)
        original_value >>= 1
    return str(reversed_value)


def brute_reverse_bits(stdin_text: str) -> str:
    """Reverse the 32 bits of an unsigned integer through its binary text form.

    Parameters
    ----------
    stdin_text : str
        Single line holding the unsigned 32-bit value.

    Returns
    -------
    str
        The reversed value in decimal.
    """
    original_value = int(read_lines(stdin_text)[0])
    bit_text = format(original_value, "032b")
    return str(int(bit_text[::-1], 2))


# ---------------------------------------------------------------------------
# Number of 1 Bits
# ---------------------------------------------------------------------------


def solve_number_of_1_bits(stdin_text: str) -> str:
    """Count the set bits of an unsigned integer by clearing the lowest one each pass.

    Parameters
    ----------
    stdin_text : str
        Single line holding the unsigned 32-bit value.

    Returns
    -------
    str
        The number of set bits.
    """
    remaining_value = int(read_lines(stdin_text)[0])
    set_bit_count = 0
    while remaining_value:
        remaining_value &= remaining_value - 1
        set_bit_count += 1
    return str(set_bit_count)


def brute_number_of_1_bits(stdin_text: str) -> str:
    """Count the set bits of an unsigned integer by testing each of the 32 positions.

    Parameters
    ----------
    stdin_text : str
        Single line holding the unsigned 32-bit value.

    Returns
    -------
    str
        The number of set bits.
    """
    value = int(read_lines(stdin_text)[0])
    set_bit_count = 0
    for bit_position in range(UNSIGNED_32_BIT_WIDTH):
        if (value >> bit_position) & 1:
            set_bit_count += 1
    return str(set_bit_count)


# ---------------------------------------------------------------------------
# Single Number
# ---------------------------------------------------------------------------


def solve_single_number(stdin_text: str) -> str:
    """Return the value appearing once by exclusive-oring the whole array.

    Parameters
    ----------
    stdin_text : str
        Count line followed by the values line.

    Returns
    -------
    str
        The value that appears exactly once.
    """
    lines = read_lines(stdin_text)
    unpaired_value = 0
    for value in read_integers(lines[1]):
        unpaired_value ^= value
    return str(unpaired_value)


def brute_single_number(stdin_text: str) -> str:
    """Return the value appearing once by tallying occurrences.

    Parameters
    ----------
    stdin_text : str
        Count line followed by the values line.

    Returns
    -------
    str
        The value that appears exactly once.
    """
    lines = read_lines(stdin_text)
    occurrences = Counter(read_integers(lines[1]))
    for value, times_seen in occurrences.items():
        if times_seen == 1:
            return str(value)
    raise ValueError("no value appears exactly once")


# ---------------------------------------------------------------------------
# Single Number II
# ---------------------------------------------------------------------------


def solve_single_number_ii(stdin_text: str) -> str:
    """Return the value appearing once by reducing each bit column modulo three.

    Parameters
    ----------
    stdin_text : str
        Count line followed by the values line.

    Returns
    -------
    str
        The value that appears exactly once.
    """
    lines = read_lines(stdin_text)
    values = read_integers(lines[1])
    unpaired_value = 0
    for bit_position in range(UNSIGNED_32_BIT_WIDTH):
        column_total = sum((value >> bit_position) & 1 for value in values)
        if column_total % 3:
            unpaired_value |= 1 << bit_position
    # Bit 31 set means the answer is negative in two's complement.
    if unpaired_value > UNSIGNED_32_BIT_MASK >> 1:
        unpaired_value -= 1 << UNSIGNED_32_BIT_WIDTH
    return str(unpaired_value)


def brute_single_number_ii(stdin_text: str) -> str:
    """Return the value appearing once by tallying occurrences.

    Parameters
    ----------
    stdin_text : str
        Count line followed by the values line.

    Returns
    -------
    str
        The value that appears exactly once.
    """
    lines = read_lines(stdin_text)
    occurrences = Counter(read_integers(lines[1]))
    for value, times_seen in occurrences.items():
        if times_seen == 1:
            return str(value)
    raise ValueError("no value appears exactly once")


# ---------------------------------------------------------------------------
# Bitwise AND of Numbers Range
# ---------------------------------------------------------------------------


def solve_bitwise_and_of_numbers_range(stdin_text: str) -> str:
    """Return the bitwise AND over a range as the shared prefix of its endpoints.

    Parameters
    ----------
    stdin_text : str
        Left endpoint line, right endpoint line.

    Returns
    -------
    str
        The bitwise AND of every integer in the range.
    """
    lines = read_lines(stdin_text)
    left_value = int(lines[0])
    right_value = int(lines[1])
    shared_shift = 0
    while left_value < right_value:
        left_value >>= 1
        right_value >>= 1
        shared_shift += 1
    return str(left_value << shared_shift)


def brute_bitwise_and_of_numbers_range(stdin_text: str) -> str:
    """Return the bitwise AND over a range by folding every integer in it.

    Parameters
    ----------
    stdin_text : str
        Left endpoint line, right endpoint line.

    Returns
    -------
    str
        The bitwise AND of every integer in the range.
    """
    lines = read_lines(stdin_text)
    left_value = int(lines[0])
    right_value = int(lines[1])
    folded_value = left_value
    for current_value in range(left_value, right_value + 1):
        folded_value &= current_value
        if folded_value == 0:
            break
    return str(folded_value)


PROBLEMS = [
    {
        "title": "Maximum Subarray",
        "level": "Medium",
        "topics": "Array, Divide and Conquer, Dynamic Programming",
        "companies": "Amazon, Microsoft, Bloomberg, LinkedIn",
        "description": """Given a list of integers, find the contiguous block of one or more
neighbouring values whose sum is as large as possible, and report that sum.

Input (from standard input):
- Line 1: an integer `n`, how many values follow.
- Line 2: `n` integers separated by single spaces.

Output (to standard output):
- A single line holding the largest sum of any contiguous non-empty block.

""",
        "examples": """```
Input:
9
-2 1 -3 4 -1 2 1 -5 4
Output:
6
```

```
Input:
5
-5 -2 -9 -4 -1
Output:
-1
```

""",
        "constraints": """- `1 <= n <= 10^5`
- `-10^4 <= values[i] <= 10^4`
- The chosen block must contain at least one value.

""",
        "inputs": [
            "9\n-2 1 -3 4 -1 2 1 -5 4",
            "1\n7",
            "5\n-5 -2 -9 -4 -1",
            "5\n1 2 3 4 5",
            "6\n5 4 -1 7 8 -30",
        ],
        "solve": solve_maximum_subarray,
        "brute": brute_maximum_subarray,
    },
    {
        "title": "Maximum Sum Circular Subarray",
        "level": "Medium",
        "topics": "Array, Divide and Conquer, Dynamic Programming, Queue",
        "companies": "Amazon, Google, Adobe, Uber",
        "description": """The values form a ring, so the element after the last one is the first
one again. Find the largest sum of a run of one or more neighbouring values on that
ring, where a run may wrap past the end but may not use any element twice.

Input (from standard input):
- Line 1: an integer `n`, how many values follow.
- Line 2: `n` integers separated by single spaces.

Output (to standard output):
- A single line holding the largest such sum.

""",
        "examples": """```
Input:
4
1 -2 3 -2
Output:
3
```

```
Input:
5
3 -1 2 -1 3
Output:
7
```

""",
        "constraints": """- `1 <= n <= 10^4`
- `-3 * 10^4 <= values[i] <= 3 * 10^4`
- A run holds between 1 and `n` elements.

""",
        "inputs": [
            "4\n1 -2 3 -2",
            "3\n5 -3 5",
            "3\n-3 -2 -3",
            "1\n-4",
            "5\n3 -1 2 -1 3",
        ],
        "solve": solve_maximum_sum_circular_subarray,
        "brute": brute_maximum_sum_circular_subarray,
    },
    {
        "title": "Search Insert Position",
        "level": "Easy",
        "topics": "Array, Binary Search",
        "companies": "Amazon, Apple, Microsoft",
        "description": """A list of distinct integers is already sorted from smallest to largest.
Report the index of a target value, or, when the target is missing, the index it would
occupy if it were inserted while keeping the list sorted. Indices start at zero.

Input (from standard input):
- Line 1: an integer `n`, how many values follow.
- Line 2: `n` sorted integers separated by single spaces.
- Line 3: the target integer.

Output (to standard output):
- A single line holding that index.

""",
        "examples": """```
Input:
4
1 3 5 6
5
Output:
2
```

```
Input:
4
1 3 5 6
7
Output:
4
```

""",
        "constraints": """- `1 <= n <= 10^4`
- `-10^4 <= values[i] <= 10^4`
- The values are strictly increasing.
- `-10^4 <= target <= 10^4`

""",
        "inputs": [
            "4\n1 3 5 6\n5",
            "4\n1 3 5 6\n2",
            "4\n1 3 5 6\n7",
            "1\n1\n0",
            "5\n-10 -5 0 3 9\n-10",
        ],
        "solve": solve_search_insert_position,
        "brute": brute_search_insert_position,
    },
    {
        "title": "Search a 2D Matrix",
        "level": "Medium",
        "topics": "Array, Binary Search, Matrix",
        "companies": "Amazon, Facebook, Microsoft, Bloomberg",
        "description": """A grid of integers is sorted twice over: each row increases from left to
right, and the first value of every row is larger than the last value of the row above
it. Report whether a target value appears anywhere in the grid.

Input (from standard input):
- Line 1: two integers `rows` and `cols` separated by a space.
- Next `rows` lines: `cols` integers each, separated by single spaces.
- Last line: the target integer.

Output (to standard output):
- A single line holding `true` when the target is present, otherwise `false`.

""",
        "examples": """```
Input:
3 4
1 3 5 7
10 11 16 20
23 30 34 60
3
Output:
true
```

```
Input:
3 4
1 3 5 7
10 11 16 20
23 30 34 60
13
Output:
false
```

""",
        "constraints": """- `1 <= rows, cols <= 100`
- `-10^4 <= grid value <= 10^4`
- Reading the grid row by row gives one strictly increasing sequence.
- `-10^4 <= target <= 10^4`

""",
        "inputs": [
            "3 4\n1 3 5 7\n10 11 16 20\n23 30 34 60\n3",
            "3 4\n1 3 5 7\n10 11 16 20\n23 30 34 60\n13",
            "1 1\n5\n5",
            "1 1\n5\n-1",
            "2 3\n-5 -3 0\n2 4 9\n9",
        ],
        "solve": solve_search_a_2d_matrix,
        "brute": brute_search_a_2d_matrix,
    },
    {
        "title": "Find Peak Element",
        "level": "Medium",
        "topics": "Array, Binary Search",
        "companies": "Google, Microsoft, Amazon, Nvidia",
        "description": """An index is a peak when its value is larger than the value on each side of
it. Positions off either end of the list count as smaller than everything, so the first
and last index only have to beat their single neighbour. Several peaks can exist, so
report the smallest index that is a peak.

Input (from standard input):
- Line 1: an integer `n`, how many values follow.
- Line 2: `n` integers separated by single spaces.

Output (to standard output):
- A single line holding the smallest peak index, counting from zero.

""",
        "examples": """```
Input:
4
1 2 3 1
Output:
2
```

```
Input:
7
1 2 1 3 5 6 4
Output:
1
```

""",
        "constraints": """- `1 <= n <= 10^5`
- `-2^31 <= values[i] <= 2^31 - 1`
- No two neighbouring values are equal, so at least one peak always exists.

""",
        "inputs": [
            "4\n1 2 3 1",
            "7\n1 2 1 3 5 6 4",
            "1\n9",
            "2\n1 2",
            "5\n5 4 3 2 1",
        ],
        "solve": solve_find_peak_element,
        "brute": brute_find_peak_element,
    },
    {
        "title": "Search in Rotated Sorted Array",
        "level": "Medium",
        "topics": "Array, Binary Search",
        "companies": "Amazon, Facebook, Microsoft, Bloomberg",
        "description": """A sorted list of distinct integers was cut at one position and the two
pieces were swapped, so the values rise, drop once, then rise again. Report the index of
a target value in this rotated list, or `-1` when it is not there.

Input (from standard input):
- Line 1: an integer `n`, how many values follow.
- Line 2: `n` integers separated by single spaces.
- Line 3: the target integer.

Output (to standard output):
- A single line holding the index of the target, counting from zero, or `-1`.

""",
        "examples": """```
Input:
7
4 5 6 7 0 1 2
0
Output:
4
```

```
Input:
7
4 5 6 7 0 1 2
3
Output:
-1
```

""",
        "constraints": """- `1 <= n <= 5000`
- `-10^4 <= values[i] <= 10^4`
- All values are distinct.
- The list is a rotation of a sorted list, possibly by zero positions.

""",
        "inputs": [
            "7\n4 5 6 7 0 1 2\n0",
            "7\n4 5 6 7 0 1 2\n3",
            "1\n1\n0",
            "1\n1\n1",
            "5\n5 1 2 3 4\n5",
            "4\n3 4 5 1\n1",
        ],
        "solve": solve_search_in_rotated_sorted_array,
        "brute": brute_search_in_rotated_sorted_array,
    },
    {
        "title": "Find First and Last Position of Element in Sorted Array",
        "level": "Medium",
        "topics": "Array, Binary Search",
        "companies": "Facebook, Amazon, LinkedIn, Microsoft",
        "description": """A list of integers is sorted from smallest to largest and may repeat
values. Report the first and the last index at which a target value appears. When the
target is missing, report `-1 -1`.

Input (from standard input):
- Line 1: an integer `n`, how many values follow.
- Line 2: `n` sorted integers separated by single spaces.
- Line 3: the target integer.

Output (to standard output):
- A single line holding the first index and the last index, separated by one space.

""",
        "examples": """```
Input:
6
5 7 7 8 8 10
8
Output:
3 4
```

```
Input:
6
5 7 7 8 8 10
6
Output:
-1 -1
```

""",
        "constraints": """- `1 <= n <= 10^5`
- `-10^9 <= values[i] <= 10^9`
- The values never decrease from left to right.
- `-10^9 <= target <= 10^9`

""",
        "inputs": [
            "6\n5 7 7 8 8 10\n8",
            "6\n5 7 7 8 8 10\n6",
            "1\n1\n1",
            "1\n1\n2",
            "5\n2 2 2 2 2\n2",
        ],
        "solve": solve_find_first_and_last_position_of_element_in_sorted_array,
        "brute": brute_find_first_and_last_position_of_element_in_sorted_array,
    },
    {
        "title": "Find Minimum in Rotated Sorted Array",
        "level": "Medium",
        "topics": "Array, Binary Search",
        "companies": "Amazon, Microsoft, Goldman Sachs",
        "description": """A sorted list of distinct integers was cut at one position and the two
pieces were swapped. Report the smallest value in the resulting list.

Input (from standard input):
- Line 1: an integer `n`, how many values follow.
- Line 2: `n` integers separated by single spaces.

Output (to standard output):
- A single line holding the smallest value.

""",
        "examples": """```
Input:
5
3 4 5 1 2
Output:
1
```

```
Input:
4
11 13 15 17
Output:
11
```

""",
        "constraints": """- `1 <= n <= 5000`
- `-5000 <= values[i] <= 5000`
- All values are distinct.
- The list is a rotation of a sorted list, possibly by zero positions.

""",
        "inputs": [
            "5\n3 4 5 1 2",
            "7\n4 5 6 7 0 1 2",
            "4\n11 13 15 17",
            "1\n5",
            "2\n2 1",
        ],
        "solve": solve_find_minimum_in_rotated_sorted_array,
        "brute": brute_find_minimum_in_rotated_sorted_array,
    },
    {
        "title": "Median of Two Sorted Arrays",
        "level": "Hard",
        "topics": "Array, Binary Search, Divide and Conquer",
        "companies": "Google, Amazon, Microsoft, Adobe",
        "description": """Two sorted lists of integers are given. Imagine every value from both
lists placed in one sorted sequence, and report its median: the middle value when the
combined count is odd, or the average of the two middle values when it is even.

Input (from standard input):
- Line 1: an integer `m`, the size of the first list.
- Line 2: `m` sorted integers separated by single spaces.
- Line 3: an integer `n`, the size of the second list.
- Line 4: `n` sorted integers separated by single spaces.

Output (to standard output):
- A single line holding the median written with exactly five digits after the decimal
  point, for example `2.00000`.

""",
        "examples": """```
Input:
2
1 3
1
2
Output:
2.00000
```

```
Input:
2
1 2
2
3 4
Output:
2.50000
```

""",
        "constraints": """- `1 <= m, n <= 1000`
- `-10^6 <= value <= 10^6`
- Each list never decreases from left to right.

""",
        "inputs": [
            "2\n1 3\n1\n2",
            "2\n1 2\n2\n3 4",
            "1\n1\n1\n1",
            "3\n-5 -3 -1\n2\n-4 -2",
            "1\n5\n4\n1 2 3 4",
        ],
        "solve": solve_median_of_two_sorted_arrays,
        "brute": brute_median_of_two_sorted_arrays,
    },
    {
        "title": "Kth Largest Element in an Array",
        "level": "Medium",
        "topics": "Array, Divide and Conquer, Sorting, Heap",
        "companies": "Facebook, Amazon, Microsoft, Apple",
        "description": """Report the kth largest value in a list of integers. Rank by value and not
by distinctness, so in `[3, 2, 3, 1]` the second largest is `3`.

Input (from standard input):
- Line 1: an integer `n`, how many values follow.
- Line 2: `n` integers separated by single spaces.
- Line 3: an integer `k`.

Output (to standard output):
- A single line holding the kth largest value.

""",
        "examples": """```
Input:
6
3 2 1 5 6 4
2
Output:
5
```

```
Input:
6
3 2 1 5 6 4
6
Output:
1
```

""",
        "constraints": """- `1 <= k <= n <= 10^5`
- `-10^4 <= values[i] <= 10^4`

""",
        "inputs": [
            "6\n3 2 1 5 6 4\n2",
            "6\n3 2 1 5 6 4\n6",
            "1\n1\n1",
            "5\n-1 -1 -2 -3 -4\n2",
            "9\n3 2 3 1 2 4 5 5 6\n4",
        ],
        "solve": solve_kth_largest_element_in_an_array,
        "brute": brute_kth_largest_element_in_an_array,
    },
    {
        "title": "IPO",
        "level": "Hard",
        "topics": "Array, Greedy, Sorting, Heap",
        "companies": "Amazon, Google, Bloomberg",
        "description": """You start with `w` units of capital and may finish at most `k` of `n`
projects, one after another. Project `i` can only be started once your capital is at
least `capital[i]`, and finishing it adds `profit[i]` to your capital forever. Report the
largest capital you can hold at the end. Stop early when no remaining project is
affordable.

Input (from standard input):
- Line 1: an integer `k`, the most projects you may finish.
- Line 2: an integer `w`, your starting capital.
- Line 3: an integer `n`, how many projects exist.
- Line 4: `n` integers, the profit of each project, separated by single spaces.
- Line 5: `n` integers, the capital each project requires, in the same project order.

Output (to standard output):
- A single line holding the final capital.

""",
        "examples": """```
Input:
2
0
3
1 2 3
0 1 1
Output:
4
```

```
Input:
2
0
2
1 2
1 2
Output:
0
```

""",
        "constraints": """- `1 <= n <= 10^5`
- `1 <= k <= 10^5`
- `0 <= w <= 10^9`
- `0 <= profit[i] <= 10^4`
- `0 <= capital[i] <= 10^9`

""",
        "inputs": [
            "2\n0\n3\n1 2 3\n0 1 1",
            "3\n0\n3\n1 2 3\n0 1 2",
            "1\n0\n1\n5\n0",
            "2\n0\n2\n1 2\n1 2",
            "3\n2\n2\n4 6\n0 3",
        ],
        "solve": solve_ipo,
        "brute": brute_ipo,
    },
    {
        "title": "Find K Pairs with Smallest Sums",
        "level": "Medium",
        "topics": "Array, Heap, Sorting",
        "companies": "Google, Amazon, Uber, LinkedIn",
        "description": """Two sorted lists are given. A pair takes one value `u` from the first list
and one value `v` from the second, and every combination of positions counts as its own
pair even when the values repeat. Print the `k` pairs with the smallest sums.

Order the printed pairs by sum from smallest to largest; break a tie in sum by the
smaller `u`, and a remaining tie by the smaller `v`. When `k` is larger than the number
of pairs that exist, print every pair.

Input (from standard input):
- Line 1: an integer `m`, the size of the first list.
- Line 2: `m` sorted integers separated by single spaces.
- Line 3: an integer `n`, the size of the second list.
- Line 4: `n` sorted integers separated by single spaces.
- Line 5: an integer `k`.

Output (to standard output):
- One line per printed pair, holding `u` and `v` separated by a single space.

""",
        "examples": """```
Input:
2
1 7
2
2 4
2
Output:
1 2
1 4
```

```
Input:
3
1 2 4
2
-1 2
3
Output:
1 -1
2 -1
1 2
```

""",
        "constraints": """- `1 <= m, n <= 1000`
- `-10^9 <= value <= 10^9`
- Each list never decreases from left to right.
- `1 <= k <= 1000`

""",
        "inputs": [
            "2\n1 7\n2\n2 4\n2",
            "3\n1 7 11\n3\n2 4 6\n3",
            "2\n1 1\n2\n1 1\n4",
            "1\n-5\n1\n3\n1",
            "2\n1 2\n3\n3 5 7\n10",
            "3\n1 2 4\n2\n-1 2\n3",
        ],
        "solve": solve_find_k_pairs_with_smallest_sums,
        "brute": brute_find_k_pairs_with_smallest_sums,
    },
    {
        "title": "Find Median from Data Stream",
        "level": "Hard",
        "topics": "Design, Two Pointers, Data Stream, Sorting, Heap",
        "companies": "Amazon, Google, Microsoft, Apple",
        "description": """Numbers arrive one at a time, and at any moment you may be asked for the
median of everything seen so far. The median is the middle value when the count is odd,
or the average of the two middle values when it is even.

Input (from standard input):
- Line 1: an integer `q`, how many operations follow.
- Next `q` lines: either `addNum x`, which records the integer `x`, or `findMedian`,
  which asks for the median of the values recorded so far.

Output (to standard output):
- One line per `findMedian` operation, in the order the operations appear, holding the
  median written with exactly five digits after the decimal point.

""",
        "examples": """```
Input:
5
addNum 1
addNum 2
findMedian
addNum 3
findMedian
Output:
1.50000
2.00000
```

```
Input:
4
addNum -1
addNum -2
addNum -3
findMedian
Output:
-2.00000
```

""",
        "constraints": """- `2 <= q <= 10^4`
- `-10^5 <= x <= 10^5`
- The first operation is always `addNum`, so `findMedian` never runs on an empty set.
- At least one operation is `findMedian`.

""",
        "inputs": [
            "5\naddNum 1\naddNum 2\nfindMedian\naddNum 3\nfindMedian",
            "3\naddNum 5\nfindMedian\nfindMedian",
            "4\naddNum -1\naddNum -2\naddNum -3\nfindMedian",
            "6\naddNum 4\naddNum 4\nfindMedian\naddNum 4\naddNum 0\nfindMedian",
            "7\naddNum 10\naddNum 20\naddNum 30\nfindMedian\naddNum 40\naddNum 50\nfindMedian",
        ],
        "solve": solve_find_median_from_data_stream,
        "brute": brute_find_median_from_data_stream,
    },
    {
        "title": "Add Binary",
        "level": "Easy",
        "topics": "Math, String, Bit Manipulation, Simulation",
        "companies": "Facebook, Amazon, Microsoft",
        "description": """Two non-negative numbers are written in base two. Add them and print the
sum, also in base two.

Input (from standard input):
- Line 1: the first binary string.
- Line 2: the second binary string.

Output (to standard output):
- A single line holding the sum in base two, with no leading zeros unless the sum is
  zero, which prints as `0`.

""",
        "examples": """```
Input:
11
1
Output:
100
```

```
Input:
1010
1011
Output:
10101
```

""",
        "constraints": """- Each string has between 1 and 10^4 characters.
- Each character is `0` or `1`.
- Neither input string has a leading zero unless it is exactly `0`.

""",
        "inputs": [
            "11\n1",
            "1010\n1011",
            "0\n0",
            "1111\n1111",
            "0\n1101",
        ],
        "solve": solve_add_binary,
        "brute": brute_add_binary,
    },
    {
        "title": "Reverse Bits",
        "level": "Easy",
        "topics": "Divide and Conquer, Bit Manipulation",
        "companies": "Apple, Amazon, Microsoft, Qualcomm",
        "description": """Treat the given value as an unsigned 32-bit integer, so it is written with
exactly 32 bits and is never negative. Reverse the order of those 32 bits, so the lowest
bit becomes the highest and the highest becomes the lowest, then print the value the
reversed bits spell out.

Input (from standard input):
- Line 1: a single integer between `0` and `4294967295`.

Output (to standard output):
- A single line holding the reversed value in ordinary decimal notation.

""",
        "examples": """```
Input:
43261596
Output:
964176192
```

```
Input:
1
Output:
2147483648
```

""",
        "constraints": """- `0 <= value <= 4294967295`, that is, `2^32 - 1`.
- The value is unsigned, so bit 31 carries no sign.

""",
        "inputs": [
            "43261596",
            "4294967293",
            "0",
            "1",
            "2147483648",
        ],
        "solve": solve_reverse_bits,
        "brute": brute_reverse_bits,
    },
    {
        "title": "Number of 1 Bits",
        "level": "Easy",
        "topics": "Divide and Conquer, Bit Manipulation",
        "companies": "Apple, Microsoft, Amazon",
        "description": """Treat the given value as an unsigned 32-bit integer and count how many of
its bits are set to one.

Input (from standard input):
- Line 1: a single integer between `0` and `4294967295`.

Output (to standard output):
- A single line holding the count of one bits.

""",
        "examples": """```
Input:
11
Output:
3
```

```
Input:
128
Output:
1
```

""",
        "constraints": """- `0 <= value <= 4294967295`, that is, `2^32 - 1`.
- The value is unsigned, so bit 31 carries no sign.

""",
        "inputs": [
            "11",
            "128",
            "2147483645",
            "0",
            "4294967295",
        ],
        "solve": solve_number_of_1_bits,
        "brute": brute_number_of_1_bits,
    },
    {
        "title": "Single Number",
        "level": "Easy",
        "topics": "Array, Bit Manipulation",
        "companies": "Amazon, Google, Airbnb, Palantir",
        "description": """Every value in the list appears exactly twice except for one, which appears
once. Report that lone value.

Input (from standard input):
- Line 1: an integer `n`, how many values follow.
- Line 2: `n` integers separated by single spaces.

Output (to standard output):
- A single line holding the value that appears only once.

""",
        "examples": """```
Input:
3
2 2 1
Output:
1
```

```
Input:
5
4 1 2 1 2
Output:
4
```

""",
        "constraints": """- `1 <= n <= 3 * 10^4`
- `n` is odd.
- `-3 * 10^4 <= values[i] <= 3 * 10^4`
- Exactly one value appears once; every other value appears exactly twice.

""",
        "inputs": [
            "3\n2 2 1",
            "5\n4 1 2 1 2",
            "1\n1",
            "5\n-3 1 1 -4 -4",
            "7\n7 3 5 3 7 5 9",
        ],
        "solve": solve_single_number,
        "brute": brute_single_number,
    },
    {
        "title": "Single Number II",
        "level": "Medium",
        "topics": "Array, Bit Manipulation",
        "companies": "Amazon, Google, Bloomberg",
        "description": """Every value in the list appears exactly three times except for one, which
appears once. Report that lone value.

Input (from standard input):
- Line 1: an integer `n`, how many values follow.
- Line 2: `n` integers separated by single spaces.

Output (to standard output):
- A single line holding the value that appears only once.

""",
        "examples": """```
Input:
4
2 2 3 2
Output:
3
```

```
Input:
7
0 1 0 1 0 1 99
Output:
99
```

""",
        "constraints": """- `1 <= n <= 3 * 10^4`
- `-2^31 <= values[i] <= 2^31 - 1`
- Exactly one value appears once; every other value appears exactly three times.

""",
        "inputs": [
            "4\n2 2 3 2",
            "7\n0 1 0 1 0 1 99",
            "1\n5",
            "4\n-2 -2 -2 -7",
            "7\n30000 500 100 30000 100 30000 100",
        ],
        "solve": solve_single_number_ii,
        "brute": brute_single_number_ii,
    },
    {
        "title": "Bitwise AND of Numbers Range",
        "level": "Medium",
        "topics": "Bit Manipulation",
        "companies": "Amazon, Facebook, Qualcomm",
        "description": """Take every integer from `left` to `right`, both ends included, and combine
them all with the bitwise AND operator. Print the result.

Input (from standard input):
- Line 1: the integer `left`.
- Line 2: the integer `right`.

Output (to standard output):
- A single line holding the bitwise AND of the whole range.

""",
        "examples": """```
Input:
5
7
Output:
4
```

```
Input:
20
30
Output:
16
```

""",
        "constraints": """- `0 <= left <= right <= 2^31 - 1`
- `right - left <= 10^5`, so even a plain loop over the range finishes in time.

""",
        "inputs": [
            "5\n7",
            "0\n0",
            "1\n1",
            "20\n30",
            "2147483646\n2147483647",
            "4\n2000",
        ],
        "solve": solve_bitwise_and_of_numbers_range,
        "brute": brute_bitwise_and_of_numbers_range,
    },
]
