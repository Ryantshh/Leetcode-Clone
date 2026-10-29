"""Math and dynamic-programming problems for the study-plan seed data.

Every solver reads a whole stdin payload and returns the exact stdout text the
judge compares against.
"""

from __future__ import annotations

import math
from itertools import combinations
from typing import Any

# ---------------------------------------------------------------------------
# Palindrome Number
# ---------------------------------------------------------------------------


def solve_palindrome_number(stdin_text: str) -> str:
    """Report whether a signed integer reads the same forwards and backwards.

    Parameters
    ----------
    stdin_text : str
        One line holding the integer.

    Returns
    -------
    str
        "true" or "false".
    """
    digits = stdin_text.strip()
    if digits.startswith("-"):
        return "false"
    return "true" if digits == digits[::-1] else "false"


def brute_palindrome_number(stdin_text: str) -> str:
    """Report palindromicity by rebuilding the number from its digits.

    Parameters
    ----------
    stdin_text : str
        One line holding the integer.

    Returns
    -------
    str
        "true" or "false".
    """
    value = int(stdin_text.strip())
    if value < 0:
        return "false"
    remaining = value
    reversed_value = 0
    while remaining > 0:
        reversed_value = reversed_value * 10 + remaining % 10
        remaining //= 10
    return "true" if reversed_value == value else "false"


# ---------------------------------------------------------------------------
# Plus One
# ---------------------------------------------------------------------------


def solve_plus_one(stdin_text: str) -> str:
    """Add one to a big number stored as a digit list.

    Parameters
    ----------
    stdin_text : str
        Count line, then the digits on one space separated line.

    Returns
    -------
    str
        Space separated digits of the incremented number.
    """
    tokens = stdin_text.split()
    digit_count = int(tokens[0])
    digits = [int(token) for token in tokens[1 : 1 + digit_count]]
    position = digit_count - 1
    while position >= 0:
        if digits[position] < 9:
            digits[position] += 1
            return " ".join(str(digit) for digit in digits)
        digits[position] = 0
        position -= 1
    return " ".join(str(digit) for digit in [1] + digits)


def brute_plus_one(stdin_text: str) -> str:
    """Add one by converting the digit list to an integer and back.

    Parameters
    ----------
    stdin_text : str
        Count line, then the digits on one space separated line.

    Returns
    -------
    str
        Space separated digits of the incremented number.
    """
    tokens = stdin_text.split()
    digit_count = int(tokens[0])
    joined = "".join(tokens[1 : 1 + digit_count])
    incremented = str(int(joined) + 1)
    return " ".join(incremented)


# ---------------------------------------------------------------------------
# Factorial Trailing Zeroes
# ---------------------------------------------------------------------------


def solve_factorial_trailing_zeroes(stdin_text: str) -> str:
    """Count trailing zeroes of n! by counting factors of five.

    Parameters
    ----------
    stdin_text : str
        One line holding n.

    Returns
    -------
    str
        The number of trailing zeroes.
    """
    number = int(stdin_text.strip())
    zero_count = 0
    power_of_five = 5
    while power_of_five <= number:
        zero_count += number // power_of_five
        power_of_five *= 5
    return str(zero_count)


def brute_factorial_trailing_zeroes(stdin_text: str) -> str:
    """Count trailing zeroes by expanding n! and stripping tens from it.

    Parameters
    ----------
    stdin_text : str
        One line holding n.

    Returns
    -------
    str
        The number of trailing zeroes.
    """
    number = int(stdin_text.strip())
    factorial_value = math.factorial(number)
    zero_count = 0
    while factorial_value % 10 == 0:
        factorial_value //= 10
        zero_count += 1
    return str(zero_count)


# ---------------------------------------------------------------------------
# Sqrt(x)
# ---------------------------------------------------------------------------


def solve_sqrt_x(stdin_text: str) -> str:
    """Compute the truncated integer square root by binary search.

    Parameters
    ----------
    stdin_text : str
        One line holding x.

    Returns
    -------
    str
        The integer part of the square root of x.
    """
    value = int(stdin_text.strip())
    low, high = 0, value
    best = 0
    while low <= high:
        middle = (low + high) // 2
        if middle * middle <= value:
            best = middle
            low = middle + 1
        else:
            high = middle - 1
    return str(best)


def brute_sqrt_x(stdin_text: str) -> str:
    """Compute the truncated integer square root by stepping upward.

    Parameters
    ----------
    stdin_text : str
        One line holding x.

    Returns
    -------
    str
        The integer part of the square root of x.
    """
    value = int(stdin_text.strip())
    root = 0
    while (root + 1) * (root + 1) <= value:
        root += 1
    return str(root)


# ---------------------------------------------------------------------------
# Pow(x, n)
# ---------------------------------------------------------------------------


def solve_pow_x_n(stdin_text: str) -> str:
    """Raise x to the integer power n by repeated squaring.

    Parameters
    ----------
    stdin_text : str
        First line x as a decimal, second line the integer exponent n.

    Returns
    -------
    str
        The result written with exactly five decimal places.
    """
    lines = stdin_text.split("\n")
    base = float(lines[0].strip())
    exponent = int(lines[1].strip())
    if exponent < 0:
        base = 1.0 / base
        exponent = -exponent
    result = 1.0
    while exponent > 0:
        if exponent % 2 == 1:
            result *= base
        base *= base
        exponent //= 2
    return f"{result:.5f}"


def brute_pow_x_n(stdin_text: str) -> str:
    """Raise x to the integer power n by multiplying one factor at a time.

    Parameters
    ----------
    stdin_text : str
        First line x as a decimal, second line the integer exponent n.

    Returns
    -------
    str
        The result written with exactly five decimal places.
    """
    lines = stdin_text.split("\n")
    base = float(lines[0].strip())
    exponent = int(lines[1].strip())
    product = 1.0
    for _ in range(abs(exponent)):
        product *= base
    if exponent < 0:
        product = 1.0 / product
    return f"{product:.5f}"


# ---------------------------------------------------------------------------
# Max Points on a Line
# ---------------------------------------------------------------------------


def solve_max_points_on_a_line(stdin_text: str) -> str:
    """Find the largest number of given points sharing one straight line.

    Parameters
    ----------
    stdin_text : str
        Count line, then one "x y" line per point.

    Returns
    -------
    str
        The size of the largest collinear subset.
    """
    tokens = stdin_text.split()
    point_count = int(tokens[0])
    points = [
        (int(tokens[1 + 2 * index]), int(tokens[2 + 2 * index])) for index in range(point_count)
    ]
    if point_count <= 2:
        return str(point_count)
    best = 1
    for anchor_index, anchor in enumerate(points):
        directions: dict[tuple[int, int], int] = {}
        for other in points[anchor_index + 1 :]:
            delta_x = other[0] - anchor[0]
            delta_y = other[1] - anchor[1]
            divisor = math.gcd(abs(delta_x), abs(delta_y))
            delta_x //= divisor
            delta_y //= divisor
            if delta_x < 0 or (delta_x == 0 and delta_y < 0):
                delta_x, delta_y = -delta_x, -delta_y
            directions[(delta_x, delta_y)] = directions.get((delta_x, delta_y), 0) + 1
        for shared_count in directions.values():
            best = max(best, shared_count + 1)
    return str(best)


