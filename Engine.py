from posixpath import split
from Map import Map
from Cell import Plain, Mountain, Swamp
from GameCharacter import Player, Goblin


class Engine:
    def __init__(self, data_file):
        self._actors = []
        self._remove = []
        self._map = None
        self._player = None
        with open(data_file, "r") as fp:
            line = fp.readline()
            if not line:
                return None
            else:
                items = line.split()
                if len(items) != 5:
                    print("INVALID DATA FILE.")
                    return None
                num_of_row = int(items[0])
                num_of_col = int(items[1])
                p_ox = int(items[2])
                p_hp = int(items[3])
                num_of_goblins = int(items[4])

            self._map = Map(num_of_row, num_of_col)

            # TODO: initialize each cell of the map object
            #       using the build_cell method
            for i in range(num_of_row):
                line = fp.readline()
                split_line = line.split()
                for j in range(len(split_line)):
                    if (split_line[j] == 'P'):
                        self._map.build_cell(i, j, Plain(i, j))
                    elif (split_line[j] == 'M'):
                        self._map.build_cell(i, j, Mountain(i, j))
                    elif (split_line[j] == 'S'):
                        self._map.build_cell(i, j, Swamp(i, j))
            # END TODO

            self._player = Player(num_of_row - 1, 0, p_hp, p_ox)

            # TODO: initilize the position of the player
            #       using the set_occupant and occupying setter;
            #       add the player to _actors array
            init_cell = self._map.get_cell(num_of_row-1, 0)
            init_cell.set_occupant(self._player)
            self._player.occupying = init_cell
            self._actors.append(self._player)
            # END TODO

            for gno in range(num_of_goblins):
                # TODO: initilize each Goblin on the map
                #       using the set_occupant and occupying setter;
                #       add each Goblin to _actors array
                line = fp.readline()
                split_line = line.split()
                g_row = int(split_line[0])
                g_col = int(split_line[1])
                g_actions = []
                for i in range(2, len(split_line)):
                    g_actions.append(split_line[i])
                gob = Goblin(g_row, g_col, g_actions)
                self._actors.append(gob)
                init_cell = self._map.get_cell(g_row, g_col)
                init_cell.set_occupant(gob)
                gob.occupying = init_cell
                # END TODO

    def run(self):
        # main rountine of the game
        self.print_info()
        while not self.state():
            for obj in self._actors:
                if obj.active:
                    obj.act(self._map)
            self.print_info()
            self.clean_up()
        self.print_result()

    def clean_up(self):
        # TODO: remove all objects in _actors which is not active
        # for i in range(len(self._actors)):
        i = 0
        x = len(self._actors)
        while i < x:
            if(not self._actors[i].active):
                self._actors.pop(i)
                x -= 1
            i += 1
        # END TODO

    # check if the game ends and return if the player win or not.
    def state(self):
        # TODO: check if the game ends and
        #       return an integer for the game status
        if(self._player.hp <= 0 or self._player.oxygen <= 0):
            return -1
        elif(self._player.row == 0 and self._player.col == self._map.cols - 1):
            return 1
        return 0
        # END TODO

    def print_info(self):
        self._map.display()
        # TODO: display the remaining oxygen and HP
        print('Oxygen: ', self._player.oxygen, ', HP: ', self._player.hp)
        # END TODO

    def print_result(self):
        # TODO: print a string that shows the result of the game.
        if self.state() == 1:
            print('\033[1;33;41mCongrats! You win!\033[0;0m')
        elif (self.state() == -1):
            print('\033[1;33;41mBad Luck! You lose.\033[0;0m')
        # END TODO
