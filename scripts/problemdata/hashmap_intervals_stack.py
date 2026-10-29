"""Problem specs for the hash map, interval and stack study group.

Every problem is a complete stdin-to-stdout task: the statement fixes the exact
input layout and the exact output bytes, since the editor opens with no starter
code and the judge compares stdout literally.
"""

from __future__ import annotations

import itertools
from collections import Counter
from typing import Any

# ---------------------------------------------------------------- Ransom Note


def solve_ransom_note(stdin_text: str) -> str:
    """Decide whether the note can be cut out of the magazine letters.

    Parameters
    ----------
    stdin_text : str
        Note on the first line, magazine on the second line.

    Returns
    -------
    str
        "true" when every note letter is available, otherwise "false".
    """
    note_line, magazine_line = stdin_text.strip().split("\n")[:2]
    note_counts = Counter(note_line.strip())
    magazine_counts = Counter(magazine_line.strip())
    is_buildable = all(
        magazine_counts[letter] >= needed for letter, needed in note_counts.items()
    )
    return "true" if is_buildable else "false"


def brute_ransom_note(stdin_text: str) -> str:
    """Decide the same question by consuming magazine letters one at a time.

    Parameters
    ----------
    stdin_text : str
        Note on the first line, magazine on the second line.

    Returns
    -------
    str
        "true" when every note letter is available, otherwise "false".
    """
    note_line, magazine_line = stdin_text.strip().split("\n")[:2]
    available_letters = list(magazine_line.strip())
    for letter in note_line.strip():
        if letter not in available_letters:
            return "false"
        available_letters.remove(letter)
    return "true"


# ------------------------------------------------------------ Isomorphic Strings


def solve_isomorphic_strings(stdin_text: str) -> str:
    """Decide whether two equal-length strings share one letter substitution.

    Parameters
    ----------
    stdin_text : str
        First string on line one, second string on line two.

    Returns
    -------
    str
        "true" when a one-to-one letter mapping exists, otherwise "false".
    """
    first_line, second_line = stdin_text.strip().split("\n")[:2]
    first_string = first_line.strip()
    second_string = second_line.strip()
    forward_mapping: dict[str, str] = {}
    backward_mapping: dict[str, str] = {}
    for first_letter, second_letter in zip(first_string, second_string):
        if forward_mapping.setdefault(first_letter, second_letter) != second_letter:
            return "false"
        if backward_mapping.setdefault(second_letter, first_letter) != first_letter:
            return "false"
    return "true"


def brute_isomorphic_strings(stdin_text: str) -> str:
    """Decide the same question by comparing first-occurrence index patterns.

    Parameters
    ----------
    stdin_text : str
        First string on line one, second string on line two.

    Returns
    -------
    str
        "true" when a one-to-one letter mapping exists, otherwise "false".
    """
    first_line, second_line = stdin_text.strip().split("\n")[:2]

    def index_pattern(text: str) -> tuple[int, ...]:
        """Replace each character by the position of its first appearance."""
        return tuple(text.index(character) for character in text)

    is_isomorphic = index_pattern(first_line.strip()) == index_pattern(second_line.strip())
    return "true" if is_isomorphic else "false"


# ----------------------------------------------------------------- Word Pattern


def solve_word_pattern(stdin_text: str) -> str:
    """Decide whether a letter pattern matches a sequence of words.

    Parameters
    ----------
    stdin_text : str
        Pattern on line one, space separated words on line two.

    Returns
    -------
    str
        "true" when a one-to-one letter to word mapping exists, otherwise "false".
    """
    pattern_line, words_line = stdin_text.strip().split("\n")[:2]
    pattern = pattern_line.strip()
    words = words_line.split()
    if len(pattern) != len(words):
        return "false"
    letter_to_word: dict[str, str] = {}
    word_to_letter: dict[str, str] = {}
    for letter, word in zip(pattern, words):
        if letter_to_word.setdefault(letter, word) != word:
            return "false"
        if word_to_letter.setdefault(word, letter) != letter:
            return "false"
    return "true"


def brute_word_pattern(stdin_text: str) -> str:
    """Decide the same question by normalising both sequences to label numbers.

    Parameters
    ----------
    stdin_text : str
        Pattern on line one, space separated words on line two.

    Returns
    -------
    str
        "true" when a one-to-one letter to word mapping exists, otherwise "false".
    """
    pattern_line, words_line = stdin_text.strip().split("\n")[:2]

    def label_sequence(items: list[str]) -> list[int]:
        """Number each item by the order in which it first shows up."""
        labels: dict[str, int] = {}
        return [labels.setdefault(item, len(labels)) for item in items]

    pattern_labels = label_sequence(list(pattern_line.strip()))
    word_labels = label_sequence(words_line.split())
    return "true" if pattern_labels == word_labels else "false"


# ---------------------------------------------------------------- Valid Anagram


def solve_valid_anagram(stdin_text: str) -> str:
    """Decide whether two strings use exactly the same letters.

    Parameters
    ----------
    stdin_text : str
        First string on line one, second string on line two.

    Returns
    -------
    str
        "true" when the strings are anagrams, otherwise "false".
    """
    first_line, second_line = stdin_text.strip().split("\n")[:2]
    is_anagram = Counter(first_line.strip()) == Counter(second_line.strip())
    return "true" if is_anagram else "false"


def brute_valid_anagram(stdin_text: str) -> str:
    """Decide the same question by comparing sorted letter sequences.

    Parameters
    ----------
    stdin_text : str
        First string on line one, second string on line two.

    Returns
    -------
    str
        "true" when the strings are anagrams, otherwise "false".
    """
    first_line, second_line = stdin_text.strip().split("\n")[:2]
    is_anagram = sorted(first_line.strip()) == sorted(second_line.strip())
    return "true" if is_anagram else "false"


# --------------------------------------------------------------- Group Anagrams


def solve_group_anagrams(stdin_text: str) -> str:
    """Group words that are anagrams of each other.

    Parameters
    ----------
    stdin_text : str
        Word count on line one, then that many words one per line.

    Returns
    -------
    str
        One group per line, words sorted inside a group, groups sorted by their
        first word.
    """
    lines = stdin_text.strip().split("\n")
    word_count = int(lines[0])
    words = [lines[offset + 1].strip() for offset in range(word_count)]
    groups_by_signature: dict[str, list[str]] = {}
    for word in words:
        signature = "".join(sorted(word))
        groups_by_signature.setdefault(signature, []).append(word)
    groups = [sorted(group) for group in groups_by_signature.values()]
    groups.sort(key=lambda group: group[0])
    return "\n".join(" ".join(group) for group in groups)


