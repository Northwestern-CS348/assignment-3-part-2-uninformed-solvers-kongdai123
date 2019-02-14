from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')
    def _get_disk (self, term):
        #takes in a term about a disk and output the number the disk correspondes
        return int(str(term)[4:])

    def _get_peg (self, term):
        #takes in a term about a peg and output the number the disk correspondes
        return int(str(term)[3:])

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here
        peg = []
        for i in self.kb.facts:
            if i.statement.predicate == 'peg': peg.append([])
        for i in self.kb.facts:
            if i.statement.predicate == 'on':
                disk_num = self._get_disk(i.statement.terms[0])
                peg_num = self._get_peg(i.statement.terms[1])
                ##insertion sort the disks
                inserted = False
                i = 0
                while i != len(peg[peg_num - 1]) and disk_num > peg[peg_num - 1][i]:
                    i = i + 1
                peg[peg_num - 1].insert(i, disk_num)

        for i, l in enumerate(peg):
            peg[i] = tuple(l)
        return tuple(peg)



    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        state = self.getGameState()
        disk = movable_statement.terms[0]
        disk_num = self._get_disk(disk)
        start = movable_statement.terms[1]
        start_num = self._get_peg(start)
        end = movable_statement.terms[2]
        end_num = self._get_peg(end)
        #retract top
        print ('initial state')
        self.kb.kb_retract(Fact(['top', str(disk), str(start)]))
        print ('now has removed top fact')
        #retract fact
        self.kb.kb_retract(Fact(['on', str(disk), str(start)]))
        print ('now has removed on peg fact')
        #assign new top

        for i in self.kb.facts:
            if i.statement.predicate == 'ontop' and i.statement.terms[0] == disk:
                print(i)
                self.kb.kb_assert(Fact(['top', i.statement.terms[1], start]))
                #retract old ontop
                self.kb.kb_retract(i)
        print('new top established')
        print('leaving finished')
        #find the old top of the end peg and add the disk onto that
        for i in self.kb.facts:
            if i.statement.predicate == 'top' and i.statement.terms[1] == end:
                self.kb.kb_assert(Fact(['ontop', disk, i.statement.terms[0]]))
                self.kb.kb_retract(i)
                self.kb.kb_assert(Fact(['top', disk, end]))
                self.kb.kb_assert(Fact(['on',disk, end]))
                break



        print('landing finished')
        return

        #START MOVING


    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        print('reversing')
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')
    def _get_tile (self, term):
        #takes in a term about a disk and output the number the disk correspondes
        if str(term) == 'empty': return -1
        return int(str(term)[4:])

    def _get_pos (self, term):
        #takes in a term about a peg and output the number the disk correspondes
        return int(str(term)[3:])

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        #every second level array represents a row
        #so if we want to  locate a block with coords (x, y)
        #we go state[y - 1][x - 1]
        state = [[-1, -1, -1 ], [-1, -1, -1 ] ,[-1, -1, -1]]
        for i in self.kb.facts:
            if i.statement.predicate == 'coords':
                #turn pos into numbers
                tile = self._get_tile(i.statement.terms[0])
                x = self._get_pos(i.statement.terms[1])
                y = self._get_pos(i.statement.terms[2])
                state[y - 1][x - 1] = tile
        #generate tuple
        for i, l in enumerate(state):
            state[i] = tuple(l)
        return tuple(state)



    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        tile = movable_statement.terms[0]
        tile_num = self._get_tile(tile)
        pos1 = movable_statement.terms[1]
        start_x = self._get_pos(pos1)
        pos2 = movable_statement.terms[2]
        start_y = self._get_pos(pos2)
        pos3 = movable_statement.terms[3]
        end_x = self._get_pos(pos3)
        pos4 = movable_statement.terms[4]
        end_y = self._get_pos(pos4)


        print('initial state')

        for i in self.kb.facts:
            if i.statement.predicate == 'coords' and i.statement.terms[0] == tile:
                start_fact = i
            if i.statement.predicate == 'coords' and str(i.statement.terms[0]) == 'empty':
                end_fact = i
        print('position located')

        self.kb.kb_retract(start_fact)
        self.kb.kb_retract(end_fact)
        self.kb.kb_assert(Fact(['coords', 'empty', pos1, pos2]))
        self.kb.kb_assert(Fact(['coords', tile, pos3, pos4]))
        print("change done")

        pass

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
