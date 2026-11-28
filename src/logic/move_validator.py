# grid là 1 tuple lưu độ chiều rộng và chiều dài của bảng
# pos là 1 tuple lưu tọa độ cell
# move_dict là dictionary lưu các nước đi
# game_state là trạng thái game
class Move_validator:
    def __init__ (self, pos = None, grid = None, game_state = None, move_dict = None):
        self.pos = pos
        self.grid = grid
        self.state = game_state
        self.is_in_bound = False
        self.move_dict = move_dict
        self.is_empti = False
    def is_within_bound(self):
        if self.pos == None:
            self.is_in_bound = False
            return
        if (self.grid[0] > self.pos[0] and self.pos[0] >= 0) and (self.grid[1] > self.pos[1] and self.pos[1] >= 0):
            self.is_in_bound = True
            return
        self.is_in_bound = False
        return
    def is_cell_empti (self):
        if self.move_dict[self.pos] == 0:
            self.is_empti = True
        else:
            self.is_empti = False
    def validate_move(self):
        self.is_within_bound()
        if self.is_in_bound and self.state == "playing":
            self.is_cell_empti()
            if self.is_empti:
                return True
        return False