def brute_group_anagrams(stdin_text: str) -> str:
    """Group the same words by comparing every remaining word against a pivot.

    Parameters
    ----------
    stdin_text : str
        Word count on line one, then that many words one per line.

    Returns
    -------
    str
        One group per line, words sorted inside a group, groups sorted by their
        first word.
    """
    lines = stdin_text.strip().split("\n")
    word_count = int(lines[0])
    remaining_words = [lines[offset + 1].strip() for offset in range(word_count)]
    groups: list[list[str]] = []
    while remaining_words:
        pivot_word = remaining_words.pop(0)
        group = [pivot_word]
        leftovers: list[str] = []
        for candidate_word in remaining_words:
            if Counter(candidate_word) == Counter(pivot_word):
                group.append(candidate_word)
            else:
                leftovers.append(candidate_word)
        remaining_words = leftovers
        groups.append(sorted(group))
    groups.sort(key=lambda group: group[0])
    return "\n".join(" ".join(group) for group in groups)


# --------------------------------------------------------------------- Two Sum


def solve_two_sum(stdin_text: str) -> str:
    """Find the two positions whose values add up to the target.

    Parameters
    ----------
    stdin_text : str
        Count on line one, the values on line two, the target on line three.

    Returns
    -------
    str
        The two zero-based positions in ascending order, separated by a space.
    """
    lines = stdin_text.strip().split("\n")
    numbers = [int(token) for token in lines[1].split()]
    target = int(lines[2])
    position_by_value: dict[int, int] = {}
    for position, number in enumerate(numbers):
        complement = target - number
        if complement in position_by_value:
            return f"{position_by_value[complement]} {position}"
        position_by_value[number] = position
    return "-1 -1"


def brute_two_sum(stdin_text: str) -> str:
    """Find the same pair by testing every pair of positions.

    Parameters
    ----------
    stdin_text : str
        Count on line one, the values on line two, the target on line three.

    Returns
    -------
    str
        The two zero-based positions in ascending order, separated by a space.
    """
    lines = stdin_text.strip().split("\n")
    numbers = [int(token) for token in lines[1].split()]
    target = int(lines[2])
    for left_position in range(len(numbers)):
        for right_position in range(left_position + 1, len(numbers)):
            if numbers[left_position] + numbers[right_position] == target:
                return f"{left_position} {right_position}"
    return "-1 -1"


# ----------------------------------------------------------------- Happy Number


def solve_happy_number(stdin_text: str) -> str:
    """Decide whether repeated digit-square sums reach one.

    Parameters
    ----------
    stdin_text : str
        A single positive integer on one line.

    Returns
    -------
    str
        "true" when the process reaches one, otherwise "false".
    """
    current = int(stdin_text.strip())
    seen_values: set[int] = set()
    while current != 1 and current not in seen_values:
        seen_values.add(current)
        current = sum(int(digit) ** 2 for digit in str(current))
    return "true" if current == 1 else "false"


def brute_happy_number(stdin_text: str) -> str:
    """Decide the same question by running the process a fixed number of steps.

    Parameters
    ----------
    stdin_text : str
        A single positive integer on one line.

    Returns
    -------
    str
        "true" when the process reaches one, otherwise "false".
    """
    current = int(stdin_text.strip())
    for _iteration in range(1000):
        if current == 1:
            return "true"
        current = sum(int(digit) ** 2 for digit in str(current))
    return "true" if current == 1 else "false"


# ---------------------------------------------------------- Contains Duplicate II


def solve_contains_duplicate_ii(stdin_text: str) -> str:
    """Decide whether an equal pair of values sits within distance k.

    Parameters
    ----------
    stdin_text : str
        Count on line one, the values on line two, the distance k on line three.

    Returns
    -------
    str
        "true" when such a pair exists, otherwise "false".
    """
    lines = stdin_text.strip().split("\n")
    numbers = [int(token) for token in lines[1].split()]
    max_distance = int(lines[2])
    last_position_by_value: dict[int, int] = {}
    for position, number in enumerate(numbers):
        previous_position = last_position_by_value.get(number)
        if previous_position is not None and position - previous_position <= max_distance:
            return "true"
        last_position_by_value[number] = position
    return "false"


def brute_contains_duplicate_ii(stdin_text: str) -> str:
    """Decide the same question by testing every pair of positions.

    Parameters
    ----------
    stdin_text : str
        Count on line one, the values on line two, the distance k on line three.

    Returns
    -------
    str
        "true" when such a pair exists, otherwise "false".
    """
    lines = stdin_text.strip().split("\n")
    numbers = [int(token) for token in lines[1].split()]
    max_distance = int(lines[2])
    for left_position in range(len(numbers)):
        for right_position in range(left_position + 1, len(numbers)):
            is_close_pair = right_position - left_position <= max_distance
            if is_close_pair and numbers[left_position] == numbers[right_position]:
                return "true"
    return "false"


# -------------------------------------------------- Longest Consecutive Sequence


def solve_longest_consecutive_sequence(stdin_text: str) -> str:
    """Measure the longest run of consecutive integers present in the values.

    Parameters
    ----------
    stdin_text : str
        Count on line one, the values on line two.

    Returns
    -------
    str
        Length of the longest consecutive run.
    """
    lines = stdin_text.strip().split("\n")
    present_values = {int(token) for token in lines[1].split()}
    longest_run = 0
    for value in present_values:
        if value - 1 in present_values:
            continue
        run_length = 1
        while value + run_length in present_values:
            run_length += 1
        longest_run = max(longest_run, run_length)
    return str(longest_run)


def brute_longest_consecutive_sequence(stdin_text: str) -> str:
    """Measure the same run by scanning the sorted distinct values.

    Parameters
    ----------
    stdin_text : str
        Count on line one, the values on line two.

    Returns
    -------
    str
        Length of the longest consecutive run.
    """
    lines = stdin_text.strip().split("\n")
    sorted_values = sorted({int(token) for token in lines[1].split()})
    longest_run = 0
    current_run = 0
    previous_value: int | None = None
    for value in sorted_values:
        if previous_value is not None and value == previous_value + 1:
            current_run += 1
        else:
            current_run = 1
        previous_value = value
        longest_run = max(longest_run, current_run)
    return str(longest_run)


# --------------------------------------------------------------- Summary Ranges


