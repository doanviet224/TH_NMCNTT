
class WinChecker:
    DIRECTIONS = [
        (0, 1),    # Ngang
        (1, 0),    # Dọc
        (1, 1),    # Cheo xuoi
        (1, -1)    # Cheo nguoc
    ]

    def __init__(self, win_count=5, block_both_ends=True):
        self.win_count = win_count
        self.block_both_ends = block_both_ends

    def get_cell(self, board, row, col):
        """
        Ho tro:
        - Dictionary: {(row, col): player}
        - List 2 chieu: board[row][col]
        """

        if isinstance(board, dict):
            return board.get((row, col), None)

        if isinstance(board, list):
            if 0 <= row < len(board):
                if 0 <= col < len(board[row]):
                    return board[row][col]

        return None

    def count_direction(self, board, row, col, player, dr, dc):
        """
        Dem so quan lien tiep theo mot huong.
        """

        count = 0
        r = row + dr
        c = col + dc

        while self.get_cell(board, r, c) == player:
            count += 1
            r += dr
            c += dc

        return count, (r, c)

    def is_blocked(self, board, row, col, opponent):
        """
        Kiem tra dau day co bi chan khong.

        - Quan doi phuong: bi chan.
        - Bien ban co huu han: bi chan.
        - O trong: khong bi chan.
        - Ban co vo han: o chua co quan la o trong.
        """

        cell = self.get_cell(board, row, col)

        return cell == opponent

    def check_direction(self, board, row, col, player, dr, dc):
        """
        Kiem tra 5 quan lien tiep theo mot duong.
        """

        opponent = self.get_opponent(board, player)

        left_count, left_end = self.count_direction(
            board, row, col, player, -dr, -dc
        )

        right_count, right_end = self.count_direction(
            board, row, col, player, dr, dc
        )

        total = 1 + left_count + right_count

        if total < self.win_count:
            return False

        if not self.block_both_ends:
            return True

        left_blocked = self.is_blocked(
            board, left_end[0], left_end[1], opponent
        )

        right_blocked = self.is_blocked(
            board, right_end[0], right_end[1], opponent
        )

        return not (left_blocked and right_blocked)

    def get_opponent(self, board, player):
        """
        Tim quan cua doi thu.
        Ho tro X/O hoac 1/2.
        """

        if player == "X":
            return "O"

        if player == "O":
            return "X"

        if player == 1:
            return 2

        if player == 2:
            return 1

        return None

    def check_winner(self, board, row, col, player):
        """
        Kiem tra nguoi choi vua danh co thang hay khong.
        """

        if self.get_cell(board, row, col) != player:
            return False

        for dr, dc in self.DIRECTIONS:
            if self.check_direction(
                board, row, col, player, dr, dc
            ):
                return True

        return False
