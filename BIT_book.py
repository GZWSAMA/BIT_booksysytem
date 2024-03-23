# coding=GBK
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QMenuBar, QAction, \
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QFrame, QScrollArea, QTextEdit, \
    QPushButton, QMessageBox, QFileDialog, QSizePolicy
from PyQt5.QtGui import QFont, QIcon, QBrush, QPalette, QPixmap, QPainter
from PyQt5.QtCore import Qt, QSize


# 定义用户类
class User:
    def __init__(self, id, password):
        self.id = id
        self.password = password


# 定义座位类
class Seat:
    def __init__(self, id, status):
        self.id = id
        self.status = status  # '已预约'或'未预约'


# 定义预约模块
class ReservationSystem:
    def __init__(self):
        # 初始化用户列表和座位列表
        self.users = {'1120226666': {'password': '666666'}}
        self.seats = []
    def reserve_seat(self, user, seat_id):
        # 检查座位是否可用并进行预约操作
        pass

    def manage_seats(self, admin_user):
        # 提供管理员操作接口，如更改座位状态
        pass

    def authenticate(self, user_id, password):
        if user_id in self.users and self.users[user_id]['password'] == password:
            return True
        else:
            return False

    # 其他方法...

# GUI模块
class StudyRoomReservationApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # 初始化UI组件
        self.init_ui()

        # 实例化预约系统
        self.reservation_system = ReservationSystem()

    def init_ui(self):
        # 设置主窗口大小和标题
        self.setGeometry(400, 200, 450, 800)
        self.setWindowTitle("自习室座位预约系统")

        self.background_image = QPixmap('./images/2.jpg')

        # 缩放图片以适应窗口大小（保持原图比例并居中裁剪）
        newsize = QSize(int(self.background_image.width()), int(self.background_image.height()))
        self.scaled_bg = self.background_image.scaled(newsize, Qt.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
        # offset = ((self.width() - self.scaled_bg.width()) // 2, (self.height() - self.scaled_bg.height()) // 2)

        self.background_label = QLabel(self)
        self.background_label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.background_label.setPixmap(self.scaled_bg)
        self.background_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        # self.background_label.setScaledContents(True)  # 自动缩放图片以适应标签大小
        
        # 设置窗口的中央布局
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.background_label)
        self.setCentralWidget(central_widget)

        # 创建菜单栏
        menu_bar = self.menuBar()

        # 创建“文件”菜单项
        file_menu = menu_bar.addMenu("静音自习仓预约系统")
        exit_action = QAction("退出", self)
        exit_action.triggered.connect(QApplication.quit)
        file_menu.addAction(exit_action)

        # 创建登录区域
        login_frame = QFrame(self)
        login_frame.setFrameShape(QFrame.StyledPanel)
        login_frame.setFrameShadow(QFrame.Raised)
        login_frame.setGeometry(10, 30, 430, 120)

        login_label = QLabel("学号", login_frame)
        login_label.move(10, 25)
        login_label.setFont(QFont("Arial", 12, QFont.Bold))

        self.user_id_entry = QLineEdit(login_frame)
        self.user_id_entry.move(100, 20)
        self.user_id_entry.setFixedWidth(150)

        user_id_label = QLabel("密码", login_frame)
        user_id_label.move(10, 55)
        user_id_label.setFont(QFont("Arial", 10))

        self.password_entry = QLineEdit(login_frame)
        self.password_entry.move(100, 50)
        self.password_entry.setFixedWidth(150)
        self.password_entry.setEchoMode(QLineEdit.Password)

        login_button = QPushButton("登录", login_frame)
        login_button.move(280, 70)
        login_button.clicked.connect(self.on_login)

        # 创建座位展示区域
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

        # 创建预约按钮
        reserve_button = QPushButton("预约座位", self)
        reserve_button.setGeometry(10, 750, 100, 30)
        reserve_button.clicked.connect(self.on_reserve_button_click)
        self.reserve_button = reserve_button

    def on_reserve_button_click(self):
        selected_seat = self.get_selected_seat()  # 假设这是获取选中座位的方法
        if selected_seat is not None:
            if self.reservation_system.reserve_seat(selected_seat, self.get_logged_in_user_id()):
                QMessageBox.information(self, "预约成功", "您已成功预约了座位!")
                self.update_seat_display()
            else:
                QMessageBox.critical(self, "预约失败", "该座位已被预约或出现其他错误!")

    def on_login(self):
        user_id = self.user_id_entry.text()
        password = self.password_entry.text()

        if self.reservation_system.authenticate(user_id, password):
            self.logged_in_user_id = user_id
            QMessageBox.information(self, "登录成功", "欢迎您，{}!".format(user_id))
            self.enable_reservation_button(True)  # 假设这是一个启用预约按钮的方法
            self.update_seat_display()
        else:
            QMessageBox.critical(self, "登录失败", "用户名或密码错误，请重新输入！")

    def update_seat_display(self):
    
        # 假设有一个seat_data字典，其中包含房间编号作为键，每个键对应的值是该房间的座位状态列表
        seat_data = {
            '综教': ['Available', 'Reserved', 'Available', 'Available'],
            '理教': ['Available', 'Available', 'Reserved', 'Available'],
            '文萃A': ['Available', 'Available', 'Reserved', 'Available'],
            '文萃B': ['Available', 'Available', 'Reserved', 'Available'],
            '文萃C': ['Available', 'Available', 'Reserved', 'Available'],
            '文萃D': ['Available', 'Available', 'Reserved', 'Available'],
            '文萃E': ['Available', 'Available', 'Reserved', 'Available'],
            '文萃F': ['Available', 'Available', 'Reserved', 'Available'],
            '文萃G': ['Available', 'Available', 'Reserved', 'Available']
        }

        # 清除现有座位展示区的内容
        self.seat_display_text.clear()

        # 遍历座位数据
        for room_number, seat_status_list in seat_data.items():
            room_text = f"静音仓{room_number}："
            for index, status in enumerate(seat_status_list):
                seat_text = f"{status}" if status == 'Available' else f"{status} (已预约)"
                room_text += f"\n静音仓 {index + 1}: {seat_text}"
            
            # 将房间及其座位状态添加到座位展示区
            self.seat_display_text.append(room_text)

    def get_selected_seat(self):
        # 获取用户选择的座位信息
        pass

    def get_logged_in_user_id(self):
        # 获取当前已登录用户的ID
        return self.logged_in_user_id if hasattr(self, 'logged_in_user_id') else None

    def enable_reservation_button(self, enabled=True):
        # 启用或禁用预约按钮
        self.reserve_button.setEnabled(enabled)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Arial", 10))
    app.setStyle("fusion")
    app.setWindowIcon(QIcon("./images/2.jpg"))
    main_win = StudyRoomReservationApp()
    main_win.show()
    sys.exit(app.exec_())