def brute_max_points_on_a_line(stdin_text: str) -> str:
    """Find the largest collinear subset by testing every pair of points.

    Parameters
    ----------
    stdin_text : str
        Count line, then one "x y" line per point.

    Returns
    -------
    str
        The size of the largest collinear subset.
    """
    tokens = stdin_text.split()
    point_count = int(tokens[0])
    points = [
        (int(tokens[1 + 2 * index]), int(tokens[2 + 2 * index])) for index in range(point_count)
    ]
    if point_count <= 2:
        return str(point_count)
    best = 2
    for first, second in combinations(points, 2):
        on_line = 0
        for candidate in points:
            cross = (second[0] - first[0]) * (candidate[1] - first[1]) - (
                second[1] - first[1]
            ) * (candidate[0] - first[0])
            if cross == 0:
                on_line += 1
        best = max(best, on_line)
    return str(best)


# ---------------------------------------------------------------------------
# Climbing Stairs
# ---------------------------------------------------------------------------


def solve_climbing_stairs(stdin_text: str) -> str:
    """Count the ways to climb n stairs taking one or two steps at a time.

    Parameters
    ----------
    stdin_text : str
        One line holding n.

    Returns
    -------
    str
        The number of distinct climbing orders.
    """
    step_count = int(stdin_text.strip())
    ways_two_back, ways_one_back = 1, 1
    for _ in range(step_count - 1):
        ways_two_back, ways_one_back = ways_one_back, ways_one_back + ways_two_back
    return str(ways_one_back)


