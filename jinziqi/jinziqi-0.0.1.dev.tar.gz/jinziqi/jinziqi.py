#coding:utf8
import unittest
import itertools
from jinziqi_chess import Player, Chess, ChessBoard

DEBUG = False

class Jinziqi_core():
    def __init__(self, player_a_tag = 'A', player_b_tag = 'B'):
        self.players = []
        self.player_a = Player()
        self.player_a.avatar = player_a_tag
        self.player_b = Player()
        self.player_b.avatar = player_b_tag
        self.players.append(self.player_a)
        self.players.append(self.player_b)
        self.x = 3
        self.cb = ChessBoard(self.x, self.x)

    def print_chessboard(self):                         
        cbc = self.cb._chesses
        step = 1
        for c in cbc:
            if c.content == None:
                print c.id,
            else:
                print c.content.owner.avatar,
            if step == self.x:
                step = 1
                print ''
                continue
            step = step + 1
    def add_chess(self, player, location):
        return player.put_chess(location, self.cb)
    def exit_jinziqi(self, info):
        self.print_chessboard()
        who = info
        print "%s is win" % who
        print 'congratulation %s please run the program again' % who
        exit(0)
    def jinziqi_start2(self):
        '''
        input: player,location
        '''
        while(1):
            self.print_chessboard()
            str_in = input('enter player, location')
            player, location = str_in.split(',')
            location = int(location)
            if player == 'a':
                self.add_chess(self.player_a, location)
                if self.is_win([c.id for c in self.player_a.my_chesses(self.cb)]):
                    self.exit_jinziqi('p1')
            if player == 'b':
                self.add_chess(self.player_b, location)
                if self.is_win([c.id for c in self.player_b.my_chesses(self.cb)]):
                    self.exit_jinziqi('p2')
            if self.cb.is_full():
                print 'no one win'
    def is_win(self, p):
        combinations = self.player_chesses_combinations(p)
        #cb = [self.chessboard(c) for c in combinations] # 有坐标的棋子集合
        for chesses in combinations:
            a = self.chessboard(chesses[0])
            b = self.chessboard(chesses[1])
            c = self.chessboard(chesses[2])
            if self.isline(a, b, c):
                return True
        return False
    def get_chessboard(self):
        return self.cb
    def player_chesses_combinations(self, player, c = 3 ):
        return tuple(itertools.combinations(player, c))
    def chessboard(self, t):
        _ch = self.cb.get_chess(t)
        convert_obj = None
        if _ch:
            convert_obj = (_ch.x, _ch.y)
        return convert_obj
    def isline(self, a, b, c):
        if self._isline_x(a,b,c):
            return True
        if self._isline_y(a,b,c):
            return True
        if self._isline_xy_1(a,b,c):
            return True
        if self._isline_xy_2(a,b,c):
            return True
        return False
    def _isline_x(self, a, b, c):
        if a[0] == b[0] :
            if b[0] == c[0]:
                return True
            else:
                return False
        else:
            return False
    def _isline_y(self, a, b, c):
        if a[1] == b[1] :
            if b[1] == c[1]:
                return True
            else:
                return False
        else:
            return False
    def _isline_xy_1(self, a, b, c):
        #y=x
        c = [a,b,c]
        result = True
        for x,y in c:
            if x==y:
                result = True
            else:
                result = False
                break
        return result
    def _isline_xy_2(self, a, b, c):
        #y = 2-x
        c = [a,b,c]
        result = True
        for x,y in c:
            if y == (2-x):
                result = True
            else:
                result = False
                break
        return result

