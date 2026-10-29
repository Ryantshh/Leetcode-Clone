"""Problem specs for the two pointers, sliding window and matrix group.

Every solve reads one stdin payload and returns the exact stdout text the judge
compares against. Every brute is an independent implementation used only as a
cross-check by the build script.
"""

from __future__ import annotations

from bisect import bisect_left
from collections import Counter
from typing import Any

# --------------------------------------------------------------------------
# Valid Palindrome
# --------------------------------------------------------------------------


def solve_valid_palindrome(stdin_text: str) -> str:
    """Decide whether a line reads the same forwards and backwards.

    Parameters
    ----------
    stdin_text : str
        One line holding the candidate string.

    Returns
    -------
    str
        "true" or "false".
    """
    line = stdin_text.split("\n")[0].strip()
    left_index = 0
    right_index = len(line) - 1
    while left_index < right_index:
        if not line[left_index].isalnum():
            left_index += 1
            continue
        if not line[right_index].isalnum():
            right_index -= 1
            continue
        if line[left_index].lower() != line[right_index].lower():
            return "false"
        left_index += 1
        right_index -= 1
    return "true"


def brute_valid_palindrome(stdin_text: str) -> str:
    """Decide palindromity by filtering the line and comparing with its reverse.

    Parameters
    ----------
    stdin_text : str
        One line holding the candidate string.

    Returns
    -------
    str
        "true" or "false".
    """
    line = stdin_text.split("\n")[0].strip()
    kept_characters = [character.lower() for character in line if character.isalnum()]
    return "true" if kept_characters == kept_characters[::-1] else "false"


# --------------------------------------------------------------------------
# Is Subsequence
# --------------------------------------------------------------------------


def solve_is_subsequence(stdin_text: str) -> str:
    """Decide whether the first line is a subsequence of the second.

    Parameters
    ----------
    stdin_text : str
        Line one is the candidate, line two is the host string.

    Returns
    -------
    str
        "true" or "false".
    """
    lines = stdin_text.split("\n")
    candidate = lines[0].strip()
    host = lines[1].strip()
    candidate_index = 0
    for host_character in host:
        if candidate_index < len(candidate) and host_character == candidate[candidate_index]:
            candidate_index += 1
    return "true" if candidate_index == len(candidate) else "false"


def brute_is_subsequence(stdin_text: str) -> str:
    """Decide subsequence membership by repeatedly searching for the next character.

    Parameters
    ----------
    stdin_text : str
        Line one is the candidate, line two is the host string.

    Returns
    -------
    str
        "true" or "false".
    """
    lines = stdin_text.split("\n")
    candidate = lines[0].strip()
    host = lines[1].strip()
    search_from = 0
    for candidate_character in candidate:
        found_at = host.find(candidate_character, search_from)
        if found_at < 0:
            return "false"
        search_from = found_at + 1
    return "true"


# --------------------------------------------------------------------------
# Two Sum II - Input Array Is Sorted
# --------------------------------------------------------------------------


def solve_two_sum_ii_input_array_is_sorted(stdin_text: str) -> str:
    """Find the lexicographically smallest index pair summing to the target.

    Parameters
    ----------
    stdin_text : str
        Line one holds the count and the target, line two the sorted values.

    Returns
    -------
    str
        The two one-based indices separated by a space, or "-1".
    """
    lines = stdin_text.split("\n")
    count, target = (int(token) for token in lines[0].split())
    numbers = [int(token) for token in lines[1].split()]
    for first_index in range(count - 1):
        needed = target - numbers[first_index]
        position = bisect_left(numbers, needed, first_index + 1, count)
        if position < count and numbers[position] == needed:
            return f"{first_index + 1} {position + 1}"
    return "-1"


def brute_two_sum_ii_input_array_is_sorted(stdin_text: str) -> str:
    """Find the index pair summing to the target by scanning every pair in order.

    Parameters
    ----------
    stdin_text : str
        Line one holds the count and the target, line two the sorted values.

    Returns
    -------
    str
        The two one-based indices separated by a space, or "-1".
    """
    lines = stdin_text.split("\n")
    count, target = (int(token) for token in lines[0].split())
    numbers = [int(token) for token in lines[1].split()]
    for first_index in range(count):
        for second_index in range(first_index + 1, count):
            if numbers[first_index] + numbers[second_index] == target:
                return f"{first_index + 1} {second_index + 1}"
    return "-1"


# --------------------------------------------------------------------------
# Container With Most Water
# --------------------------------------------------------------------------


def solve_container_with_most_water(stdin_text: str) -> str:
    """Compute the largest water area between two of the given vertical lines.

    Parameters
    ----------
    stdin_text : str
        Line one holds the line count, line two the heights.

    Returns
    -------
    str
        The maximum area as a decimal integer.
    """
    lines = stdin_text.split("\n")
    heights = [int(token) for token in lines[1].split()]
    left_index = 0
    right_index = len(heights) - 1
    largest_area = 0
    while left_index < right_index:
        width = right_index - left_index
        area = width * min(heights[left_index], heights[right_index])
        largest_area = max(largest_area, area)
        if heights[left_index] <= heights[right_index]:
            left_index += 1
        else:
            right_index -= 1
    return str(largest_area)


def brute_container_with_most_water(stdin_text: str) -> str:
    """Compute the largest water area by measuring every pair of lines.

    Parameters
    ----------
    stdin_text : str
        Line one holds the line count, line two the heights.

    Returns
    -------
    str
        The maximum area as a decimal integer.
    """
    lines = stdin_text.split("\n")
    heights = [int(token) for token in lines[1].split()]
    largest_area = 0
    for left_index in range(len(heights)):
        for right_index in range(left_index + 1, len(heights)):
            area = (right_index - left_index) * min(heights[left_index], heights[right_index])
            largest_area = max(largest_area, area)
    return str(largest_area)


# --------------------------------------------------------------------------
# 3Sum
# --------------------------------------------------------------------------


def solve_3sum(stdin_text: str) -> str:
    """List the distinct value triplets that sum to zero.

    Parameters
    ----------
    stdin_text : str
        Line one holds the value count, line two the values.

    Returns
    -------
    str
        One sorted triplet per line in lexicographic order, or "none".
    """
    lines = stdin_text.split("\n")
    numbers = sorted(int(token) for token in lines[1].split())
    count = len(numbers)
    triplets: list[tuple[int, int, int]] = []
    for first_index in range(count - 2):
        if first_index > 0 and numbers[first_index] == numbers[first_index - 1]:
            continue
        left_index = first_index + 1
        right_index = count - 1
        while left_index < right_index:
            total = numbers[first_index] + numbers[left_index] + numbers[right_index]
            if total < 0:
                left_index += 1
            elif total > 0:
                right_index -= 1
            else:
                triplets.append((numbers[first_index], numbers[left_index], numbers[right_index]))
                left_index += 1
                while left_index < right_index and numbers[left_index] == numbers[left_index - 1]:
                    left_index += 1
                right_index -= 1
    if not triplets:
        return "none"
    return "\n".join(" ".join(str(value) for value in triplet) for triplet in triplets)


