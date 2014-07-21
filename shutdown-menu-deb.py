#!/usr/bin/python
# -*- coding: utf-8 -*-
#Author: Bruno Expósito
#Contact: bruno.exposito@openmailbox.org
#License: GPL 3
#Original design: http://hxmarius.deviantart.com/art/Elementary-Shutdown-Dialog-Mockup-V2-359472999

import sys, os
from PyQt4 import QtCore
from PyQt4.QtGui import *


class HoverButton(QToolButton):
    def __init__(self, name="", parent=None):
        super(HoverButton, self).__init__(parent)
        self.setStyleSheet("background-image: url(" + absolutePath(name + ".png") + ");")
        self.setObjectName(name)
        self.setFixedSize(30,30) if name == 'close' else self.setFixedSize(110,104)

    def enterEvent(self,event):
        self.setStyleSheet("background-image: url(" + absolutePath(self.objectName() + "2.png") + ");")

    def leaveEvent(self,event):
        self.setStyleSheet("background-image: url(" + absolutePath(self.objectName() + ".png") + ");")

    def mousePressEvent(self, event):
        if self.objectName() == 'shutdown':
            run("/usr/bin/dbus-send --system --print-reply --dest='org.freedesktop.ConsoleKit' /org/freedesktop/ConsoleKit/Manager org.freedesktop.ConsoleKit.Manager.Stop")
        elif self.objectName() == 'restart':
            run("/usr/bin/dbus-send --system --print-reply --dest='org.freedesktop.ConsoleKit' /org/freedesktop/ConsoleKit/Manager org.freedesktop.ConsoleKit.Manager.Restart")
        elif self.objectName() == 'logout':
            run("pkill -u `whoami`")
        elif self.objectName() == 'lock':
            run("xset dpms force off")  
            QApplication.quit()
        else:
            QApplication.quit()
            

def main():    
    app = QApplication(sys.argv)
    w = QWidget()

    #Basic config
    w.setWindowTitle('Shutdown')
    w.resize(525, 148)
    w.setWindowIcon(QIcon(absolutePath("icon.png")))

    #Background
    background = QLabel(w)
    background.setGeometry(0, 0, 525, 148)
    background.setPixmap(QPixmap(absolutePath("background.png")))

    #Buttons
    shutdown=HoverButton("shutdown")        
    restart=HoverButton("restart")        
    logout=HoverButton("logout")        
    lock=HoverButton("lock")

    #Labels
    separator1 = QLabel()
    separator2 = QLabel()
    separator3 = QLabel()
    separator1.setPixmap(QPixmap(absolutePath("separator.png")))
    separator2.setPixmap(QPixmap(absolutePath("separator.png")))
    separator3.setPixmap(QPixmap(absolutePath("separator.png")))

    #Layout
    layout = QHBoxLayout()
    layout.addStretch()  
    layout.setContentsMargins(23,22,23,22)

    layout.addWidget(shutdown)
    layout.addWidget(separator1)
    layout.addWidget(restart)
    layout.addWidget(separator2)
    layout.addWidget(logout)
    layout.addWidget(separator3)
    layout.addWidget(lock)

    w.setLayout(layout)

    #Forever alone (button version)
    close = HoverButton("close", w)

    #Move the window at the center 
    w.move(QApplication.desktop().screen().rect().center()- w.rect().center())
    
    #Remove the borders, buttons, etc
    w.setWindowFlags(w.windowFlags() | QtCore.Qt.FramelessWindowHint)

    #Background transparent
    w.setAttribute(QtCore.Qt.WA_TranslucentBackground)

    #CSS
    QApplication.instance().setStyleSheet('QToolButton {border: none;}')

    w.show()
    sys.exit(app.exec_())

def absolutePath(myFile):
    return os.path.dirname(os.path.abspath(__file__)) + "/pictures/" + myFile

def run(command):
    return os.popen(command).read()

if __name__ == '__main__':
    main()
