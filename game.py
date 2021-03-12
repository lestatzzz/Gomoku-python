import os
import time


class Gomoku:

    def __init__(self):
        self.g_map = [[0 for y in range(15)] for x in range(15)] # 当前的棋盘
        self.cur_step = 0 # 步数

    
    def move_1step(self):
        # 玩家落子
        while True:
            try:
                pos_x = int(input("x: ")) # 接受玩家的输入
                pos_y = int(input("y: "))
                if 0 <= pos_x <= 14 and 0 <= pos_y <= 14: # 判断这个格子能否落子
                    if self.g_map[pos_x][pos_y] == 0:
                        self.g_map[pos_x][pos_y] = 1
                        self.cur_step += 1
                        return
            except ValueError: # 玩家输入不正确的情况（例如输入了“A”）
                continue
    
    def ai_move_1step(self):
        # 电脑落子
        for x in range(15):  # 遍历棋盘，哪里空下哪里
            for y in range(15):
                if self.g_map[x][y] == 0:
                    self.g_map[x][y] = 2
                    self.cur_step += 1
                    return 


    def game_result(self):
        # 判断游戏的结局，0为游戏进行中，1为玩家获胜，2为电脑获胜，3为平局
        # 1. 判断是否横向五连子
        for x in range(11):
            for y in range(11):
                if self.g_map[x][y] == 1 and self.g_map[x+1][y] == 1 and self.g_map[x+2][y] == 1 and self.g_map[x+3][y] == 1 and self.g_map[x+4][y] == 1:
                    return 1
                if self.g_map[x][y] == 2 and self.g_map[x+1][y] == 2 and self.g_map[x+2][y] == 2 and self.g_map[x+3][y] == 2 and self.g_map[x+4][y] == 2:
                    return 2

        # 2. 判断是否纵向五连子
        for x in range(11):
            for y in range(11):
                if self.g_map[x][y] == 1 and self.g_map[x][y+1] == 1 and self.g_map[x][y+2] == 1 and self.g_map[x][y+3] == 1 and self.g_map[x][y+4] == 1:
                    return 1
                if self.g_map[x][y] == 2 and self.g_map[x][y+1] == 2 and self.g_map[x][y+2] == 2 and self.g_map[x][y+3] == 2 and self.g_map[x][y+4] == 2:
                    return 2

        # 3. 判断是否有左上-右下五连子
        for x in range(11):
            for y in range(11):
                if self.g_map[x][y] == 1 and self.g_map[x+1][y+1] == 1 and self.g_map[x+2][y+2] == 1 and self.g_map[x+3][y+3] == 1 and self.g_map[x+4][y+4] == 1:
                    return 1
                if self.g_map[x][y] == 2 and self.g_map[x+1][y+1] == 2 and self.g_map[x+2][y+2] == 2 and self.g_map[x+3][y+3] == 2 and self.g_map[x+4][y+4] == 2:
                    return 2

        # 4. 判断是否有右上-左下五连子
        for x in range(11):
            for y in range(11):
                if self.g_map[x+4][y] == 1 and self.g_map[x+3][y+1] == 1 and self.g_map[x+2][y+2] == 1 and self.g_map[x+1][y+3] == 1 and self.g_map[x][y+4] == 1:
                    return 1
                if self.g_map[x+4][y] == 2 and self.g_map[x+3][y+1] == 2 and self.g_map[x+2][y+2] == 2 and self.g_map[x+1][y+3] == 2 and self.g_map[x][y+4] == 2:
                    return 2

        # 5. 判断是否为平局
        for x in range(15):
            for y in range(15):
                if self.g_map[x][y] == 0: # 棋盘中还有剩余的格子，不能判断为平局
                    return 0

        return 3

    def show(self, res):
        # 显示游戏内容
        for y in range(15):
            for x in range(15):
                if self.g_map[x][y] == 0:
                    print(' ', end='')
                elif self.g_map[x][y] == 1:
                    print('🀅', end='')
                elif self.g_map[x][y] == 2:
                    print('🀆', end='')
                
                if x != 14:
                    print('-', end='')
            print('\n', end='')
            for x in range(15):
                print('| ', end='')
            print('\n', end='')
            
        if res == 1:
            print("YOU WIN!!!")
        elif res == 2:
            print("YOU LOSE!!!")
        elif res == 3:
            print("IT'S A TIE!!!")



    def play(self):
        while True:
            self.move_1step()  # 玩家下一步
            res = self.game_result() # 判断游戏结果
            if res != 0:   # 如果游戏为“已经结束”，则显示游戏内容，并退出主循环
                self.show(res)
                return
            self.ai_move_1step()  # 电脑下一步
            res = self.game_result()
            if res != 0:
                self:show(res)
                return
            self.show(0)  # 在游戏还没有结束的情况下，现实游戏内容，并继续下一轮循环