def solve_summary_ranges(stdin_text: str) -> str:
    """Collapse a sorted list of distinct integers into consecutive ranges.

    Parameters
    ----------
    stdin_text : str
        Count on line one, the sorted distinct values on line two.

    Returns
    -------
    str
        One range per line, written "a" for a single value and "a->b" otherwise.
    """
    lines = stdin_text.strip().split("\n")
    numbers = [int(token) for token in lines[1].split()]

    def format_range(range_start: int, range_end: int) -> str:
        """Render one range in the single-value or arrow form."""
        return str(range_start) if range_start == range_end else f"{range_start}->{range_end}"

    pieces: list[str] = []
    range_start = numbers[0]
    previous_number = numbers[0]
    for number in numbers[1:]:
        if number == previous_number + 1:
            previous_number = number
            continue
        pieces.append(format_range(range_start, previous_number))
        range_start = number
        previous_number = number
    pieces.append(format_range(range_start, previous_number))
    return "\n".join(pieces)


def brute_summary_ranges(stdin_text: str) -> str:
    """Build the same ranges by growing each run from its smallest member.

    Parameters
    ----------
    stdin_text : str
        Count on line one, the sorted distinct values on line two.

    Returns
    -------
    str
        One range per line, written "a" for a single value and "a->b" otherwise.
    """
    lines = stdin_text.strip().split("\n")
    numbers = [int(token) for token in lines[1].split()]
    present_values = set(numbers)
    pieces: list[str] = []
    for number in numbers:
        if number - 1 in present_values:
            continue
        range_end = number
        while range_end + 1 in present_values:
            range_end += 1
        pieces.append(str(number) if range_end == number else f"{number}->{range_end}")
    return "\n".join(pieces)


# -------------------------------------------------------------- Merge Intervals


def solve_merge_intervals(stdin_text: str) -> str:
    """Merge every pair of overlapping or touching intervals.

    Parameters
    ----------
    stdin_text : str
        Interval count on line one, then that many "start end" lines.

    Returns
    -------
    str
        Merged intervals sorted by start, one "start end" per line.
    """
    lines = stdin_text.strip().split("\n")
    interval_count = int(lines[0])
    intervals = [
        tuple(int(token) for token in lines[offset + 1].split())
        for offset in range(interval_count)
    ]
    merged: list[list[int]] = []
    for start, end in sorted(intervals):
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return "\n".join(f"{start} {end}" for start, end in merged)


def brute_merge_intervals(stdin_text: str) -> str:
    """Merge the same intervals by fusing any overlapping pair until none remain.

    Parameters
    ----------
    stdin_text : str
        Interval count on line one, then that many "start end" lines.

    Returns
    -------
    str
        Merged intervals sorted by start, one "start end" per line.
    """
    lines = stdin_text.strip().split("\n")
    interval_count = int(lines[0])
    intervals = [
        [int(token) for token in lines[offset + 1].split()] for offset in range(interval_count)
    ]
    has_changed = True
    while has_changed:
        has_changed = False
        for left_index in range(len(intervals)):
            for right_index in range(left_index + 1, len(intervals)):
                left_interval = intervals[left_index]
                right_interval = intervals[right_index]
                is_overlapping = (
                    left_interval[0] <= right_interval[1] and right_interval[0] <= left_interval[1]
                )
                if is_overlapping:
                    intervals[left_index] = [
                        min(left_interval[0], right_interval[0]),
                        max(left_interval[1], right_interval[1]),
                    ]
                    intervals.pop(right_index)
                    has_changed = True
                    break
            if has_changed:
                break
    intervals.sort()
    return "\n".join(f"{start} {end}" for start, end in intervals)


# --------------------------------------------------------------- Insert Interval


def solve_insert_interval(stdin_text: str) -> str:
    """Insert one interval into a sorted disjoint list and merge what overlaps.

    Parameters
    ----------
    stdin_text : str
        Interval count on line one, then that many "start end" lines, then the
        interval to insert on its own line.

    Returns
    -------
    str
        Resulting intervals sorted by start, one "start end" per line.
    """
    lines = stdin_text.strip().split("\n")
    interval_count = int(lines[0])
    intervals = [
        [int(token) for token in lines[offset + 1].split()] for offset in range(interval_count)
    ]
    new_start, new_end = (int(token) for token in lines[interval_count + 1].split())
    result: list[list[int]] = []
    position = 0
    while position < interval_count and intervals[position][1] < new_start:
        result.append(intervals[position])
        position += 1
    while position < interval_count and intervals[position][0] <= new_end:
        new_start = min(new_start, intervals[position][0])
        new_end = max(new_end, intervals[position][1])
        position += 1
    result.append([new_start, new_end])
    result.extend(intervals[position:])
    return "\n".join(f"{start} {end}" for start, end in result)


def brute_insert_interval(stdin_text: str) -> str:
    """Append the interval, then fuse any overlapping pair until none remain.

    Parameters
    ----------
    stdin_text : str
        Interval count on line one, then that many "start end" lines, then the
        interval to insert on its own line.

    Returns
    -------
    str
        Resulting intervals sorted by start, one "start end" per line.
    """
    lines = stdin_text.strip().split("\n")
    interval_count = int(lines[0])
    intervals = [
        [int(token) for token in lines[offset + 1].split()] for offset in range(interval_count)
    ]
    intervals.append([int(token) for token in lines[interval_count + 1].split()])
    has_changed = True
    while has_changed:
        has_changed = False
        for left_index in range(len(intervals)):
            for right_index in range(left_index + 1, len(intervals)):
                left_interval = intervals[left_index]
                right_interval = intervals[right_index]
                is_overlapping = (
                    left_interval[0] <= right_interval[1] and right_interval[0] <= left_interval[1]
                )
                if is_overlapping:
                    intervals[left_index] = [
                        min(left_interval[0], right_interval[0]),
                        max(left_interval[1], right_interval[1]),
                    ]
                    intervals.pop(right_index)
                    has_changed = True
                    break
            if has_changed:
                break
    intervals.sort()
    return "\n".join(f"{start} {end}" for start, end in intervals)


# ----------------------------------- Minimum Number of Arrows to Burst Balloons


def solve_minimum_number_of_arrows_to_burst_balloons(stdin_text: str) -> str:
    """Count the fewest vertical arrows that pierce every balloon.

    Parameters
    ----------
    stdin_text : str
        Balloon count on line one, then that many "start end" lines.

    Returns
    -------
    str
        The minimum number of arrows.
    """
    lines = stdin_text.strip().split("\n")
    balloon_count = int(lines[0])
    balloons = [
        [int(token) for token in lines[offset + 1].split()] for offset in range(balloon_count)
    ]
    balloons.sort(key=lambda balloon: balloon[1])
    arrow_count = 0
    last_arrow_position = 0
    for balloon in balloons:
        if arrow_count == 0 or balloon[0] > last_arrow_position:
            arrow_count += 1
            last_arrow_position = balloon[1]
    return str(arrow_count)