class JinziqiTest(unittest.TestCase):
    def setUp(self):
        self.jinziqi = Jinziqi_core()
    def testPlayerCount(self):
        '''only 2 player
        '''
        self.assertTrue(len(self.jinziqi.players) == 2)

    def test_player(self):
        '''测试玩家
        '''
        jinziqi_program = Jinziqi_core()
        self.assertEquals([],jinziqi_program.player_a.my_chesses(jinziqi_program.cb))
        self.assertEquals([],jinziqi_program.player_b.my_chesses(jinziqi_program.cb))

    def test_line_x(self):
        '''测试坐标是否符合一条横直线
        '''
        jinziqi_program = Jinziqi_core()
        chessboard = jinziqi_program.get_chessboard()
        chessboard.put_chess(Chess(0, Player()))
        a = jinziqi_program.chessboard(0)
        chessboard.put_chess(Chess(1, Player()))
        b = jinziqi_program.chessboard(1)
        chessboard.put_chess(Chess(2, Player()))
        c = jinziqi_program.chessboard(2)
        self.assertTrue(jinziqi_program.isline(a, b, c))
        chessboard.put_chess(Chess(1, Player()))
        a = jinziqi_program.chessboard(1)
        chessboard.put_chess(Chess(8, Player()))
        b = jinziqi_program.chessboard(8)
        chessboard.put_chess(Chess(3, Player()))
        c = jinziqi_program.chessboard(3)
        self.assertFalse(jinziqi_program.isline(a, b, c))
    def test_line_y(self):
        '''测试坐标是否符合一条纵直线
        '''
        jinziqi_program = Jinziqi_core()
        chessboard = jinziqi_program.get_chessboard()
        chessboard = jinziqi_program.get_chessboard()
        chessboard.put_chess(Chess(1, Player()))
        chessboard.put_chess(Chess(4, Player()))
        chessboard.put_chess(Chess(7, Player()))
        a = jinziqi_program.chessboard(1)
        b = jinziqi_program.chessboard(4)
        c = jinziqi_program.chessboard(7)
        self.assertTrue(jinziqi_program.isline(a, b, c))
    def test_line_xy(self):
        '''测试方程y=x和y=2-x两条直线
        '''
        jinziqi_program = Jinziqi_core()
        chessboard = jinziqi_program.get_chessboard()
        chessboard.put_chess(Chess(0, Player()))
        chessboard.put_chess(Chess(4, Player()))
        chessboard.put_chess(Chess(8, Player()))
        a = jinziqi_program.chessboard(0)
        b = jinziqi_program.chessboard(4)
        c = jinziqi_program.chessboard(8)
        self.assertTrue(jinziqi_program.isline(a, b, c))
        chessboard.put_chess(Chess(6, Player()))
        chessboard.put_chess(Chess(4, Player()))
        chessboard.put_chess(Chess(2, Player()))
        a = jinziqi_program.chessboard(6)
        b = jinziqi_program.chessboard(4)
        c = jinziqi_program.chessboard(2)
        self.assertTrue(jinziqi_program.isline(a, b, c))
    def test_chesses_combinations(self):
        '''测试棋子的组合
        '''
        jinziqi_program = Jinziqi_core()
        a = jinziqi_program.player_chesses_combinations([1,2,3,4,5])
        b = tuple(itertools.combinations([1,2,3,4,5], 3))
        self.assertTrue(b == a)
    def test_win(self):
        '''测试检测获胜的判断
        '''
        jinziqi_program = Jinziqi_core()
        chessboard = jinziqi_program.get_chessboard()
        chessboard.put_chess(Chess(0, Player()))
        chessboard.put_chess(Chess(1, Player()))
        chessboard.put_chess(Chess(2, Player()))
        chessboard.put_chess(Chess(6, Player()))
        chessboard.put_chess(Chess(7, Player()))
        self.assertTrue(jinziqi_program.is_win([0,1,2,6,7]))
    def test_add_chess(self):
        jinziqi_program = Jinziqi_core('X', 'O')
        p1 = Player()
        chess = jinziqi_program.add_chess(p1, 1)
        self.assertTrue(chess.owner == p1)
        self.assertTrue(chess.id == 1)
    def test_print_chessboard(self):
        jinziqi_program = Jinziqi_core('X', 'O')
        position = 7
        play_a = [1,2]
        play_b = [3,7]
        self.assertTrue('O' == jinziqi_program.print_chess(position, play_a, play_b))
        position = 7
        play_a = [1,7]
        play_b = [3,6]
        self.assertTrue('X' == jinziqi_program.print_chess(position, play_a, play_b))
        position = 5
        play_a = [1,2]
        play_b = [3,7]
        self.assertTrue('5' == jinziqi_program.print_chess(position, play_a, play_b))


if __name__ == '__main__':
    if DEBUG:
        unittest.main()
    else:
        jinziqi_program = Jinziqi_core()
        jinziqi_program.jinziqi_start2()