def brute_3sum(stdin_text: str) -> str:
    """List the distinct zero-sum triplets by trying every index combination.

    Parameters
    ----------
    stdin_text : str
        Line one holds the value count, line two the values.

    Returns
    -------
    str
        One sorted triplet per line in lexicographic order, or "none".
    """
    lines = stdin_text.split("\n")
    numbers = [int(token) for token in lines[1].split()]
    count = len(numbers)
    found: set[tuple[int, int, int]] = set()
    for first_index in range(count):
        for second_index in range(first_index + 1, count):
            for third_index in range(second_index + 1, count):
                picked = (numbers[first_index], numbers[second_index], numbers[third_index])
                if sum(picked) == 0:
                    ordered = tuple(sorted(picked))
                    found.add((ordered[0], ordered[1], ordered[2]))
    if not found:
        return "none"
    return "\n".join(" ".join(str(value) for value in triplet) for triplet in sorted(found))


# --------------------------------------------------------------------------
# Minimum Size Subarray Sum
# --------------------------------------------------------------------------


def solve_minimum_size_subarray_sum(stdin_text: str) -> str:
    """Compute the shortest contiguous block whose sum reaches the target.

    Parameters
    ----------
    stdin_text : str
        Line one holds the count and the target, line two the values.

    Returns
    -------
    str
        The shortest qualifying length, or "0" when no block qualifies.
    """
    lines = stdin_text.split("\n")
    _, target = (int(token) for token in lines[0].split())
    numbers = [int(token) for token in lines[1].split()]
    shortest_length = len(numbers) + 1
    window_start = 0
    window_sum = 0
    for window_end, value in enumerate(numbers):
        window_sum += value
        while window_sum >= target:
            shortest_length = min(shortest_length, window_end - window_start + 1)
            window_sum -= numbers[window_start]
            window_start += 1
    return str(0 if shortest_length > len(numbers) else shortest_length)


def brute_minimum_size_subarray_sum(stdin_text: str) -> str:
    """Compute the shortest qualifying block by summing every contiguous range.

    Parameters
    ----------
    stdin_text : str
        Line one holds the count and the target, line two the values.

    Returns
    -------
    str
        The shortest qualifying length, or "0" when no block qualifies.
    """
    lines = stdin_text.split("\n")
    _, target = (int(token) for token in lines[0].split())
    numbers = [int(token) for token in lines[1].split()]
    best_length = 0
    for start_index in range(len(numbers)):
        running_sum = 0
        for end_index in range(start_index, len(numbers)):
            running_sum += numbers[end_index]
            if running_sum >= target:
                length = end_index - start_index + 1
                if best_length == 0 or length < best_length:
                    best_length = length
                break
    return str(best_length)


# --------------------------------------------------------------------------
# Longest Substring Without Repeating Characters
# --------------------------------------------------------------------------


def solve_longest_substring_without_repeating_characters(stdin_text: str) -> str:
    """Compute the length of the longest substring with no repeated character.

    Parameters
    ----------
    stdin_text : str
        One line holding the string.

    Returns
    -------
    str
        The longest length as a decimal integer.
    """
    line = stdin_text.split("\n")[0].strip()
    last_seen_at: dict[str, int] = {}
    window_start = 0
    longest_length = 0
    for index, character in enumerate(line):
        if character in last_seen_at and last_seen_at[character] >= window_start:
            window_start = last_seen_at[character] + 1
        last_seen_at[character] = index
        longest_length = max(longest_length, index - window_start + 1)
    return str(longest_length)


def brute_longest_substring_without_repeating_characters(stdin_text: str) -> str:
    """Compute the longest repeat-free substring length by growing every start.

    Parameters
    ----------
    stdin_text : str
        One line holding the string.

    Returns
    -------
    str
        The longest length as a decimal integer.
    """
    line = stdin_text.split("\n")[0].strip()
    longest_length = 0
    for start_index in range(len(line)):
        seen_characters: set[str] = set()
        for end_index in range(start_index, len(line)):
            if line[end_index] in seen_characters:
                break
            seen_characters.add(line[end_index])
            longest_length = max(longest_length, end_index - start_index + 1)
    return str(longest_length)


# --------------------------------------------------------------------------
# Substring with Concatenation of All Words
# --------------------------------------------------------------------------


def solve_substring_with_concatenation_of_all_words(stdin_text: str) -> str:
    """List the start indices of windows that are a permutation of all words.

    Parameters
    ----------
    stdin_text : str
        Line one is the text, line two the equal-length words separated by spaces.

    Returns
    -------
    str
        Ascending indices on one space-separated line, or "none".
    """
    lines = stdin_text.split("\n")
    text = lines[0].strip()
    words = lines[1].split()
    word_length = len(words[0])
    wanted_counts = Counter(words)
    starts: list[int] = []
    for offset in range(word_length):
        window_counts: Counter[str] = Counter()
        matched_words = 0
        window_start = offset
        for chunk_end in range(offset + word_length, len(text) + 1, word_length):
            chunk = text[chunk_end - word_length : chunk_end]
            if chunk in wanted_counts:
                window_counts[chunk] += 1
                matched_words += 1
                while window_counts[chunk] > wanted_counts[chunk]:
                    dropped = text[window_start : window_start + word_length]
                    window_counts[dropped] -= 1
                    matched_words -= 1
                    window_start += word_length
            else:
                window_counts.clear()
                matched_words = 0
                window_start = chunk_end
            if matched_words == len(words):
                starts.append(window_start)
                dropped = text[window_start : window_start + word_length]
                window_counts[dropped] -= 1
                matched_words -= 1
                window_start += word_length
    if not starts:
        return "none"
    return " ".join(str(index) for index in sorted(starts))


def brute_substring_with_concatenation_of_all_words(stdin_text: str) -> str:
    """List the qualifying start indices by counting the words in every window.

    Parameters
    ----------
    stdin_text : str
        Line one is the text, line two the equal-length words separated by spaces.

    Returns
    -------
    str
        Ascending indices on one space-separated line, or "none".
    """
    lines = stdin_text.split("\n")
    text = lines[0].strip()
    words = lines[1].split()
    word_length = len(words[0])
    window_length = word_length * len(words)
    wanted_counts = Counter(words)
    starts: list[int] = []
    for start_index in range(len(text) - window_length + 1):
        window = text[start_index : start_index + window_length]
        chunks = [
            window[chunk_start : chunk_start + word_length]
            for chunk_start in range(0, window_length, word_length)
        ]
        if Counter(chunks) == wanted_counts:
            starts.append(start_index)
    if not starts:
        return "none"
    return " ".join(str(index) for index in starts)


