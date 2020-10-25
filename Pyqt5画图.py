import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from VipCode import *
import easygui as gui


# 画直线的类
class Draw_line(PyQt5_QDialog):

    def init(self):
        # 初始化页面-- 设置标签 设置固定大小 设置标签的拖动事件 设定坐标的初始值
        self.setFixedSize(800,800)
        self.setWindowTitle('画图-PyQt5')
        self.pos = []
        self.label = PyQt5_Qlabel(self,0,0,800,800)
        self.label.moved.connect(self.get_position)
        def a():self.pos.append([self.color,self.pensize])
        self.label.pressed.connect(a)
        self.x = 0
        self.y = 0

        self.color = [0,0,0]
        self.color_btn = PyQt5_QPushButton(self,0,0)
        self.color_btn.setText('color')
        self.color_btn.pressed.connect(self.change_color)
        self.color_btn.setStyleSheet('background-color:rgb(235,235,235)')

        self.pensize = 10
        self.size_btn = PyQt5_QPushButton(self,114,0)
        self.size_btn.setText('pensize:%d'%self.pensize)
        self.size_btn.pressed.connect(self.change_size)
        self.size_btn.setStyleSheet('background-color:rgb(235,235,235)')

        self.btn = PyQt5_QPushButton(self,227,0)
        self.btn.setText('clear')
        def clear():
            if gui.boolbox('Do you mean clear the screen?'+'\nThis is the last warning!'*3):
                self.pos = []
        self.btn.pressed.connect(clear)
        self.btn.setStyleSheet('background-color:rgb(235,235,235)')

    def change_size(self):
        dl = QDialog()
        dl.setWindowTitle('Change Pensize')
        dl.setFixedSize(300,200)

        size = QSlider(Qt.Horizontal,dl)        #FIXME:QSlider不显示
        size.move(25,200)
        size.setRange(1,100)
        size.setFixedWidth(250)
        size.setValue(self.pensize)
        size.setTickPosition(QSlider.TicksBelow)
        size.setTickInterval(5)

        def change():
            self.pensize = size.value()
            def paintEvent(dl,event):
                qp = QPainter(dl)
                qp.setPen(QPen(QColor(0,0,0),self.pensize))
                qp.drawLine(25,50,275,50)
        change()

        size.valueChanged.connect(change)

        dl.exec_()
    def change_color(self):
        dl = QDialog()
        dl.setWindowTitle('Change Color')
        dl.setFixedSize(300,200)
        label = QLabel(dl)
        label.setFixedSize(300,50)
        label.move(0,0)
        label.setAutoFillBackground(True)
        label.setStyleSheet('background-color:rgb%s'%str(tuple(self.color)))

        r = QSlider(dl)
        r.move(50,60)
        r.setFixedHeight(140)
        g = QSlider(dl)
        g.move(150,60)
        g.setFixedHeight(140)
        b = QSlider(dl)
        b.move(250,60)
        b.setFixedHeight(140)

        r.setMinimum(0)
        r.setMaximum(255)
        r.setValue(self.color[0])
        g.setMinimum(0)
        g.setMaximum(255)
        g.setValue(self.color[1])
        b.setMinimum(0)
        b.setMaximum(255)
        b.setValue(self.color[2])

        def change():
            self.color = [r.value(),g.value(),b.value()]
            label.setStyleSheet('background-color:rgb%s;'%str(tuple(self.color)))
            self.color_btn.setStyleSheet('background-color:rgb%s'%str(tuple(self.color)))
        r.valueChanged.connect(change)
        g.valueChanged.connect(change)
        b.valueChanged.connect(change)

        dl.exec_()
    def get_position(self,event):
        self.x = event.x()
        self.y = event.y()
        self.pos[-1].append([self.x,self.y])
    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setPen(QPen(QColor(40,40,40),10))
        for t in self.pos:
            qp.setPen(QPen(QColor(t[0][0],t[0][1],t[0][2]),t[1]))
            if len(t) > 3:
                for i in range(2,len(t)-1):
                    x,y = t[i]
                    x1,y1 = t[i+1]
                    qp.drawPoint(x,y)
                    qp.drawLine(x,y,x1,y1)
        # 刷新页面
        self.update()

# 创建窗口的主程序
app = QApplication(sys.argv)
d = Draw_line()
d.init()
d.show()
app.exec_()        