def brute_minimum_number_of_arrows_to_burst_balloons(stdin_text: str) -> str:
    """Search arrow sets of growing size, drawn from the balloon right edges.

    Parameters
    ----------
    stdin_text : str
        Balloon count on line one, then that many "start end" lines.

    Returns
    -------
    str
        The minimum number of arrows.
    """
    lines = stdin_text.strip().split("\n")
    balloon_count = int(lines[0])
    balloons = [
        [int(token) for token in lines[offset + 1].split()] for offset in range(balloon_count)
    ]
    candidate_positions = sorted({balloon[1] for balloon in balloons})
    for arrow_count in range(1, len(candidate_positions) + 1):
        for chosen_positions in itertools.combinations(candidate_positions, arrow_count):
            is_covering = all(
                any(balloon[0] <= position <= balloon[1] for position in chosen_positions)
                for balloon in balloons
            )
            if is_covering:
                return str(arrow_count)
    return str(balloon_count)


# ------------------------------------------------------------ Valid Parentheses


def solve_valid_parentheses(stdin_text: str) -> str:
    """Decide whether a bracket string is correctly nested and closed.

    Parameters
    ----------
    stdin_text : str
        One line holding only the characters ()[]{}.

    Returns
    -------
    str
        "true" when the brackets balance, otherwise "false".
    """
    brackets = stdin_text.strip()
    closing_to_opening = {")": "(", "]": "[", "}": "{"}
    open_stack: list[str] = []
    for bracket in brackets:
        if bracket in closing_to_opening:
            if not open_stack or open_stack.pop() != closing_to_opening[bracket]:
                return "false"
        else:
            open_stack.append(bracket)
    return "true" if not open_stack else "false"


def brute_valid_parentheses(stdin_text: str) -> str:
    """Decide the same question by erasing adjacent matching pairs repeatedly.

    Parameters
    ----------
    stdin_text : str
        One line holding only the characters ()[]{}.

    Returns
    -------
    str
        "true" when the brackets balance, otherwise "false".
    """
    brackets = stdin_text.strip()
    previous_form = ""
    while previous_form != brackets:
        previous_form = brackets
        for pair in ("()", "[]", "{}"):
            brackets = brackets.replace(pair, "")
    return "true" if not brackets else "false"


# ---------------------------------------------------------------- Simplify Path


def solve_simplify_path(stdin_text: str) -> str:
    """Reduce an absolute Unix-style path to its canonical form.

    Parameters
    ----------
    stdin_text : str
        One line holding an absolute path.

    Returns
    -------
    str
        The canonical path, always starting with a single slash.
    """
    path = stdin_text.strip()
    resolved_names: list[str] = []
    for segment in path.split("/"):
        if segment in ("", "."):
            continue
        if segment == "..":
            if resolved_names:
                resolved_names.pop()
            continue
        resolved_names.append(segment)
    return "/" + "/".join(resolved_names)


def brute_simplify_path(stdin_text: str) -> str:
    """Reduce the same path by scanning characters and trimming the tail name.

    Parameters
    ----------
    stdin_text : str
        One line holding an absolute path.

    Returns
    -------
    str
        The canonical path, always starting with a single slash.
    """
    path = stdin_text.strip()
    canonical = ""
    position = 0
    while position < len(path):
        if path[position] == "/":
            position += 1
            continue
        segment_end = position
        while segment_end < len(path) and path[segment_end] != "/":
            segment_end += 1
        segment = path[position:segment_end]
        position = segment_end
        if segment == ".":
            continue
        if segment == "..":
            last_slash = canonical.rfind("/")
            if last_slash >= 0:
                canonical = canonical[:last_slash]
            continue
        canonical += "/" + segment
    return canonical if canonical else "/"


# -------------------------------------------------------------------- Min Stack


def solve_min_stack(stdin_text: str) -> str:
    """Replay stack commands, carrying the running minimum alongside the values.

    Parameters
    ----------
    stdin_text : str
        Command count on line one, then that many command lines.

    Returns
    -------
    str
        One line per command that returns a value, in command order.
    """
    lines = stdin_text.strip().split("\n")
    command_count = int(lines[0])
    values: list[int] = []
    running_minimums: list[int] = []
    outputs: list[str] = []
    for line in lines[1 : command_count + 1]:
        parts = line.split()
        command = parts[0]
        if command == "push":
            pushed_value = int(parts[1])
            values.append(pushed_value)
            if running_minimums:
                running_minimums.append(min(pushed_value, running_minimums[-1]))
            else:
                running_minimums.append(pushed_value)
        elif command == "pop":
            values.pop()
            running_minimums.pop()
        elif command == "top":
            outputs.append(str(values[-1]))
        else:
            outputs.append(str(running_minimums[-1]))
    return "\n".join(outputs)


def brute_min_stack(stdin_text: str) -> str:
    """Replay the same commands on a plain list, rescanning it for the minimum.

    Parameters
    ----------
    stdin_text : str
        Command count on line one, then that many command lines.

    Returns
    -------
    str
        One line per command that returns a value, in command order.
    """
    lines = stdin_text.strip().split("\n")
    command_count = int(lines[0])
    values: list[int] = []
    outputs: list[str] = []
    for line in lines[1 : command_count + 1]:
        parts = line.split()
        command = parts[0]
        if command == "push":
            values.append(int(parts[1]))
        elif command == "pop":
            del values[-1]
        elif command == "top":
            outputs.append(str(values[len(values) - 1]))
        else:
            smallest_value = values[0]
            for value in values:
                if value < smallest_value:
                    smallest_value = value
            outputs.append(str(smallest_value))
    return "\n".join(outputs)


# ------------------------------------------ Evaluate Reverse Polish Notation


def solve_evaluate_reverse_polish_notation(stdin_text: str) -> str:
    """Evaluate a postfix arithmetic expression left to right with a stack.

    Parameters
    ----------
    stdin_text : str
        One line of space separated operands and operators.

    Returns
    -------
    str
        The value of the expression.
    """
    tokens = stdin_text.strip().split()
    operands: list[int] = []
    for token in tokens:
        if token not in ("+", "-", "*", "/"):
            operands.append(int(token))
            continue
        right_operand = operands.pop()
        left_operand = operands.pop()
        if token == "+":
            operands.append(left_operand + right_operand)
        elif token == "-":
            operands.append(left_operand - right_operand)
        elif token == "*":
            operands.append(left_operand * right_operand)
        else:
            magnitude = abs(left_operand) // abs(right_operand)
            has_mixed_signs = (left_operand < 0) != (right_operand < 0)
            operands.append(-magnitude if has_mixed_signs else magnitude)
    return str(operands[-1])


