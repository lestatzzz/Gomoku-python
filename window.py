from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtGui import QPainter, QPen, QColor, QPalette, QBrush, QPixmap, QRadialGradient
from PyQt5.QtCore import Qt, QPoint, QTimer
import traceback
from game import Gomoku
from corner_widget import CornerWidget


def run_with_exc(f):
    # 游戏运行出现错误书，用messagebox显示错误信息
    def call(window, *args, **kwargs):
        try:
            return f(window, *args, *kwargs)
        except Exception:
            exc_info = traceback.format_exc()
            QMessageBox.about(window, '错误信息', exc_info)
        return call


class GomokuWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.init_ui()  # 初始化游戏界面
        self.g = Gomoku()  # 初始化游戏内容

        self.last_pos = (-1, -1)
        self.res = 0  # 记录哪边获得了胜利
        self.operate_status = 0  # 游戏操作状态。0为游戏中（可操作），1为游戏结束闪烁过程中（不可操作）
    
    def init_ui(self):
        '''初始化游戏界面'''  
        # 1. 确定游戏界面的标题， 大小和背景颜色
        # self.setObejectName("MainWindow")
        self.setWindowTitle('五子棋')
        self.setFixedSize(650, 650)
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(QPixmap('imgs/muzm.jpg')))
        self.setPalette(palette)
        # 2. 开启鼠标位置的追踪，并在鼠标位置移动时，使用特殊符号标记当前的位置
        self.setMouseTracking(True)
        # 3. 鼠标位置移动时，对鼠标位置进行特殊标记
        self.corner_widget = CornerWidget(self)
        self.corner_widget.repaint()
        self.corner_widget.hide()
        # 4. 游戏结束时闪烁的定时器
        self.end_timer = QTimer(self)
        self.end_timer.timeout.connect(self.end_flash)
        self.flash_cnt = 0  # 游戏结束前闪烁了多少次
        self.flash_pieces = ((-1, -1), )  # 哪些棋子需要闪烁
        # 5. 显示初始化的游戏界面
        self.show()
        
    @run_with_exc
    def paintEvent(self, e):
        """绘制游戏内容"""

        def draw_map():
            """绘制棋盘"""
            qp.setPen(QPen(QColor(0, 0, 0), 2, Qt.SolidLine))  # 棋盘的颜色为黑色
            # 绘制横线
            for x in range(15):
                qp.drawLine(40 * (x + 1), 40, 40 * (x + 1), 600)
            #  绘制竖线
            for y in range(15):
                qp.drawLine(40, 40 * (y + 1), 600, 40 * (y + 1))
            # 绘制棋盘中的黑点
            qp.setBrush(QColor(0, 0, 0))
            key_points = [(4, 4), (12, 4), (4, 12), (12, 12), (8, 8)]
            for t in key_points:
                qp.drawEllipse(QPoint(40 * t[0], 40 * t[1], 5, 5))

        def draw_pieces():
            '''绘制棋子'''
            # 绘制黑棋子
            qp.setPen(QPen(QColor(0,0,0), 1, Qt.SolidLine))
            for x in range(15):
                for y in range(15):
                    if self.g.g_map[x][y] == 1:
                        if self.flash_cnt % 2 == 1 and (x, y) in self.flash_pieces:
                            continue
                        radial = QRadialGradient(40 * (x + 1), 40 * (y + 1), 15, 40 * x + 35, 40 * y + 35)
                        radial.setColorAt(0, QColor(96, 96, 96))
                        radial.setColorAt(1, QColor(0, 0, 0))
                        qp.setBrush(QBrush(radial))
                        qp.drawEllipse(QPoint(40 * (x + 1), 40 * (y + 1)), 15, 15)
            # 绘制白棋子
            qp.setPen(QPen(QColor(160, 160, 160), 1, Qt.SolidLine))
            for x in range(15):
                for y in range(15):
                    if self.g.g_map[x][y] == 2:
                        if self.flash_cnt % 2 == 1 and (x, y) in self.flash_pieces:
                            continue
                        radial = QRadialGradient(40 * (x + 1), 40 * (y + 1), 15, 40 * x + 35, 40 * y + 35) # 棋子的渐变效果
                        radial.setColorAt(0, QColor(255, 255, 255))
                        radial.setColorAt(1, QColor(160, 160, 160))
                        qp.setBrush(QBrush(radial))
                        qp.drawEllipse(QPoint(40 * ( x + 1), 40 * (y + 1)), 15, 15)

        if hasattr(self, 'g'):
            qp = QPainter()
            qp.begin(self)
            draw_map()  # 绘制棋盘
            draw_pieces()   # 绘制棋子
            qp.end()
        
    @run_with_exc
    def mouseMoveEvent(self, e):
        # 1. 首先判断鼠标位置对应棋盘中的哪一个格子
        mouse_x = e.windowPos().x()
        mouse_y = e.windowPos().y()