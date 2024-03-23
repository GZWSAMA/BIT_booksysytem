# coding=GBK
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QMenuBar, QAction, \
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QFrame, QScrollArea, QTextEdit, \
    QPushButton, QMessageBox, QFileDialog, QSizePolicy
from PyQt5.QtGui import QFont, QIcon, QBrush, QPalette, QPixmap, QPainter
from PyQt5.QtCore import Qt, QSize


# �����û���
class User:
    def __init__(self, id, password):
        self.id = id
        self.password = password


# ������λ��
class Seat:
    def __init__(self, id, status):
        self.id = id
        self.status = status  # '��ԤԼ'��'δԤԼ'


# ����ԤԼģ��
class ReservationSystem:
    def __init__(self):
        # ��ʼ���û��б����λ�б�
        self.users = {'1120226666': {'password': '666666'}}
        self.seats = []
    def reserve_seat(self, user, seat_id):
        # �����λ�Ƿ���ò�����ԤԼ����
        pass

    def manage_seats(self, admin_user):
        # �ṩ����Ա�����ӿڣ��������λ״̬
        pass

    def authenticate(self, user_id, password):
        if user_id in self.users and self.users[user_id]['password'] == password:
            return True
        else:
            return False

    # ��������...

# GUIģ��
class StudyRoomReservationApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # ��ʼ��UI���
        self.init_ui()

        # ʵ����ԤԼϵͳ
        self.reservation_system = ReservationSystem()

    def init_ui(self):
        # ���������ڴ�С�ͱ���
        self.setGeometry(400, 200, 450, 800)
        self.setWindowTitle("��ϰ����λԤԼϵͳ")

        self.background_image = QPixmap('./images/2.jpg')

        # ����ͼƬ����Ӧ���ڴ�С������ԭͼ���������вü���
        newsize = QSize(int(self.background_image.width()), int(self.background_image.height()))
        self.scaled_bg = self.background_image.scaled(newsize, Qt.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
        # offset = ((self.width() - self.scaled_bg.width()) // 2, (self.height() - self.scaled_bg.height()) // 2)

        self.background_label = QLabel(self)
        self.background_label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.background_label.setPixmap(self.scaled_bg)
        self.background_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        # self.background_label.setScaledContents(True)  # �Զ�����ͼƬ����Ӧ��ǩ��С
        
        # ���ô��ڵ����벼��
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.background_label)
        self.setCentralWidget(central_widget)

        # �����˵���
        menu_bar = self.menuBar()

        # �������ļ����˵���
        file_menu = menu_bar.addMenu("������ϰ��ԤԼϵͳ")
        exit_action = QAction("�˳�", self)
        exit_action.triggered.connect(QApplication.quit)
        file_menu.addAction(exit_action)

        # ������¼����
        login_frame = QFrame(self)
        login_frame.setFrameShape(QFrame.StyledPanel)
        login_frame.setFrameShadow(QFrame.Raised)
        login_frame.setGeometry(10, 30, 430, 120)

        login_label = QLabel("ѧ��", login_frame)
        login_label.move(10, 25)
        login_label.setFont(QFont("Arial", 12, QFont.Bold))

        self.user_id_entry = QLineEdit(login_frame)
        self.user_id_entry.move(100, 20)
        self.user_id_entry.setFixedWidth(150)

        user_id_label = QLabel("����", login_frame)
        user_id_label.move(10, 55)
        user_id_label.setFont(QFont("Arial", 10))

        self.password_entry = QLineEdit(login_frame)
        self.password_entry.move(100, 50)
        self.password_entry.setFixedWidth(150)
        self.password_entry.setEchoMode(QLineEdit.Password)

        login_button = QPushButton("��¼", login_frame)
        login_button.move(280, 70)
        login_button.clicked.connect(self.on_login)

        # ������λչʾ����
        seat_display_frame = QFrame(self)
        seat_display_frame.setFrameShape(QFrame.StyledPanel)
        seat_display_frame.setFrameShadow(QFrame.Raised)
        seat_display_frame.setGeometry(10, 150, 430, 430)

        self.seat_display_text = QTextEdit(seat_display_frame)
        self.seat_display_text.setGeometry(10, 10, 390, 200)
        self.seat_display_text.setReadOnly(True)
        self.seat_display_text.setLineWrapMode(QTextEdit.NoWrap)

        scroll_area = QScrollArea(self)
        scroll_area.setGeometry(10, 500, 430, 240)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setWidget(seat_display_frame)
        scroll_area.setWidgetResizable(True)

        # ����ԤԼ��ť
        reserve_button = QPushButton("ԤԼ��λ", self)
        reserve_button.setGeometry(10, 750, 100, 30)
        reserve_button.clicked.connect(self.on_reserve_button_click)
        self.reserve_button = reserve_button

    def on_reserve_button_click(self):
        selected_seat = self.get_selected_seat()  # �������ǻ�ȡѡ����λ�ķ���
        if selected_seat is not None:
            if self.reservation_system.reserve_seat(selected_seat, self.get_logged_in_user_id()):
                QMessageBox.information(self, "ԤԼ�ɹ�", "���ѳɹ�ԤԼ����λ!")
                self.update_seat_display()
            else:
                QMessageBox.critical(self, "ԤԼʧ��", "����λ�ѱ�ԤԼ�������������!")

    def on_login(self):
        user_id = self.user_id_entry.text()
        password = self.password_entry.text()

        if self.reservation_system.authenticate(user_id, password):
            self.logged_in_user_id = user_id
            QMessageBox.information(self, "��¼�ɹ�", "��ӭ����{}!".format(user_id))
            self.enable_reservation_button(True)  # ��������һ������ԤԼ��ť�ķ���
            self.update_seat_display()
        else:
            QMessageBox.critical(self, "��¼ʧ��", "�û���������������������룡")

    def update_seat_display(self):
    
        # ������һ��seat_data�ֵ䣬���а�����������Ϊ����ÿ������Ӧ��ֵ�Ǹ÷������λ״̬�б�
        seat_data = {
            '�۽�': ['Available', 'Reserved', 'Available', 'Available'],
            '���': ['Available', 'Available', 'Reserved', 'Available'],
            '����A': ['Available', 'Available', 'Reserved', 'Available'],
            '����B': ['Available', 'Available', 'Reserved', 'Available'],
            '����C': ['Available', 'Available', 'Reserved', 'Available'],
            '����D': ['Available', 'Available', 'Reserved', 'Available'],
            '����E': ['Available', 'Available', 'Reserved', 'Available'],
            '����F': ['Available', 'Available', 'Reserved', 'Available'],
            '����G': ['Available', 'Available', 'Reserved', 'Available']
        }

        # ���������λչʾ��������
        self.seat_display_text.clear()

        # ������λ����
        for room_number, seat_status_list in seat_data.items():
            room_text = f"������{room_number}��"
            for index, status in enumerate(seat_status_list):
                seat_text = f"{status}" if status == 'Available' else f"{status} (��ԤԼ)"
                room_text += f"\n������ {index + 1}: {seat_text}"
            
            # �����估����λ״̬��ӵ���λչʾ��
            self.seat_display_text.append(room_text)

    def get_selected_seat(self):
        # ��ȡ�û�ѡ�����λ��Ϣ
        pass

    def get_logged_in_user_id(self):
        # ��ȡ��ǰ�ѵ�¼�û���ID
        return self.logged_in_user_id if hasattr(self, 'logged_in_user_id') else None

    def enable_reservation_button(self, enabled=True):
        # ���û����ԤԼ��ť
        self.reserve_button.setEnabled(enabled)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Arial", 10))
    app.setStyle("fusion")
    app.setWindowIcon(QIcon("./images/2.jpg"))
    main_win = StudyRoomReservationApp()
    main_win.show()
    sys.exit(app.exec_())