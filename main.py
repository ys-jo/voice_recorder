import sys
import numpy as np
import time
import os

# PyQt5
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QPushButton, QMainWindow, QFileDialog, \
    QProgressBar, QLabel, QMessageBox, QCheckBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QThread, QDate, Qt, pyqtSlot

# other src file
from record import record_process


# main program class
class program_exe(QMainWindow):
    def __init__(self):
        super().__init__()
        #A@@@
        self.record_time = 0
        self.listen_time = 0

        self.date = QDate.currentDate()
        self.save_dir = "./"
        # Thread
        self.Timer_thread = Thread_timer(self)

        self.label_inform = 0
        self.progress_bar = QProgressBar(self)
        self.time = QLabel("0:00", self)
        self.label = QLabel(self)
        # button
        self.btn_record = QPushButton('Record', self)
        self.btn_listen = QPushButton('Listen', self)
        self.btn_dir = QPushButton('Set save dir', self)
        self.time_check_1 = QCheckBox('time 1 Sec', self)
        self.time_check_2 = QCheckBox('time 2 Sec', self)
        self.btn_save_1 = QPushButton('사진찍어(2초)', self)
        self.btn_save_2 = QPushButton('전원꺼(2초)', self)
        self.btn_save_3 = QPushButton('전원켜(2초)', self)
        self.btn_save_4 = QPushButton('조명꺼(2초)', self)
        self.btn_save_5 = QPushButton('조명켜(2초)', self)
        self.btn_save_6 = QPushButton('조명밝게(2초)', self)
        self.btn_save_7 = QPushButton('조명어둡게(2초)', self)
        self.btn_save_8 = QPushButton('딤채(1초)', self)
        self.btn_save_9 = QPushButton('팜인홈(1초)', self)
        self.btn_save_10 = QPushButton('위니야(1초)', self)
        self.btn_save_11 = QPushButton('돌체(1초)', self)
        self.btn_save_12 = QPushButton('딤채야(1초)', self)
        # self.dir = "./"

        # Init UI
        self.initUI()
        self.record_process = record_process(self, time=1)

    def initUI(self):

        # status Bar
        self.statusBar().showMessage(self.date.toString(Qt.DefaultLocaleLongDate))

        # Label for text
        label_log = QLabel("log: ", self)
        label_log.move(30, 300)
        label_save = QLabel("Save button", self)
        label_save.move(600, 5)
        font_save = label_log.font()
        font_save.setPointSize(20)
        font_save.setFamily('나눔손글씨 붓')
        font_save.setBold(True)
        font = label_log.font()
        font.setPointSize(10)
        font.setFamily('나눔손글씨 붓')
        font.setBold(True)
        label_log.setFont(font)
        label_save.setFont(font_save)
        label_save.resize(200,20)
        self.label_inform = QLabel(self)
        self.label_inform.move(60, 300)
        self.label_inform.resize(300,30)
        self.label_inform.setFont(font)
        label_main = QLabel("1초 or 2초 녹음 프로그램", self)
        label_main.move(30, 20)
        label_main.setFont(font)
        label_main.resize(300,20)

        # button for record, listen, save

        self.btn_dir.setToolTip('This is a <b>set save dir</b> button')
        self.btn_dir.setStyleSheet("background-color: khaki;font-size:30px;font-family:나눔손글씨 붓;");
        self.btn_dir.move(30, 350)
        self.btn_dir.resize(200, 80)
        self.btn_dir.clicked.connect(self.get_dir)


        self.btn_record.setToolTip('This is a <b>record</b> button')
        self.btn_record.setStyleSheet("background-color: khaki;font-size:30px;font-family:나눔손글씨 붓;");
        self.btn_record.move(380, 30)
        self.btn_record.resize(150, 80)
        self.btn_record.clicked.connect(self.record)

        self.btn_listen.setToolTip('This is a <b>listen</b> button')
        self.btn_listen.setStyleSheet("background-color: khaki;font-size:30px;font-family:나눔손글씨 붓;");
        self.btn_listen.move(380, 140)
        self.btn_listen.resize(150, 80)
        self.btn_listen.clicked.connect(self.listen)

        self.time_check_1.move(380, 230)
        self.time_check_2.move(380, 260)
        self.time_check_1.toggle()
        self.time_check_1.clicked.connect(self.checkbox_toggled1)
        self.time_check_2.clicked.connect(self.checkbox_toggled2)

        self.btn_save_1.setToolTip('This is a <b>사진 찍어</b> button')
        self.btn_save_1.setStyleSheet("background-color: khaki;font-size:15px;font-family:나눔손글씨 붓;");
        self.btn_save_1.move(570, 40)
        self.btn_save_1.resize(110, 50)
        self.btn_save_1.clicked.connect(lambda: self.save("take_picture"))

        self.btn_save_2.setToolTip('This is a <b>전원 꺼</b> button')
        self.btn_save_2.setStyleSheet("background-color: khaki;font-size:15px;font-family:나눔손글씨 붓;");
        self.btn_save_2.move(700, 40)
        self.btn_save_2.resize(110, 50)
        self.btn_save_2.clicked.connect(lambda: self.save("trun_off"))

        self.btn_save_3.setToolTip('This is a <b>전원 켜</b> button')
        self.btn_save_3.setStyleSheet("background-color: khaki;font-size:15px;font-family:나눔손글씨 붓;");
        self.btn_save_3.move(570, 110)
        self.btn_save_3.resize(110, 50)
        self.btn_save_3.clicked.connect(lambda: self.save("turn_on"))

        self.btn_save_4.setToolTip('This is a <b>조명 꺼</b> button')
        self.btn_save_4.setStyleSheet("background-color: khaki;font-size:15px;font-family:나눔손글씨 붓;");
        self.btn_save_4.move(700, 110)
        self.btn_save_4.resize(110, 50)
        self.btn_save_4.clicked.connect(lambda: self.save("light_off"))

        self.btn_save_5.setToolTip('This is a <b>조명 켜</b> button')
        self.btn_save_5.setStyleSheet("background-color: khaki;font-size:15px;font-family:나눔손글씨 붓;");
        self.btn_save_5.move(570, 180)
        self.btn_save_5.resize(110, 50)
        self.btn_save_5.clicked.connect(lambda: self.save("light_on"))

        self.btn_save_6.setToolTip('This is a <b>조명 밝게</b> button')
        self.btn_save_6.setStyleSheet("background-color: khaki;font-size:15px;font-family:나눔손글씨 붓;");
        self.btn_save_6.move(700, 180)
        self.btn_save_6.resize(110, 50)
        self.btn_save_6.clicked.connect(lambda: self.save("light_up_bright"))

        self.btn_save_7.setToolTip('This is a <b>조명 어둡게</b> button')
        self.btn_save_7.setStyleSheet("background-color: khaki;font-size:15px;font-family:나눔손글씨 붓;");
        self.btn_save_7.move(570, 250)
        self.btn_save_7.resize(110, 50)
        self.btn_save_7.clicked.connect(lambda: self.save("dim_the_light"))

        self.btn_save_8.setToolTip('This is a <b>딤채</b> button')
        self.btn_save_8.setStyleSheet("background-color: khaki;font-size:15px;font-family:나눔손글씨 붓;");
        self.btn_save_8.move(700, 250)
        self.btn_save_8.resize(110, 50)
        self.btn_save_8.clicked.connect(lambda: self.save("dimchae"))

        self.btn_save_9.setToolTip('This is a <b>팜인홈</b> button')
        self.btn_save_9.setStyleSheet("background-color: khaki;font-size:15px;font-family:나눔손글씨 붓;");
        self.btn_save_9.move(570, 320)
        self.btn_save_9.resize(110, 50)
        self.btn_save_9.clicked.connect(lambda: self.save("farm_in_home"))

        self.btn_save_10.setToolTip('This is a <b>위니아</b> button')
        self.btn_save_10.setStyleSheet("background-color: khaki;font-size:15px;font-family:나눔손글씨 붓;");
        self.btn_save_10.move(700, 320)
        self.btn_save_10.resize(110, 50)
        self.btn_save_10.clicked.connect(lambda: self.save("winia"))

        self.btn_save_11.setToolTip('This is a <b>돌체</b> button')
        self.btn_save_11.setStyleSheet("background-color: khaki;font-size:15px;font-family:나눔손글씨 붓;");
        self.btn_save_11.move(570, 390)
        self.btn_save_11.resize(110, 50)
        self.btn_save_11.clicked.connect(lambda: self.save("dolce"))

        self.btn_save_12.setToolTip('This is a <b>딤채야</b> button')
        self.btn_save_12.setStyleSheet("background-color: khaki;font-size:15px;font-family:나눔손글씨 붓;");
        self.btn_save_12.move(700, 390)
        self.btn_save_12.resize(110, 50)
        self.btn_save_12.clicked.connect(lambda: self.save("dimchae_ya"))


        self.btn_listen.setDisabled(True)
        self.btn_save_1.setDisabled(True)
        self.btn_save_2.setDisabled(True)
        self.btn_save_3.setDisabled(True)
        self.btn_save_4.setDisabled(True)
        self.btn_save_5.setDisabled(True)
        self.btn_save_6.setDisabled(True)
        self.btn_save_7.setDisabled(True)
        self.btn_save_8.setDisabled(True)
        self.btn_save_9.setDisabled(True)
        self.btn_save_10.setDisabled(True)
        self.btn_save_11.setDisabled(True)
        self.btn_save_12.setDisabled(True)

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
        try:
            # sys.MEIPASS is temp directory for pyinstaller
            cat_path = os.path.join(getattr(sys, '_MEIPASS'), "cat.png")

        except Exception:
            cat_path = os.path.join(os.path.abspath("."), "cat.png")
        image = QPixmap(cat_path)
        image = image.scaledToHeight(250)
        image = image.scaledToWidth(220)
        # self.label = QLabel(self)
        self.label.setPixmap(image)
        self.label.setGeometry(340, 230, 220, 250)

        #btn disable
        self.button_disable()
        self.setWindowIcon(QIcon(icon_path))
        self.setFixedSize(830, 480)  # 1 6:9 ratio    + 190  -> 640 -> 830
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
        self.record_time = 1
        self.listen_time = 0
        if self.time_check_2.isChecked():
            self.record_process.record(2)
        else:
            self.record_process.record(1)

    def listen(self):
        self.listen_time = 1
        self.record_process.listen()

    def checkbox_toggled1(self):
        if self.time_check_1.isChecked():
            if self.time_check_2.isChecked():
                self.time_check_2.toggle()
        else:
            if not self.time_check_2.isChecked():
                self.time_check_2.toggle()

    def checkbox_toggled2(self):
        if self.time_check_2.isChecked():
            if self.time_check_1.isChecked():
                self.time_check_1.toggle()
        else:
            if not self.time_check_1.isChecked():
                self.time_check_1.toggle()

    def save(self, arg):
        #make dir
        if not os.path.isdir(self.save_dir):
            os.mkdir(self.save_dir)
        # print(self.save_dir+arg)
        i = 1
        filename = self.save_dir + arg + ".wav"
        while(True):
            if not os.path.isfile(filename):
                break
            else:
                filename = self.save_dir+arg+str(i)+".wav"
                # print(filename)
                i += 1
        # filename = QFileDialog.getSaveFileName(self, 'Save file', self.dir, 'wav File(*.wav)')
        # self.dir = '/'.join(filename[0].split('/')[:-1])
        self.record_process.save(filename)
        self.record_time = 0
        self.listen_time = 0

    def get_dir(self):
        self.save_dir = str(QFileDialog.getExistingDirectory(self, "Select Directory"))+"/"
        # print(self.save_dir)
        self.btn_record.setEnabled(True)

    def button_disable(self):
        self.btn_listen.setDisabled(True)
        self.btn_record.setDisabled(True)
        self.btn_save_1.setDisabled(True)
        self.btn_save_2.setDisabled(True)
        self.btn_save_3.setDisabled(True)
        self.btn_save_4.setDisabled(True)
        self.btn_save_5.setDisabled(True)
        self.btn_save_6.setDisabled(True)
        self.btn_save_7.setDisabled(True)
        self.btn_save_8.setDisabled(True)
        self.btn_save_9.setDisabled(True)
        self.btn_save_10.setDisabled(True)
        self.btn_save_11.setDisabled(True)
        self.btn_save_12.setDisabled(True)

    def button_disable_2(self):
        self.btn_save_1.setDisabled(True)
        self.btn_save_2.setDisabled(True)
        self.btn_save_3.setDisabled(True)
        self.btn_save_4.setDisabled(True)
        self.btn_save_5.setDisabled(True)
        self.btn_save_6.setDisabled(True)
        self.btn_save_7.setDisabled(True)
        self.btn_save_8.setDisabled(True)
        self.btn_save_9.setDisabled(True)
        self.btn_save_10.setDisabled(True)
        self.btn_save_11.setDisabled(True)
        self.btn_save_12.setDisabled(True)

    def button_enable(self):
        self.btn_listen.setEnabled(True)
        self.btn_record.setEnabled(True)
        if self.record_time == 1 and self.listen_time == 1:
            self.btn_save_1.setEnabled(True)
            self.btn_save_2.setEnabled(True)
            self.btn_save_3.setEnabled(True)
            self.btn_save_4.setEnabled(True)
            self.btn_save_5.setEnabled(True)
            self.btn_save_6.setEnabled(True)
            self.btn_save_7.setEnabled(True)
            self.btn_save_8.setEnabled(True)
            self.btn_save_9.setEnabled(True)
            self.btn_save_10.setEnabled(True)
            self.btn_save_11.setEnabled(True)
            self.btn_save_12.setEnabled(True)

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
        self.time = 2

    def get_arg(self, arg):
        self.time = arg

    def run(self):
        self.arg.button_disable()
        self.th_run = True
        self.start_time = time.time()
        self.step = 0
        self.arg.progress_bar.setValue(0)
        while self.th_run:
            self.end_time = time.time()
            timer = round(self.end_time - self.start_time, 2)
            if self.time == 2:
                if timer > 1.9:
                    timer = "2:00"
                    self.arg.time.setText(str(timer).replace(".", ":"))
                    self.arg.time.repaint()
                    self.arg.progress_bar.setValue(100)
                else:
                    self.arg.time.setText(str(timer).replace(".", ":"))
                    self.arg.time.repaint()
                    self.arg.progress_bar.setValue(int((self.end_time - self.start_time) * 50))
            else:
                if timer > 0.9:
                    timer = "1:00"
                    self.arg.time.setText(str(timer).replace(".", ":"))
                    self.arg.time.repaint()
                    self.arg.progress_bar.setValue(100)
                else:
                    self.arg.time.setText(str(timer).replace(".", ":"))
                    self.arg.time.repaint()
                    self.arg.progress_bar.setValue(int((self.end_time - self.start_time) * 100))

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
