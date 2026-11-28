class GameLogic:
    def __init__(self, size):
        self.size = size
        self.board = {}
        self.turn_count = 0

    def notify_cell_clicked(self, row, col):
        print(f"Pressed cell: ({row}, {col})")

        # --DEMO--- will be removed
        
        if (row, col) not in self.board:
            self.turn_count += 1
            player = 1 if self.turn_count % 2 == 1 else 2
            self.board[(row, col)] = player
        # ---------------------------------------------------------

        # Call
        #
        #