def brute_evaluate_reverse_polish_notation(stdin_text: str) -> str:
    """Evaluate the same expression by recursing from the rightmost token.

    Parameters
    ----------
    stdin_text : str
        One line of space separated operands and operators.

    Returns
    -------
    str
        The value of the expression.
    """
    tokens = stdin_text.strip().split()

    def evaluate(position: int) -> tuple[int, int]:
        """Return the value ending at this token and the next position leftward."""
        token = tokens[position]
        if token not in ("+", "-", "*", "/"):
            return int(token), position - 1
        right_operand, position = evaluate(position - 1)
        left_operand, position = evaluate(position)
        if token == "+":
            return left_operand + right_operand, position
        if token == "-":
            return left_operand - right_operand, position
        if token == "*":
            return left_operand * right_operand, position
        quotient = left_operand // right_operand
        if quotient < 0 and quotient * right_operand != left_operand:
            quotient += 1
        return quotient, position

    value, _position = evaluate(len(tokens) - 1)
    return str(value)


# ----------------------------------------------------------- Basic Calculator


def solve_basic_calculator(stdin_text: str) -> str:
    """Evaluate an expression of integers, plus, minus and parentheses.

    Parameters
    ----------
    stdin_text : str
        One line holding the whole expression, possibly with spaces.

    Returns
    -------
    str
        The value of the expression.
    """
    expression = stdin_text.strip()
    total = 0
    sign = 1
    number = 0
    pending: list[int] = []
    for character in expression:
        if character.isdigit():
            number = number * 10 + int(character)
        elif character in "+-":
            total += sign * number
            number = 0
            sign = 1 if character == "+" else -1
        elif character == "(":
            pending.append(total)
            pending.append(sign)
            total = 0
            sign = 1
        elif character == ")":
            total += sign * number
            number = 0
            total = total * pending.pop() + pending.pop()
            sign = 1
    return str(total + sign * number)


def brute_basic_calculator(stdin_text: str) -> str:
    """Evaluate the same expression with a recursive descent parser.

    Parameters
    ----------
    stdin_text : str
        One line holding the whole expression, possibly with spaces.

    Returns
    -------
    str
        The value of the expression.
    """
    expression = stdin_text.strip()

    def parse_term(position: int) -> tuple[int, int]:
        """Return a signed number or parenthesised group and the next position."""
        while expression[position] == " ":
            position += 1
        character = expression[position]
        if character == "+":
            return parse_term(position + 1)
        if character == "-":
            value, position = parse_term(position + 1)
            return -value, position
        if character == "(":
            value, position = parse_sum(position + 1)
            while expression[position] == " ":
                position += 1
            return value, position + 1
        digits = ""
        while position < len(expression) and expression[position].isdigit():
            digits += expression[position]
            position += 1
        return int(digits), position

    def parse_sum(position: int) -> tuple[int, int]:
        """Return a chain of terms joined by plus and minus, and the next position."""
        value, position = parse_term(position)
        while True:
            while position < len(expression) and expression[position] == " ":
                position += 1
            if position >= len(expression) or expression[position] not in "+-":
                return value, position
            operator = expression[position]
            right_value, position = parse_term(position + 1)
            value = value + right_value if operator == "+" else value - right_value

    total, _position = parse_sum(0)
    return str(total)


