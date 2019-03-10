# -*- coding: utf-8 -*-

# Created by: PyQt5 UI code generator 5.11.3


from PyQt5 import QtCore, QtGui, QtWidgets
from googletrans import Translator
import time

class Ui_MainWindow(object):

    #--Gelobal Variable--#
    isThreadRun = False
    curent_text = ""
    #--------------------#

    #start timer thread
    def __init__(self):
        self.Worker=Timer_Thread()
        self.Worker_Thread=QtCore.QThread()
        self.Worker_Thread.started.connect(self.Worker.run)
        self.Worker.SignalTimer.connect(self.Handel)
        self.Worker.moveToThread(self.Worker_Thread)
        self.Worker_Thread.start()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(819, 302)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.tabWidgetOrgianl = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidgetOrgianl.setObjectName("tabWidgetOrgianl")
        self.tabDetect = QtWidgets.QWidget()
        self.tabDetect.setAccessibleName("")
        self.tabDetect.setObjectName("tabDetect")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.tabDetect)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.txtEditOrginDetect = QtWidgets.QPlainTextEdit(self.tabDetect)
        self.txtEditOrginDetect.setObjectName("txtEditOrginDetect")
        self.horizontalLayout_3.addWidget(self.txtEditOrginDetect)
        self.tabWidgetOrgianl.addTab(self.tabDetect, "")
        self.horizontalLayout_5.addWidget(self.tabWidgetOrgianl)
        self.tabWidgetTranslate = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidgetTranslate.setObjectName("tabWidgetTranslate")
        self.tabTranslateEnglish = QtWidgets.QWidget()
        self.tabTranslateEnglish.setObjectName("tabTranslateEnglish")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.tabTranslateEnglish)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.txtEditTranslateEnglish = QtWidgets.QPlainTextEdit(self.tabTranslateEnglish)
        self.txtEditTranslateEnglish.setObjectName("txtEditTranslateEnglish")
        self.horizontalLayout_4.addWidget(self.txtEditTranslateEnglish)
        self.tabWidgetTranslate.addTab(self.tabTranslateEnglish, "")
        self.tabTranslatePersian = QtWidgets.QWidget()
        self.tabTranslatePersian.setObjectName("tabTranslatePersian")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.tabTranslatePersian)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.txtEditTranslatePersian = QtWidgets.QPlainTextEdit(self.tabTranslatePersian)
        self.txtEditTranslatePersian.setObjectName("txtEditTranslatePersian")
        self.horizontalLayout.addWidget(self.txtEditTranslatePersian)
        self.tabWidgetTranslate.addTab(self.tabTranslatePersian, "")
        self.horizontalLayout_5.addWidget(self.tabWidgetTranslate)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidgetOrgianl.setCurrentIndex(0)
        self.tabWidgetTranslate.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Google Translate"))
        self.tabWidgetOrgianl.setTabText(self.tabWidgetOrgianl.indexOf(self.tabDetect), _translate("MainWindow", "Detect Language"))
        self.tabWidgetTranslate.setTabText(self.tabWidgetTranslate.indexOf(self.tabTranslateEnglish), _translate("MainWindow", "English"))
        self.tabWidgetTranslate.setTabText(self.tabWidgetTranslate.indexOf(self.tabTranslatePersian), _translate("MainWindow", "Persian"))

#------------------------------ my methodes ---------------------------#
    def Handel(self):
        text = self.txtEditOrginDetect.toPlainText()
        if not self.isThreadRun and text != self.curent_text:
            if self.tabWidgetTranslate.currentIndex() == 1 :
                dest = 'fa'
            else:
                dest = 'en'
            self.RunThread(dest,text)
            self.curent_text=text
        else:
            pass

    def RunThread(self,dest,wrd):
        self.isThreadRun = True

        self.MainThread=Translate_Thread(destLang=dest,word=wrd)
        self.Main_Thread=QtCore.QThread()
        self.Main_Thread.started.connect(self.MainThread.run)
        self.MainThread.SignalTranslate.connect(self.SetTranslate)
        self.MainThread.moveToThread(self.Main_Thread)
        self.Main_Thread.start()

    def SetTranslate(self,text,dest):
        self.Main_Thread.quit()
        self.isThreadRun = False
        if dest == 'fa':
            self.txtEditTranslatePersian.setPlainText(text)
        elif dest == 'en':
            self.txtEditTranslateEnglish.setPlainText(text)
    #---------------------------------------------------------------------#


    #------------------------------ my classes -----------------------------#
class Timer_Thread(QtCore.QObject):
    SignalTimer = QtCore.pyqtSignal()
    def __init__(self):
        super().__init__()

    @QtCore.pyqtSlot()
    def run(self):
        while True:
            time.sleep(.7)
            self.SignalTimer.emit()

class Translate_Thread(QtCore.QObject):
    SignalTranslate = QtCore.pyqtSignal(str,str)
    translator = Translator()
    def __init__(self,word,destLang):
        super().__init__()
        self.word = word
        self.destLang = destLang

    @QtCore.pyqtSlot()
    def run(self):
        if self.destLang == 'fa':
            r = self.Translat()
            self.SignalTranslate.emit(r.text,'fa')
        elif self.destLang == 'en':
            r = self.Translat()
            self.SignalTranslate.emit(r.text,'en')

    def Translat(self):
        try:
            return self.translator.translate(self.word,dest=self.destLang)
        except:
            return "We have some error to translate,this is not good :("
    #---------------------------------------------------------------------#
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