# --------------------------------------------------------------------------
# Minimum Window Substring
# --------------------------------------------------------------------------


def solve_minimum_window_substring(stdin_text: str) -> str:
    """Find the shortest window of the text covering every character of the pattern.

    Parameters
    ----------
    stdin_text : str
        Line one is the text, line two the pattern.

    Returns
    -------
    str
        The leftmost shortest covering window, or "none".
    """
    lines = stdin_text.split("\n")
    text = lines[0].strip()
    pattern = lines[1].strip()
    wanted_counts = Counter(pattern)
    missing_count = len(pattern)
    best_start = 0
    best_length = len(text) + 1
    window_start = 0
    for window_end, character in enumerate(text):
        if wanted_counts[character] > 0:
            missing_count -= 1
        wanted_counts[character] -= 1
        while missing_count == 0:
            if window_end - window_start + 1 < best_length:
                best_start = window_start
                best_length = window_end - window_start + 1
            dropped = text[window_start]
            wanted_counts[dropped] += 1
            if wanted_counts[dropped] > 0:
                missing_count += 1
            window_start += 1
    if best_length > len(text):
        return "none"
    return text[best_start : best_start + best_length]


def brute_minimum_window_substring(stdin_text: str) -> str:
    """Find the shortest covering window by testing every substring in order.

    Parameters
    ----------
    stdin_text : str
        Line one is the text, line two the pattern.

    Returns
    -------
    str
        The leftmost shortest covering window, or "none".
    """
    lines = stdin_text.split("\n")
    text = lines[0].strip()
    pattern = lines[1].strip()
    wanted_counts = Counter(pattern)
    best_window = ""
    for start_index in range(len(text)):
        for end_index in range(start_index + len(pattern), len(text) + 1):
            window = text[start_index:end_index]
            if not wanted_counts - Counter(window):
                if not best_window or len(window) < len(best_window):
                    best_window = window
                break
    return best_window if best_window else "none"


# --------------------------------------------------------------------------
# Valid Sudoku
# --------------------------------------------------------------------------


