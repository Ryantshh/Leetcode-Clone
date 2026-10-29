"""Problem specs for the arrays and strings group of the study plan.

Every spec is a complete stdin-to-stdout task: the editor ships no starter code,
so each description fixes the exact input and output bytes.
"""

from __future__ import annotations

from collections import Counter

# ---------------------------------------------------------------------------
# Shared parsing helpers
# ---------------------------------------------------------------------------


def line_at(stdin_text: str, line_index: int) -> str:
    """Return one line of a payload, or an empty string when the line is absent.

    Parameters
    ----------
    stdin_text : str
        Whole stdin payload.
    line_index : int
        Zero based line number.

    Returns
    -------
    str
        The requested line, or "" when the payload has fewer lines.
    """
    lines = stdin_text.split("\n")
    return lines[line_index] if line_index < len(lines) else ""


def parse_integer_line(line: str) -> list[int]:
    """Parse a whitespace separated line of integers.

    Parameters
    ----------
    line : str
        Line of integer tokens, possibly empty.

    Returns
    -------
    list[int]
        Parsed integers in input order.
    """
    return [int(token) for token in line.split()]


def format_integers(values: list[int]) -> str:
    """Join integers with single spaces.

    Parameters
    ----------
    values : list[int]
        Integers to render.

    Returns
    -------
    str
        Space separated decimal representation.
    """
    return " ".join(str(value) for value in values)


def format_kept_prefix(kept: list[int]) -> str:
    """Render a count line followed by the kept elements when there are any.

    Parameters
    ----------
    kept : list[int]
        Elements that survive an in-place removal.

    Returns
    -------
    str
        Either "0" alone, or the count followed by the elements on a second line.
    """
    if not kept:
        return "0"
    return f"{len(kept)}\n{format_integers(kept)}"


# ---------------------------------------------------------------------------
# Merge Sorted Array
# ---------------------------------------------------------------------------


def solve_merge_sorted_array(stdin_text: str) -> str:
    """Merge two sorted arrays by filling the first array from the back.

    Parameters
    ----------
    stdin_text : str
        Sizes line, then the first array, then the second array.

    Returns
    -------
    str
        The merged array, space separated.
    """
    first_count, second_count = parse_integer_line(line_at(stdin_text, 0))
    first_values = parse_integer_line(line_at(stdin_text, 1))
    second_values = parse_integer_line(line_at(stdin_text, 2))

    merged = first_values + [0] * second_count
    write_position = first_count + second_count - 1
    first_cursor = first_count - 1
    second_cursor = second_count - 1
    while second_cursor >= 0:
        if first_cursor >= 0 and first_values[first_cursor] > second_values[second_cursor]:
            merged[write_position] = first_values[first_cursor]
            first_cursor -= 1
        else:
            merged[write_position] = second_values[second_cursor]
            second_cursor -= 1
        write_position -= 1
    return format_integers(merged)


def brute_merge_sorted_array(stdin_text: str) -> str:
    """Merge two sorted arrays by concatenating and sorting.

    Parameters
    ----------
    stdin_text : str
        Sizes line, then the first array, then the second array.

    Returns
    -------
    str
        The merged array, space separated.
    """
    first_values = parse_integer_line(line_at(stdin_text, 1))
    second_values = parse_integer_line(line_at(stdin_text, 2))
    return format_integers(sorted(first_values + second_values))


# ---------------------------------------------------------------------------
# Remove Element
# ---------------------------------------------------------------------------


def solve_remove_element(stdin_text: str) -> str:
    """Compact an array in place by dropping every copy of one value.

    Parameters
    ----------
    stdin_text : str
        Length line, values line, then the value to remove.

    Returns
    -------
    str
        Kept count, then the kept values when the count is positive.
    """
    values = parse_integer_line(line_at(stdin_text, 1))
    removed_value = int(line_at(stdin_text, 2))

    write_position = 0
    for value in values:
        if value != removed_value:
            values[write_position] = value
            write_position += 1
    return format_kept_prefix(values[:write_position])


def brute_remove_element(stdin_text: str) -> str:
    """Rebuild the array without one value using a filtered copy.

    Parameters
    ----------
    stdin_text : str
        Length line, values line, then the value to remove.

    Returns
    -------
    str
        Kept count, then the kept values when the count is positive.
    """
    values = parse_integer_line(line_at(stdin_text, 1))
    removed_value = int(line_at(stdin_text, 2))
    kept = [value for value in values if value != removed_value]
    return format_kept_prefix(kept)


# ---------------------------------------------------------------------------
# Remove Duplicates from Sorted Array
# ---------------------------------------------------------------------------


def solve_remove_duplicates_from_sorted_array(stdin_text: str) -> str:
    """Compact a sorted array in place so each value appears once.

    Parameters
    ----------
    stdin_text : str
        Length line, then the sorted values.

    Returns
    -------
    str
        Kept count, then the kept values.
    """
    values = parse_integer_line(line_at(stdin_text, 1))
    write_position = 0
    for value in values:
        if write_position == 0 or values[write_position - 1] != value:
            values[write_position] = value
            write_position += 1
    return format_kept_prefix(values[:write_position])


def brute_remove_duplicates_from_sorted_array(stdin_text: str) -> str:
    """Deduplicate a sorted array through a sorted set.

    Parameters
    ----------
    stdin_text : str
        Length line, then the sorted values.

    Returns
    -------
    str
        Kept count, then the kept values.
    """
    values = parse_integer_line(line_at(stdin_text, 1))
    return format_kept_prefix(sorted(set(values)))


# ---------------------------------------------------------------------------
# Remove Duplicates from Sorted Array II
# ---------------------------------------------------------------------------


def solve_remove_duplicates_from_sorted_array_ii(stdin_text: str) -> str:
    """Compact a sorted array in place so each value appears at most twice.

    Parameters
    ----------
    stdin_text : str
        Length line, then the sorted values.

    Returns
    -------
    str
        Kept count, then the kept values.
    """
    values = parse_integer_line(line_at(stdin_text, 1))
    write_position = 0
    for value in values:
        if write_position < 2 or values[write_position - 2] != value:
            values[write_position] = value
            write_position += 1
    return format_kept_prefix(values[:write_position])


def brute_remove_duplicates_from_sorted_array_ii(stdin_text: str) -> str:
    """Rebuild a sorted array keeping at most two copies, using occurrence counts.

    Parameters
    ----------
    stdin_text : str
        Length line, then the sorted values.

    Returns
    -------
    str
        Kept count, then the kept values.
    """
    values = parse_integer_line(line_at(stdin_text, 1))
    occurrences = Counter(values)
    kept: list[int] = []
    for value in sorted(occurrences):
        kept.extend([value] * min(2, occurrences[value]))
    return format_kept_prefix(kept)


# ---------------------------------------------------------------------------
# Majority Element
# ---------------------------------------------------------------------------


def solve_majority_element(stdin_text: str) -> str:
    """Find the value occupying more than half the array by vote cancelling.

    Parameters
    ----------
    stdin_text : str
        Length line, then the values.

    Returns
    -------
    str
        The majority value.
    """
    values = parse_integer_line(line_at(stdin_text, 1))
    candidate = values[0]
    balance = 0
    for value in values:
        if balance == 0:
            candidate = value
        balance += 1 if value == candidate else -1
    return str(candidate)


def brute_majority_element(stdin_text: str) -> str:
    """Find the most frequent value by tallying every value.

    Parameters
    ----------
    stdin_text : str
        Length line, then the values.

    Returns
    -------
    str
        The majority value.
    """
    values = parse_integer_line(line_at(stdin_text, 1))
    occurrences = Counter(values)
    best_value = values[0]
    for value in values:
        if occurrences[value] > occurrences[best_value]:
            best_value = value
    return str(best_value)


# ---------------------------------------------------------------------------
# Rotate Array
# ---------------------------------------------------------------------------


def solve_rotate_array(stdin_text: str) -> str:
    """Rotate an array right by k steps using three in-place reversals.

    Parameters
    ----------
    stdin_text : str
        Length and shift line, then the values.

    Returns
    -------
    str
        The rotated array, space separated.
    """
    length, shift = parse_integer_line(line_at(stdin_text, 0))
    values = parse_integer_line(line_at(stdin_text, 1))
    shift %= length

    def reverse_range(low: int, high: int) -> None:
        """Reverse a closed index range of the working array.

        Parameters
        ----------
        low : int
            First index of the range.
        high : int
            Last index of the range.

        Returns
        -------
        None
        """
        while low < high:
            values[low], values[high] = values[high], values[low]
            low += 1
            high -= 1

    reverse_range(0, length - 1)
    reverse_range(0, shift - 1)
    reverse_range(shift, length - 1)
    return format_integers(values)


def brute_rotate_array(stdin_text: str) -> str:
    """Rotate an array right by k steps by repeatedly moving the last element.

    Parameters
    ----------
    stdin_text : str
        Length and shift line, then the values.

    Returns
    -------
    str
        The rotated array, space separated.
    """
    length, shift = parse_integer_line(line_at(stdin_text, 0))
    values = parse_integer_line(line_at(stdin_text, 1))
    for _ in range(shift % length):
        values.insert(0, values.pop())
    return format_integers(values)


# ---------------------------------------------------------------------------
# Best Time to Buy and Sell Stock
# ---------------------------------------------------------------------------


def solve_best_time_to_buy_and_sell_stock(stdin_text: str) -> str:
    """Find the best single buy-then-sell profit in one pass.

    Parameters
    ----------
    stdin_text : str
        Length line, then the daily prices.

    Returns
    -------
    str
        The best profit, or 0 when no trade helps.
    """
    prices = parse_integer_line(line_at(stdin_text, 1))
    cheapest_so_far = prices[0]
    best_profit = 0
    for price in prices:
        if price < cheapest_so_far:
            cheapest_so_far = price
        elif price - cheapest_so_far > best_profit:
            best_profit = price - cheapest_so_far
    return str(best_profit)


