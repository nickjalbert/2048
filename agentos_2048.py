"""An implementation of 2048 that satisifes the AgentOS Environment spec."""
import random
from etc.squash_lookup_table import squash_lookup
import enum


class Direction(enum.Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3


class AgentOS2048:
    STATE_LEN = 16
    RIGHT = Direction.RIGHT
    DOWN = Direction.DOWN
    LEFT = Direction.LEFT
    UP = Direction.UP
    action_space = [RIGHT, DOWN, UP, LEFT]

    @classmethod
    def get_valid_actions_from_board(cls, board):
        test_game = cls()
        test_game.set_board(board)
        return test_game.get_valid_actions()

    @classmethod
    def get_valid_actions_by_reward_from_board(cls, board):
        test_game = cls()
        test_game.set_board(board)
        return test_game.get_valid_actions_by_reward()

    def get_valid_actions(self):
        """Returns list of 3-tuples: [(action, reward, board),...]"""
        test_game = self.__class__()
        valid_actions = []
        all_actions = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
        random.shuffle(all_actions)
        for action in all_actions:
            test_game.set_board(self.board)
            board, reward, _, _ = test_game.step(action)
            if board != self.board:
                valid_actions.append((action, reward, board))
        return valid_actions

    def get_valid_actions_by_reward(self):
        return sorted(self.get_valid_actions(), key=lambda x: -1 * x[1])

    def render_board(self):
        def j(el):
            return str(el).rjust(5)

        p = ["·" if x == 0 else x for x in self.board]
        print(
            f"{j(p[0])} {j(p[1])} {j(p[2])} {j(p[3])}\n"
            f"{j(p[4])} {j(p[5])} {j(p[6])} {j(p[7])}\n"
            f"{j(p[8])} {j(p[9])} {j(p[10])} {j(p[11])}\n"
            f"{j(p[12])} {j(p[13])} {j(p[14])} {j(p[15])}\n\n"
        )





# self.board is a 1D list that represents the 2D board follows:
#       [
#           board[0]   board[1]   board[2]   board[3]
#           board[4]   board[5]   board[6]   board[7]
#           board[8]   board[9]  board[10]  board[11]
#          board[12]  board[13]  board[14]  board[15]
#       ]
#
# TODO: allow for boards of different dimensions


    def __init__(self, random_seed=None):

        self.random_seed = random_seed
        self.reset()

    @classmethod
    def get_canonical_afterstate(cls, board, action):
        afterstate, reward = cls.get_afterstate(board, action)
        return cls.get_canonical_board(afterstate)

    @classmethod
    def get_afterstate(cls, board, action):
        game = cls()
        game.set_board(board)
        do_action = {
            Direction.UP: game._do_up,
            Direction.RIGHT: game._do_right,
            Direction.DOWN: game._do_down,
            Direction.LEFT: game._do_left,
        }
        do_action[action]()
        return game.board, game.score

    @classmethod
    def get_canonical_board(cls, board):
        r0 = board
        r90 = cls.rotate_board_right(board)
        r180 = cls.rotate_board_right(r90)
        r270 = cls.rotate_board_right(r180)
        xr0 = cls.reflect_board_across_x(board)
        xr90 = cls.rotate_board_right(xr0)
        xr180 = cls.rotate_board_right(xr90)
        xr270 = cls.rotate_board_right(xr180)
        rotations_and_reflections = set([r0, r90, r180, r270, xr0, xr90, xr180, xr270])
        # treat each board as a 16 digit number (where each digit is 0 to 2^17)
        # return the board that corresponds to the largest digit.
        for idx in range(16):
            max_num = max(r[idx] for r in rotations_and_reflections)
            rotations_and_reflections = set(
                [r for r in rotations_and_reflections if r[idx] >= max_num]
            )
            if len(rotations_and_reflections) == 1:
                break
        assert len(rotations_and_reflections) == 1
        return rotations_and_reflections.pop()

    @classmethod
    def reflect_board_across_x(cls, board):
        return (
            board[12],
            board[13],
            board[14],
            board[15],
            board[8],
            board[9],
            board[10],
            board[11],
            board[4],
            board[5],
            board[6],
            board[7],
            board[0],
            board[1],
            board[2],
            board[3],
        )

    @classmethod
    def reflect_board_across_y(cls, board):
        return (
            board[3],
            board[2],
            board[1],
            board[0],
            board[7],
            board[6],
            board[5],
            board[4],
            board[11],
            board[10],
            board[9],
            board[8],
            board[15],
            board[14],
            board[13],
            board[12],
        )

    @classmethod
    def rotate_board_right(cls, board):
        return (
            board[12],
            board[8],
            board[4],
            board[0],
            board[13],
            board[9],
            board[5],
            board[1],
            board[14],
            board[10],
            board[6],
            board[2],
            board[15],
            board[11],
            board[7],
            board[3],
        )

    @property
    def done(self):
        if len(self.empty_indexes) > 0:
            return False
        # board is full, so just check neighbors to see if we can squish
        idx0 = self.board[0]
        idx1 = self.board[1]
        if idx0 == idx1:
            return False
        idx4 = self.board[4]
        if idx0 == idx4:
            return False
        idx2 = self.board[2]
        if idx1 == idx2:
            return False
        idx5 = self.board[5]
        if idx1 == idx5:
            return False
        idx3 = self.board[3]
        if idx2 == idx3:
            return False
        idx6 = self.board[6]
        if idx2 == idx6:
            return False
        idx7 = self.board[7]
        if idx3 == idx7:
            return False
        if idx4 == idx5:
            return False
        idx8 = self.board[8]
        if idx4 == idx8:
            return False
        if idx5 == idx6:
            return False
        idx9 = self.board[9]
        if idx5 == idx9:
            return False
        if idx6 == idx7:
            return False
        idx10 = self.board[10]
        if idx6 == idx10:
            return False
        idx11 = self.board[11]
        if idx7 == idx11:
            return False
        if idx8 == idx9:
            return False
        idx12 = self.board[12]
        if idx8 == idx12:
            return False
        idx13 = self.board[13]
        if idx9 == idx10:
            return False
        if idx9 == idx13:
            return False
        if idx10 == idx11:
            return False
        idx14 = self.board[14]
        if idx10 == idx14:
            return False
        idx15 = self.board[15]
        if idx11 == idx15:
            return False
        if idx12 == idx13:
            return False
        if idx13 == idx14:
            return False
        if idx14 == idx15:
            return False
        return True

    def get_state(self):
        return self.board, self.score, self.done

    def set_board(self, board):
        # Copy board as we set so we don't get surprising aliasing errors
        assert len(board) == 16
        self.empty_indexes = [i for (i, v) in enumerate(board) if v == 0]
        self.board = tuple(board)

    def step(self, action):
        """Returns a 3-tuple of (board, reward for action, boolean is_done)"""
        assert action in self.action_space
        do_action = {
            Direction.UP: self._do_up,
            Direction.RIGHT: self._do_right,
            Direction.DOWN: self._do_down,
            Direction.LEFT: self._do_left,
        }
        old_board = self.board
        old_score = self.score
        do_action[action]()
        if old_board != self.board:
            self.add_new_random_number()
        board, new_score, done = self.get_state()
        return board, new_score - old_score, done, {}

    def reset(self):
        self.set_board((0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
        self.add_new_random_number()
        self.add_new_random_number()
        self.score = 0
        return self.board

    def reseed(self):
        if self.random_seed:
            random.seed(self.random_seed)

    def add_new_random_number(self):
        self.reseed()
        return self._set_random_position(2 if random.random() <= 0.9 else 4)

    def _set_random_position(self, value):
        try:
            self.reseed()
            idx = random.choice(self.empty_indexes)
        except IndexError:
            return -1
        idx_plus_one = idx + 1
        board = self.board[:idx] + (value,) + self.board[idx_plus_one:]
        self.set_board(board)
        return idx

    def _do_up(self):
        sq1, r1 = squash_lookup[
            (self.board[0], self.board[4], self.board[8], self.board[12])
        ]
        sq2, r2 = squash_lookup[
            (self.board[1], self.board[5], self.board[9], self.board[13])
        ]
        sq3, r3 = squash_lookup[
            (self.board[2], self.board[6], self.board[10], self.board[14])
        ]
        sq4, r4 = squash_lookup[
            (self.board[3], self.board[7], self.board[11], self.board[15])
        ]
        self.set_board(
            (
                sq1[0],
                sq2[0],
                sq3[0],
                sq4[0],
                sq1[1],
                sq2[1],
                sq3[1],
                sq4[1],
                sq1[2],
                sq2[2],
                sq3[2],
                sq4[2],
                sq1[3],
                sq2[3],
                sq3[3],
                sq4[3],
            )
        )
        self.score += r1 + r2 + r3 + r4

    def _do_right(self):
        sq1, r1 = squash_lookup[
            (self.board[3], self.board[2], self.board[1], self.board[0])
        ]
        sq2, r2 = squash_lookup[
            (self.board[7], self.board[6], self.board[5], self.board[4])
        ]
        sq3, r3 = squash_lookup[
            (self.board[11], self.board[10], self.board[9], self.board[8])
        ]
        sq4, r4 = squash_lookup[
            (self.board[15], self.board[14], self.board[13], self.board[12])
        ]
        self.set_board(
            (
                sq1[3],
                sq1[2],
                sq1[1],
                sq1[0],
                sq2[3],
                sq2[2],
                sq2[1],
                sq2[0],
                sq3[3],
                sq3[2],
                sq3[1],
                sq3[0],
                sq4[3],
                sq4[2],
                sq4[1],
                sq4[0],
            )
        )
        self.score += r1 + r2 + r3 + r4

    def _do_down(self):
        sq1, r1 = squash_lookup[
            (self.board[12], self.board[8], self.board[4], self.board[0])
        ]
        sq2, r2 = squash_lookup[
            (self.board[13], self.board[9], self.board[5], self.board[1])
        ]
        sq3, r3 = squash_lookup[
            (self.board[14], self.board[10], self.board[6], self.board[2])
        ]
        sq4, r4 = squash_lookup[
            (self.board[15], self.board[11], self.board[7], self.board[3])
        ]
        self.set_board(
            (
                sq1[3],
                sq2[3],
                sq3[3],
                sq4[3],
                sq1[2],
                sq2[2],
                sq3[2],
                sq4[2],
                sq1[1],
                sq2[1],
                sq3[1],
                sq4[1],
                sq1[0],
                sq2[0],
                sq3[0],
                sq4[0],
            )
        )
        self.score += r1 + r2 + r3 + r4

    def _do_left(self):
        sq1, r1 = squash_lookup[
            (self.board[0], self.board[1], self.board[2], self.board[3])
        ]
        sq2, r2 = squash_lookup[
            (self.board[4], self.board[5], self.board[6], self.board[7])
        ]
        sq3, r3 = squash_lookup[
            (self.board[8], self.board[9], self.board[10], self.board[11])
        ]
        sq4, r4 = squash_lookup[
            (self.board[12], self.board[13], self.board[14], self.board[15])
        ]
        self.set_board(
            (
                sq1[0],
                sq1[1],
                sq1[2],
                sq1[3],
                sq2[0],
                sq2[1],
                sq2[2],
                sq2[3],
                sq3[0],
                sq3[1],
                sq3[2],
                sq3[3],
                sq4[0],
                sq4[1],
                sq4[2],
                sq4[3],
            )
        )
        self.score += r1 + r2 + r3 + r4

