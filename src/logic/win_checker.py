
DIRECTIONS = [
    (0, 1),    # Horizontal
    (1, 0),    # Vertical
    (1, 1),    # Diagonal \
    (1, -1)    # Diagonal /
]


def count_direction(board, row, col, dr, dc, player):
    """
    Count consecutive pieces in one direction.
    Does not include the starting cell.
    """
    count = 0

    row += dr
    col += dc

    while board.get_cell(row, col) == player:
        count += 1
        row += dr
        col += dc

    return count


def check_blocked_ends(board, row, col, dr, dc, player):
    """
    Check whether both ends of a consecutive line are blocked.

    An end is blocked if:
    - It is outside the board.
    - It contains the opponent's piece.

    An empty cell is not blocked.
    """
    count_forward = count_direction(
        board, row, col, dr, dc, player
    )

    count_backward = count_direction(
        board, row, col, -dr, -dc, player
    )

    start_row = row - (count_backward + 1) * dr
    start_col = col - (count_backward + 1) * dc

    end_row = row + (count_forward + 1) * dr
    end_col = col + (count_forward + 1) * dc

    before = board.get_cell(start_row, start_col)
    after = board.get_cell(end_row, end_col)

    blocked_before = (
        before is None or before != player
    )

    blocked_after = (
        after is None or after != player
    )

    return blocked_before, blocked_after


def check_win_conditions(
    board,
    row,
    col,
    player,
    block_both_ends=False,
    win_length=5
):
    """
    Check winning conditions in all four directions.
    """
    if board.get_cell(row, col) != player:
        return False

    for dr, dc in DIRECTIONS:

        count_forward = count_direction(
            board, row, col, dr, dc, player
        )

        count_backward = count_direction(
            board, row, col, -dr, -dc, player
        )

        total = 1 + count_forward + count_backward

        if total < win_length:
            continue

        if block_both_ends:
            blocked_before, blocked_after = check_blocked_ends(
                board, row, col, dr, dc, player
            )

            if blocked_before and blocked_after:
                continue

        return True

    return False


def check_win(
    board,
    row,
    col,
    player,
    block_both_ends=False,
    win_length=5
):
    """
    Public function used by the game.
    """
    return check_win_conditions(
        board,
        row,
        col,
        player,
        block_both_ends,
        win_length
    )


def check_draw(board):
    """
    Check whether the board is full.
    """
    return board.is_full()