def brute_best_time_to_buy_and_sell_stock(stdin_text: str) -> str:
    """Find the best single buy-then-sell profit by trying every pair of days.

    Parameters
    ----------
    stdin_text : str
        Length line, then the daily prices.

    Returns
    -------
    str
        The best profit, or 0 when no trade helps.
    """
    prices = parse_integer_line(line_at(stdin_text, 1))
    best_profit = 0
    for buy_day in range(len(prices)):
        for sell_day in range(buy_day + 1, len(prices)):
            best_profit = max(best_profit, prices[sell_day] - prices[buy_day])
    return str(best_profit)


# ---------------------------------------------------------------------------
# Best Time to Buy and Sell Stock II
# ---------------------------------------------------------------------------


def solve_best_time_to_buy_and_sell_stock_ii(stdin_text: str) -> str:
    """Sum every upward price step to get the unlimited-trade profit.

    Parameters
    ----------
    stdin_text : str
        Length line, then the daily prices.

    Returns
    -------
    str
        The best total profit.
    """
    prices = parse_integer_line(line_at(stdin_text, 1))
    total_profit = 0
    for day in range(1, len(prices)):
        if prices[day] > prices[day - 1]:
            total_profit += prices[day] - prices[day - 1]
    return str(total_profit)


def brute_best_time_to_buy_and_sell_stock_ii(stdin_text: str) -> str:
    """Track cash with and without a held share to get the unlimited-trade profit.

    Parameters
    ----------
    stdin_text : str
        Length line, then the daily prices.

    Returns
    -------
    str
        The best total profit.
    """
    prices = parse_integer_line(line_at(stdin_text, 1))
    cash_without_share = 0
    cash_holding_share = -prices[0]
    for price in prices[1:]:
        cash_without_share = max(cash_without_share, cash_holding_share + price)
        cash_holding_share = max(cash_holding_share, cash_without_share - price)
    return str(cash_without_share)


# ---------------------------------------------------------------------------
# Jump Game
# ---------------------------------------------------------------------------


def solve_jump_game(stdin_text: str) -> str:
    """Decide reachability of the last index by tracking the furthest reach.

    Parameters
    ----------
    stdin_text : str
        Length line, then the jump lengths.

    Returns
    -------
    str
        "true" when the last index is reachable, otherwise "false".
    """
    jumps = parse_integer_line(line_at(stdin_text, 1))
    furthest_reach = 0
    for index, jump in enumerate(jumps):
        if index > furthest_reach:
            return "false"
        furthest_reach = max(furthest_reach, index + jump)
    return "true"


def brute_jump_game(stdin_text: str) -> str:
    """Decide reachability of the last index with a backward reachability table.

    Parameters
    ----------
    stdin_text : str
        Length line, then the jump lengths.

    Returns
    -------
    str
        "true" when the last index is reachable, otherwise "false".
    """
    jumps = parse_integer_line(line_at(stdin_text, 1))
    last_index = len(jumps) - 1
    can_reach_end = [False] * len(jumps)
    can_reach_end[last_index] = True
    for index in range(last_index - 1, -1, -1):
        for step in range(1, jumps[index] + 1):
            if index + step <= last_index and can_reach_end[index + step]:
                can_reach_end[index] = True
                break
    return "true" if can_reach_end[0] else "false"


# ---------------------------------------------------------------------------
# Jump Game II
# ---------------------------------------------------------------------------


def solve_jump_game_ii(stdin_text: str) -> str:
    """Count the fewest jumps to the last index by expanding one level at a time.

    Parameters
    ----------
    stdin_text : str
        Length line, then the jump lengths.

    Returns
    -------
    str
        The minimum number of jumps.
    """
    jumps = parse_integer_line(line_at(stdin_text, 1))
    last_index = len(jumps) - 1
    jump_count = 0
    current_level_end = 0
    furthest_reach = 0
    for index in range(last_index):
        furthest_reach = max(furthest_reach, index + jumps[index])
        if index == current_level_end:
            jump_count += 1
            current_level_end = furthest_reach
    return str(jump_count)


def brute_jump_game_ii(stdin_text: str) -> str:
    """Count the fewest jumps to the last index with a quadratic cost table.

    Parameters
    ----------
    stdin_text : str
        Length line, then the jump lengths.

    Returns
    -------
    str
        The minimum number of jumps.
    """
    jumps = parse_integer_line(line_at(stdin_text, 1))
    last_index = len(jumps) - 1
    unreachable = len(jumps) + 1
    fewest_jumps = [unreachable] * len(jumps)
    fewest_jumps[0] = 0
    for index in range(len(jumps)):
        for step in range(1, jumps[index] + 1):
            target = index + step
            if target <= last_index:
                fewest_jumps[target] = min(fewest_jumps[target], fewest_jumps[index] + 1)
    return str(fewest_jumps[last_index])


# ---------------------------------------------------------------------------
# H-Index
# ---------------------------------------------------------------------------


def solve_h_index(stdin_text: str) -> str:
    """Compute the h-index by walking the citation counts in descending order.

    Parameters
    ----------
    stdin_text : str
        Length line, then the citation counts.

    Returns
    -------
    str
        The h-index.
    """
    citations = sorted(parse_integer_line(line_at(stdin_text, 1)), reverse=True)
    h_index = 0
    for position, citation in enumerate(citations, start=1):
        if citation >= position:
            h_index = position
    return str(h_index)


def brute_h_index(stdin_text: str) -> str:
    """Compute the h-index by testing every candidate value from high to low.

    Parameters
    ----------
    stdin_text : str
        Length line, then the citation counts.

    Returns
    -------
    str
        The h-index.
    """
    citations = parse_integer_line(line_at(stdin_text, 1))
    for candidate in range(len(citations), 0, -1):
        well_cited_papers = sum(1 for citation in citations if citation >= candidate)
        if well_cited_papers >= candidate:
            return str(candidate)
    return "0"


# ---------------------------------------------------------------------------
# Insert Delete GetRandom O(1)
# ---------------------------------------------------------------------------


def solve_insert_delete_getrandom_o1(stdin_text: str) -> str:
    """Replay set operations using a hash set plus a swap-to-end index list.

    Parameters
    ----------
    stdin_text : str
        Operation count line, then one operation per line.

    Returns
    -------
    str
        One result line per operation.
    """
    operation_count = int(line_at(stdin_text, 0))
    stored_values: list[int] = []
    position_of_value: dict[int, int] = {}
    results: list[str] = []

    for operation_index in range(1, operation_count + 1):
        tokens = line_at(stdin_text, operation_index).split()
        name = tokens[0]
        if name == "insert":
            value = int(tokens[1])
            if value in position_of_value:
                results.append("false")
            else:
                position_of_value[value] = len(stored_values)
                stored_values.append(value)
                results.append("true")
        elif name == "remove":
            value = int(tokens[1])
            if value not in position_of_value:
                results.append("false")
            else:
                hole = position_of_value.pop(value)
                last_value = stored_values.pop()
                if hole < len(stored_values):
                    stored_values[hole] = last_value
                    position_of_value[last_value] = hole
                results.append("true")
        else:
            results.append("none" if not stored_values else "true")
    return "\n".join(results)


def brute_insert_delete_getrandom_o1(stdin_text: str) -> str:
    """Replay set operations against a plain list scanned linearly.

    Parameters
    ----------
    stdin_text : str
        Operation count line, then one operation per line.

    Returns
    -------
    str
        One result line per operation.
    """
    operation_count = int(line_at(stdin_text, 0))
    members: list[int] = []
    results: list[str] = []

    for operation_index in range(1, operation_count + 1):
        tokens = line_at(stdin_text, operation_index).split()
        name = tokens[0]
        if name == "getRandom":
            results.append("true" if len(members) > 0 else "none")
            continue
        value = int(tokens[1])
        is_member = False
        for member in members:
            if member == value:
                is_member = True
                break
        if name == "insert":
            if is_member:
                results.append("false")
            else:
                members.append(value)
                results.append("true")
        else:
            if is_member:
                members = [member for member in members if member != value]
                results.append("true")
            else:
                results.append("false")
    return "\n".join(results)


# ---------------------------------------------------------------------------
# Product of Array Except Self
# ---------------------------------------------------------------------------


def solve_product_of_array_except_self(stdin_text: str) -> str:
    """Build the except-self products from a prefix sweep and a suffix sweep.

    Parameters
    ----------
    stdin_text : str
        Length line, then the values.

    Returns
    -------
    str
        The products, space separated.
    """
    values = parse_integer_line(line_at(stdin_text, 1))
    products = [1] * len(values)
    prefix_product = 1
    for index in range(len(values)):
        products[index] = prefix_product
        prefix_product *= values[index]
    suffix_product = 1
    for index in range(len(values) - 1, -1, -1):
        products[index] *= suffix_product
        suffix_product *= values[index]
    return format_integers(products)


def brute_product_of_array_except_self(stdin_text: str) -> str:
    """Build the except-self products by multiplying the other entries each time.

    Parameters
    ----------
    stdin_text : str
        Length line, then the values.

    Returns
    -------
    str
        The products, space separated.
    """
    values = parse_integer_line(line_at(stdin_text, 1))
    products: list[int] = []
    for skipped_index in range(len(values)):
        product = 1
        for index, value in enumerate(values):
            if index != skipped_index:
                product *= value
        products.append(product)
    return format_integers(products)


# ---------------------------------------------------------------------------
# Gas Station
# ---------------------------------------------------------------------------


def solve_gas_station(stdin_text: str) -> str:
    """Find the starting station with a single greedy sweep over the deficits.

    Parameters
    ----------
    stdin_text : str
        Station count line, then the gas line, then the cost line.

    Returns
    -------
    str
        The smallest workable starting index, or -1 when the loop is impossible.
    """
    gas_amounts = parse_integer_line(line_at(stdin_text, 1))
    travel_costs = parse_integer_line(line_at(stdin_text, 2))
    total_balance = 0
    tank = 0
    start_station = 0
    for station, gas_amount in enumerate(gas_amounts):
        gain = gas_amount - travel_costs[station]
        total_balance += gain
        tank += gain
        if tank < 0:
            start_station = station + 1
            tank = 0
    return str(start_station) if total_balance >= 0 else "-1"