def solve_valid_sudoku(stdin_text: str) -> str:
    """Decide whether a partially filled 9 by 9 board breaks no Sudoku rule.

    Parameters
    ----------
    stdin_text : str
        Nine lines of nine space-separated cells, a dot marking an empty cell.

    Returns
    -------
    str
        "true" or "false".
    """
    board = [line.split() for line in stdin_text.split("\n")[:9]]
    seen_in_row: list[set[str]] = [set() for _ in range(9)]
    seen_in_column: list[set[str]] = [set() for _ in range(9)]
    seen_in_box: list[set[str]] = [set() for _ in range(9)]
    for row_index in range(9):
        for column_index in range(9):
            cell = board[row_index][column_index]
            if cell == ".":
                continue
            box_index = (row_index // 3) * 3 + column_index // 3
            if (
                cell in seen_in_row[row_index]
                or cell in seen_in_column[column_index]
                or cell in seen_in_box[box_index]
            ):
                return "false"
            seen_in_row[row_index].add(cell)
            seen_in_column[column_index].add(cell)
            seen_in_box[box_index].add(cell)
    return "true"


def brute_valid_sudoku(stdin_text: str) -> str:
    """Decide board validity by comparing every pair of filled cells.

    Parameters
    ----------
    stdin_text : str
        Nine lines of nine space-separated cells, a dot marking an empty cell.

    Returns
    -------
    str
        "true" or "false".
    """
    board = [line.split() for line in stdin_text.split("\n")[:9]]
    filled_cells = [
        (row_index, column_index, board[row_index][column_index])
        for row_index in range(9)
        for column_index in range(9)
        if board[row_index][column_index] != "."
    ]
    for first_position in range(len(filled_cells)):
        first_row, first_column, first_value = filled_cells[first_position]
        for second_position in range(first_position + 1, len(filled_cells)):
            second_row, second_column, second_value = filled_cells[second_position]
            if first_value != second_value:
                continue
            is_same_box = (first_row // 3, first_column // 3) == (
                second_row // 3,
                second_column // 3,
            )
            if first_row == second_row or first_column == second_column or is_same_box:
                return "false"
    return "true"


# --------------------------------------------------------------------------
# Spiral Matrix
# --------------------------------------------------------------------------


def solve_spiral_matrix(stdin_text: str) -> str:
    """Read a matrix in clockwise spiral order starting at the top-left cell.

    Parameters
    ----------
    stdin_text : str
        Line one holds the row and column counts, then that many matrix rows.

    Returns
    -------
    str
        The visited values on one space-separated line.
    """
    lines = stdin_text.split("\n")
    row_count, column_count = (int(token) for token in lines[0].split())
    matrix = [[int(token) for token in lines[1 + index].split()] for index in range(row_count)]
    top_row = 0
    bottom_row = row_count - 1
    left_column = 0
    right_column = column_count - 1
    visited: list[int] = []
    while top_row <= bottom_row and left_column <= right_column:
        for column_index in range(left_column, right_column + 1):
            visited.append(matrix[top_row][column_index])
        top_row += 1
        for row_index in range(top_row, bottom_row + 1):
            visited.append(matrix[row_index][right_column])
        right_column -= 1
        if top_row <= bottom_row:
            for column_index in range(right_column, left_column - 1, -1):
                visited.append(matrix[bottom_row][column_index])
            bottom_row -= 1
        if left_column <= right_column:
            for row_index in range(bottom_row, top_row - 1, -1):
                visited.append(matrix[row_index][left_column])
            left_column += 1
    return " ".join(str(value) for value in visited)


def brute_spiral_matrix(stdin_text: str) -> str:
    """Read a matrix in spiral order by walking and turning on blocked cells.

    Parameters
    ----------
    stdin_text : str
        Line one holds the row and column counts, then that many matrix rows.

    Returns
    -------
    str
        The visited values on one space-separated line.
    """
    lines = stdin_text.split("\n")
    row_count, column_count = (int(token) for token in lines[0].split())
    matrix = [[int(token) for token in lines[1 + index].split()] for index in range(row_count)]
    directions = ((0, 1), (1, 0), (0, -1), (-1, 0))
    is_visited = [[False] * column_count for _ in range(row_count)]
    visited: list[int] = []
    row_index = 0
    column_index = 0
    direction_index = 0
    for _ in range(row_count * column_count):
        visited.append(matrix[row_index][column_index])
        is_visited[row_index][column_index] = True
        for turn in range(4):
            candidate_direction = directions[(direction_index + turn) % 4]
            next_row = row_index + candidate_direction[0]
            next_column = column_index + candidate_direction[1]
            is_inside = 0 <= next_row < row_count and 0 <= next_column < column_count
            if is_inside and not is_visited[next_row][next_column]:
                direction_index = (direction_index + turn) % 4
                row_index = next_row
                column_index = next_column
                break
    return " ".join(str(value) for value in visited)


# --------------------------------------------------------------------------
# Rotate Image
# --------------------------------------------------------------------------


def solve_rotate_image(stdin_text: str) -> str:
    """Rotate a square matrix a quarter turn clockwise in place.

    Parameters
    ----------
    stdin_text : str
        Line one holds the side length, then that many matrix rows.

    Returns
    -------
    str
        The rotated matrix, one space-separated row per line.
    """
    lines = stdin_text.split("\n")
    side_length = int(lines[0].strip())
    matrix = [[int(token) for token in lines[1 + index].split()] for index in range(side_length)]
    for row_index in range(side_length):
        for column_index in range(row_index + 1, side_length):
            matrix[row_index][column_index], matrix[column_index][row_index] = (
                matrix[column_index][row_index],
                matrix[row_index][column_index],
            )
    for row in matrix:
        row.reverse()
    return "\n".join(" ".join(str(value) for value in row) for row in matrix)


def brute_rotate_image(stdin_text: str) -> str:
    """Rotate a square matrix clockwise by copying cells into a fresh matrix.

    Parameters
    ----------
    stdin_text : str
        Line one holds the side length, then that many matrix rows.

    Returns
    -------
    str
        The rotated matrix, one space-separated row per line.
    """
    lines = stdin_text.split("\n")
    side_length = int(lines[0].strip())
    matrix = [[int(token) for token in lines[1 + index].split()] for index in range(side_length)]
    rotated = [
        [matrix[side_length - 1 - column_index][row_index] for column_index in range(side_length)]
        for row_index in range(side_length)
    ]
    return "\n".join(" ".join(str(value) for value in row) for row in rotated)


# --------------------------------------------------------------------------
# Set Matrix Zeroes
# --------------------------------------------------------------------------


def solve_set_matrix_zeroes(stdin_text: str) -> str:
    """Blank the row and column of every zero cell, using the border as storage.

    Parameters
    ----------
    stdin_text : str
        Line one holds the row and column counts, then that many matrix rows.

    Returns
    -------
    str
        The updated matrix, one space-separated row per line.
    """
    lines = stdin_text.split("\n")
    row_count, column_count = (int(token) for token in lines[0].split())
    matrix = [[int(token) for token in lines[1 + index].split()] for index in range(row_count)]
    has_zero_in_first_row = any(matrix[0][index] == 0 for index in range(column_count))
    has_zero_in_first_column = any(matrix[index][0] == 0 for index in range(row_count))
    for row_index in range(1, row_count):
        for column_index in range(1, column_count):
            if matrix[row_index][column_index] == 0:
                matrix[row_index][0] = 0
                matrix[0][column_index] = 0
    for row_index in range(1, row_count):
        for column_index in range(1, column_count):
            if matrix[row_index][0] == 0 or matrix[0][column_index] == 0:
                matrix[row_index][column_index] = 0
    if has_zero_in_first_row:
        for column_index in range(column_count):
            matrix[0][column_index] = 0
    if has_zero_in_first_column:
        for row_index in range(row_count):
            matrix[row_index][0] = 0
    return "\n".join(" ".join(str(value) for value in row) for row in matrix)


def brute_set_matrix_zeroes(stdin_text: str) -> str:
    """Blank the rows and columns holding a zero using collected index sets.

    Parameters
    ----------
    stdin_text : str
        Line one holds the row and column counts, then that many matrix rows.

    Returns
    -------
    str
        The updated matrix, one space-separated row per line.
    """
    lines = stdin_text.split("\n")
    row_count, column_count = (int(token) for token in lines[0].split())
    matrix = [[int(token) for token in lines[1 + index].split()] for index in range(row_count)]
    zero_rows = {
        row_index
        for row_index in range(row_count)
        for column_index in range(column_count)
        if matrix[row_index][column_index] == 0
    }
    zero_columns = {
        column_index
        for row_index in range(row_count)
        for column_index in range(column_count)
        if matrix[row_index][column_index] == 0
    }
    result = [
        [
            0 if row_index in zero_rows or column_index in zero_columns
            else matrix[row_index][column_index]
            for column_index in range(column_count)
        ]
        for row_index in range(row_count)
    ]
    return "\n".join(" ".join(str(value) for value in row) for row in result)


# --------------------------------------------------------------------------
# Game of Life
# --------------------------------------------------------------------------


def solve_game_of_life(stdin_text: str) -> str:
    """Advance a life board one generation in place using a second state bit.

    Parameters
    ----------
    stdin_text : str
        Line one holds the row and column counts, then that many rows of 0 and 1.

    Returns
    -------
    str
        The next generation, one space-separated row per line.
    """
    lines = stdin_text.split("\n")
    row_count, column_count = (int(token) for token in lines[0].split())
    board = [[int(token) for token in lines[1 + index].split()] for index in range(row_count)]
    for row_index in range(row_count):
        for column_index in range(column_count):
            live_neighbours = 0
            for row_offset in (-1, 0, 1):
                for column_offset in (-1, 0, 1):
                    if row_offset == 0 and column_offset == 0:
                        continue
                    neighbour_row = row_index + row_offset
                    neighbour_column = column_index + column_offset
                    is_inside = (
                        0 <= neighbour_row < row_count and 0 <= neighbour_column < column_count
                    )
                    if is_inside:
                        live_neighbours += board[neighbour_row][neighbour_column] & 1
            is_alive = board[row_index][column_index] & 1 == 1
            stays_alive = live_neighbours in (2, 3) if is_alive else live_neighbours == 3
            if stays_alive:
                board[row_index][column_index] |= 2
    for row_index in range(row_count):
        for column_index in range(column_count):
            board[row_index][column_index] >>= 1
    return "\n".join(" ".join(str(value) for value in row) for row in board)


def brute_game_of_life(stdin_text: str) -> str:
    """Advance a life board one generation by writing into a separate board.

    Parameters
    ----------
    stdin_text : str
        Line one holds the row and column counts, then that many rows of 0 and 1.

    Returns
    -------
    str
        The next generation, one space-separated row per line.
    """
    lines = stdin_text.split("\n")
    row_count, column_count = (int(token) for token in lines[0].split())
    board = [[int(token) for token in lines[1 + index].split()] for index in range(row_count)]
    next_board = [[0] * column_count for _ in range(row_count)]
    for row_index in range(row_count):
        for column_index in range(column_count):
            neighbours = [
                board[neighbour_row][neighbour_column]
                for neighbour_row in range(max(0, row_index - 1), min(row_count, row_index + 2))
                for neighbour_column in range(
                    max(0, column_index - 1), min(column_count, column_index + 2)
                )
                if (neighbour_row, neighbour_column) != (row_index, column_index)
            ]
            live_neighbours = sum(neighbours)
            if board[row_index][column_index] == 1:
                next_board[row_index][column_index] = 1 if live_neighbours in (2, 3) else 0
            else:
                next_board[row_index][column_index] = 1 if live_neighbours == 3 else 0
    return "\n".join(" ".join(str(value) for value in row) for row in next_board)


VALID_SUDOKU_BOARD = (
    "5 3 . . 7 . . . .\n"
    "6 . . 1 9 5 . . .\n"
    ". . 8 . . . 6 . .\n"
    "8 . . . 6 . . . 3\n"
    "4 . . 8 . 3 . . 1\n"
    "7 . . . 2 . . . 6\n"
    ". 6 . . . . 2 8 .\n"
    ". . . 4 1 9 . . 5\n"
    ". . . . 8 . . 7 9"
)

COLUMN_CLASH_SUDOKU_BOARD = (
    "8 3 . . 7 . . . .\n"
    "6 . . 1 9 5 . . .\n"
    ". . 9 . . . 6 . .\n"
    "8 . . . 6 . . . 3\n"
    "4 . . 8 . 3 . . 1\n"
    "7 . . . 2 . . . 6\n"
    ". 6 . . . . 2 8 .\n"
    ". . . 4 1 9 . . 5\n"
    ". . . . 8 . . 7 9"
)

EMPTY_SUDOKU_BOARD = "\n".join(" ".join("." for _ in range(9)) for _ in range(9))

ROW_CLASH_SUDOKU_BOARD = "\n".join(
    ["1 1 . . . . . . ."] + [" ".join("." for _ in range(9)) for _ in range(8)]
)

BOX_CLASH_SUDOKU_BOARD = "\n".join(
    ["4 . . . . . . . .", ". 4 . . . . . . ."]
    + [" ".join("." for _ in range(9)) for _ in range(7)]
)


PROBLEMS: list[dict[str, Any]] = [
    {
        "title": "Valid Palindrome",
        "level": "Easy",
        "topics": "String, Two Pointers",
        "companies": "Amazon, Microsoft, Adobe",
        "description": (
            "A phrase counts as a palindrome when, after dropping every character that is "
            "not a letter or a digit and lowering the case of the letters that remain, the "
            "text reads the same from the front and from the back. Decide whether the given "
            "phrase is a palindrome.\n"
            "\n"
            "**Input**\n"
            "\n"
            "A single line holding the phrase. The whole line is the phrase, inner spaces "
            "included, so do not split it on whitespace. The phrase never starts or ends "
            "with a space.\n"
            "\n"
            "**Output**\n"
            "\n"
            "Print `true` when the phrase is a palindrome and `false` otherwise, in lower "
            "case. A phrase with no letters or digits at all counts as a palindrome.\n"
            "\n"
        ),
        "examples": (
            "```\n"
            "Input\n"
            "A man, a plan, a canal: Panama\n"
            "\n"
            "Output\n"
            "true\n"
            "```\n"
            "\n"
            "```\n"
            "Input\n"
            "race a car\n"
            "\n"
            "Output\n"
            "false\n"
            "```\n"
            "\n"
        ),
        "constraints": (
            "- The phrase holds between 1 and 200000 characters.\n"
            "- Every character is printable ASCII.\n"
            "- The phrase has no leading or trailing spaces.\n"
            "\n"
        ),
        "inputs": [
            "A man, a plan, a canal: Panama",
            "race a car",
            "a",
            ".,",
            "0P",
            "Was it a car or a cat I saw?",
        ],
        "solve": solve_valid_palindrome,
        "brute": brute_valid_palindrome,
    },
    {
        "title": "Is Subsequence",
        "level": "Easy",
        "topics": "String, Two Pointers, Dynamic Programming",
        "companies": "Google, Meta, Bloomberg",
        "description": (
            "One string is a subsequence of another when you can delete some characters of "
            "the longer string, without reordering what is left, and end up with the shorter "
            "one. Decide whether the first string is a subsequence of the second.\n"
            "\n"
            "**Input**\n"
            "\n"
            "Line 1: the candidate string.\n"
            "\n"
            "Line 2: the host string.\n"
            "\n"
            "**Output**\n"
            "\n"
            "Print `true` when the candidate is a subsequence of the host and `false` "
            "otherwise, in lower case.\n"
            "\n"
        ),
        "examples": (
            "```\n"
            "Input\n"
            "abc\n"
            "ahbgdc\n"
            "\n"
            "Output\n"
            "true\n"
            "```\n"
            "\n"
            "```\n"
            "Input\n"
            "axc\n"
            "ahbgdc\n"
            "\n"
            "Output\n"
            "false\n"
            "```\n"
            "\n"
        ),
        "constraints": (
            "- Each string holds between 1 and 100000 lower case English letters.\n"
            "- Neither line is blank.\n"
            "\n"
        ),
        "inputs": [
            "abc\nahbgdc",
            "axc\nahbgdc",
            "a\na",
            "b\na",
            "aaa\naaaa",
            "abcde\nabcde",
        ],
        "solve": solve_is_subsequence,
        "brute": brute_is_subsequence,
    },
    {
        "title": "Two Sum II - Input Array Is Sorted",
        "level": "Medium",
        "topics": "Array, Two Pointers, Binary Search",
        "companies": "Amazon, Apple, Uber",
        "description": (
            "Given a list of integers already sorted from smallest to largest, find two "
            "different positions whose values add up to a target.\n"
            "\n"
            "**Input**\n"
            "\n"
            "Line 1: two integers, the count of values and the target.\n"
            "\n"
            "Line 2: that many integers in non-decreasing order, separated by spaces.\n"
            "\n"
            "**Output**\n"
            "\n"
            "Print the two positions as one-based indices, smaller index first, separated by "
            "a single space. When more than one pair works, print the pair with the smallest "
            "first index, and among those the one with the smallest second index. Print `-1` "
            "when no pair adds up to the target.\n"
            "\n"
        ),
        "examples": (
            "```\n"
            "Input\n"
            "4 9\n"
            "2 7 11 15\n"
            "\n"
            "Output\n"
            "1 2\n"
            "```\n"
            "\n"
            "```\n"
            "Input\n"
            "2 5\n"
            "1 2\n"
            "\n"
            "Output\n"
            "-1\n"
            "```\n"
            "\n"
        ),
        "constraints": (
            "- The count of values is between 2 and 30000.\n"
            "- Each value and the target lie between -1000 and 1000.\n"
            "- The values are given in non-decreasing order.\n"
            "\n"
        ),
        "inputs": [
            "4 9\n2 7 11 15",
            "3 6\n2 3 4",
            "2 -1\n-1 0",
            "2 5\n1 2",
            "5 -6\n-5 -3 -2 -1 4",
            "4 0\n0 0 0 0",
        ],
        "solve": solve_two_sum_ii_input_array_is_sorted,
        "brute": brute_two_sum_ii_input_array_is_sorted,
    },
    {
        "title": "Container With Most Water",
        "level": "Medium",
        "topics": "Array, Two Pointers, Greedy",
        "companies": "Amazon, Meta, Goldman Sachs",
        "description": (
            "Each value in the list is the height of a vertical line standing at that "
            "position, one unit apart. Pick two lines so that the rectangle they form with "
            "the horizontal axis holds the most water. The water level is capped by the "
            "shorter of the two lines, and the width is the distance between their "
            "positions.\n"
            "\n"
            "**Input**\n"
            "\n"
            "Line 1: one integer, the number of lines.\n"
            "\n"
            "Line 2: that many non-negative integers, the heights, separated by spaces.\n"
            "\n"
            "**Output**\n"
            "\n"
            "Print the largest area as a single integer.\n"
            "\n"
        ),
        "examples": (
            "```\n"
            "Input\n"
            "9\n"
            "1 8 6 2 5 4 8 3 7\n"
            "\n"
            "Output\n"
            "49\n"
            "```\n"
            "\n"
            "```\n"
            "Input\n"
            "2\n"
            "1 1\n"
            "\n"
            "Output\n"
            "1\n"
            "```\n"
            "\n"
        ),
        "constraints": (
            "- The number of lines is between 2 and 100000.\n"
            "- Each height lies between 0 and 10000.\n"
            "\n"
        ),
        "inputs": [
            "9\n1 8 6 2 5 4 8 3 7",
            "2\n1 1",
            "5\n4 4 4 4 4",
            "3\n0 0 0",
            "6\n1 2 4 3 7 5",
            "4\n2 3 10 5",
        ],
        "solve": solve_container_with_most_water,
        "brute": brute_container_with_most_water,
    },
    {
        "title": "3Sum",
        "level": "Medium",
        "topics": "Array, Two Pointers, Sorting",
        "companies": "Amazon, Microsoft, Meta",
        "description": (
            "Find every group of three values in the list that adds up to zero. Two groups "
            "count as the same when they use the same multiset of values, so each distinct "
            "combination of values is reported once even if the list repeats it.\n"
            "\n"
            "**Input**\n"
            "\n"
            "Line 1: one integer, the number of values.\n"
            "\n"
            "Line 2: that many integers separated by spaces.\n"
            "\n"
            "**Output**\n"
            "\n"
            "Print one triplet per line. Inside a triplet the three values are sorted from "
            "smallest to largest and separated by single spaces. The lines themselves are "
            "sorted lexicographically, that is by first value, then second, then third. "
            "Print `none` when no triplet adds up to zero.\n"
            "\n"
        ),
        "examples": (
            "```\n"
            "Input\n"
            "6\n"
            "-1 0 1 2 -1 -4\n"
            "\n"
            "Output\n"
            "-1 -1 2\n"
            "-1 0 1\n"
            "```\n"
            "\n"
            "```\n"
            "Input\n"
            "3\n"
            "1 2 3\n"
            "\n"
            "Output\n"
            "none\n"
            "```\n"
            "\n"
        ),
        "constraints": (
            "- The number of values is between 1 and 3000.\n"
            "- Each value lies between -100000 and 100000.\n"
            "\n"
        ),
        "inputs": [
            "6\n-1 0 1 2 -1 -4",
            "3\n0 0 0",
            "3\n1 2 3",
            "1\n5",
            "7\n-2 0 1 1 2 -1 -1",
            "4\n0 0 0 0",
        ],
        "solve": solve_3sum,
        "brute": brute_3sum,
    },
    {
        "title": "Minimum Size Subarray Sum",
        "level": "Medium",
        "topics": "Array, Sliding Window, Prefix Sum",
        "companies": "Amazon, Google, Bloomberg",
        "description": (
            "Find the shortest run of neighbouring values whose sum is at least the target. "
            "A run must be contiguous, and its length is the count of values it covers.\n"
            "\n"
            "**Input**\n"
            "\n"
            "Line 1: two integers, the count of values and the target.\n"
            "\n"
            "Line 2: that many positive integers separated by spaces.\n"
            "\n"
            "**Output**\n"
            "\n"
            "Print the length of the shortest qualifying run as a single integer. Print `0` "
            "when no run reaches the target.\n"
            "\n"
        ),
        "examples": (
            "```\n"
            "Input\n"
            "6 7\n"
            "2 3 1 2 4 3\n"
            "\n"
            "Output\n"
            "2\n"
            "```\n"
            "\n"
            "```\n"
            "Input\n"
            "3 11\n"
            "1 1 1\n"
            "\n"
            "Output\n"
            "0\n"
            "```\n"
            "\n"
        ),
        "constraints": (
            "- The count of values is between 1 and 100000.\n"
            "- Each value lies between 1 and 10000.\n"
            "- The target lies between 1 and 1000000000.\n"
            "\n"
        ),
        "inputs": [
            "6 7\n2 3 1 2 4 3",
            "2 4\n1 4",
            "3 11\n1 1 1",
            "1 1\n1",
            "5 6\n2 2 2 2 2",
            "4 15\n1 2 3 4",
        ],
        "solve": solve_minimum_size_subarray_sum,
        "brute": brute_minimum_size_subarray_sum,
    },
    {
        "title": "Longest Substring Without Repeating Characters",
        "level": "Medium",
        "topics": "String, Sliding Window, Hash Table",
        "companies": "Amazon, Adobe, Bloomberg",
        "description": (
            "Find the longest stretch of neighbouring characters in the string in which no "
            "character appears twice. Only the length is asked for, not the stretch "
            "itself.\n"
            "\n"
            "**Input**\n"
            "\n"
            "A single line holding the string. It contains no spaces.\n"
            "\n"
            "**Output**\n"
            "\n"
            "Print the length of the longest repeat-free stretch as a single integer.\n"
            "\n"
        ),
        "examples": (
            "```\n"
            "Input\n"
            "abcabcbb\n"
            "\n"
            "Output\n"
            "3\n"
            "```\n"
            "\n"
            "```\n"
            "Input\n"
            "pwwkew\n"
            "\n"
            "Output\n"
            "3\n"
            "```\n"
            "\n"
        ),
        "constraints": (
            "- The string holds between 1 and 50000 characters.\n"
            "- Every character is a printable ASCII character other than a space.\n"
            "\n"
        ),
        "inputs": [
            "abcabcbb",
            "bbbbb",
            "pwwkew",
            "a",
            "abcdef",
            "dvdf",
        ],
        "solve": solve_longest_substring_without_repeating_characters,
        "brute": brute_longest_substring_without_repeating_characters,
    },
    {
        "title": "Substring with Concatenation of All Words",
        "level": "Hard",
        "topics": "String, Sliding Window, Hash Table",
        "companies": "Amazon, Meta, Microsoft",
        "description": (
            "Every word in the word list has the same length. A window of the text is a "
            "match when it is exactly the words of the list glued together in some order, "
            "each word used as many times as it appears in the list. Find where every such "
            "window starts.\n"
            "\n"
            "**Input**\n"
            "\n"
            "Line 1: the text, a string with no spaces.\n"
            "\n"
            "Line 2: the words, separated by single spaces.\n"
            "\n"
            "**Output**\n"
            "\n"
            "Print the zero-based starting positions of the matching windows in ascending "
            "order, separated by single spaces, on one line. Print `none` when no window "
            "matches.\n"
            "\n"
        ),
        "examples": (
            "```\n"
            "Input\n"
            "barfoothefoobarman\n"
            "foo bar\n"
            "\n"
            "Output\n"
            "0 9\n"
            "```\n"
            "\n"
            "```\n"
            "Input\n"
            "wordgoodgoodgoodbestword\n"
            "word good best word\n"
            "\n"
            "Output\n"
            "none\n"
            "```\n"
            "\n"
        ),
        "constraints": (
            "- The text holds between 1 and 10000 lower case English letters.\n"
            "- There are between 1 and 5000 words.\n"
            "- Every word holds between 1 and 30 lower case English letters.\n"
            "- All words have the same length.\n"
            "\n"
        ),
        "inputs": [
            "barfoothefoobarman\nfoo bar",
            "wordgoodgoodgoodbestword\nword good best word",
            "barfoofoobarthefoobarman\nbar foo the",
            "aaa\na a",
            "ab\nab",
            "aaaa\naa aa",
        ],
        "solve": solve_substring_with_concatenation_of_all_words,
        "brute": brute_substring_with_concatenation_of_all_words,
    },
    {
        "title": "Minimum Window Substring",
        "level": "Hard",
        "topics": "String, Sliding Window, Hash Table",
        "companies": "Amazon, Meta, LinkedIn",
        "description": (
            "Find the shortest stretch of neighbouring characters in the text that contains "
            "every character of the pattern, counting repeats: a character needed three "
            "times must appear at least three times inside the stretch. Extra characters are "
            "allowed.\n"
            "\n"
            "**Input**\n"
            "\n"
            "Line 1: the text, a string with no spaces.\n"
            "\n"
            "Line 2: the pattern, a string with no spaces.\n"
            "\n"
            "**Output**\n"
            "\n"
            "Print the shortest covering stretch exactly as it appears in the text. When "
            "several stretches tie on length, print the one that starts furthest to the "
            "left. Print `none` when no stretch covers the pattern.\n"
            "\n"
        ),
        "examples": (
            "```\n"
            "Input\n"
            "ADOBECODEBANC\n"
            "ABC\n"
            "\n"
            "Output\n"
            "BANC\n"
            "```\n"
            "\n"
            "```\n"
            "Input\n"
            "a\n"
            "aa\n"
            "\n"
            "Output\n"
            "none\n"
            "```\n"
            "\n"
        ),
        "constraints": (
            "- The text and the pattern each hold between 1 and 100000 characters.\n"
            "- Every character is an English letter, upper or lower case.\n"
            "\n"
        ),
        "inputs": [
            "ADOBECODEBANC\nABC",
            "a\na",
            "a\naa",
            "aa\naa",
            "bba\nab",
            "cabwefgewcwaefgcf\ncae",
        ],
        "solve": solve_minimum_window_substring,
        "brute": brute_minimum_window_substring,
    },
    {
        "title": "Valid Sudoku",
        "level": "Medium",
        "topics": "Array, Matrix, Hash Table",
        "companies": "Amazon, Apple, Uber",
        "description": (
            "A partially filled 9 by 9 Sudoku board is valid when no digit repeats inside "
            "any single row, inside any single column, or inside any of the nine 3 by 3 "
            "blocks. Empty cells are ignored, and the board does not have to be solvable.\n"
            "\n"
            "**Input**\n"
            "\n"
            "Nine lines, each holding nine cells separated by single spaces. A cell is "
            "either a digit from `1` to `9` or a dot `.` for an empty cell.\n"
            "\n"
            "**Output**\n"
            "\n"
            "Print `true` when the board breaks no rule and `false` otherwise, in lower "
            "case.\n"
            "\n"
        ),
        "examples": (
            "```\n"
            "Input\n" + VALID_SUDOKU_BOARD + "\n"
            "\n"
            "Output\n"
            "true\n"
            "```\n"
            "\n"
            "```\n"
            "Input\n" + ROW_CLASH_SUDOKU_BOARD + "\n"
            "\n"
            "Output\n"
            "false\n"
            "```\n"
            "\n"
        ),
        "constraints": (
            "- The board is always exactly 9 rows of 9 cells.\n"
            "- Every cell is a digit from 1 to 9 or a dot.\n"
            "\n"
        ),
        "inputs": [
            VALID_SUDOKU_BOARD,
            COLUMN_CLASH_SUDOKU_BOARD,
            EMPTY_SUDOKU_BOARD,
            ROW_CLASH_SUDOKU_BOARD,
            BOX_CLASH_SUDOKU_BOARD,
        ],
        "solve": solve_valid_sudoku,
        "brute": brute_valid_sudoku,
    },
    {
        "title": "Spiral Matrix",
        "level": "Medium",
        "topics": "Array, Matrix, Simulation",
        "companies": "Amazon, Microsoft, Walmart",
        "description": (
            "Walk the matrix in a clockwise spiral: start at the top-left cell, run along "
            "the top row to the right, down the right column, back along the bottom row to "
            "the left, up the left column, then repeat on the ring that is left over. "
            "Report the values in the order they are visited.\n"
            "\n"
            "**Input**\n"
            "\n"
            "Line 1: two integers, the number of rows and the number of columns.\n"
            "\n"
            "Line 2 onwards: that many rows, each holding the row's cells as integers "
            "separated by single spaces.\n"
            "\n"
            "**Output**\n"
            "\n"
            "Print every value in spiral order on one line, separated by single spaces.\n"
            "\n"
        ),
        "examples": (
            "```\n"
            "Input\n"
            "3 3\n"
            "1 2 3\n"
            "4 5 6\n"
            "7 8 9\n"
            "\n"
            "Output\n"
            "1 2 3 6 9 8 7 4 5\n"
            "```\n"
            "\n"
            "```\n"
            "Input\n"
            "3 4\n"
            "1 2 3 4\n"
            "5 6 7 8\n"
            "9 10 11 12\n"
            "\n"
            "Output\n"
            "1 2 3 4 8 12 11 10 9 5 6 7\n"
            "```\n"
            "\n"
        ),
        "constraints": (
            "- The number of rows and columns are each between 1 and 10.\n"
            "- Each cell lies between -100 and 100.\n"
            "\n"
        ),
        "inputs": [
            "3 3\n1 2 3\n4 5 6\n7 8 9",
            "3 4\n1 2 3 4\n5 6 7 8\n9 10 11 12",
            "1 1\n7",
            "1 5\n1 2 3 4 5",
            "4 1\n1\n2\n3\n4",
            "2 2\n-1 -1\n-1 -1",
        ],
        "solve": solve_spiral_matrix,
        "brute": brute_spiral_matrix,
    },
    {
        "title": "Rotate Image",
        "level": "Medium",
        "topics": "Array, Matrix, Math",
        "companies": "Amazon, Apple, Cisco",
        "description": (
            "Turn a square matrix a quarter turn clockwise, so the first row becomes the "
            "last column, the second row becomes the second to last column, and so on.\n"
            "\n"
            "**Input**\n"
            "\n"
            "Line 1: one integer, the side length of the matrix.\n"
            "\n"
            "Line 2 onwards: that many rows, each holding that many integers separated by "
            "single spaces.\n"
            "\n"
            "**Output**\n"
            "\n"
            "Print the rotated matrix, one row per line, the values of a row separated by "
            "single spaces.\n"
            "\n"
        ),
        "examples": (
            "```\n"
            "Input\n"
            "3\n"
            "1 2 3\n"
            "4 5 6\n"
            "7 8 9\n"
            "\n"
            "Output\n"
            "7 4 1\n"
            "8 5 2\n"
            "9 6 3\n"
            "```\n"
            "\n"
            "```\n"
            "Input\n"
            "1\n"
            "5\n"
            "\n"
            "Output\n"
            "5\n"
            "```\n"
            "\n"
        ),
        "constraints": (
            "- The side length is between 1 and 20.\n"
            "- Each cell lies between -1000 and 1000.\n"
            "\n"
        ),
        "inputs": [
            "3\n1 2 3\n4 5 6\n7 8 9",
            "1\n5",
            "2\n-1 -2\n-3 -4",
            "4\n5 1 9 11\n2 4 8 10\n13 3 6 7\n15 14 12 16",
            "2\n7 7\n7 7",
        ],
        "solve": solve_rotate_image,
        "brute": brute_rotate_image,
    },
    {
        "title": "Set Matrix Zeroes",
        "level": "Medium",
        "topics": "Array, Matrix, Hash Table",
        "companies": "Amazon, Microsoft, Oracle",
        "description": (
            "Wherever the matrix holds a zero, the whole row and the whole column through "
            "that cell become zero. All zeroes present in the original matrix trigger this "
            "at once, so zeroes written by the process do not spread further.\n"
            "\n"
            "**Input**\n"
            "\n"
            "Line 1: two integers, the number of rows and the number of columns.\n"
            "\n"
            "Line 2 onwards: that many rows, each holding the row's cells as integers "
            "separated by single spaces.\n"
            "\n"
            "**Output**\n"
            "\n"
            "Print the updated matrix, one row per line, the values of a row separated by "
            "single spaces.\n"
            "\n"
        ),
        "examples": (
            "```\n"
            "Input\n"
            "3 3\n"
            "1 1 1\n"
            "1 0 1\n"
            "1 1 1\n"
            "\n"
            "Output\n"
            "1 0 1\n"
            "0 0 0\n"
            "1 0 1\n"
            "```\n"
            "\n"
            "```\n"
            "Input\n"
            "3 4\n"
            "0 1 2 0\n"
            "3 4 5 2\n"
            "1 3 1 5\n"
            "\n"
            "Output\n"
            "0 0 0 0\n"
            "0 4 5 0\n"
            "0 3 1 0\n"
            "```\n"
            "\n"
        ),
        "constraints": (
            "- The number of rows and columns are each between 1 and 200.\n"
            "- Each cell lies between -2147483648 and 2147483647.\n"
            "\n"
        ),
        "inputs": [
            "3 3\n1 1 1\n1 0 1\n1 1 1",
            "3 4\n0 1 2 0\n3 4 5 2\n1 3 1 5",
            "1 1\n0",
            "1 1\n4",
            "2 2\n1 2\n3 4",
            "2 3\n0 0 0\n0 0 0",
        ],
        "solve": solve_set_matrix_zeroes,
        "brute": brute_set_matrix_zeroes,
    },
    {
        "title": "Game of Life",
        "level": "Medium",
        "topics": "Array, Matrix, Simulation",
        "companies": "Google, Amazon, Dropbox",
        "description": (
            "Each cell of the board is live, written `1`, or dead, written `0`. A cell has "
            "up to eight neighbours, counting diagonals, and cells outside the board do not "
            "exist. Every cell updates at the same time from the current board: a live cell "
            "with two or three live neighbours stays live and dies otherwise, and a dead "
            "cell with exactly three live neighbours becomes live. Report the board after "
            "one such update.\n"
            "\n"
            "**Input**\n"
            "\n"
            "Line 1: two integers, the number of rows and the number of columns.\n"
            "\n"
            "Line 2 onwards: that many rows, each holding the row's cells as `0` or `1` "
            "separated by single spaces.\n"
            "\n"
            "**Output**\n"
            "\n"
            "Print the next board, one row per line, the values of a row separated by single "
            "spaces.\n"
            "\n"
        ),
        "examples": (
            "```\n"
            "Input\n"
            "4 3\n"
            "0 1 0\n"
            "0 0 1\n"
            "1 1 1\n"
            "0 0 0\n"
            "\n"
            "Output\n"
            "0 0 0\n"
            "1 0 1\n"
            "0 1 1\n"
            "0 1 0\n"
            "```\n"
            "\n"
            "```\n"
            "Input\n"
            "2 2\n"
            "1 1\n"
            "1 1\n"
            "\n"
            "Output\n"
            "1 1\n"
            "1 1\n"
            "```\n"
            "\n"
        ),
        "constraints": (
            "- The number of rows and columns are each between 1 and 25.\n"
            "- Every cell is 0 or 1.\n"
            "\n"
        ),
        "inputs": [
            "4 3\n0 1 0\n0 0 1\n1 1 1\n0 0 0",
            "2 2\n1 1\n1 1",
            "1 1\n1",
            "1 1\n0",
            "3 3\n0 0 0\n0 0 0\n0 0 0",
            "3 3\n1 1 1\n1 1 1\n1 1 1",
        ],
        "solve": solve_game_of_life,
        "brute": brute_game_of_life,
    },
]