def brute_climbing_stairs(stdin_text: str) -> str:
    """Count the climbing orders by summing over the number of double steps.

    Parameters
    ----------
    stdin_text : str
        One line holding n.

    Returns
    -------
    str
        The number of distinct climbing orders.
    """
    step_count = int(stdin_text.strip())
    total = 0
    for double_steps in range(step_count // 2 + 1):
        single_steps = step_count - 2 * double_steps
        total += math.comb(single_steps + double_steps, double_steps)
    return str(total)


# ---------------------------------------------------------------------------
# House Robber
# ---------------------------------------------------------------------------


def solve_house_robber(stdin_text: str) -> str:
    """Maximise the loot taken from a row of houses without hitting neighbours.

    Parameters
    ----------
    stdin_text : str
        Count line, then the house values on one space separated line.

    Returns
    -------
    str
        The largest reachable total.
    """
    tokens = stdin_text.split()
    house_count = int(tokens[0])
    values = [int(token) for token in tokens[1 : 1 + house_count]]
    skip_best, take_best = 0, 0
    for value in values:
        skip_best, take_best = max(skip_best, take_best), skip_best + value
    return str(max(skip_best, take_best))


def brute_house_robber(stdin_text: str) -> str:
    """Maximise the loot by enumerating every non-adjacent house selection.

    Parameters
    ----------
    stdin_text : str
        Count line, then the house values on one space separated line.

    Returns
    -------
    str
        The largest reachable total.
    """
    tokens = stdin_text.split()
    house_count = int(tokens[0])
    values = [int(token) for token in tokens[1 : 1 + house_count]]
    best = 0
    for selection in range(1 << house_count):
        if selection & (selection >> 1):
            continue
        total = sum(values[index] for index in range(house_count) if selection >> index & 1)
        best = max(best, total)
    return str(best)


# ---------------------------------------------------------------------------
# Word Break
# ---------------------------------------------------------------------------


def solve_word_break(stdin_text: str) -> str:
    """Decide whether a string splits into a sequence of dictionary words.

    Parameters
    ----------
    stdin_text : str
        The string, a count line, then that many dictionary words.

    Returns
    -------
    str
        "true" or "false".
    """
    lines = stdin_text.split("\n")
    target = lines[0].strip()
    word_count = int(lines[1].strip())
    dictionary = {lines[2 + index].strip() for index in range(word_count)}
    is_reachable = [False] * (len(target) + 1)
    is_reachable[0] = True
    for end in range(1, len(target) + 1):
        for start in range(end):
            if is_reachable[start] and target[start:end] in dictionary:
                is_reachable[end] = True
                break
    return "true" if is_reachable[len(target)] else "false"


def brute_word_break(stdin_text: str) -> str:
    """Decide segmentability by recursively peeling dictionary prefixes.

    Parameters
    ----------
    stdin_text : str
        The string, a count line, then that many dictionary words.

    Returns
    -------
    str
        "true" or "false".
    """
    lines = stdin_text.split("\n")
    target = lines[0].strip()
    word_count = int(lines[1].strip())
    dictionary = [lines[2 + index].strip() for index in range(word_count)]

    def can_split(remaining: str) -> bool:
        if not remaining:
            return True
        for word in dictionary:
            if remaining.startswith(word) and can_split(remaining[len(word) :]):
                return True
        return False

    return "true" if can_split(target) else "false"


# ---------------------------------------------------------------------------
# Coin Change
# ---------------------------------------------------------------------------


def solve_coin_change(stdin_text: str) -> str:
    """Find the fewest coins that add up to a target amount.

    Parameters
    ----------
    stdin_text : str
        Amount line, coin count line, then the coin values on one line.

    Returns
    -------
    str
        The minimum number of coins, or "-1" when the amount is unreachable.
    """
    tokens = stdin_text.split()
    amount = int(tokens[0])
    coin_count = int(tokens[1])
    coins = [int(token) for token in tokens[2 : 2 + coin_count]]
    unreachable = amount + 1
    fewest = [0] + [unreachable] * amount
    for subtotal in range(1, amount + 1):
        for coin in coins:
            if coin <= subtotal and fewest[subtotal - coin] + 1 < fewest[subtotal]:
                fewest[subtotal] = fewest[subtotal - coin] + 1
    return str(fewest[amount]) if fewest[amount] != unreachable else "-1"


def brute_coin_change(stdin_text: str) -> str:
    """Find the fewest coins by breadth-first search over reachable subtotals.

    Parameters
    ----------
    stdin_text : str
        Amount line, coin count line, then the coin values on one line.

    Returns
    -------
    str
        The minimum number of coins, or "-1" when the amount is unreachable.
    """
    tokens = stdin_text.split()
    amount = int(tokens[0])
    coin_count = int(tokens[1])
    coins = [int(token) for token in tokens[2 : 2 + coin_count]]
    frontier = {0}
    visited = {0}
    coins_used = 0
    while frontier:
        if amount in frontier:
            return str(coins_used)
        next_frontier: set[int] = set()
        for subtotal in frontier:
            for coin in coins:
                candidate = subtotal + coin
                if candidate <= amount and candidate not in visited:
                    visited.add(candidate)
                    next_frontier.add(candidate)
        frontier = next_frontier
        coins_used += 1
    return "-1"


# ---------------------------------------------------------------------------
# Longest Increasing Subsequence
# ---------------------------------------------------------------------------


def solve_longest_increasing_subsequence(stdin_text: str) -> str:
    """Measure the longest strictly increasing subsequence of an array.

    Parameters
    ----------
    stdin_text : str
        Count line, then the values on one space separated line.

    Returns
    -------
    str
        The length of the longest strictly increasing subsequence.
    """
    tokens = stdin_text.split()
    value_count = int(tokens[0])
    values = [int(token) for token in tokens[1 : 1 + value_count]]
    tails: list[int] = []
    for value in values:
        low, high = 0, len(tails)
        while low < high:
            middle = (low + high) // 2
            if tails[middle] < value:
                low = middle + 1
            else:
                high = middle
        if low == len(tails):
            tails.append(value)
        else:
            tails[low] = value
    return str(len(tails))


def brute_longest_increasing_subsequence(stdin_text: str) -> str:
    """Measure the longest increasing subsequence by enumerating every subset.

    Parameters
    ----------
    stdin_text : str
        Count line, then the values on one space separated line.

    Returns
    -------
    str
        The length of the longest strictly increasing subsequence.
    """
    tokens = stdin_text.split()
    value_count = int(tokens[0])
    values = [int(token) for token in tokens[1 : 1 + value_count]]
    best = 0
    for selection in range(1, 1 << value_count):
        chosen = [values[index] for index in range(value_count) if selection >> index & 1]
        is_increasing = all(
            earlier < later for earlier, later in zip(chosen, chosen[1:], strict=False)
        )
        if is_increasing:
            best = max(best, len(chosen))
    return str(best)


# ---------------------------------------------------------------------------
# Triangle
# ---------------------------------------------------------------------------


def _read_triangle(stdin_text: str) -> list[list[int]]:
    """Parse a triangle payload into its rows.

    Parameters
    ----------
    stdin_text : str
        Row count line, then one row per line.

    Returns
    -------
    list[list[int]]
        The triangle rows, shortest first.
    """
    lines = stdin_text.split("\n")
    row_count = int(lines[0].strip())
    return [[int(token) for token in lines[1 + index].split()] for index in range(row_count)]


def solve_triangle(stdin_text: str) -> str:
    """Find the cheapest top-to-bottom path through a number triangle.

    Parameters
    ----------
    stdin_text : str
        Row count line, then one row per line.

    Returns
    -------
    str
        The smallest achievable path total.
    """
    rows = _read_triangle(stdin_text)
    best_from_here = list(rows[-1])
    for row in reversed(rows[:-1]):
        best_from_here = [
            value + min(best_from_here[index], best_from_here[index + 1])
            for index, value in enumerate(row)
        ]
    return str(best_from_here[0])


def brute_triangle(stdin_text: str) -> str:
    """Find the cheapest triangle path by walking every route from the apex.

    Parameters
    ----------
    stdin_text : str
        Row count line, then one row per line.

    Returns
    -------
    str
        The smallest achievable path total.
    """
    rows = _read_triangle(stdin_text)

    def walk(row_index: int, position: int) -> int:
        if row_index == len(rows) - 1:
            return rows[row_index][position]
        return rows[row_index][position] + min(
            walk(row_index + 1, position), walk(row_index + 1, position + 1)
        )

    return str(walk(0, 0))


# ---------------------------------------------------------------------------
# Minimum Path Sum
# ---------------------------------------------------------------------------


def _read_grid(stdin_text: str) -> list[list[int]]:
    """Parse a "rows cols" header followed by that many grid rows.

    Parameters
    ----------
    stdin_text : str
        Dimension line, then one grid row per line.

    Returns
    -------
    list[list[int]]
        The grid values.
    """
    lines = stdin_text.split("\n")
    row_count, column_count = (int(token) for token in lines[0].split())
    grid: list[list[int]] = []
    for index in range(row_count):
        row = [int(token) for token in lines[1 + index].split()]
        grid.append(row[:column_count])
    return grid


def solve_minimum_path_sum(stdin_text: str) -> str:
    """Find the cheapest right-and-down walk across a cost grid.

    Parameters
    ----------
    stdin_text : str
        Dimension line, then one grid row per line.

    Returns
    -------
    str
        The smallest achievable total cost.
    """
    grid = _read_grid(stdin_text)
    column_count = len(grid[0])
    best_cost = [0] * column_count
    for row_index, row in enumerate(grid):
        for column_index, value in enumerate(row):
            if row_index == 0 and column_index == 0:
                best_cost[0] = value
            elif row_index == 0:
                best_cost[column_index] = best_cost[column_index - 1] + value
            elif column_index == 0:
                best_cost[0] += value
            else:
                best_cost[column_index] = value + min(
                    best_cost[column_index], best_cost[column_index - 1]
                )
    return str(best_cost[column_count - 1])


def brute_minimum_path_sum(stdin_text: str) -> str:
    """Find the cheapest grid walk by exploring every right-and-down route.

    Parameters
    ----------
    stdin_text : str
        Dimension line, then one grid row per line.

    Returns
    -------
    str
        The smallest achievable total cost.
    """
    grid = _read_grid(stdin_text)
    last_row = len(grid) - 1
    last_column = len(grid[0]) - 1

    def walk(row_index: int, column_index: int) -> int:
        value = grid[row_index][column_index]
        if row_index == last_row and column_index == last_column:
            return value
        options: list[int] = []
        if row_index < last_row:
            options.append(walk(row_index + 1, column_index))
        if column_index < last_column:
            options.append(walk(row_index, column_index + 1))
        return value + min(options)

    return str(walk(0, 0))


# ---------------------------------------------------------------------------
# Unique Paths II
# ---------------------------------------------------------------------------


def solve_unique_paths_ii(stdin_text: str) -> str:
    """Count right-and-down routes across a grid with blocked cells.

    Parameters
    ----------
    stdin_text : str
        Dimension line, then one grid row per line of 0 and 1 markers.

    Returns
    -------
    str
        The number of routes from the top-left cell to the bottom-right cell.
    """
    grid = _read_grid(stdin_text)
    column_count = len(grid[0])
    route_count = [0] * column_count
    route_count[0] = 1
    for row in grid:
        for column_index, marker in enumerate(row):
            if marker == 1:
                route_count[column_index] = 0
            elif column_index > 0:
                route_count[column_index] += route_count[column_index - 1]
    return str(route_count[column_count - 1])


def brute_unique_paths_ii(stdin_text: str) -> str:
    """Count routes across a blocked grid by walking each one explicitly.

    Parameters
    ----------
    stdin_text : str
        Dimension line, then one grid row per line of 0 and 1 markers.

    Returns
    -------
    str
        The number of routes from the top-left cell to the bottom-right cell.
    """
    grid = _read_grid(stdin_text)
    last_row = len(grid) - 1
    last_column = len(grid[0]) - 1

    def walk(row_index: int, column_index: int) -> int:
        if grid[row_index][column_index] == 1:
            return 0
        if row_index == last_row and column_index == last_column:
            return 1
        total = 0
        if row_index < last_row:
            total += walk(row_index + 1, column_index)
        if column_index < last_column:
            total += walk(row_index, column_index + 1)
        return total

    return str(walk(0, 0))


# ---------------------------------------------------------------------------
# Longest Palindromic Substring
# ---------------------------------------------------------------------------


def solve_longest_palindromic_substring(stdin_text: str) -> str:
    """Find the leftmost longest palindromic substring by centre expansion.

    Parameters
    ----------
    stdin_text : str
        One line holding the string.

    Returns
    -------
    str
        The leftmost substring of maximum palindromic length.
    """
    text = stdin_text.strip()
    best_start, best_length = 0, 1
    for centre in range(len(text)):
        for left_seed, right_seed in ((centre, centre), (centre, centre + 1)):
            left, right = left_seed, right_seed
            while left >= 0 and right < len(text) and text[left] == text[right]:
                left -= 1
                right += 1
            span = right - left - 1
            if span > best_length:
                best_start, best_length = left + 1, span
    return text[best_start : best_start + best_length]


def brute_longest_palindromic_substring(stdin_text: str) -> str:
    """Find the leftmost longest palindrome by scanning lengths downward.

    Parameters
    ----------
    stdin_text : str
        One line holding the string.

    Returns
    -------
    str
        The leftmost substring of maximum palindromic length.
    """
    text = stdin_text.strip()
    for length in range(len(text), 0, -1):
        for start in range(len(text) - length + 1):
            candidate = text[start : start + length]
            if candidate == candidate[::-1]:
                return candidate
    return text


# ---------------------------------------------------------------------------
# Interleaving String
# ---------------------------------------------------------------------------


def solve_interleaving_string(stdin_text: str) -> str:
    """Decide whether the third string is an interleaving of the first two.

    Parameters
    ----------
    stdin_text : str
        Three lines holding s1, s2 and s3.

    Returns
    -------
    str
        "true" or "false".
    """
    lines = stdin_text.split("\n")
    first, second, target = (line.strip() for line in lines[:3])
    if len(first) + len(second) != len(target):
        return "false"
    is_reachable = [[False] * (len(second) + 1) for _ in range(len(first) + 1)]
    is_reachable[0][0] = True
    for taken_first in range(len(first) + 1):
        for taken_second in range(len(second) + 1):
            if not is_reachable[taken_first][taken_second]:
                continue
            consumed = taken_first + taken_second
            if taken_first < len(first) and first[taken_first] == target[consumed]:
                is_reachable[taken_first + 1][taken_second] = True
            if taken_second < len(second) and second[taken_second] == target[consumed]:
                is_reachable[taken_first][taken_second + 1] = True
    return "true" if is_reachable[len(first)][len(second)] else "false"


def brute_interleaving_string(stdin_text: str) -> str:
    """Decide interleaving by recursively consuming one character at a time.

    Parameters
    ----------
    stdin_text : str
        Three lines holding s1, s2 and s3.

    Returns
    -------
    str
        "true" or "false".
    """
    lines = stdin_text.split("\n")
    first, second, target = (line.strip() for line in lines[:3])
    if len(first) + len(second) != len(target):
        return "false"

    def consume(taken_first: int, taken_second: int) -> bool:
        if taken_first == len(first) and taken_second == len(second):
            return True
        consumed = taken_first + taken_second
        if (
            taken_first < len(first)
            and first[taken_first] == target[consumed]
            and consume(taken_first + 1, taken_second)
        ):
            return True
        return (
            taken_second < len(second)
            and second[taken_second] == target[consumed]
            and consume(taken_first, taken_second + 1)
        )

    return "true" if consume(0, 0) else "false"


# ---------------------------------------------------------------------------
# Edit Distance
# ---------------------------------------------------------------------------


def solve_edit_distance(stdin_text: str) -> str:
    """Count the fewest single-character edits turning one word into another.

    Parameters
    ----------
    stdin_text : str
        Two lines holding the source word and the target word.

    Returns
    -------
    str
        The minimum number of insertions, deletions and replacements.
    """
    lines = stdin_text.split("\n")
    source, target = lines[0].strip(), lines[1].strip()
    previous_row = list(range(len(target) + 1))
    for source_index, source_character in enumerate(source, start=1):
        current_row = [source_index]
        for target_index, target_character in enumerate(target, start=1):
            if source_character == target_character:
                current_row.append(previous_row[target_index - 1])
            else:
                current_row.append(
                    1
                    + min(
                        previous_row[target_index - 1],
                        previous_row[target_index],
                        current_row[target_index - 1],
                    )
                )
        previous_row = current_row
    return str(previous_row[len(target)])


def brute_edit_distance(stdin_text: str) -> str:
    """Count the fewest edits by recursing over the three possible operations.

    Parameters
    ----------
    stdin_text : str
        Two lines holding the source word and the target word.

    Returns
    -------
    str
        The minimum number of insertions, deletions and replacements.
    """
    lines = stdin_text.split("\n")
    source, target = lines[0].strip(), lines[1].strip()

    def distance(source_length: int, target_length: int) -> int:
        if source_length == 0:
            return target_length
        if target_length == 0:
            return source_length
        if source[source_length - 1] == target[target_length - 1]:
            return distance(source_length - 1, target_length - 1)
        return 1 + min(
            distance(source_length - 1, target_length),
            distance(source_length, target_length - 1),
            distance(source_length - 1, target_length - 1),
        )

    return str(distance(len(source), len(target)))


# ---------------------------------------------------------------------------
# Best Time to Buy and Sell Stock III
# ---------------------------------------------------------------------------


def _read_prices(stdin_text: str) -> list[int]:
    """Parse a count line followed by that many prices.

    Parameters
    ----------
    stdin_text : str
        Count line, then the prices on one space separated line.

    Returns
    -------
    list[int]
        The daily prices.
    """
    tokens = stdin_text.split()
    price_count = int(tokens[0])
    return [int(token) for token in tokens[1 : 1 + price_count]]


def solve_best_time_to_buy_and_sell_stock_iii(stdin_text: str) -> str:
    """Maximise profit over at most two complete buy-and-sell rounds.

    Parameters
    ----------
    stdin_text : str
        Count line, then the prices on one space separated line.

    Returns
    -------
    str
        The largest achievable profit.
    """
    prices = _read_prices(stdin_text)
    first_buy = float("-inf")
    first_sell = 0.0
    second_buy = float("-inf")
    second_sell = 0.0
    for price in prices:
        first_buy = max(first_buy, -price)
        first_sell = max(first_sell, first_buy + price)
        second_buy = max(second_buy, first_sell - price)
        second_sell = max(second_sell, second_buy + price)
    return str(int(second_sell))


def brute_best_time_to_buy_and_sell_stock_iii(stdin_text: str) -> str:
    """Maximise profit by enumerating every pair of disjoint trade windows.

    Parameters
    ----------
    stdin_text : str
        Count line, then the prices on one space separated line.

    Returns
    -------
    str
        The largest achievable profit.
    """
    prices = _read_prices(stdin_text)
    day_count = len(prices)
    best = 0
    for first_buy_day in range(day_count):
        for first_sell_day in range(first_buy_day, day_count):
            first_profit = prices[first_sell_day] - prices[first_buy_day]
            best = max(best, first_profit)
            for second_buy_day in range(first_sell_day, day_count):
                for second_sell_day in range(second_buy_day, day_count):
                    second_profit = prices[second_sell_day] - prices[second_buy_day]
                    best = max(best, first_profit + second_profit)
    return str(best)


# ---------------------------------------------------------------------------
# Best Time to Buy and Sell Stock IV
# ---------------------------------------------------------------------------


def _read_capped_prices(stdin_text: str) -> tuple[int, list[int]]:
    """Parse a transaction cap, a count line and that many prices.

    Parameters
    ----------
    stdin_text : str
        Cap line, count line, then the prices on one space separated line.

    Returns
    -------
    tuple[int, list[int]]
        The transaction cap and the daily prices.
    """
    tokens = stdin_text.split()
    transaction_cap = int(tokens[0])
    price_count = int(tokens[1])
    return transaction_cap, [int(token) for token in tokens[2 : 2 + price_count]]


def solve_best_time_to_buy_and_sell_stock_iv(stdin_text: str) -> str:
    """Maximise profit over at most k complete buy-and-sell rounds.

    Parameters
    ----------
    stdin_text : str
        Cap line, count line, then the prices on one space separated line.

    Returns
    -------
    str
        The largest achievable profit.
    """
    transaction_cap, prices = _read_capped_prices(stdin_text)
    if transaction_cap == 0 or not prices:
        return "0"
    best_held = [float("-inf")] * (transaction_cap + 1)
    best_free = [0.0] * (transaction_cap + 1)
    for price in prices:
        for round_index in range(1, transaction_cap + 1):
            best_held[round_index] = max(best_held[round_index], best_free[round_index - 1] - price)
            best_free[round_index] = max(best_free[round_index], best_held[round_index] + price)
    return str(int(best_free[transaction_cap]))


def brute_best_time_to_buy_and_sell_stock_iv(stdin_text: str) -> str:
    """Maximise profit by recursing over hold, sell and skip on every day.

    Parameters
    ----------
    stdin_text : str
        Cap line, count line, then the prices on one space separated line.

    Returns
    -------
    str
        The largest achievable profit.
    """
    transaction_cap, prices = _read_capped_prices(stdin_text)

    def explore(day_index: int, rounds_left: int, is_holding: bool) -> int:
        if day_index == len(prices) or rounds_left == 0:
            return 0
        best = explore(day_index + 1, rounds_left, is_holding)
        if is_holding:
            best = max(best, prices[day_index] + explore(day_index + 1, rounds_left - 1, False))
        else:
            best = max(best, -prices[day_index] + explore(day_index + 1, rounds_left, True))
        return best

    return str(explore(0, transaction_cap, False))


# ---------------------------------------------------------------------------
# Maximal Square
# ---------------------------------------------------------------------------


def solve_maximal_square(stdin_text: str) -> str:
    """Find the area of the largest all-ones square inside a binary grid.

    Parameters
    ----------
    stdin_text : str
        Dimension line, then one grid row per line of 0 and 1 markers.

    Returns
    -------
    str
        The area of the largest all-ones square.
    """
    grid = _read_grid(stdin_text)
    row_count, column_count = len(grid), len(grid[0])
    side_at = [[0] * (column_count + 1) for _ in range(row_count + 1)]
    best_side = 0
    for row_index in range(row_count):
        for column_index in range(column_count):
            if grid[row_index][column_index] == 0:
                continue
            side_at[row_index + 1][column_index + 1] = 1 + min(
                side_at[row_index][column_index + 1],
                side_at[row_index + 1][column_index],
                side_at[row_index][column_index],
            )
            best_side = max(best_side, side_at[row_index + 1][column_index + 1])
    return str(best_side * best_side)


def brute_maximal_square(stdin_text: str) -> str:
    """Find the largest all-ones square by testing every corner and side.

    Parameters
    ----------
    stdin_text : str
        Dimension line, then one grid row per line of 0 and 1 markers.

    Returns
    -------
    str
        The area of the largest all-ones square.
    """
    grid = _read_grid(stdin_text)
    row_count, column_count = len(grid), len(grid[0])
    best_side = 0
    for row_index in range(row_count):
        for column_index in range(column_count):
            largest_possible = min(row_count - row_index, column_count - column_index)
            for side in range(1, largest_possible + 1):
                is_solid = all(
                    grid[row_index + offset_row][column_index + offset_column] == 1
                    for offset_row in range(side)
                    for offset_column in range(side)
                )
                if not is_solid:
                    break
                best_side = max(best_side, side)
    return str(best_side * best_side)


PROBLEMS: list[dict[str, Any]] = [
    {
        "title": "Palindrome Number",
        "level": "Easy",
        "topics": "Math, Two Pointers",
        "companies": "Amazon, Adobe, Bloomberg",
        "description": """Read one integer and decide whether its decimal form reads the same from
left to right as it does from right to left. A leading minus sign counts as part
of the number, so any negative value fails straight away.

Input: a single line holding the integer.

Output: a single line holding `true` when the number is a palindrome and
`false` otherwise.

""",
        "examples": """```
Input
121

Output
true
```

```
Input
-121

Output
false
```

""",
        "constraints": """- The integer fits in a signed 32-bit range: -2147483648 to 2147483647.
- The line carries no spaces and no leading zeroes.

""",
        "inputs": ["121", "-121", "10", "0", "1000000001", "-2147483648"],
        "solve": solve_palindrome_number,
        "brute": brute_palindrome_number,
    },
    {
        "title": "Plus One",
        "level": "Easy",
        "topics": "Array, Math",
        "companies": "Google, Microsoft, Apple",
        "description": """A non-negative whole number is given one digit at a time, most significant digit
first. Add one to that number and print the digits of the result. A number such
as 999 grows an extra digit, so the answer may be one digit longer than the
input.

Input: the first line holds the number of digits. The second line holds that
many digits separated by single spaces.

Output: a single line holding the digits of the incremented number, separated by
single spaces.

""",
        "examples": """```
Input
3
1 2 3

Output
1 2 4
```

```
Input
3
9 9 9

Output
1 0 0 0
```

""",
        "constraints": """- 1 <= number of digits <= 100.
- Each digit is between 0 and 9.
- The number has no leading zero unless it is the single digit 0.

""",
        "inputs": ["3\n1 2 3", "3\n9 9 9", "1\n0", "1\n9", "4\n4 3 2 1", "2\n1 9"],
        "solve": solve_plus_one,
        "brute": brute_plus_one,
    },
    {
        "title": "Factorial Trailing Zeroes",
        "level": "Medium",
        "topics": "Math",
        "companies": "Bloomberg, Expedia, Goldman Sachs",
        "description": """Given n, report how many zeroes sit at the end of n factorial. Only count the
unbroken run of zeroes at the very end of the number, not zeroes that appear
elsewhere in it.

Input: a single line holding n.

Output: a single line holding the number of trailing zeroes.

""",
        "examples": """```
Input
3

Output
0
```

```
Input
5

Output
1
```

""",
        "constraints": """- 0 <= n <= 10000.

""",
        "inputs": ["3", "5", "0", "100", "1000", "9999"],
        "solve": solve_factorial_trailing_zeroes,
        "brute": brute_factorial_trailing_zeroes,
    },
    {
        "title": "Sqrt(x)",
        "level": "Easy",
        "topics": "Math, Binary Search",
        "companies": "Facebook, Apple, Uber",
        "description": """Compute the square root of a non-negative integer and throw away anything after
the decimal point. The answer is the largest whole number whose square is still
at most x, so the root of 8 truncates to 2 rather than rounding up to 3.

Input: a single line holding x.

Output: a single line holding the truncated integer square root of x.

""",
        "examples": """```
Input
4

Output
2
```

```
Input
8

Output
2
```

""",
        "constraints": """- 0 <= x <= 2147483647.

""",
        "inputs": ["4", "8", "0", "1", "2147395600", "2147483647"],
        "solve": solve_sqrt_x,
        "brute": brute_sqrt_x,
    },
    {
        "title": "Pow(x, n)",
        "level": "Medium",
        "topics": "Math, Recursion, Divide and Conquer",
        "companies": "Facebook, LinkedIn, Bloomberg",
        "description": """Raise a decimal number x to an integer power n. The exponent may be negative,
in which case the answer is one divided by x raised to the matching positive
power.

Input: the first line holds x written as a decimal number. The second line holds
the integer exponent n.

Output: a single line holding the result written with exactly five digits after
the decimal point.

""",
        "examples": """```
Input
2.00000
10

Output
1024.00000
```

```
Input
2.00000
-2

Output
0.25000
```

""",
        "constraints": """- -100.0 < x < 100.0 and x is not zero when n is negative.
- -100 <= n <= 100.
- The result always fits in a double precision float.

""",
        "inputs": [
            "2.00000\n10",
            "2.10000\n3",
            "2.00000\n-2",
            "1.00000\n0",
            "-2.00000\n3",
            "0.50000\n-3",
        ],
        "solve": solve_pow_x_n,
        "brute": brute_pow_x_n,
    },
    {
        "title": "Max Points on a Line",
        "level": "Hard",
        "topics": "Math, Geometry, Hash Table",
        "companies": "LinkedIn, Google, Twitter",
        "description": """A set of distinct points on a plane is given. Find the largest number of those
points that a single straight line can pass through. A line may run in any
direction, including straight up and down.

Input: the first line holds the number of points. Each of the next lines holds
one point as its x coordinate and its y coordinate separated by a space.

Output: a single line holding the size of the largest group of points lying on
one line.

""",
        "examples": """```
Input
3
1 1
2 2
3 3

Output
3
```

```
Input
6
1 1
3 2
5 3
4 1
2 3
1 4

Output
4
```

""",
        "constraints": """- 1 <= number of points <= 300.
- -10000 <= x, y <= 10000.
- No two given points are the same.

""",
        "inputs": [
            "3\n1 1\n2 2\n3 3",
            "6\n1 1\n3 2\n5 3\n4 1\n2 3\n1 4",
            "1\n0 0",
            "2\n-1 -1\n4 4",
            "4\n0 0\n0 1\n0 2\n1 5",
            "4\n0 0\n1 5\n2 1\n3 7",
        ],
        "solve": solve_max_points_on_a_line,
        "brute": brute_max_points_on_a_line,
    },
    {
        "title": "Climbing Stairs",
        "level": "Easy",
        "topics": "Dynamic Programming, Math",
        "companies": "Amazon, Adobe, Apple",
        "description": """A staircase has n steps. Each move climbs either one step or two steps. Count
how many different orders of moves reach the top.

Input: a single line holding n.

Output: a single line holding the number of distinct ways to reach the top.

""",
        "examples": """```
Input
2

Output
2
```

```
Input
3

Output
3
```

""",
        "constraints": """- 1 <= n <= 45.

""",
        "inputs": ["2", "3", "1", "45", "10", "30"],
        "solve": solve_climbing_stairs,
        "brute": brute_climbing_stairs,
    },
    {
        "title": "House Robber",
        "level": "Medium",
        "topics": "Dynamic Programming, Array",
        "companies": "Amazon, LinkedIn, Google",
        "description": """Houses stand in a row and each one holds a known amount of money. Two houses
next to each other cannot both be emptied. Work out the largest total that can
be taken.

Input: the first line holds the number of houses. The second line holds that
many house values separated by single spaces.

Output: a single line holding the largest total that can be taken.

""",
        "examples": """```
Input
4
1 2 3 1

Output
4
```

```
Input
5
2 7 9 3 1

Output
12
```

""",
        "constraints": """- 1 <= number of houses <= 15.
- 0 <= house value <= 400.

""",
        "inputs": [
            "4\n1 2 3 1",
            "5\n2 7 9 3 1",
            "1\n0",
            "1\n100",
            "6\n2 1 1 2 1 2",
            "10\n5 5 10 100 10 5 5 1 1 1",
        ],
        "solve": solve_house_robber,
        "brute": brute_house_robber,
    },
    {
        "title": "Word Break",
        "level": "Medium",
        "topics": "Dynamic Programming, String, Hash Table",
        "companies": "Facebook, Amazon, Uber",
        "description": """Given a string and a dictionary, decide whether the string can be cut into a
sequence of dictionary words laid end to end with nothing left over. A
dictionary word may be reused as many times as needed.

Input: the first line holds the string. The second line holds the number of
dictionary words. Each of the next lines holds one dictionary word.

Output: a single line holding `true` when such a split exists and `false`
otherwise.

""",
        "examples": """```
Input
leetcode
2
leet
code

Output
true
```

```
Input
catsandog
5
cats
dog
sand
and
cat

Output
false
```

""",
        "constraints": """- 1 <= length of the string <= 300.
- 1 <= number of dictionary words <= 1000.
- 1 <= length of each dictionary word <= 20.
- Every string holds lowercase English letters only.

""",
        "inputs": [
            "leetcode\n2\nleet\ncode",
            "applepenapple\n2\napple\npen",
            "catsandog\n5\ncats\ndog\nsand\nand\ncat",
            "a\n1\na",
            "b\n1\na",
            "aaaaaaaaaaaaaaaaaaab\n2\na\naa",
        ],
        "solve": solve_word_break,
        "brute": brute_word_break,
    },
    {
        "title": "Coin Change",
        "level": "Medium",
        "topics": "Dynamic Programming, Breadth-First Search, Array",
        "companies": "Amazon, Microsoft, Goldman Sachs",
        "description": """Coins of given face values are available in unlimited supply. Make up an exact
target amount using as few coins as possible.

Input: the first line holds the target amount. The second line holds the number
of coin types. The third line holds that many coin values separated by single
spaces.

Output: a single line holding the smallest number of coins that reaches the
amount, or `-1` when no combination of the given coins adds up to it.

""",
        "examples": """```
Input
11
3
1 2 5

Output
3
```

```
Input
3
1
2

Output
-1
```

""",
        "constraints": """- 0 <= amount <= 10000.
- 1 <= number of coin types <= 12.
- 1 <= coin value <= 1000.

""",
        "inputs": ["11\n3\n1 2 5", "3\n1\n2", "0\n1\n1", "100\n4\n1 5 10 25", "7\n2\n2 4"],
        "solve": solve_coin_change,
        "brute": brute_coin_change,
    },
    {
        "title": "Longest Increasing Subsequence",
        "level": "Medium",
        "topics": "Dynamic Programming, Binary Search, Array",
        "companies": "Microsoft, Amazon, Facebook",
        "description": """Pick values out of an array, keeping their original left-to-right order, so that
each picked value is strictly larger than the one before it. Report how many
values the longest such pick contains. The picked values need not sit next to
each other in the array.

Input: the first line holds the number of values. The second line holds that
many values separated by single spaces.

Output: a single line holding the length of the longest strictly increasing
pick.

""",
        "examples": """```
Input
8
10 9 2 5 3 7 101 18

Output
4
```

```
Input
7
7 7 7 7 7 7 7

Output
1
```

""",
        "constraints": """- 1 <= number of values <= 9.
- -10000 <= each value <= 10000.

""",
        "inputs": [
            "8\n10 9 2 5 3 7 101 18",
            "6\n0 1 0 3 2 3",
            "7\n7 7 7 7 7 7 7",
            "1\n5",
            "5\n5 4 3 2 1",
            "9\n1 3 6 7 9 4 10 5 6",
        ],
        "solve": solve_longest_increasing_subsequence,
        "brute": brute_longest_increasing_subsequence,
    },
    {
        "title": "Triangle",
        "level": "Medium",
        "topics": "Dynamic Programming, Array",
        "companies": "Bloomberg, Amazon, Adobe",
        "description": """Numbers are arranged in a triangle whose first row holds one value, second row
two values, and so on. A walk starts at the single top value and, on each step
down, moves to one of the two values directly beneath the current one. Find the
smallest total a walk from the top row to the bottom row can collect.

Input: the first line holds the number of rows. Each of the next lines holds one
row, with row number i carrying i values separated by single spaces.

Output: a single line holding the smallest achievable total.

""",
        "examples": """```
Input
4
2
3 4
6 5 7
4 1 8 3

Output
11
```

```
Input
1
-10

Output
-10
```

""",
        "constraints": """- 1 <= number of rows <= 10.
- -10000 <= each value <= 10000.

""",
        "inputs": [
            "4\n2\n3 4\n6 5 7\n4 1 8 3",
            "1\n-10",
            "2\n1\n2 3",
            "3\n-1\n2 3\n1 -1 -3",
            "5\n1\n2 3\n4 5 6\n7 8 9 10\n11 12 13 14 15",
        ],
        "solve": solve_triangle,
        "brute": brute_triangle,
    },
    {
        "title": "Minimum Path Sum",
        "level": "Medium",
        "topics": "Dynamic Programming, Array, Matrix",
        "companies": "Amazon, Google, Goldman Sachs",
        "description": """A grid of non-negative costs is given. A walk starts at the top-left cell, ends
at the bottom-right cell, and may only step one cell right or one cell down.
Find the smallest total cost such a walk can collect, counting both the starting
cell and the finishing cell.

Input: the first line holds the number of rows and the number of columns,
separated by a space. Each of the next lines holds one grid row with that many
values separated by single spaces.

Output: a single line holding the smallest achievable total cost.

""",
        "examples": """```
Input
3 3
1 3 1
1 5 1
4 2 1

Output
7
```

```
Input
2 3
1 2 3
4 5 6

Output
12
```

""",
        "constraints": """- 1 <= rows, columns <= 10.
- 0 <= each grid value <= 200.

""",
        "inputs": [
            "3 3\n1 3 1\n1 5 1\n4 2 1",
            "2 3\n1 2 3\n4 5 6",
            "1 1\n5",
            "1 4\n1 2 3 4",
            "4 1\n1\n2\n3\n4",
            "3 4\n1 1 1 1\n9 9 9 1\n1 1 1 1",
        ],
        "solve": solve_minimum_path_sum,
        "brute": brute_minimum_path_sum,
    },
    {
        "title": "Unique Paths II",
        "level": "Medium",
        "topics": "Dynamic Programming, Array, Matrix",
        "companies": "Amazon, Microsoft, Bloomberg",
        "description": """A grid is marked with `0` for an open cell and `1` for a blocked cell. Count the
routes from the top-left cell to the bottom-right cell that only step right or
down and never enter a blocked cell. If either the starting cell or the
finishing cell is blocked the answer is 0.

Input: the first line holds the number of rows and the number of columns,
separated by a space. Each of the next lines holds one grid row with that many
markers separated by single spaces.

Output: a single line holding the number of routes.

""",
        "examples": """```
Input
3 3
0 0 0
0 1 0
0 0 0

Output
2
```

```
Input
1 1
1

Output
0
```

""",
        "constraints": """- 1 <= rows, columns <= 10.
- Each marker is 0 or 1.

""",
        "inputs": [
            "3 3\n0 0 0\n0 1 0\n0 0 0",
            "2 2\n0 1\n0 0",
            "1 1\n0",
            "1 1\n1",
            "3 3\n1 0 0\n0 0 0\n0 0 0",
            "3 7\n0 0 0 0 0 0 0\n0 0 1 0 0 0 0\n0 0 0 0 0 0 0",
        ],
        "solve": solve_unique_paths_ii,
        "brute": brute_unique_paths_ii,
    },
    {
        "title": "Longest Palindromic Substring",
        "level": "Medium",
        "topics": "Dynamic Programming, String, Two Pointers",
        "companies": "Amazon, Microsoft, Adobe",
        "description": """Find the longest run of neighbouring characters in a string that reads the same
in both directions. When several runs tie for the longest, print the one that
starts earliest in the string.

Input: a single line holding the string.

Output: a single line holding the leftmost longest palindromic run.

""",
        "examples": """```
Input
babad

Output
bab
```

```
Input
cbbd

Output
bb
```

""",
        "constraints": """- 1 <= length of the string <= 1000.
- The string holds lowercase and uppercase English letters only.

""",
        "inputs": ["babad", "cbbd", "a", "ac", "aaaa", "forgeeksskeegfor"],
        "solve": solve_longest_palindromic_substring,
        "brute": brute_longest_palindromic_substring,
    },
    {
        "title": "Interleaving String",
        "level": "Medium",
        "topics": "Dynamic Programming, String",
        "companies": "Google, Amazon, Apple",
        "description": """Three strings are given. Decide whether the third one can be built by taking the
characters of the first two in order and weaving them together, so that the
characters of each source string keep their relative order and every character
of both source strings is used exactly once.

Input: the first line holds s1, the second line holds s2 and the third line
holds s3.

Output: a single line holding `true` when s3 is such a weave of s1 and s2, and
`false` otherwise.

""",
        "examples": """```
Input
aabcc
dbbca
aadbbcbcac

Output
true
```

```
Input
aabcc
dbbca
aadbbbaccc

Output
false
```

""",
        "constraints": """- 1 <= length of s1, s2 <= 50.
- 1 <= length of s3 <= 100.
- Every string holds lowercase English letters only.

""",
        "inputs": [
            "aabcc\ndbbca\naadbbcbcac",
            "aabcc\ndbbca\naadbbbaccc",
            "a\nb\nab",
            "a\nb\nba",
            "a\nb\na",
            "abc\nde\nabdce",
        ],
        "solve": solve_interleaving_string,
        "brute": brute_interleaving_string,
    },
    {
        "title": "Edit Distance",
        "level": "Medium",
        "topics": "Dynamic Programming, String",
        "companies": "Google, Amazon, Microsoft",
        "description": """Turn one word into another using as few single-character edits as possible. An
edit inserts a character, deletes a character, or replaces one character with
another. Report the smallest number of edits needed.

Input: the first line holds the starting word. The second line holds the target
word.

Output: a single line holding the smallest number of edits.

""",
        "examples": """```
Input
horse
ros

Output
3
```

```
Input
kitten
sitting

Output
3
```

""",
        "constraints": """- 1 <= length of each word <= 8.
- Both words hold lowercase English letters only.

""",
        "inputs": [
            "horse\nros",
            "kitten\nsitting",
            "a\na",
            "a\nb",
            "abc\nabcdef",
            "sunday\nsaturday",
        ],
        "solve": solve_edit_distance,
        "brute": brute_edit_distance,
    },
    {
        "title": "Best Time to Buy and Sell Stock III",
        "level": "Hard",
        "topics": "Dynamic Programming, Array",
        "companies": "Amazon, Bloomberg, Facebook",
        "description": """Daily prices of one share are given. At most two complete rounds of buying and
then selling are allowed, and a share must be sold before the next one is
bought. Find the largest profit available. Doing nothing is allowed, so the
answer is never below zero.

Input: the first line holds the number of days. The second line holds that many
prices separated by single spaces, in day order.

Output: a single line holding the largest achievable profit.

""",
        "examples": """```
Input
8
3 3 5 0 0 3 1 4

Output
6
```

```
Input
5
7 6 4 3 1

Output
0
```

""",
        "constraints": """- 1 <= number of days <= 10.
- 0 <= each price <= 100000.

""",
        "inputs": [
            "8\n3 3 5 0 0 3 1 4",
            "5\n1 2 3 4 5",
            "5\n7 6 4 3 1",
            "1\n5",
            "6\n1 2 4 2 5 7",
            "2\n2 1",
        ],
        "solve": solve_best_time_to_buy_and_sell_stock_iii,
        "brute": brute_best_time_to_buy_and_sell_stock_iii,
    },
    {
        "title": "Best Time to Buy and Sell Stock IV",
        "level": "Hard",
        "topics": "Dynamic Programming, Array",
        "companies": "Amazon, Citadel, Bloomberg",
        "description": """Daily prices of one share are given together with a cap k on how many complete
rounds of buying and then selling may be made. A share must be sold before the
next one is bought. Find the largest profit available. Doing nothing is allowed,
so the answer is never below zero.

Input: the first line holds the cap k. The second line holds the number of days.
The third line holds that many prices separated by single spaces, in day order.

Output: a single line holding the largest achievable profit.

""",
        "examples": """```
Input
2
4
2 4 1 7

Output
8
```

```
Input
0
3
1 2 3

Output
0
```

""",
        "constraints": """- 0 <= k <= 10.
- 1 <= number of days <= 10.
- 0 <= each price <= 1000.

""",
        "inputs": [
            "2\n4\n2 4 1 7",
            "2\n6\n3 2 6 5 0 3",
            "1\n3\n2 4 1",
            "0\n3\n1 2 3",
            "5\n4\n1 2 3 4",
            "3\n5\n5 4 3 2 1",
        ],
        "solve": solve_best_time_to_buy_and_sell_stock_iv,
        "brute": brute_best_time_to_buy_and_sell_stock_iv,
    },
    {
        "title": "Maximal Square",
        "level": "Medium",
        "topics": "Dynamic Programming, Matrix",
        "companies": "Facebook, Amazon, Airbnb",
        "description": """A grid is filled with `0` and `1` markers. Find the largest square block made up
only of `1` markers and report its area, which is its side length multiplied by
itself. When the grid holds no `1` marker at all the area is 0.

Input: the first line holds the number of rows and the number of columns,
separated by a space. Each of the next lines holds one grid row with that many
markers separated by single spaces.

Output: a single line holding the area of the largest all-ones square.

""",
        "examples": """```
Input
4 5
1 0 1 0 0
1 0 1 1 1
1 1 1 1 1
1 0 0 1 0

Output
4
```

```
Input
3 3
0 0 0
0 0 0
0 0 0

Output
0
```

""",
        "constraints": """- 1 <= rows, columns <= 20.
- Each marker is 0 or 1.

""",
        "inputs": [
            "4 5\n1 0 1 0 0\n1 0 1 1 1\n1 1 1 1 1\n1 0 0 1 0",
            "2 2\n0 1\n1 0",
            "1 1\n0",
            "1 1\n1",
            "3 3\n0 0 0\n0 0 0\n0 0 0",
            "4 4\n1 1 1 1\n1 1 1 1\n1 1 1 1\n1 1 1 1",
        ],
        "solve": solve_maximal_square,
        "brute": brute_maximal_square,
    },
]
