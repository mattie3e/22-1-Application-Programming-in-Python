import sys
import datetime
import calendar
import random
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QPoint
from PyQt5 import QtCore
from PyQt5 import uic
import sqlite3
import re
import numpy as np
import pyqtgraph as pg
import seaborn as sns
from PyQt5 import QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.ticker as mticker
from custom import practice as p

form_class = uic.loadUiType("main.ui")[0]

now = datetime.datetime.now()
calendar.setfirstweekday(calendar.SUNDAY)


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self):
        fig = Figure()
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MyWindow(QMainWindow, form_class):
    current_month: int = now.month
    current_year: int = now.year
    print(current_month)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.ChangeDay(self.current_month)
        self.ChangeMonth(self.current_month)
        self.change_spend()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.center()
        self.oldPos = self.pos()

        # CALENDAR
        self.Btn_Toggle.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_1))

        # ASSIGNMENT
        self.btn_page_2.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_2))

        # ACCOUNT BOOK
        self.btn_page_3.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_3))
        self.btn_page_3.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.graph_show()))

        # HEALTH MANAGEMENT
        self.btn_page_4.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_4))

        # close, minimize, fullscreen
        def min_fuc():
            self.showMinimized()

        def full_fuc():
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()

        self.btn_close.clicked.connect(QApplication.instance().quit)
        self.btn_min.clicked.connect(lambda: min_fuc())
        self.btn_max.clicked.connect(lambda: full_fuc())

        self.lastmonth.clicked.connect(lambda: self.ChangeMonth(self.current_month - 1))  # 나중에 현재 (달력에 표시된)달 - 1 로 바꾸기
        self.nextmonth.clicked.connect(lambda: self.ChangeMonth(self.current_month + 1))  # 나중에 현재 (달력에 표시된)달 + 1 로 바꾸기

        self.days = [self.day1, self.day2, self.day3, self.day4, self.day5, self.day6, self.day7, self.day8, self.day9,
                     self.day10, self.day11, self.day12, self.day13, self.day14, self.day15, self.day16, self.day17,
                     self.day18, self.day19, self.day20, self.day21, self.day22, self.day23, self.day24, self.day25,
                     self.day26, self.day27, self.day28, self.day29, self.day30, self.day31, self.day32, self.day33,
                     self.day34, self.day35]

        self.frames = [self.planframe1, self.planframe2, self.planframe3, self.planframe4, self.planframe5,
                       self.planframe6,
                       self.planframe7, self.planframe8, self.planframe9, self.planframe10, self.planframe11,
                       self.planframe12,
                       self.planframe13, self.planframe14, self.planframe15, self.planframe16, self.planframe17,
                       self.planframe18,
                       self.planframe19, self.planframe20, self.planframe21, self.planframe22, self.planframe23,
                       self.planframe24,
                       self.planframe25, self.planframe26, self.planframe27, self.planframe28, self.planframe29,
                       self.planframe30,
                       self.planframe31, self.planframe32, self.planframe33, self.planframe34, self.planframe35]

        for i in self.days:
            i.clicked.connect(lambda: self.addItem(self.gettext(), int(re.sub(r'\D', '', i.objectName())) - 1))

    def getFrame(self):
        return self.frames

    def gettext(self):
        print(self.sender().text())
        return self.sender().text()

    # page2 graph
    def graph_show(self):
        self.sc = MplCanvas()
        self.drawGraph()

        for j in range(self.graphcanvas.layout().count()):
            self.graphcanvas.layout().itemAt(j).widget().deleteLater()

        self.graphcanvas.layout().addWidget(self.sc)

    def drawGraph(self):
        x = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
             '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30']
        height = [0, 0, 31640, 0, 33115 + 50000, 23300/1000, 0, 0, 0, 0, 0, 0, 5000 + 5000, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.sc.axes.barh(x, height, color='pink')
        self.sc.draw()

    def change_spend(self):
        con = sqlite3.connect("E:\-\\2022-1\파이썬\CALENDAR\\test_DB.db")
        cur = con.cursor()
        m_spend = []
        if self.current_month == 13:
            cur_m = 1
        elif self.current_month == 0:
            cur_m = 12
        else:
            cur_m = self.current_month

        for row in cur.execute("SELECT spend FROM m" + str(cur_m)):
            if row[0] != None and row[0] != '':
                m_spend.append(int(row[0]))
        print(m_spend)
        self.totalspend.setText("total | " + str(format(sum(m_spend), ',')))

        return sum(m_spend)

    def addItem(self, day, i):
        window2 = addWindow(self.current_year, self.current_month, day, i)
        window2.exec_()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def printCurmonth(self):
        print(self.current_month, self.current_year)

    def ChangeMonth(self, curmonth):  # plan label 변경 / 나중에 SQL 에서 불러 오기 추가
        self.current_month = curmonth
        self.printCurmonth()
        self.sum_spend = self.change_spend()
        if curmonth == 1:
            self.month_year.setText("January " + str(self.current_year))
            self.ChangeDay(1)

        if curmonth == 2:
            self.month_year.setText("February " + str(self.current_year))
            self.ChangeDay(2)

        if curmonth == 3:
            self.month_year.setText("March " + str(self.current_year))
            self.ChangeDay(3)

        if curmonth == 4:
            self.month_year.setText("April " + str(self.current_year))
            self.ChangeDay(4)

        if curmonth == 5:
            self.month_year.setText("May " + str(self.current_year))
            self.ChangeDay(5)

        if curmonth == 6:
            self.month_year.setText("June " + str(self.current_year))
            self.ChangeDay(6)

        if curmonth == 7:
            self.month_year.setText("July " + str(self.current_year))
            self.ChangeDay(7)

        if curmonth == 8:
            self.month_year.setText("August " + str(self.current_year))
            self.ChangeDay(8)

        if curmonth == 9:
            self.month_year.setText("September " + str(self.current_year))
            self.ChangeDay(9)

        if curmonth == 10:
            self.month_year.setText("October " + str(self.current_year))
            self.ChangeDay(10)

        if curmonth == 11:
            self.month_year.setText("November " + str(self.current_year))
            self.ChangeDay(11)

        if curmonth == 12:
            self.month_year.setText("December " + str(self.current_year))
            self.ChangeDay(12)

        if curmonth == 0:  # 나중에 2021년, 2023년 등으로 넘어 가기 작성
            self.current_month = 12
            self.current_year -= 1
            self.ChangeMonth(self.current_month)

        if curmonth == 13:
            self.current_month = 1
            self.current_year += 1
            self.ChangeMonth(self.current_month)

    def ChangeDay(self, month):
        days = [self.day1, self.day2, self.day3, self.day4, self.day5, self.day6, self.day7, self.day8, self.day9,
                self.day10, self.day11, self.day12, self.day13, self.day14, self.day15, self.day16, self.day17,
                self.day18, self.day19, self.day20, self.day21, self.day22, self.day23, self.day24, self.day25,
                self.day26, self.day27, self.day28, self.day29, self.day30, self.day31, self.day32, self.day33,
                self.day34, self.day35]
        d = 1
        start = (calendar.weekday(self.current_year, month, 1) + 1) % 7
        print(start)
        for i in range(35):
            # 첫 시작 요일만 잡아서 순서 대로 출력/2월 윤년, 30, 31일 구현
            if i >= start and d <= 31:
                days[i].setText(str(d))
                self.chg_dayLabel(d, i)
                d += 1
                if month == 6 and d == 31:
                    break
            else:
                days[i].setText(str(' '))

    def chg_dayLabel(self, day, i):
        frames = [self.planframe1, self.planframe2, self.planframe3, self.planframe4, self.planframe5, self.planframe6,
                  self.planframe7, self.planframe8, self.planframe9, self.planframe10, self.planframe11,
                  self.planframe12,
                  self.planframe13, self.planframe14, self.planframe15, self.planframe16, self.planframe17,
                  self.planframe18,
                  self.planframe19, self.planframe20, self.planframe21, self.planframe22, self.planframe23,
                  self.planframe24,
                  self.planframe25, self.planframe26, self.planframe27, self.planframe28, self.planframe29,
                  self.planframe30,
                  self.planframe31, self.planframe32, self.planframe33, self.planframe34, self.planframe35]
        con = sqlite3.connect("E:\-\\2022-1\파이썬\CALENDAR\\test_DB.db")
        cur = con.cursor()
        plan = []

        if self.current_month == 13:
            cur_m = 1
        elif self.current_month == 0:
            cur_m = 12
        else:
            cur_m = self.current_month

        for row in cur.execute("SELECT date, schedule FROM m" + str(cur_m)):
            if row[0] == day and row[1] is not None and row[1] != '':
                plan.append(row[1])
            if len(plan) == 3:
                break

        for j in range(frames[i].layout().count()):
            frames[i].layout().itemAt(j).widget().deleteLater()

        print(plan)

        fst = "rgb(255, 220, 221)"
        sec = "rgb(220, 224, 255)"
        thr = "rgb(255, 230, 178)"

        color = [fst, sec, thr]

        for p in plan:
            self.label = QLabel(p)
            self.label.setMaximumHeight(25)
            self.label.setAlignment(QtCore.Qt.AlignCenter)
            frames[i].layout().addWidget(self.label)
            self.label.setStyleSheet("background-color:" + random.choice(color) + ";")


class addWindow(QDialog):
    def __init__(self, year, month, day, index):
        super().__init__()
        self.ui = uic.loadUi("E:\-\\2022-1\파이썬\CALENDAR\\additem.ui", self)
        self.show()
        self.cur_day.setText(str(year) + "-" + str(month) + "-" + day)

        self.schedule.returnPressed.connect(lambda: self.makeLabel(self.schedule.text(), month, day, index))
        self.todo.returnPressed.connect(lambda: self.makeLabel(self.schedule.text(), month, day, index))

    def makeLabel(self, text, month, day, index):
        # 만약 edit box 에서 enter 이벤트 발생 시 label 추가로 생성
        frames = myWindow.getFrame()

        self.label = QLabel(text)
        self.label.setMinimumHeight(30)
        self.label.setMaximumHeight(30)
        self.schedule_contents.layout().addWidget(self.label)
        self.label.setStyleSheet("background-color: white;"
                                 "border-radius: 3px;"
                                 "color: rgb(65, 65, 65)")

        con = sqlite3.connect("E:\-\\2022-1\파이썬\CALENDAR\\test_DB.db")
        cur = con.cursor()
        contents = [day, text, None, None]
        cur.execute('INSERT INTO m' + str(month) + ' (date, schedule, todo, spend) VALUES(?, ?, ?, ?)', contents)
        con.commit()
        con.close()


if __name__ == "__main__":
    # p.app = QApplication(sys.argv)
    # welcome = p.WelcomeScreen()
    # widget = QStackedWidget()
    # widget.addWidget(welcome)
    # widget.show()

    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