def brute_gas_station(stdin_text: str) -> str:
    """Find the starting station by simulating the full loop from every station.

    Parameters
    ----------
    stdin_text : str
        Station count line, then the gas line, then the cost line.

    Returns
    -------
    str
        The smallest workable starting index, or -1 when the loop is impossible.
    """
    station_count = int(line_at(stdin_text, 0))
    gas_amounts = parse_integer_line(line_at(stdin_text, 1))
    travel_costs = parse_integer_line(line_at(stdin_text, 2))
    for start_station in range(station_count):
        tank = 0
        is_complete_loop = True
        for offset in range(station_count):
            station = (start_station + offset) % station_count
            tank += gas_amounts[station] - travel_costs[station]
            if tank < 0:
                is_complete_loop = False
                break
        if is_complete_loop:
            return str(start_station)
    return "-1"


# ---------------------------------------------------------------------------
# Candy
# ---------------------------------------------------------------------------


def solve_candy(stdin_text: str) -> str:
    """Total the minimum candies with a left-to-right then right-to-left pass.

    Parameters
    ----------
    stdin_text : str
        Length line, then the ratings.

    Returns
    -------
    str
        The minimum total number of candies.
    """
    ratings = parse_integer_line(line_at(stdin_text, 1))
    candies = [1] * len(ratings)
    for child in range(1, len(ratings)):
        if ratings[child] > ratings[child - 1]:
            candies[child] = candies[child - 1] + 1
    for child in range(len(ratings) - 2, -1, -1):
        if ratings[child] > ratings[child + 1]:
            candies[child] = max(candies[child], candies[child + 1] + 1)
    return str(sum(candies))


def brute_candy(stdin_text: str) -> str:
    """Total the minimum candies by relaxing neighbour constraints until stable.

    Parameters
    ----------
    stdin_text : str
        Length line, then the ratings.

    Returns
    -------
    str
        The minimum total number of candies.
    """
    ratings = parse_integer_line(line_at(stdin_text, 1))
    candies = [1] * len(ratings)
    has_changed = True
    while has_changed:
        has_changed = False
        for child in range(len(ratings)):
            if child > 0 and ratings[child] > ratings[child - 1] and candies[child] <= candies[child - 1]:
                candies[child] = candies[child - 1] + 1
                has_changed = True
            if (
                child + 1 < len(ratings)
                and ratings[child] > ratings[child + 1]
                and candies[child] <= candies[child + 1]
            ):
                candies[child] = candies[child + 1] + 1
                has_changed = True
    return str(sum(candies))


# ---------------------------------------------------------------------------
# Trapping Rain Water
# ---------------------------------------------------------------------------


def solve_trapping_rain_water(stdin_text: str) -> str:
    """Total the trapped water with two pointers closing on the tallest side.

    Parameters
    ----------
    stdin_text : str
        Length line, then the bar heights.

    Returns
    -------
    str
        Units of trapped water.
    """
    heights = parse_integer_line(line_at(stdin_text, 1))
    left_index = 0
    right_index = len(heights) - 1
    tallest_left = 0
    tallest_right = 0
    trapped_water = 0
    while left_index < right_index:
        if heights[left_index] <= heights[right_index]:
            tallest_left = max(tallest_left, heights[left_index])
            trapped_water += tallest_left - heights[left_index]
            left_index += 1
        else:
            tallest_right = max(tallest_right, heights[right_index])
            trapped_water += tallest_right - heights[right_index]
            right_index -= 1
    return str(trapped_water)


def brute_trapping_rain_water(stdin_text: str) -> str:
    """Total the trapped water by scanning both sides of every bar.

    Parameters
    ----------
    stdin_text : str
        Length line, then the bar heights.

    Returns
    -------
    str
        Units of trapped water.
    """
    heights = parse_integer_line(line_at(stdin_text, 1))
    trapped_water = 0
    for index, height in enumerate(heights):
        tallest_left = max(heights[: index + 1])
        tallest_right = max(heights[index:])
        trapped_water += min(tallest_left, tallest_right) - height
    return str(trapped_water)


# ---------------------------------------------------------------------------
# Roman to Integer
# ---------------------------------------------------------------------------

ROMAN_SYMBOL_VALUES: dict[str, int] = {
    "I": 1,
    "V": 5,
    "X": 10,
    "L": 50,
    "C": 100,
    "D": 500,
    "M": 1000,
}


def solve_roman_to_integer(stdin_text: str) -> str:
    """Convert a roman numeral by subtracting any symbol smaller than its successor.

    Parameters
    ----------
    stdin_text : str
        One line holding the roman numeral.

    Returns
    -------
    str
        The decimal value.
    """
    numeral = line_at(stdin_text, 0).strip()
    total = 0
    for position, symbol in enumerate(numeral):
        value = ROMAN_SYMBOL_VALUES[symbol]
        is_subtractive = (
            position + 1 < len(numeral) and value < ROMAN_SYMBOL_VALUES[numeral[position + 1]]
        )
        total += -value if is_subtractive else value
    return str(total)


def brute_roman_to_integer(stdin_text: str) -> str:
    """Convert a roman numeral by expanding subtractive pairs, then summing symbols.

    Parameters
    ----------
    stdin_text : str
        One line holding the roman numeral.

    Returns
    -------
    str
        The decimal value.
    """
    numeral = line_at(stdin_text, 0).strip()
    expansions = (
        ("IV", "IIII"),
        ("IX", "VIIII"),
        ("XL", "XXXX"),
        ("XC", "LXXXX"),
        ("CD", "CCCC"),
        ("CM", "DCCCC"),
    )
    for pair, expansion in expansions:
        numeral = numeral.replace(pair, expansion)
    return str(sum(ROMAN_SYMBOL_VALUES[symbol] for symbol in numeral))


# ---------------------------------------------------------------------------
# Integer to Roman
# ---------------------------------------------------------------------------


def solve_integer_to_roman(stdin_text: str) -> str:
    """Build a roman numeral greedily from largest to smallest symbol value.

    Parameters
    ----------
    stdin_text : str
        One line holding the decimal number.

    Returns
    -------
    str
        The roman numeral.
    """
    number = int(line_at(stdin_text, 0))
    symbol_table = (
        (1000, "M"),
        (900, "CM"),
        (500, "D"),
        (400, "CD"),
        (100, "C"),
        (90, "XC"),
        (50, "L"),
        (40, "XL"),
        (10, "X"),
        (9, "IX"),
        (5, "V"),
        (4, "IV"),
        (1, "I"),
    )
    pieces: list[str] = []
    for value, symbol in symbol_table:
        repeats, number = divmod(number, value)
        pieces.append(symbol * repeats)
    return "".join(pieces)


