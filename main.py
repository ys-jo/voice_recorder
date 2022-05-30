import sys
import numpy as np
import time
import os

# PyQt5
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QPushButton, QMainWindow, QFileDialog, \
    QProgressBar, QLabel, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread, QDate, Qt

# other src file
from record import record_process


# main program class
class program_exe(QMainWindow):
    def __init__(self):
        super().__init__()
        self.date = QDate.currentDate()
        # Thread
        self.Timer_thread = Thread_timer(self)

        self.label_inform = 0
        self.progress_bar = QProgressBar(self)
        self.time = QLabel("0:00", self)

        # button
        self.btn_record = QPushButton('Record', self)
        self.btn_listen = QPushButton('Listen', self)
        self.btn_save = QPushButton('Save', self)

        # Init UI
        self.initUI()
        self.record_process = record_process(self)

    def initUI(self):

        # status Bar
        self.statusBar().showMessage(self.date.toString(Qt.DefaultLocaleLongDate))

        # Label for text
        label_log = QLabel("log: ", self)
        label_log.move(30, 300)
        font = label_log.font()
        font.setPointSize(10)
        font.setFamily('나눔손글씨 붓')
        font.setBold(True)
        label_log.setFont(font)
        self.label_inform = QLabel(self)
        self.label_inform.move(60, 300)
        self.label_inform.resize(300,30)
        self.label_inform.setFont(font)
        label_main = QLabel("2초간 녹음 프로그램", self)
        label_main.move(30, 20)
        label_main.setFont(font)
        label_main.resize(300,20)

        # button for record, listen, save
        self.btn_record.setToolTip('This is a <b>record</b> button')
        self.btn_record.setStyleSheet("background-color: khaki;font-size:30px;font-family:나눔손글씨 붓;");
        self.btn_record.move(450, 30)
        self.btn_record.resize(150, 80)
        self.btn_record.clicked.connect(self.record)

        self.btn_listen.setToolTip('This is a <b>listen</b> button')
        self.btn_listen.setStyleSheet("background-color: khaki;font-size:30px;font-family:나눔손글씨 붓;");
        self.btn_listen.move(450, 140)
        self.btn_listen.resize(150, 80)
        self.btn_listen.clicked.connect(self.listen)

        self.btn_save.setToolTip('This is a <b>save</b> button')
        self.btn_save.setStyleSheet("background-color: khaki;font-size:30px;font-family:나눔손글씨 붓;");
        self.btn_save.move(450, 250)
        self.btn_save.resize(150, 80)
        self.btn_save.clicked.connect(self.save)
        self.btn_save.setDisabled(True)
        self.btn_listen.setDisabled(True)

        # timer GUI & progress bar
        self.progress_bar.setGeometry(30, 60, 300, 30)

        self.time.move(30, 100)
        self.time.resize(400, 150)
        time_font = self.time.font()
        time_font.setPointSize(100)
        time_font.setFamily('나눔손글씨 붓')
        time_font.setBold(True)
        self.time.setFont(time_font)

        # for main GUI
        self.setWindowTitle('Voice Recorder program')
        try:
            # sys.MEIPASS is temp directory for pyinstaller
            icon_path = os.path.join(getattr(sys, '_MEIPASS'), "eyenix.ico")

        except Exception:
            icon_path = os.path.join(os.path.abspath("."), "eyenix.ico")

        self.setWindowIcon(QIcon(icon_path))
        self.setFixedSize(640, 360)  # 1 6:9 ratio
        self.setStyleSheet("background:beige")
        self.center()
        self.show()

    def update_canvas(self):
        self.dynamic_ax.clear()
        t = np.linspace(0, 2 * np.pi, 101)
        self.dynamic_ax.plot(t, np.sin(t + time.time()), color='deeppink')
        self.dynamic_ax.figure.dynamic_canvas.draw()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # for record, listen, save
    def record(self):
        self.record_process.record()

    def listen(self):
        self.record_process.listen()

    def save(self):
        filename = QFileDialog.getSaveFileName(self, 'Save file', './', 'wav File(*.wav)')
        self.record_process.save(filename)

    def button_disable(self):
        self.btn_save.setDisabled(True)
        self.btn_listen.setDisabled(True)
        self.btn_record.setDisabled(True)

    def button_enable(self):
        self.btn_save.setEnabled(True)
        self.btn_listen.setEnabled(True)
        self.btn_record.setEnabled(True)

    def closeEvent(self, event):
        quit_msg = "Want to exit?"
        reply = QMessageBox.question(self, 'Message', quit_msg, QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.record_process.delete_tmp_file()
            event.accept()
        else:
            event.ignore()

# for thread
class Thread_timer(QThread):
    def __init__(self, arg):
        super().__init__()
        self.arg = arg
        self.th_run = False
        self.step = 0
        self.start_time = 0
        self.end_time = 0

    def run(self):
        self.arg.button_disable()
        self.th_run = True
        self.start_time = time.time()
        self.step = 0
        self.arg.progress_bar.setValue(0)
        while self.th_run:
            self.end_time = time.time()
            timer = round(self.end_time - self.start_time, 2)
            if timer > 1.9:
                timer = "2:00"
                self.arg.time.setText(str(timer).replace(".", ":"))
                self.arg.time.repaint()
                self.arg.progress_bar.setValue(100)
            else:
                self.arg.time.setText(str(timer).replace(".", ":"))
                self.arg.time.repaint()
                self.arg.progress_bar.setValue(int((self.end_time - self.start_time) * 50))

    def stop(self):
        self.arg.button_enable()
        self.th_run = False
        self.quit()
        self.wait(1000)


# PyQt5
if __name__ == "__main__":
    app = QApplication(sys.argv)
    program = program_exe()
    program.show()
    sys.exit(app.exec_())
