from abc import abstractmethod
from operator import truediv


class GameCharacter:
    def __init__(self, row, col):
        self._row = row
        self._col = col
        self._occupying = None
        self._name = None
        self._active = True
        self._character = None
        self._color = "\033[1;31m"

    # TODO: name getter
    @property
    def name(self):
        return self._name

    # TODO: row getter
    @property
    def row(self):
        return self._row

    # TODO: col getter
    @property
    def col(self):
        return self._col

    # TODO: active getter and setter
    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, a):
        self._active = a

    # TODO: occupying getter and setter
    @property
    def occupying(self):
        return self._occupying

    @occupying.setter
    def occupying(self, a):
        self._occupying = a

    def cmd_to_pos(self, char):
        next_pos = [self._row, self._col]
        if char == "L":
            next_pos[1] -= 1
        elif char == "R":
            next_pos[1] += 1
        elif char == "U":
            next_pos[0] -= 1
        elif char == "D":
            next_pos[0] += 1
        else:
            print("Invalid Move.")
        return next_pos

    @abstractmethod
    def act(self, map):
        pass

    @abstractmethod
    def interactWith(self, comer):
        pass

    def display(self):
        # TODO: return _color followed by _character for displaying
        return self._color + self._character
        # END TODO


class Player(GameCharacter):
    def __init__(self, row, col, hp=10, oxygen=10):
        GameCharacter.__init__(self, row, col)
        self._valid_actions = ["U", "D", "R", "L"]
        self._hp = hp
        self._oxygen = oxygen
        self._name = "Player"
        self._character = "A"

    # TODO: hp getter and setter
    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, h):
        self._hp = h

    # TODO: oxygen getter and setter
    @property
    def oxygen(self):
        return self._oxygen

    @oxygen.setter
    def oxygen(self, ox):
        self._oxygen = ox

    def act(self, map):
        next_cell = None
        next_pos = [0, 0]
        while next_cell == None:
            # TODO: act method
            correctAct = False
            while(not correctAct):
                action = input("Next move (U, D, R, L): ".format(
                    self._row, self._col))
                if action in self._valid_actions:
                    next_pos = self.cmd_to_pos(action)
                    correctAct = True
                else:
                    print(
                        'Invalid command. Please enter one of {U, D, R, L}.')

            next_cell = map.get_cell(next_pos[0], next_pos[1])
            if (next_cell != None and next_cell.set_occupant(self)):
                self._row = next_pos[0]
                self._col = next_pos[1]
                self.oxygen = self.oxygen - self.occupying.hours
                self.occupying.remove_occupant()
                self.occupying = next_cell
            else:
                next_cell = None
            # END TODO

    # return whether comer entering the cell successfully or not
    def interact_with(self, comer):
        if comer.name == "Goblin":
            print(
                '\033[1;31;46mPlayer meets a Goblin! Player\'s HP - %d.\033[0m' % (comer.damage))
            # TODO: interact_with method
            self.hp = self.hp - comer.damage
            comer.active = False
        return False
        # END TODO


class Goblin(GameCharacter):
    def __init__(self, row, col, actions):
        GameCharacter.__init__(self, row, col)
        self._actions = actions
        self._cur_act = 0
        self._damage = 1
        self._name = "Goblin"
        self._character = "G"

    # TODO: damage getter
    @property
    def damage(self):
        return self._damage

    def act(self, map):
        # TODO: act method of a Goblin
        # get the next cell according to _actions and _cur_act
        next_move = self._actions[self._cur_act % len(self._actions)]
        next_pos = self.cmd_to_pos(next_move)
        next_cell = map.get_cell(next_pos[0], next_pos[1])
        self._cur_act += 1
        if (next_cell != None and next_cell.set_occupant(self)):
            self._row = next_pos[0]
            self._col = next_pos[1]
            self.occupying.remove_occupant()
            self.occupying = next_cell
            print("\033[1;31;46mGoblin enters the cell (%d, %d).\033[0;0m" %
                  (self._row, self._col))
        if(not self._active):
            print("\033[1;31;46mGoblin dies right after the movement.\033[0;0m")
            self.occupying.remove_occupant()
        # END TODO

    # return whether comer entering the cell successfully or not
    def interact_with(self, comer):
        if comer.name == "Player":
            print(
                "\033[1;31;46mA goblin at cell (%d, %d) meets Player. The goblin died. Player's HP - 1.\033[0;0m"
                % (self._row, self._col)
            )
            # TODO: update properties of the player and the Goblin
            #       return whether the Player successfully enter the cell
            comer.hp = comer.hp - self._damage
            self.active = False
            return True
        return False
        # END TODO