PROBLEMS: list[dict[str, Any]] = [
    {
        "title": "Ransom Note",
        "level": "Easy",
        "topics": "Hash Table, String, Counting",
        "companies": "Amazon, Microsoft, Bloomberg",
        "description": """Letters are cut out of a magazine to spell a ransom note. Each letter of the
magazine may be used at most once. Decide whether the note can be built.

Input is two lines:

1. the ransom note, a non-empty string of lowercase letters
2. the magazine, a non-empty string of lowercase letters

Print `true` if the note can be built from the magazine letters, otherwise print
`false`.

""",
        "examples": """**Example 1**

Input

```
aa
ab
```

Output

```
false
```

**Example 2**

Input

```
aa
aab
```

Output

```
true
```

""",
        "constraints": """- 1 <= length of the note <= 100000
- 1 <= length of the magazine <= 100000
- both lines contain only lowercase English letters

""",
        "inputs": [
            "aa\nab",
            "aa\naab",
            "a\na",
            "aaa\naaa",
            "abc\nzzz",
            "bg\nefjbdfbdgfjhhaiigfhbaejahgpmb",
        ],
        "solve": solve_ransom_note,
        "brute": brute_ransom_note,
    },
    {
        "title": "Isomorphic Strings",
        "level": "Easy",
        "topics": "Hash Table, String",
        "companies": "Google, LinkedIn, Uber",
        "description": """Two strings of equal length are isomorphic when one can be turned into the other
by replacing letters, where every occurrence of a letter is replaced by the same
letter and no two letters are replaced by the same letter.

Input is two lines:

1. the first string, lowercase letters
2. the second string, lowercase letters, the same length as the first

Print `true` when the strings are isomorphic, otherwise print `false`.

""",
        "examples": """**Example 1**

Input

```
egg
add
```

Output

```
true
```

**Example 2**

Input

```
foo
bar
```

Output

```
false
```

""",
        "constraints": """- 1 <= length of each string <= 50000
- both strings have the same length
- both lines contain only lowercase English letters

""",
        "inputs": [
            "egg\nadd",
            "foo\nbar",
            "paper\ntitle",
            "a\nb",
            "aaa\naaa",
            "badc\nbaba",
        ],
        "solve": solve_isomorphic_strings,
        "brute": brute_isomorphic_strings,
    },
    {
        "title": "Word Pattern",
        "level": "Easy",
        "topics": "Hash Table, String",
        "companies": "Amazon, Facebook, Dropbox",
        "description": """A pattern of lowercase letters matches a list of words when there is a one-to-one
pairing between letters and words: each letter always stands for the same word,
and no two letters stand for the same word.

Input is two lines:

1. the pattern, a non-empty string of lowercase letters
2. the words, lowercase words separated by single spaces

Print `true` when the pattern matches the word list, otherwise print `false`.
A pattern whose length differs from the number of words never matches.

""",
        "examples": """**Example 1**

Input

```
abba
dog cat cat dog
```

Output

```
true
```

**Example 2**

Input

```
aaaa
dog cat cat dog
```

Output

```
false
```

""",
        "constraints": """- 1 <= length of the pattern <= 300
- 1 <= number of words <= 300
- the pattern holds only lowercase English letters
- each word is one or more lowercase English letters

""",
        "inputs": [
            "abba\ndog cat cat dog",
            "abba\ndog cat cat fish",
            "aaaa\ndog cat cat dog",
            "a\ndog",
            "aaa\ndog dog dog",
            "ab\ndog",
        ],
        "solve": solve_word_pattern,
        "brute": brute_word_pattern,
    },
    {
        "title": "Valid Anagram",
        "level": "Easy",
        "topics": "Hash Table, String, Sorting",
        "companies": "Amazon, Microsoft, Spotify",
        "description": """Two strings are anagrams when they use exactly the same letters the same number
of times, in any order.

Input is two lines:

1. the first string, lowercase letters
2. the second string, lowercase letters

Print `true` when the two strings are anagrams of each other, otherwise print
`false`. Strings of different lengths are never anagrams.

""",
        "examples": """**Example 1**

Input

```
anagram
nagaram
```

Output

```
true
```

**Example 2**

Input

```
rat
car
```

Output

```
false
```

""",
        "constraints": """- 1 <= length of each string <= 50000
- both lines contain only lowercase English letters

""",
        "inputs": [
            "anagram\nnagaram",
            "rat\ncar",
            "a\na",
            "aaa\naaa",
            "ab\nabc",
            "listen\nsilent",
        ],
        "solve": solve_valid_anagram,
        "brute": brute_valid_anagram,
    },
    {
        "title": "Group Anagrams",
        "level": "Medium",
        "topics": "Hash Table, String, Sorting",
        "companies": "Amazon, Facebook, Uber",
        "description": """Collect the given words into groups, where each group holds exactly the words
that are anagrams of one another.

Input is a word count `n` on the first line, followed by `n` lines each holding
one word of lowercase letters. A word may appear more than once, and a repeated
word stays repeated inside its group.

Print one group per line. Inside a group the words are sorted lexicographically
and separated by single spaces. The groups themselves are printed in
lexicographic order of their first word.

""",
        "examples": """**Example 1**

Input

```
6
eat
tea
tan
ate
nat
bat
```

Output

```
ate eat tea
bat
nat tan
```

**Example 2**

Input

```
5
ab
ba
aab
aba
baa
```

Output

```
aab aba baa
ab ba
```

""",
        "constraints": """- 1 <= n <= 10000
- 1 <= length of each word <= 100
- every word holds only lowercase English letters

""",
        "inputs": [
            "6\neat\ntea\ntan\nate\nnat\nbat",
            "1\na",
            "3\nabc\nabc\nabc",
            "3\nabc\ndef\nghi",
            "4\nlisten\nsilent\nenlist\ngoogle",
            "5\nab\nba\naab\naba\nbaa",
        ],
        "solve": solve_group_anagrams,
        "brute": brute_group_anagrams,
    },
    {
        "title": "Two Sum",
        "level": "Easy",
        "topics": "Array, Hash Table",
        "companies": "Amazon, Google, Apple",
        "description": """Find the two positions in a list of integers whose values add up to a target.
Exactly one such pair exists, and a position cannot be paired with itself.

Input is three lines:

1. the count `n`
2. `n` integers separated by single spaces
3. the target integer

Print the two zero-based positions in ascending order on one line, separated by
a single space.

""",
        "examples": """**Example 1**

Input

```
4
2 7 11 15
9
```

Output

```
0 1
```

**Example 2**

Input

```
4
-3 4 3 90
0
```

Output

```
0 2
```

""",
        "constraints": """- 2 <= n <= 10000
- -1000000000 <= each value <= 1000000000
- -2000000000 <= target <= 2000000000
- exactly one pair of positions adds up to the target

""",
        "inputs": [
            "4\n2 7 11 15\n9",
            "3\n3 2 4\n6",
            "2\n3 3\n6",
            "4\n-3 4 3 90\n0",
            "5\n-10 -5 -3 -1 0\n-4",
            "6\n1 5 3 7 9 2\n16",
        ],
        "solve": solve_two_sum,
        "brute": brute_two_sum,
    },
    {
        "title": "Happy Number",
        "level": "Easy",
        "topics": "Hash Table, Math, Two Pointers",
        "companies": "Airbnb, Twitter, JPMorgan",
        "description": """Replace a positive integer by the sum of the squares of its digits, then repeat.
A number is happy when this process eventually reaches 1; otherwise it falls into
a cycle that never contains 1.

Input is a single line holding one positive integer `n`.

Print `true` when `n` is happy, otherwise print `false`.

""",
        "examples": """**Example 1**

Input

```
19
```

Output

```
true
```

**Example 2**

Input

```
2
```

Output

```
false
```

""",
        "constraints": """- 1 <= n <= 2147483647

""",
        "inputs": ["19", "2", "1", "7", "116", "1000000"],
        "solve": solve_happy_number,
        "brute": brute_happy_number,
    },
    {
        "title": "Contains Duplicate II",
        "level": "Easy",
        "topics": "Array, Hash Table, Sliding Window",
        "companies": "Palantir, Amazon, Adobe",
        "description": """Decide whether a list of integers holds two equal values whose positions are no
more than `k` apart.

Input is three lines:

1. the count `n`
2. `n` integers separated by single spaces
3. the distance limit `k`

Print `true` when two different positions `i` and `j` satisfy both
`value[i] == value[j]` and `abs(i - j) <= k`, otherwise print `false`.

""",
        "examples": """**Example 1**

Input

```
4
1 2 3 1
3
```

Output

```
true
```

**Example 2**

Input

```
6
1 2 3 1 2 3
2
```

Output

```
false
```

""",
        "constraints": """- 1 <= n <= 100000
- -1000000000 <= each value <= 1000000000
- 0 <= k <= 100000

""",
        "inputs": [
            "4\n1 2 3 1\n3",
            "4\n1 0 1 1\n1",
            "6\n1 2 3 1 2 3\n2",
            "1\n5\n1",
            "3\n7 7 7\n0",
            "5\n-1 -1 2 3 4\n1",
        ],
        "solve": solve_contains_duplicate_ii,
        "brute": brute_contains_duplicate_ii,
    },
    {
        "title": "Longest Consecutive Sequence",
        "level": "Medium",
        "topics": "Array, Hash Table, Union Find",
        "companies": "Google, Amazon, Stripe",
        "description": """Find the length of the longest run of consecutive integers that can be formed
from the given values. The values may arrive in any order and may repeat; a run
counts each integer once.

Input is two lines:

1. the count `n`
2. `n` integers separated by single spaces

Print the length of the longest consecutive run on one line.

""",
        "examples": """**Example 1**

Input

```
6
100 4 200 1 3 2
```

Output

```
4
```

**Example 2**

Input

```
4
7 7 7 7
```

Output

```
1
```

""",
        "constraints": """- 1 <= n <= 100000
- -1000000000 <= each value <= 1000000000

""",
        "inputs": [
            "6\n100 4 200 1 3 2",
            "10\n0 3 7 2 5 8 4 6 0 1",
            "1\n5",
            "4\n7 7 7 7",
            "5\n-3 -2 -1 1 2",
            "4\n10 20 30 40",
        ],
        "solve": solve_longest_consecutive_sequence,
        "brute": brute_longest_consecutive_sequence,
    },
    {
        "title": "Summary Ranges",
        "level": "Easy",
        "topics": "Array",
        "companies": "Google, Microsoft, Salesforce",
        "description": """Describe a sorted list of distinct integers as the smallest set of consecutive
ranges that covers exactly those values.

Input is two lines:

1. the count `n`
2. `n` integers in strictly increasing order, separated by single spaces

Print one range per line, in increasing order. A range holding a single value
`a` is printed as `a`. A range from `a` up to `b` with `b` greater than `a` is
printed as `a->b` with no spaces around the arrow.

""",
        "examples": """**Example 1**

Input

```
6
0 1 2 4 5 7
```

Output

```
0->2
4->5
7
```

**Example 2**

Input

```
7
0 2 3 4 6 8 9
```

Output

```
0
2->4
6
8->9
```

""",
        "constraints": """- 1 <= n <= 20
- -2147483648 <= each value <= 2147483647
- the values are strictly increasing, so there are no duplicates

""",
        "inputs": [
            "6\n0 1 2 4 5 7",
            "7\n0 2 3 4 6 8 9",
            "1\n-5",
            "3\n-3 -2 -1",
            "4\n1 3 5 7",
            "2\n-1 0",
        ],
        "solve": solve_summary_ranges,
        "brute": brute_summary_ranges,
    },
    {
        "title": "Merge Intervals",
        "level": "Medium",
        "topics": "Array, Sorting, Intervals",
        "companies": "Facebook, Amazon, Bloomberg",
        "description": """Combine a collection of closed intervals so that no two of the results overlap
or touch. Two intervals that share even a single point become one interval.

Input starts with the interval count `n` on the first line, followed by `n`
lines. Each of those lines holds a start and an end separated by a single space.
The intervals arrive in no particular order.

Print the merged intervals sorted by start, one per line, each as `start end`
separated by a single space.

""",
        "examples": """**Example 1**

Input

```
4
1 3
2 6
8 10
15 18
```

Output

```
1 6
8 10
15 18
```

**Example 2**

Input

```
3
5 6
1 2
8 9
```

Output

```
1 2
5 6
8 9
```

""",
        "constraints": """- 1 <= n <= 10000
- -100000 <= start <= end <= 100000

""",
        "inputs": [
            "4\n1 3\n2 6\n8 10\n15 18",
            "2\n1 4\n4 5",
            "1\n5 5",
            "3\n2 2\n2 2\n2 2",
            "3\n-5 -3\n-4 0\n3 7",
            "3\n5 6\n1 2\n8 9",
        ],
        "solve": solve_merge_intervals,
        "brute": brute_merge_intervals,
    },
    {
        "title": "Insert Interval",
        "level": "Medium",
        "topics": "Array, Sorting, Intervals",
        "companies": "Google, LinkedIn, Amazon",
        "description": """Add one closed interval to a list of closed intervals that is already sorted by
start and free of overlaps, then merge whatever now overlaps or touches.

Input layout:

1. the interval count `n`
2. `n` lines, each holding a start and an end separated by a single space,
   already sorted by start and pairwise disjoint
3. one final line holding the start and end of the interval to insert

When `n` is 0 the second block is empty and the interval to insert follows the
count directly.

Print the resulting intervals sorted by start, one per line, each as
`start end` separated by a single space.

""",
        "examples": """**Example 1**

Input

```
2
1 3
6 9
2 5
```

Output

```
1 5
6 9
```

**Example 2**

Input

```
5
1 2
3 5
6 7
8 10
12 16
4 8
```

Output

```
1 2
3 10
12 16
```

""",
        "constraints": """- 0 <= n <= 10000
- -100000 <= start <= end <= 100000
- the listed intervals are sorted by start and do not overlap

""",
        "inputs": [
            "2\n1 3\n6 9\n2 5",
            "5\n1 2\n3 5\n6 7\n8 10\n12 16\n4 8",
            "0\n5 7",
            "1\n1 5\n2 3",
            "2\n1 5\n6 8\n9 10",
            "2\n-5 -3\n0 2\n-4 1",
        ],
        "solve": solve_insert_interval,
        "brute": brute_insert_interval,
    },
    {
        "title": "Minimum Number of Arrows to Burst Balloons",
        "level": "Medium",
        "topics": "Array, Greedy, Sorting, Intervals",
        "companies": "Amazon, Microsoft, Nvidia",
        "description": """Balloons hang along a number line, each covering a closed span from `start` to
`end`. An arrow shot straight up at position `x` bursts every balloon whose span
contains `x`, endpoints included. Find the smallest number of arrows that bursts
all of them.

Input starts with the balloon count `n` on the first line, followed by `n` lines.
Each of those lines holds a start and an end separated by a single space, in no
particular order.

Print the minimum number of arrows on one line.

""",
        "examples": """**Example 1**

Input

```
4
10 16
2 8
1 6
7 12
```

Output

```
2
```

**Example 2**

Input

```
4
1 2
3 4
5 6
7 8
```

Output

```
4
```

""",
        "constraints": """- 1 <= n <= 8
- -1000 <= start <= end <= 1000

""",
        "inputs": [
            "4\n10 16\n2 8\n1 6\n7 12",
            "4\n1 2\n3 4\n5 6\n7 8",
            "1\n1 2",
            "3\n4 4\n4 4\n4 4",
            "4\n1 2\n2 3\n3 4\n4 5",
            "3\n-5 -1\n-3 2\n0 4",
        ],
        "solve": solve_minimum_number_of_arrows_to_burst_balloons,
        "brute": brute_minimum_number_of_arrows_to_burst_balloons,
    },
    {
        "title": "Valid Parentheses",
        "level": "Easy",
        "topics": "String, Stack",
        "companies": "Amazon, Google, Microsoft",
        "description": """A bracket string is valid when every opening bracket is closed by a bracket of
the same kind, closings happen in the right order, and nothing is left over.

Input is a single line made only of the characters `(`, `)`, `[`, `]`, `{` and
`}`.

Print `true` when the string is valid, otherwise print `false`.

""",
        "examples": """**Example 1**

Input

```
()[]{}
```

Output

```
true
```

**Example 2**

Input

```
([)]
```

Output

```
false
```

""",
        "constraints": """- 1 <= length of the line <= 10000
- the line holds only the six bracket characters

""",
        "inputs": ["()", "()[]{}", "(]", "([)]", "{[]}", "("],
        "solve": solve_valid_parentheses,
        "brute": brute_valid_parentheses,
    },
    {
        "title": "Simplify Path",
        "level": "Medium",
        "topics": "String, Stack",
        "companies": "Facebook, Microsoft, Bloomberg",
        "description": """Rewrite an absolute Unix-style file path in canonical form. A single dot means
the current directory, two dots mean the parent directory, and runs of slashes
count as one. Two dots at the root stay at the root.

Input is a single line holding an absolute path, so it always begins with `/`.

Print the canonical path on one line. It starts with exactly one `/`, uses single
slashes between directory names, and has no trailing slash unless the whole path
is just `/`.

""",
        "examples": """**Example 1**

Input

```
/home//foo/
```

Output

```
/home/foo
```

**Example 2**

Input

```
/a/./b/../../c/
```

Output

```
/c
```

""",
        "constraints": """- 1 <= length of the path <= 3000
- the path starts with `/`
- directory names hold letters, digits, dots, underscores and hyphens

""",
        "inputs": [
            "/home/",
            "/../",
            "/home//foo/",
            "/a/./b/../../c/",
            "/",
            "/a/../../b/../c//.//",
        ],
        "solve": solve_simplify_path,
        "brute": brute_simplify_path,
    },
    {
        "title": "Min Stack",
        "level": "Medium",
        "topics": "Stack, Design",
        "companies": "Amazon, Google, Goldman Sachs",
        "description": """Run a stack that also reports its smallest stored value in constant time.

Input starts with the command count `q` on the first line, followed by `q`
command lines, each one of:

- `push x` adds the integer `x` on top
- `pop` removes the top value
- `top` reports the top value
- `getMin` reports the smallest value currently stored

The command sequence is always valid: `pop`, `top` and `getMin` never run on an
empty stack, and at least one `top` or `getMin` appears.

Print one line per `top` and per `getMin`, in command order, holding the integer
that command reports. `push` and `pop` print nothing.

""",
        "examples": """**Example 1**

Input

```
7
push -2
push 0
push -3
getMin
pop
top
getMin
```

Output

```
-3
0
-2
```

**Example 2**

Input

```
8
push 3
push 1
push 2
getMin
pop
getMin
pop
getMin
```

Output

```
1
1
3
```

""",
        "constraints": """- 1 <= q <= 30000
- -2147483648 <= x <= 2147483647
- the command sequence is always valid

""",
        "inputs": [
            "7\npush -2\npush 0\npush -3\ngetMin\npop\ntop\ngetMin",
            "2\npush 5\ntop",
            "5\npush 4\npush 4\ngetMin\npop\ngetMin",
            "8\npush 3\npush 1\npush 2\ngetMin\npop\ngetMin\npop\ngetMin",
            "6\npush 10\ngetMin\npush 20\ngetMin\npop\ngetMin",
            "9\npush 0\npush -1\ngetMin\ntop\npop\ntop\ngetMin\npush -5\ngetMin",
        ],
        "solve": solve_min_stack,
        "brute": brute_min_stack,
    },
    {
        "title": "Evaluate Reverse Polish Notation",
        "level": "Medium",
        "topics": "Array, Math, Stack",
        "companies": "LinkedIn, Amazon, Citadel",
        "description": """Evaluate an arithmetic expression written in postfix form, where each operator
follows its two operands.

Input is a single line of tokens separated by single spaces. A token is either an
integer, possibly negative, or one of `+`, `-`, `*`, `/`. Division between two
operands truncates toward zero, so `7 -3 /` is `-2`.

Print the value of the expression on one line.

""",
        "examples": """**Example 1**

Input

```
4 13 5 / +
```

Output

```
6
```

**Example 2**

Input

```
10 6 9 3 + -11 * / * 17 + 5 +
```

Output

```
22
```

""",
        "constraints": """- 1 <= number of tokens <= 10000
- the expression is always a valid postfix expression
- -1000000000 <= every operand and every intermediate value <= 1000000000
- division never has a zero divisor

""",
        "inputs": [
            "2 1 + 3 *",
            "4 13 5 / +",
            "10 6 9 3 + -11 * / * 17 + 5 +",
            "3",
            "7 -3 /",
            "-5 -5 *",
        ],
        "solve": solve_evaluate_reverse_polish_notation,
        "brute": brute_evaluate_reverse_polish_notation,
    },
    {
        "title": "Basic Calculator",
        "level": "Hard",
        "topics": "String, Math, Stack, Recursion",
        "companies": "Google, Facebook, Snowflake",
        "description": """Evaluate an arithmetic expression built from non-negative integers, the `+` and
`-` operators, and round brackets. A `+` or `-` directly in front of a number or
a bracket acts as a sign on that value.

Input is a single line holding the whole expression. It may contain spaces
between tokens, but never a leading or trailing space.

Print the value of the expression on one line.

""",
        "examples": """**Example 1**

Input

```
(1+(4+5+2)-3)+(6+8)
```

Output

```
23
```

**Example 2**

Input

```
-2+1
```

Output

```
-1
```

""",
        "constraints": """- 1 <= length of the line <= 300000
- the line holds only digits, spaces and the characters `+`, `-`, `(`, `)`
- the expression is always valid and brackets are balanced
- every intermediate value fits in a signed 32-bit integer

""",
        "inputs": [
            "1 + 1",
            "2-1 + 2",
            "(1+(4+5+2)-3)+(6+8)",
            "1",
            "-2+1",
            "2-(5-6)",
        ],
        "solve": solve_basic_calculator,
        "brute": brute_basic_calculator,
    },
]