def brute_integer_to_roman(stdin_text: str) -> str:
    """Build a roman numeral from per-digit lookup tables.

    Parameters
    ----------
    stdin_text : str
        One line holding the decimal number.

    Returns
    -------
    str
        The roman numeral.
    """
    number = int(line_at(stdin_text, 0))
    thousands = ("", "M", "MM", "MMM")
    hundreds = ("", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM")
    tens = ("", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC")
    ones = ("", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX")
    return (
        thousands[number // 1000]
        + hundreds[number // 100 % 10]
        + tens[number // 10 % 10]
        + ones[number % 10]
    )


# ---------------------------------------------------------------------------
# Length of Last Word
# ---------------------------------------------------------------------------


def solve_length_of_last_word(stdin_text: str) -> str:
    """Report the length of the final word of a line.

    Parameters
    ----------
    stdin_text : str
        One line of words separated by spaces.

    Returns
    -------
    str
        Length of the last word.
    """
    words = line_at(stdin_text, 0).split()
    return str(len(words[-1]))


def brute_length_of_last_word(stdin_text: str) -> str:
    """Report the length of the final word by scanning backwards character by character.

    Parameters
    ----------
    stdin_text : str
        One line of words separated by spaces.

    Returns
    -------
    str
        Length of the last word.
    """
    sentence = line_at(stdin_text, 0)
    cursor = len(sentence) - 1
    while cursor >= 0 and sentence[cursor] == " ":
        cursor -= 1
    word_length = 0
    while cursor >= 0 and sentence[cursor] != " ":
        word_length += 1
        cursor -= 1
    return str(word_length)


# ---------------------------------------------------------------------------
# Longest Common Prefix
# ---------------------------------------------------------------------------


def solve_longest_common_prefix(stdin_text: str) -> str:
    """Find the longest shared prefix by trimming it against each word.

    Parameters
    ----------
    stdin_text : str
        Count line, then one word per line.

    Returns
    -------
    str
        The shared prefix, or "none" when there is none.
    """
    word_count = int(line_at(stdin_text, 0))
    words = [line_at(stdin_text, index) for index in range(1, word_count + 1)]
    prefix = words[0]
    for word in words[1:]:
        while not word.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                return "none"
    return prefix if prefix else "none"


def brute_longest_common_prefix(stdin_text: str) -> str:
    """Find the longest shared prefix by comparing one column of characters at a time.

    Parameters
    ----------
    stdin_text : str
        Count line, then one word per line.

    Returns
    -------
    str
        The shared prefix, or "none" when there is none.
    """
    word_count = int(line_at(stdin_text, 0))
    words = [line_at(stdin_text, index) for index in range(1, word_count + 1)]
    shortest_length = min(len(word) for word in words)
    shared: list[str] = []
    for column in range(shortest_length):
        column_character = words[0][column]
        if any(word[column] != column_character for word in words):
            break
        shared.append(column_character)
    return "".join(shared) if shared else "none"


# ---------------------------------------------------------------------------
# Reverse Words in a String
# ---------------------------------------------------------------------------


def solve_reverse_words_in_a_string(stdin_text: str) -> str:
    """Reverse the word order of a line, collapsing runs of spaces.

    Parameters
    ----------
    stdin_text : str
        One line of words separated by spaces.

    Returns
    -------
    str
        The words in reverse order, single spaced.
    """
    words = line_at(stdin_text, 0).split()
    return " ".join(reversed(words))


def brute_reverse_words_in_a_string(stdin_text: str) -> str:
    """Reverse the word order of a line by collecting words with a manual scan.

    Parameters
    ----------
    stdin_text : str
        One line of words separated by spaces.

    Returns
    -------
    str
        The words in reverse order, single spaced.
    """
    sentence = line_at(stdin_text, 0)
    words: list[str] = []
    current_word: list[str] = []
    for character in sentence:
        if character == " ":
            if current_word:
                words.append("".join(current_word))
                current_word = []
        else:
            current_word.append(character)
    if current_word:
        words.append("".join(current_word))
    return " ".join(words[::-1])


# ---------------------------------------------------------------------------
# Zigzag Conversion
# ---------------------------------------------------------------------------


def solve_zigzag_conversion(stdin_text: str) -> str:
    """Read a zigzag layout row by row by bouncing a row cursor over the text.

    Parameters
    ----------
    stdin_text : str
        Text line, then the row count line.

    Returns
    -------
    str
        The row-wise reading of the zigzag layout.
    """
    text = line_at(stdin_text, 0)
    row_count = int(line_at(stdin_text, 1))
    rows: list[list[str]] = [[] for _ in range(row_count)]
    row_cursor = 0
    direction = 1
    for character in text:
        rows[row_cursor].append(character)
        if row_count == 1:
            continue
        if row_cursor == 0:
            direction = 1
        elif row_cursor == row_count - 1:
            direction = -1
        row_cursor += direction
    return "".join("".join(row) for row in rows)


def brute_zigzag_conversion(stdin_text: str) -> str:
    """Read a zigzag layout row by row after placing characters on an explicit grid.

    Parameters
    ----------
    stdin_text : str
        Text line, then the row count line.

    Returns
    -------
    str
        The row-wise reading of the zigzag layout.
    """
    text = line_at(stdin_text, 0)
    row_count = int(line_at(stdin_text, 1))
    if row_count == 1:
        return text

    cycle_length = 2 * row_count - 2
    column_count = ((len(text) + cycle_length - 1) // cycle_length) * (row_count - 1) + 1
    grid = [[""] * column_count for _ in range(row_count)]
    for index, character in enumerate(text):
        cycle_index, offset = divmod(index, cycle_length)
        if offset < row_count:
            row = offset
            column = cycle_index * (row_count - 1)
        else:
            row = cycle_length - offset
            column = cycle_index * (row_count - 1) + (offset - row_count + 1)
        grid[row][column] = character
    return "".join(cell for row in grid for cell in row if cell)


# ---------------------------------------------------------------------------
# Find the Index of the First Occurrence in a String
# ---------------------------------------------------------------------------


def solve_find_the_index_of_the_first_occurrence_in_a_string(stdin_text: str) -> str:
    """Locate the first occurrence of a pattern by comparing every alignment.

    Parameters
    ----------
    stdin_text : str
        Haystack line, then the needle line.

    Returns
    -------
    str
        The first matching index, or -1 when the pattern is absent.
    """
    haystack = line_at(stdin_text, 0)
    needle = line_at(stdin_text, 1)
    for start in range(len(haystack) - len(needle) + 1):
        is_match = True
        for offset, character in enumerate(needle):
            if haystack[start + offset] != character:
                is_match = False
                break
        if is_match:
            return str(start)
    return "-1"


def brute_find_the_index_of_the_first_occurrence_in_a_string(stdin_text: str) -> str:
    """Locate the first occurrence of a pattern with the built-in substring search.

    Parameters
    ----------
    stdin_text : str
        Haystack line, then the needle line.

    Returns
    -------
    str
        The first matching index, or -1 when the pattern is absent.
    """
    haystack = line_at(stdin_text, 0)
    needle = line_at(stdin_text, 1)
    return str(haystack.find(needle))


# ---------------------------------------------------------------------------
# Text Justification
# ---------------------------------------------------------------------------


def justify_packed_line(words: list[str], letter_count: int, max_width: int) -> str:
    """Pad one full line of words to the target width, widening the leftmost gaps first.

    Parameters
    ----------
    words : list[str]
        Words placed on this line.
    letter_count : int
        Sum of the word lengths.
    max_width : int
        Target line width.

    Returns
    -------
    str
        The padded line, exactly max_width characters long.
    """
    if len(words) == 1:
        return words[0].ljust(max_width)
    gap_count = len(words) - 1
    base_gap, wider_gaps = divmod(max_width - letter_count, gap_count)
    pieces: list[str] = []
    for position, word in enumerate(words[:-1]):
        pieces.append(word + " " * (base_gap + (1 if position < wider_gaps else 0)))
    pieces.append(words[-1])
    return "".join(pieces)


def solve_text_justification(stdin_text: str) -> str:
    """Pack words greedily into lines and justify every line but the last.

    Parameters
    ----------
    stdin_text : str
        Width line, then the words line.

    Returns
    -------
    str
        One bar-delimited line per justified line.
    """
    max_width = int(line_at(stdin_text, 0))
    words = line_at(stdin_text, 1).split()
    justified_lines: list[str] = []
    packed: list[str] = []
    letter_count = 0
    for word in words:
        if packed and letter_count + len(packed) + len(word) > max_width:
            justified_lines.append(justify_packed_line(packed, letter_count, max_width))
            packed = []
            letter_count = 0
        packed.append(word)
        letter_count += len(word)
    justified_lines.append(" ".join(packed).ljust(max_width))
    return "\n".join(f"|{line}|" for line in justified_lines)


def brute_text_justification(stdin_text: str) -> str:
    """Group words by measuring joined candidates, then spread spaces round-robin.

    Parameters
    ----------
    stdin_text : str
        Width line, then the words line.

    Returns
    -------
    str
        One bar-delimited line per justified line.
    """
    max_width = int(line_at(stdin_text, 0))
    words = line_at(stdin_text, 1).split()

    groups: list[list[str]] = []
    cursor = 0
    while cursor < len(words):
        group = [words[cursor]]
        cursor += 1
        while cursor < len(words) and len(" ".join(group + [words[cursor]])) <= max_width:
            group.append(words[cursor])
            cursor += 1
        groups.append(group)

    output_lines: list[str] = []
    for group_index, group in enumerate(groups):
        is_last_group = group_index == len(groups) - 1
        if is_last_group or len(group) == 1:
            padded = " ".join(group) + " " * max_width
            output_lines.append(padded[:max_width])
            continue
        gaps = [1] * (len(group) - 1)
        leftover = max_width - sum(len(word) for word in group) - len(gaps)
        gap_cursor = 0
        while leftover > 0:
            gaps[gap_cursor] += 1
            leftover -= 1
            gap_cursor = (gap_cursor + 1) % len(gaps)
        rendered = "".join(word + " " * gap for word, gap in zip(group, gaps))
        output_lines.append(rendered + group[-1])
    return "\n".join(f"|{line}|" for line in output_lines)


# ---------------------------------------------------------------------------
# Problem specs
# ---------------------------------------------------------------------------

PROBLEMS: list[dict[str, object]] = [
    {
        "title": "Merge Sorted Array",
        "level": "Easy",
        "topics": "Array, Two Pointers, Sorting",
        "companies": "Microsoft, Amazon, Facebook, Bloomberg",
        "description": (
            "You are given two arrays that are already sorted in non-decreasing order. "
            "Combine them into one array that is also sorted in non-decreasing order.\n"
            "\n"
            "Input (stdin):\n"
            "\n"
            "- Line 1: two integers `m` and `n`, the length of the first array and the "
            "length of the second array.\n"
            "- Line 2: the `m` integers of the first array (an empty line when `m` is 0).\n"
            "- Line 3: the `n` integers of the second array (an empty line when `n` is 0).\n"
            "\n"
            "Output (stdout):\n"
            "\n"
            "- One line with all `m + n` integers in sorted order, separated by single spaces.\n"
        ),
        "examples": (
            "**Example 1**\n"
            "\n"
            "```\n"
            "Input:\n"
            "3 3\n"
            "1 2 3\n"
            "2 5 6\n"
            "Output:\n"
            "1 2 2 3 5 6\n"
            "```\n"
            "\n"
            "**Example 2**\n"
            "\n"
            "```\n"
            "Input:\n"
            "4 4\n"
            "-5 -5 0 2\n"
            "-5 1 1 3\n"
            "Output:\n"
            "-5 -5 -5 0 1 1 2 3\n"
            "```\n"
        ),
        "constraints": (
            "- `0 <= m, n <= 200`\n"
            "- `1 <= m + n <= 400`\n"
            "- `-1000 <= each value <= 1000`\n"
            "- Both input arrays are already sorted in non-decreasing order.\n"
        ),
        "inputs": [
            "3 3\n1 2 3\n2 5 6",
            "1 0\n1",
            "0 1\n\n7",
            "4 4\n-5 -5 0 2\n-5 1 1 3",
            "3 2\n2 2 2\n2 2",
            "2 3\n8 9\n1 2 3",
        ],
        "solve": solve_merge_sorted_array,
        "brute": brute_merge_sorted_array,
    },
    {
        "title": "Remove Element",
        "level": "Easy",
        "topics": "Array, Two Pointers",
        "companies": "Amazon, Adobe, Apple",
        "description": (
            "Remove every copy of a given value from an array, keeping the surviving "
            "elements in their original relative order.\n"
            "\n"
            "Input (stdin):\n"
            "\n"
            "- Line 1: the integer `n`, the length of the array.\n"
            "- Line 2: the `n` integers of the array.\n"
            "- Line 3: the integer `val` to remove.\n"
            "\n"
            "Output (stdout):\n"
            "\n"
            "- Line 1: `k`, the number of elements that are not equal to `val`.\n"
            "- Line 2: the `k` surviving elements in their original order, separated by "
            "single spaces. Print this line only when `k` is greater than 0.\n"
        ),
        "examples": (
            "**Example 1**\n"
            "\n"
            "```\n"
            "Input:\n"
            "4\n"
            "3 2 2 3\n"
            "3\n"
            "Output:\n"
            "2\n"
            "2 2\n"
            "```\n"
            "\n"
            "**Example 2**\n"
            "\n"
            "```\n"
            "Input:\n"
            "5\n"
            "4 4 4 4 4\n"
            "4\n"
            "Output:\n"
            "0\n"
            "```\n"
        ),
        "constraints": (
            "- `1 <= n <= 100`\n"
            "- `-100 <= each value <= 100`\n"
            "- `-100 <= val <= 100`\n"
        ),
        "inputs": [
            "4\n3 2 2 3\n3",
            "8\n0 1 2 2 3 0 4 2\n2",
            "1\n7\n7",
            "1\n7\n3",
            "5\n4 4 4 4 4\n4",
            "6\n-3 1 -3 0 5 -3\n-3",
        ],
        "solve": solve_remove_element,
        "brute": brute_remove_element,
    },
    {
        "title": "Remove Duplicates from Sorted Array",
        "level": "Easy",
        "topics": "Array, Two Pointers",
        "companies": "Microsoft, Amazon, Bloomberg",
        "description": (
            "An array is sorted in non-decreasing order. Keep only one copy of each "
            "distinct value, preserving the sorted order.\n"
            "\n"
            "Input (stdin):\n"
            "\n"
            "- Line 1: the integer `n`, the length of the array.\n"
            "- Line 2: the `n` sorted integers of the array.\n"
            "\n"
            "Output (stdout):\n"
            "\n"
            "- Line 1: `k`, the number of distinct values.\n"
            "- Line 2: those `k` values in sorted order, separated by single spaces.\n"
        ),
        "examples": (
            "**Example 1**\n"
            "\n"
            "```\n"
            "Input:\n"
            "3\n"
            "1 1 2\n"
            "Output:\n"
            "2\n"
            "1 2\n"
            "```\n"
            "\n"
            "**Example 2**\n"
            "\n"
            "```\n"
            "Input:\n"
            "10\n"
            "0 0 1 1 1 2 2 3 3 4\n"
            "Output:\n"
            "5\n"
            "0 1 2 3 4\n"
            "```\n"
        ),
        "constraints": (
            "- `1 <= n <= 300`\n"
            "- `-100 <= each value <= 100`\n"
            "- The array is already sorted in non-decreasing order.\n"
        ),
        "inputs": [
            "3\n1 1 2",
            "10\n0 0 1 1 1 2 2 3 3 4",
            "1\n5",
            "4\n-2 -2 -2 -2",
            "5\n-3 -1 0 0 4",
            "6\n1 2 3 4 5 6",
        ],
        "solve": solve_remove_duplicates_from_sorted_array,
        "brute": brute_remove_duplicates_from_sorted_array,
    },
    {
        "title": "Remove Duplicates from Sorted Array II",
        "level": "Medium",
        "topics": "Array, Two Pointers",
        "companies": "Facebook, Amazon, Google",
        "description": (
            "An array is sorted in non-decreasing order. Keep at most two copies of each "
            "distinct value, preserving the sorted order.\n"
            "\n"
            "Input (stdin):\n"
            "\n"
            "- Line 1: the integer `n`, the length of the array.\n"
            "- Line 2: the `n` sorted integers of the array.\n"
            "\n"
            "Output (stdout):\n"
            "\n"
            "- Line 1: `k`, the number of elements that remain.\n"
            "- Line 2: those `k` elements in sorted order, separated by single spaces.\n"
        ),
        "examples": (
            "**Example 1**\n"
            "\n"
            "```\n"
            "Input:\n"
            "5\n"
            "1 1 1 2 2\n"
            "Output:\n"
            "4\n"
            "1 1 2 2\n"
            "```\n"
            "\n"
            "**Example 2**\n"
            "\n"
            "```\n"
            "Input:\n"
            "9\n"
            "0 0 1 1 1 1 2 3 3\n"
            "Output:\n"
            "7\n"
            "0 0 1 1 2 3 3\n"
            "```\n"
        ),
        "constraints": (
            "- `1 <= n <= 300`\n"
            "- `-10000 <= each value <= 10000`\n"
            "- The array is already sorted in non-decreasing order.\n"
        ),
        "inputs": [
            "5\n1 1 1 2 2",
            "9\n0 0 1 1 1 1 2 3 3",
            "1\n9",
            "5\n-1 -1 -1 -1 -1",
            "6\n-5 -5 -5 0 0 2",
            "4\n1 2 3 4",
        ],
        "solve": solve_remove_duplicates_from_sorted_array_ii,
        "brute": brute_remove_duplicates_from_sorted_array_ii,
    },
    {
        "title": "Majority Element",
        "level": "Easy",
        "topics": "Array, Hash Table, Divide and Conquer, Counting",
        "companies": "Amazon, Adobe, Google, Zenefits",
        "description": (
            "One value in the array occurs more than `n / 2` times. Report that value.\n"
            "\n"
            "Input (stdin):\n"
            "\n"
            "- Line 1: the integer `n`, the length of the array.\n"
            "- Line 2: the `n` integers of the array.\n"
            "\n"
            "Output (stdout):\n"
            "\n"
            "- One line with the majority value.\n"
        ),
        "examples": (
            "**Example 1**\n"
            "\n"
            "```\n"
            "Input:\n"
            "3\n"
            "3 2 3\n"
            "Output:\n"
            "3\n"
            "```\n"
            "\n"
            "**Example 2**\n"
            "\n"
            "```\n"
            "Input:\n"
            "7\n"
            "2 2 1 1 1 2 2\n"
            "Output:\n"
            "2\n"
            "```\n"
        ),
        "constraints": (
            "- `1 <= n <= 500`\n"
            "- `-1000 <= each value <= 1000`\n"
            "- A majority value always exists, so it occurs more than `n / 2` times.\n"
        ),
        "inputs": [
            "3\n3 2 3",
            "7\n2 2 1 1 1 2 2",
            "1\n-4",
            "5\n7 7 7 7 7",
            "5\n-1 -1 -1 2 3",
            "9\n5 1 5 2 5 3 5 4 5",
        ],
        "solve": solve_majority_element,
        "brute": brute_majority_element,
    },
    {
        "title": "Rotate Array",
        "level": "Medium",
        "topics": "Array, Math, Two Pointers",
        "companies": "Microsoft, Amazon, Bloomberg",
        "description": (
            "Shift every element of an array `k` positions to the right. Elements pushed "
            "past the end wrap around to the front.\n"
            "\n"
            "Input (stdin):\n"
            "\n"
            "- Line 1: two integers `n` and `k`, the length of the array and the number of "
            "right shifts. `k` can be larger than `n`.\n"
            "- Line 2: the `n` integers of the array.\n"
            "\n"
            "Output (stdout):\n"
            "\n"
            "- One line with the rotated array, separated by single spaces.\n"
        ),
        "examples": (
            "**Example 1**\n"
            "\n"
            "```\n"
            "Input:\n"
            "7 3\n"
            "1 2 3 4 5 6 7\n"
            "Output:\n"
            "5 6 7 1 2 3 4\n"
            "```\n"
            "\n"
            "**Example 2**\n"
            "\n"
            "```\n"
            "Input:\n"
            "4 2\n"
            "-1 -100 3 99\n"
            "Output:\n"
            "3 99 -1 -100\n"
            "```\n"
        ),
        "constraints": (
            "- `1 <= n <= 300`\n"
            "- `0 <= k <= 1000`\n"
            "- `-1000 <= each value <= 1000`\n"
        ),
        "inputs": [
            "7 3\n1 2 3 4 5 6 7",
            "4 2\n-1 -100 3 99",
            "1 0\n5",
            "1 7\n5",
            "4 4\n2 2 2 2",
            "3 5\n1 2 3",
        ],
        "solve": solve_rotate_array,
        "brute": brute_rotate_array,
    },
    {
        "title": "Best Time to Buy and Sell Stock",
        "level": "Easy",
        "topics": "Array, Dynamic Programming",
        "companies": "Amazon, Facebook, Microsoft, Bloomberg",
        "description": (
            "You are given the price of one share on each of `n` consecutive days. Buy on "
            "one day and sell on a later day, at most once, and report the largest profit "
            "you can make. If no trade makes money, the profit is 0.\n"
            "\n"
            "Input (stdin):\n"
            "\n"
            "- Line 1: the integer `n`, the number of days.\n"
            "- Line 2: the `n` prices, one per day, in day order.\n"
            "\n"
            "Output (stdout):\n"
            "\n"
            "- One line with the largest profit.\n"
        ),
        "examples": (
            "**Example 1**\n"
            "\n"
            "```\n"
            "Input:\n"
            "6\n"
            "7 1 5 3 6 4\n"
            "Output:\n"
            "5\n"
            "```\n"
            "\n"
            "**Example 2**\n"
            "\n"
            "```\n"
            "Input:\n"
            "5\n"
            "7 6 4 3 1\n"
            "Output:\n"
            "0\n"
            "```\n"
        ),
        "constraints": (
            "- `1 <= n <= 1000`\n"
            "- `0 <= each price <= 10000`\n"
        ),
        "inputs": [
            "6\n7 1 5 3 6 4",
            "5\n7 6 4 3 1",
            "1\n3",
            "4\n2 2 2 2",
            "6\n3 2 6 5 0 3",
            "5\n1 2 90 10 100",
        ],
        "solve": solve_best_time_to_buy_and_sell_stock,
        "brute": brute_best_time_to_buy_and_sell_stock,
    },
    {
        "title": "Best Time to Buy and Sell Stock II",
        "level": "Medium",
        "topics": "Array, Dynamic Programming, Greedy",
        "companies": "Amazon, Microsoft, Bloomberg, Uber",
        "description": (
            "You are given the price of one share on each of `n` consecutive days. You may "
            "buy and sell as often as you like, but you can hold at most one share at a "
            "time, and you must sell before buying again. Report the largest total profit.\n"
            "\n"
            "Input (stdin):\n"
            "\n"
            "- Line 1: the integer `n`, the number of days.\n"
            "- Line 2: the `n` prices, one per day, in day order.\n"
            "\n"
            "Output (stdout):\n"
            "\n"
            "- One line with the largest total profit.\n"
        ),
        "examples": (
            "**Example 1**\n"
            "\n"
            "```\n"
            "Input:\n"
            "6\n"
            "7 1 5 3 6 4\n"
            "Output:\n"
            "7\n"
            "```\n"
            "\n"
            "**Example 2**\n"
            "\n"
            "```\n"
            "Input:\n"
            "5\n"
            "1 2 3 4 5\n"
            "Output:\n"
            "4\n"
            "```\n"
        ),
        "constraints": (
            "- `1 <= n <= 1000`\n"
            "- `0 <= each price <= 10000`\n"
        ),
        "inputs": [
            "6\n7 1 5 3 6 4",
            "5\n1 2 3 4 5",
            "5\n7 6 4 3 1",
            "1\n4",
            "4\n3 3 3 3",
            "7\n2 9 1 8 3 7 4",
        ],
        "solve": solve_best_time_to_buy_and_sell_stock_ii,
        "brute": brute_best_time_to_buy_and_sell_stock_ii,
    },
    {
        "title": "Jump Game",
        "level": "Medium",
        "topics": "Array, Dynamic Programming, Greedy",
        "companies": "Amazon, Microsoft, Google",
        "description": (
            "You start on the first cell of an array. The value in a cell is the largest "
            "number of cells you may move forward from there. Decide whether the last cell "
            "can be reached.\n"
            "\n"
            "Input (stdin):\n"
            "\n"
            "- Line 1: the integer `n`, the length of the array.\n"
            "- Line 2: the `n` jump lengths.\n"
            "\n"
            "Output (stdout):\n"
            "\n"
            "- One line holding `true` when the last cell is reachable, otherwise `false`, "
            "in lowercase.\n"
        ),
        "examples": (
            "**Example 1**\n"
            "\n"
            "```\n"
            "Input:\n"
            "5\n"
            "2 3 1 1 4\n"
            "Output:\n"
            "true\n"
            "```\n"
            "\n"
            "**Example 2**\n"
            "\n"
            "```\n"
            "Input:\n"
            "5\n"
            "3 2 1 0 4\n"
            "Output:\n"
            "false\n"
            "```\n"
        ),
        "constraints": (
            "- `1 <= n <= 300`\n"
            "- `0 <= each jump length <= 300`\n"
        ),
        "inputs": [
            "5\n2 3 1 1 4",
            "5\n3 2 1 0 4",
            "1\n0",
            "4\n1 1 1 0",
            "5\n2 0 0 0 1",
            "6\n1 1 1 1 1 1",
            "2\n0 1",
        ],
        "solve": solve_jump_game,
        "brute": brute_jump_game,
    },
    {
        "title": "Jump Game II",
        "level": "Medium",
        "topics": "Array, Dynamic Programming, Greedy",
        "companies": "Amazon, Google, Facebook",
        "description": (
            "You start on the first cell of an array. The value in a cell is the largest "
            "number of cells you may move forward from there, and the last cell is always "
            "reachable. Report the fewest jumps needed to land on the last cell.\n"
            "\n"
            "Input (stdin):\n"
            "\n"
            "- Line 1: the integer `n`, the length of the array.\n"
            "- Line 2: the `n` jump lengths.\n"
            "\n"
            "Output (stdout):\n"
            "\n"
            "- One line with the fewest number of jumps. It is 0 when `n` is 1.\n"
        ),
        "examples": (
            "**Example 1**\n"
            "\n"
            "```\n"
            "Input:\n"
            "5\n"
            "2 3 1 1 4\n"
            "Output:\n"
            "2\n"
            "```\n"
            "\n"
            "**Example 2**\n"
            "\n"
            "```\n"
            "Input:\n"
            "6\n"
            "1 1 1 1 1 1\n"
            "Output:\n"
            "5\n"
            "```\n"
        ),
        "constraints": (
            "- `1 <= n <= 300`\n"
            "- `0 <= each jump length <= 300`\n"
            "- The last cell is always reachable from the first cell.\n"
        ),
        "inputs": [
            "5\n2 3 1 1 4",
            "5\n2 3 0 1 4",
            "1\n0",
            "6\n1 1 1 1 1 1",
            "4\n3 1 1 1",
            "7\n7 1 1 1 1 1 1",
            "5\n1 2 1 1 1",
        ],
        "solve": solve_jump_game_ii,
        "brute": brute_jump_game_ii,
    },
    {
        "title": "H-Index",
        "level": "Medium",
        "topics": "Array, Sorting, Counting",
        "companies": "Google, Facebook, Bloomberg",
        "description": (
            "A researcher has `n` papers, and you are given how many times each paper was "
            "cited. The h-index is the largest value `h` such that at least `h` of the "
            "papers have `h` or more citations each. Report the h-index.\n"
            "\n"
            "Input (stdin):\n"
            "\n"
            "- Line 1: the integer `n`, the number of papers.\n"
            "- Line 2: the `n` citation counts, in any order.\n"
            "\n"
            "Output (stdout):\n"
            "\n"
            "- One line with the h-index.\n"
        ),
        "examples": (
            "**Example 1**\n"
            "\n"
            "```\n"
            "Input:\n"
            "5\n"
            "3 0 6 1 5\n"
            "Output:\n"
            "3\n"
            "```\n"
            "\n"
            "**Example 2**\n"
            "\n"
            "```\n"
            "Input:\n"
            "3\n"
            "1 3 1\n"
            "Output:\n"
            "1\n"
            "```\n"
        ),
        "constraints": (
            "- `1 <= n <= 500`\n"
            "- `0 <= each citation count <= 1000`\n"
        ),
        "inputs": [
            "5\n3 0 6 1 5",
            "3\n1 3 1",
            "1\n0",
            "1\n100",
            "4\n4 4 4 4",
            "6\n0 0 0 0 0 0",
            "5\n10 8 5 4 3",
        ],
        "solve": solve_h_index,
        "brute": brute_h_index,
    },
    {
        "title": "Insert Delete GetRandom O(1)",
        "level": "Medium",
        "topics": "Array, Hash Table, Math, Design, Randomized",
        "companies": "Facebook, Amazon, Google, LinkedIn",
        "description": (
            "Build a collection of distinct integers that supports inserting a value, "
            "removing a value, and returning a uniformly random member, each in average "
            "constant time. Replay a list of operations on an initially empty collection.\n"
            "\n"
            "Input (stdin):\n"
            "\n"
            "- Line 1: the integer `q`, the number of operations.\n"
            "- Next `q` lines: one operation each, in one of these forms:\n"
            "  - `insert x` - add `x` to the collection.\n"
            "  - `remove x` - delete `x` from the collection.\n"
            "  - `getRandom` - pick a uniformly random member.\n"
            "\n"
            "Output (stdout):\n"
            "\n"
            "- One line per operation:\n"
            "  - `insert x` prints `true` when `x` was not present and was added, otherwise "
            "`false`.\n"
            "  - `remove x` prints `true` when `x` was present and was deleted, otherwise "
            "`false`.\n"
            "  - `getRandom` prints `true` when the picked value is a current member, and "
            "`none` when the collection is empty.\n"
        ),
        "examples": (
            "**Example 1**\n"
            "\n"
            "```\n"
            "Input:\n"
            "5\n"
            "insert 1\n"
            "remove 2\n"
            "insert 2\n"
            "getRandom\n"
            "remove 1\n"
            "Output:\n"
            "true\n"
            "false\n"
            "true\n"
            "true\n"
            "true\n"
            "```\n"
            "\n"
            "**Example 2**\n"
            "\n"
            "```\n"
            "Input:\n"
            "4\n"
            "getRandom\n"
            "insert 3\n"
            "insert 3\n"
            "getRandom\n"
            "Output:\n"
            "none\n"
            "true\n"
            "false\n"
            "true\n"
            "```\n"
        ),
        "constraints": (
            "- `1 <= q <= 200`\n"
            "- `-1000 <= x <= 1000`\n"
            "- Every operation name is exactly `insert`, `remove`, or `getRandom`.\n"
        ),
        "inputs": [
            "5\ninsert 1\nremove 2\ninsert 2\ngetRandom\nremove 1",
            "4\ngetRandom\ninsert 3\ninsert 3\ngetRandom",
            "1\ngetRandom",
            "6\ninsert -5\ninsert -5\nremove -5\nremove -5\ngetRandom\ninsert 0",
            "7\ninsert 10\ninsert 20\ninsert 30\nremove 20\ngetRandom\nremove 30\nremove 10",
            "3\ninsert 4\ninsert 4\ninsert 4",
        ],
        "solve": solve_insert_delete_getrandom_o1,
        "brute": brute_insert_delete_getrandom_o1,
    },
    {
        "title": "Product of Array Except Self",
        "level": "Medium",
        "topics": "Array, Prefix Sum",
        "companies": "Facebook, Amazon, Microsoft, Apple",
        "description": (
            "For each position of an array, compute the product of all the other elements.\n"
            "\n"
            "Input (stdin):\n"
            "\n"
            "- Line 1: the integer `n`, the length of the array.\n"
            "- Line 2: the `n` integers of the array.\n"
            "\n"
            "Output (stdout):\n"
            "\n"
            "- One line with the `n` products, in the same order as the input, separated by "
            "single spaces.\n"
        ),
        "examples": (
            "**Example 1**\n"
            "\n"
            "```\n"
            "Input:\n"
            "4\n"
            "1 2 3 4\n"
            "Output:\n"
            "24 12 8 6\n"
            "```\n"
            "\n"
            "**Example 2**\n"
            "\n"
            "```\n"
            "Input:\n"
            "5\n"
            "-1 1 0 -3 3\n"
            "Output:\n"
            "0 0 9 0 0\n"
            "```\n"
        ),
        "constraints": (
            "- `2 <= n <= 300`\n"
            "- `-30 <= each value <= 30`\n"
            "- Every product fits in a 32-bit signed integer.\n"
        ),
        "inputs": [
            "4\n1 2 3 4",
            "5\n-1 1 0 -3 3",
            "2\n3 7",
            "4\n2 2 2 2",
            "3\n-2 -3 -4",
            "4\n0 0 2 3",
        ],
        "solve": solve_product_of_array_except_self,
        "brute": brute_product_of_array_except_self,
    },
    {
        "title": "Gas Station",
        "level": "Medium",
        "topics": "Array, Greedy",
        "companies": "Amazon, Bloomberg, Microsoft",
        "description": (
            "There are `n` gas stations arranged in a circle. Station `i` gives you "
            "`gas[i]` units of fuel, and driving from station `i` to the next station burns "
            "`cost[i]` units. You start with an empty tank and must finish the whole loop "
            "without the tank ever going negative. Report a station you can start from.\n"
            "\n"
            "Input (stdin):\n"
            "\n"
            "- Line 1: the integer `n`, the number of stations.\n"
            "- Line 2: the `n` values of `gas`.\n"
            "- Line 3: the `n` values of `cost`.\n"
            "\n"
            "Output (stdout):\n"
            "\n"
            "- One line with the index of a workable starting station, counting from 0. If "
            "several stations work, print the smallest such index. Print `-1` when no "
            "station works.\n"
        ),
        "examples": (
            "**Example 1**\n"
            "\n"
            "```\n"
            "Input:\n"
            "5\n"
            "1 2 3 4 5\n"
            "3 4 5 1 2\n"
            "Output:\n"
            "3\n"
            "```\n"
            "\n"
            "**Example 2**\n"
            "\n"
            "```\n"
            "Input:\n"
            "3\n"
            "2 3 4\n"
            "3 4 3\n"
            "Output:\n"
            "-1\n"
            "```\n"
        ),
        "constraints": (
            "- `1 <= n <= 300`\n"
            "- `0 <= each gas value <= 1000`\n"
            "- `0 <= each cost value <= 1000`\n"
        ),
        "inputs": [
            "5\n1 2 3 4 5\n3 4 5 1 2",
            "3\n2 3 4\n3 4 3",
            "1\n5\n4",
            "1\n3\n9",
            "4\n2 2 2 2\n2 2 2 2",
            "4\n3 1 1 1\n1 1 1 3",
            "5\n2 0 1 2 3\n1 3 2 1 1",
        ],
        "solve": solve_gas_station,
        "brute": brute_gas_station,
    },
    {
        "title": "Candy",
        "level": "Hard",
        "topics": "Array, Greedy",
        "companies": "Amazon, Google, Microsoft",
        "description": (
            "Children stand in a row and each has a rating. Give every child at least one "
            "candy, and give a child strictly more candies than a neighbour whose rating is "
            "lower. Report the smallest total number of candies that satisfies both rules.\n"
            "\n"
            "Input (stdin):\n"
            "\n"
            "- Line 1: the integer `n`, the number of children.\n"
            "- Line 2: the `n` ratings, in row order.\n"
            "\n"
            "Output (stdout):\n"
            "\n"
            "- One line with the smallest total number of candies.\n"
        ),
        "examples": (
            "**Example 1**\n"
            "\n"
            "```\n"
            "Input:\n"
            "3\n"
            "1 0 2\n"
            "Output:\n"
            "5\n"
            "```\n"
            "\n"
            "**Example 2**\n"
            "\n"
            "```\n"
            "Input:\n"
            "3\n"
            "1 2 2\n"
            "Output:\n"
            "4\n"
            "```\n"
        ),
        "constraints": (
            "- `1 <= n <= 300`\n"
            "- `0 <= each rating <= 10000`\n"
        ),
        "inputs": [
            "3\n1 0 2",
            "3\n1 2 2",
            "1\n5",
            "4\n3 3 3 3",
            "5\n1 2 3 2 1",
            "6\n1 3 2 2 1 1",
            "5\n5 4 3 2 1",
        ],
        "solve": solve_candy,
        "brute": brute_candy,
    },
    {
        "title": "Trapping Rain Water",
        "level": "Hard",
        "topics": "Array, Two Pointers, Dynamic Programming, Stack",
        "companies": "Amazon, Google, Facebook, Bloomberg",
        "description": (
            "Bars of width 1 stand side by side, and the array gives their heights. After "
            "rain, water settles in the dips between taller bars. Report how many units of "
            "water are held.\n"
            "\n"
            "Input (stdin):\n"
            "\n"
            "- Line 1: the integer `n`, the number of bars.\n"
            "- Line 2: the `n` bar heights, left to right.\n"
            "\n"
            "Output (stdout):\n"
            "\n"
            "- One line with the total units of trapped water.\n"
        ),
        "examples": (
            "**Example 1**\n"
            "\n"
            "```\n"
            "Input:\n"
            "12\n"
            "0 1 0 2 1 0 1 3 2 1 2 1\n"
            "Output:\n"
            "6\n"
            "```\n"
            "\n"
            "**Example 2**\n"
            "\n"
            "```\n"
            "Input:\n"
            "6\n"
            "4 2 0 3 2 5\n"
            "Output:\n"
            "9\n"
            "```\n"
        ),
        "constraints": (
            "- `1 <= n <= 500`\n"
            "- `0 <= each height <= 1000`\n"
        ),
        "inputs": [
            "12\n0 1 0 2 1 0 1 3 2 1 2 1",
            "6\n4 2 0 3 2 5",
            "1\n0",
            "4\n3 3 3 3",
            "5\n5 4 3 2 1",
            "7\n3 0 2 0 4 0 1",
        ],
        "solve": solve_trapping_rain_water,
        "brute": brute_trapping_rain_water,
    },
    {
        "title": "Roman to Integer",
        "level": "Easy",
        "topics": "Hash Table, Math, String",
        "companies": "Amazon, Microsoft, Facebook, Yahoo",
        "description": (
            "Roman numerals use the symbols `I`, `V`, `X`, `L`, `C`, `D`, and `M` for 1, 5, "
            "10, 50, 100, 500, and 1000. Symbols are normally written from largest to "
            "smallest and added up, but a smaller symbol placed directly before a larger "
            "one is subtracted instead, as in `IV` for 4 and `CM` for 900. Convert a roman "
            "numeral to its decimal value.\n"
            "\n"
            "Input (stdin):\n"
            "\n"
            "- Line 1: the roman numeral, in uppercase letters with no spaces.\n"
            "\n"
            "Output (stdout):\n"
            "\n"
            "- One line with the decimal value.\n"
        ),
        "examples": (
            "**Example 1**\n"
            "\n"
            "```\n"
            "Input:\n"
            "LVIII\n"
            "Output:\n"
            "58\n"
            "```\n"
            "\n"
            "**Example 2**\n"
            "\n"
            "```\n"
            "Input:\n"
            "MCMXCIV\n"
            "Output:\n"
            "1994\n"
            "```\n"
        ),
        "constraints": (
            "- The numeral is 1 to 15 characters long.\n"
            "- It contains only the characters `I`, `V`, `X`, `L`, `C`, `D`, and `M`.\n"
            "- It is a valid roman numeral for a value between 1 and 3999.\n"
        ),
        "inputs": [
            "III",
            "LVIII",
            "MCMXCIV",
            "I",
            "MMMCMXCIX",
            "XL",
        ],
        "solve": solve_roman_to_integer,
        "brute": brute_roman_to_integer,
    },
    {
        "title": "Integer to Roman",
        "level": "Medium",
        "topics": "Hash Table, Math, String, Greedy",
        "companies": "Amazon, Microsoft, Twitter",
        "description": (
            "Roman numerals use the symbols `I`, `V`, `X`, `L`, `C`, `D`, and `M` for 1, 5, "
            "10, 50, 100, 500, and 1000, plus the subtractive pairs `IV`, `IX`, `XL`, `XC`, "
            "`CD`, and `CM` for 4, 9, 40, 90, 400, and 900. Write a decimal number as the "
            "standard roman numeral, which always takes the largest symbol or pair that "
            "still fits, from left to right.\n"
            "\n"
            "Input (stdin):\n"
            "\n"
            "- Line 1: the decimal number.\n"
            "\n"
            "Output (stdout):\n"
            "\n"
            "- One line with the roman numeral, in uppercase letters with no spaces.\n"
        ),
        "examples": (
            "**Example 1**\n"
            "\n"
            "```\n"
            "Input:\n"
            "3749\n"
            "Output:\n"
            "MMMDCCXLIX\n"
            "```\n"
            "\n"
            "**Example 2**\n"
            "\n"
            "```\n"
            "Input:\n"
            "1994\n"
            "Output:\n"
            "MCMXCIV\n"
            "```\n"
        ),
        "constraints": (
            "- `1 <= number <= 3999`\n"
        ),
        "inputs": [
            "3749",
            "58",
            "1994",
            "1",
            "3999",
            "40",
        ],
        "solve": solve_integer_to_roman,
        "brute": brute_integer_to_roman,
    },
    {
        "title": "Length of Last Word",
        "level": "Easy",
        "topics": "String",
        "companies": "Amazon, Microsoft, Adobe",
        "description": (
            "A line holds words made of letters, separated by one or more spaces. Report "
            "how many letters the last word has.\n"
            "\n"
            "Input (stdin):\n"
            "\n"
            "- Line 1: the sentence. It may begin with spaces and may use runs of several "
            "spaces between words.\n"
            "\n"
            "Output (stdout):\n"
            "\n"
            "- One line with the length of the last word.\n"
        ),
        "examples": (
            "**Example 1**\n"
            "\n"
            "```\n"
            "Input:\n"
            "Hello World\n"
            "Output:\n"
            "5\n"
            "```\n"
            "\n"
            "**Example 2**\n"
            "\n"
            "```\n"
            "Input:\n"
            "   fly me   to   the moon\n"
            "Output:\n"
            "4\n"
            "```\n"
        ),
        "constraints": (
            "- The line is 1 to 200 characters long.\n"
            "- It contains only English letters and spaces.\n"
            "- It holds at least one word.\n"
        ),
        "inputs": [
            "Hello World",
            "   fly me   to   the moon",
            "luffy is still joyboy",
            "a",
            "aaa aaa aaa",
            "  single",
        ],
        "solve": solve_length_of_last_word,
        "brute": brute_length_of_last_word,
    },
    {
        "title": "Longest Common Prefix",
        "level": "Easy",
        "topics": "String, Trie",
        "companies": "Amazon, Google, Yelp",
        "description": (
            "Find the longest run of characters that starts every one of the given words.\n"
            "\n"
            "Input (stdin):\n"
            "\n"
            "- Line 1: the integer `n`, the number of words.\n"
            "- Next `n` lines: one word each.\n"
            "\n"
            "Output (stdout):\n"
            "\n"
            "- One line with the longest common prefix, or `none` when the words share no "
            "starting character.\n"
        ),
        "examples": (
            "**Example 1**\n"
            "\n"
            "```\n"
            "Input:\n"
            "3\n"
            "flower\n"
            "flow\n"
            "flight\n"
            "Output:\n"
            "fl\n"
            "```\n"
            "\n"
            "**Example 2**\n"
            "\n"
            "```\n"
            "Input:\n"
            "3\n"
            "dog\n"
            "racecar\n"
            "car\n"
            "Output:\n"
            "none\n"
            "```\n"
        ),
        "constraints": (
            "- `1 <= n <= 200`\n"
            "- Each word is 1 to 200 lowercase English letters.\n"
        ),
        "inputs": [
            "3\nflower\nflow\nflight",
            "3\ndog\nracecar\ncar",
            "1\nalone",
            "4\nsame\nsame\nsame\nsame",
            "2\nabc\nabcdef",
            "3\na\nab\nabc",
        ],
        "solve": solve_longest_common_prefix,
        "brute": brute_longest_common_prefix,
    },
    {
        "title": "Reverse Words in a String",
        "level": "Medium",
        "topics": "Two Pointers, String",
        "companies": "Microsoft, Amazon, Apple, Snapchat",
        "description": (
            "A line holds words separated by one or more spaces. Print the same words in "
            "the opposite order, with exactly one space between neighbours and no spaces at "
            "either end.\n"
            "\n"
            "Input (stdin):\n"
            "\n"
            "- Line 1: the sentence. It may begin with spaces and may use runs of several "
            "spaces between words.\n"
            "\n"
            "Output (stdout):\n"
            "\n"
            "- One line with the words in reverse order, joined by single spaces.\n"
        ),
        "examples": (
            "**Example 1**\n"
            "\n"
            "```\n"
            "Input:\n"
            "the sky is blue\n"
            "Output:\n"
            "blue is sky the\n"
            "```\n"
            "\n"
            "**Example 2**\n"
            "\n"
            "```\n"
            "Input:\n"
            "a good   example\n"
            "Output:\n"
            "example good a\n"
            "```\n"
        ),
        "constraints": (
            "- The line is 1 to 300 characters long.\n"
            "- It contains only English letters, digits, and spaces.\n"
            "- It holds at least one word.\n"
        ),
        "inputs": [
            "the sky is blue",
            "   hello world   ",
            "a good   example",
            "one",
            "go go go",
            "  Bob    Loves  Alice",
        ],
        "solve": solve_reverse_words_in_a_string,
        "brute": brute_reverse_words_in_a_string,
    },
    {
        "title": "Zigzag Conversion",
        "level": "Medium",
        "topics": "String, Simulation",
        "companies": "Amazon, Microsoft, PayPal",
        "description": (
            "Write a string downwards and diagonally across a fixed number of rows: fill "
            "the rows top to bottom, then climb back up diagonally to the top row, and "
            "repeat until the string runs out. Then read the layout back one row at a time, "
            "left to right.\n"
            "\n"
            "For `PAYPALISHIRING` with 3 rows the layout is\n"
            "\n"
            "```\n"
            "P   A   H   N\n"
            "A P L S I I G\n"
            "Y   I   R\n"
            "```\n"
            "\n"
            "so the reading is `PAHNAPLSIIGYIR`.\n"
            "\n"
            "Input (stdin):\n"
            "\n"
            "- Line 1: the string.\n"
            "- Line 2: the integer number of rows.\n"
            "\n"
            "Output (stdout):\n"
            "\n"
            "- One line with the row-by-row reading of the layout.\n"
        ),
        "examples": (
            "**Example 1**\n"
            "\n"
            "```\n"
            "Input:\n"
            "PAYPALISHIRING\n"
            "3\n"
            "Output:\n"
            "PAHNAPLSIIGYIR\n"
            "```\n"
            "\n"
            "**Example 2**\n"
            "\n"
            "```\n"
            "Input:\n"
            "PAYPALISHIRING\n"
            "4\n"
            "Output:\n"
            "PINALSIGYAHRPI\n"
            "```\n"
        ),
        "constraints": (
            "- The string is 1 to 500 characters long.\n"
            "- It contains only English letters, commas, and full stops.\n"
            "- `1 <= number of rows <= 500`\n"
        ),
        "inputs": [
            "PAYPALISHIRING\n3",
            "PAYPALISHIRING\n4",
            "A\n1",
            "ABCDE\n1",
            "AAAA\n2",
            "ABCDEFG\n5",
        ],
        "solve": solve_zigzag_conversion,
        "brute": brute_zigzag_conversion,
    },
    {
        "title": "Find the Index of the First Occurrence in a String",
        "level": "Easy",
        "topics": "Two Pointers, String, String Matching",
        "companies": "Facebook, Amazon, Microsoft, Apple",
        "description": (
            "Report where a pattern first appears inside a longer string.\n"
            "\n"
            "Input (stdin):\n"
            "\n"
            "- Line 1: the haystack, the string being searched.\n"
            "- Line 2: the needle, the pattern to find.\n"
            "\n"
            "Output (stdout):\n"
            "\n"
            "- One line with the index of the first character of the first match, counting "
            "from 0, or `-1` when the needle never appears.\n"
        ),
        "examples": (
            "**Example 1**\n"
            "\n"
            "```\n"
            "Input:\n"
            "sadbutsad\n"
            "sad\n"
            "Output:\n"
            "0\n"
            "```\n"
            "\n"
            "**Example 2**\n"
            "\n"
            "```\n"
            "Input:\n"
            "leetcode\n"
            "leeto\n"
            "Output:\n"
            "-1\n"
            "```\n"
        ),
        "constraints": (
            "- Each string is 1 to 200 lowercase English letters.\n"
        ),
        "inputs": [
            "sadbutsad\nsad",
            "leetcode\nleeto",
            "a\na",
            "aaaaa\nbba",
            "mississippi\nissip",
            "aaab\nab",
        ],
        "solve": solve_find_the_index_of_the_first_occurrence_in_a_string,
        "brute": brute_find_the_index_of_the_first_occurrence_in_a_string,
    },
    {
        "title": "Text Justification",
        "level": "Hard",
        "topics": "Array, String, Simulation",
        "companies": "Amazon, LinkedIn, Google, Airbnb",
        "description": (
            "Lay out words into lines of exactly `maxWidth` characters. Walk the words in "
            "order and put as many as fit on the current line, where a line needs at least "
            "one space between neighbouring words. Pad every line but the last so it is "
            "exactly `maxWidth` wide: spread the extra spaces over the gaps between words, "
            "and when they do not divide evenly give the extra spaces to the leftmost gaps "
            "first. A line holding a single word, and the final line, are left aligned and "
            "padded on the right.\n"
            "\n"
            "Input (stdin):\n"
            "\n"
            "- Line 1: the integer `maxWidth`.\n"
            "- Line 2: the words, separated by single spaces.\n"
            "\n"
            "Output (stdout):\n"
            "\n"
            "- One line per laid out line. Each one is printed between two `|` characters, "
            "so that the padding spaces are visible: exactly `maxWidth` characters sit "
            "between the bars.\n"
        ),
        "examples": (
            "**Example 1**\n"
            "\n"
            "```\n"
            "Input:\n"
            "16\n"
            "This is an example of text justification.\n"
            "Output:\n"
            "|This    is    an|\n"
            "|example  of text|\n"
            "|justification.  |\n"
            "```\n"
            "\n"
            "**Example 2**\n"
            "\n"
            "```\n"
            "Input:\n"
            "10\n"
            "a b c d e f g\n"
            "Output:\n"
            "|a  b c d e|\n"
            "|f g       |\n"
            "```\n"
        ),
        "constraints": (
            "- `1 <= maxWidth <= 100`\n"
            "- There are 1 to 300 words.\n"
            "- Each word is 1 to `maxWidth` characters of printable non-space text.\n"
        ),
        "inputs": [
            "16\nThis is an example of text justification.",
            "16\nWhat must be acknowledgment shall be",
            "20\nScience is what we understand well enough to explain to a computer. Art is"
            " everything else we do",
            "1\na",
            "5\nab ab ab",
            "10\na b c d e f g",
        ],
        "solve": solve_text_justification,
        "brute": brute_text_justification,
    },
]
