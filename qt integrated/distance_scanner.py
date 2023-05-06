from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtMultimedia
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtMultimedia import QSound
import sys
import time
import serial

class MyWindow(QMainWindow):
    def __init__(self):
        # Initializeds stuff!
        self.thread={}
        super(MyWindow,self).__init__()
        self.initUI()

    def initUI(self):
        
        # Creates the window.
        self.setGeometry(760,200,300,170)
        # self.setStyleSheet("background: brown;") 
        self.setWindowTitle("Screech Prank 9000")
        # Creates a label.
        self.label = QtWidgets.QLabel(self)
        self.label.setText("Let the scare commence!")
        self.label.setStyleSheet("border: 1px solid black; background: pink;") 
        self.label.setGeometry(65, 20, 170, 40)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        # Creates a button.
        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText("Click to begin haunting.")
        self.b1.clicked.connect(self.begin_scan)
        self.b1.setGeometry(50, 70, 200, 40)

        self.b2 = QtWidgets.QPushButton(self)
        self.b2.setText("Test your fate.")
        self.b2.clicked.connect(self.pause_scan)
        self.b2.setGeometry(50, 110, 200, 40)
        self.b2.setDisabled(True)
   
    def begin_scan(self):
        self.thread[1] = ThreadClass(parent=None,index=1)
        self.thread[1].start()
        self.b1.setText("There's no going back now!")
        self.b2.setText("Click to end scan.")
        self.b1.setEnabled(False)
        self.b2.setEnabled(True)
        try: 
            self.thread[1].any_signal.connect(self.my_function)
        except:
            self.label.setText("Failed to launch the scanner!")
        

    def pause_scan(self):
        self.b1.setText("Click to begin scan.")
        self.b2.setText("Ceasefire...")
        try:
            self.thread[1].stop()
        except:
            print("No scream, not commenced.")
        self.b1.setDisabled(False)
        self.b2.setDisabled(True)
        
    def my_function(self,counter):
        
        index = self.sender().index
        if index == 1:
            QSound.play("scream.wav")


        
class ThreadClass(QtCore.QThread):

    any_signal = QtCore.pyqtSignal(int)
    
    def __init__(self, parent=None,index=0):
        super(ThreadClass, self).__init__(parent)
        self.index=index
        self.is_running = True
    def run(self):
        # sound_file = 'scream.mp3'
        # sound = QtMultimedia.QSound(sound_file)
        # sound.play()
        print('Starting thread...',self.index)  
        while (True):
            try:
                arduino = serial.Serial("/dev/cu.usbmodem14201",timeout=1)
                line=str(arduino.readline())
                print(line[2:-5])
                if "BEEP" in line:
                    self.any_signal.emit(1)
                    time.sleep(10)
            except:
                print('Please check the port')
                break
    def stop(self):
        self.is_running = False
        print('Stopping thread...',self.index)
        self.terminate()

# Creates a window with properties to close.
def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())
    
# Starts the program.
window()