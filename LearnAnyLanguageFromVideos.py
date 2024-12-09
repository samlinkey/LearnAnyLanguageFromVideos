import sys
import keyboard
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPalette, QColor, QCursor

class LearnAnyLanguageFromVideos(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置窗口无边框且始终置顶
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        
        # 背景颜色设置
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(0, 0, 0, 255))  # 黑色不透明背景
        self.setPalette(palette)

        # 设置窗口默认大小
        self.resize(800, 100)  # 窗口宽 800，高 100

        # 将窗口移动到屏幕中间靠下的位置
        self.move_to_bottom_center()

        # 初始化鼠标拖动的变量
        self.drag_position = None
        self.resizing = False  # 是否在调整大小
        self.resize_edge = 10  # 可调整大小的边缘范围

        # 添加全局热键监听
        keyboard.on_press_key("ctrl", self.handle_ctrl_press, suppress=True)
        keyboard.on_release_key("ctrl", self.handle_ctrl_release, suppress=True)
        keyboard.add_hotkey('ctrl+x', self.close, suppress=True)

    def move_to_bottom_center(self):
        """将窗口移动到屏幕中间靠下的位置"""
        screen = QDesktopWidget().availableGeometry()  # 获取屏幕可用区域
        screen_width = screen.width()
        screen_height = screen.height()
        window_width = self.width()
        window_height = self.height()

        # 计算窗口位置：水平居中，垂直靠下（离底部 50 像素）
        x = (screen_width - window_width) // 2
        y = screen_height - window_height - 50
        self.move(x, y)

    def mousePressEvent(self, event):
        """鼠标按下事件"""
        if event.button() == Qt.LeftButton:
            if self.is_near_edge(event.pos()):
                self.resizing = True
            else:
                self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        """鼠标移动事件"""
        if event.buttons() == Qt.LeftButton:
            if self.resizing:
                self.resize_window(event.globalPos())
            elif self.drag_position:
                self.move(event.globalPos() - self.drag_position)
        else:
            # 改变鼠标样式
            if self.is_near_edge(event.pos()):
                self.setCursor(QCursor(Qt.SizeFDiagCursor))  # 设置调整大小的光标
            else:
                self.setCursor(QCursor(Qt.ArrowCursor))  # 恢复默认光标

        event.accept()

    def mouseReleaseEvent(self, event):
        """鼠标释放事件"""
        self.resizing = False
        self.drag_position = None
        self.setCursor(QCursor(Qt.ArrowCursor))  # 恢复默认光标

    def is_near_edge(self, pos):
        """判断鼠标是否在窗口边缘"""
        rect = self.rect()
        return (
            pos.x() >= rect.width() - self.resize_edge
            and pos.y() >= rect.height() - self.resize_edge
        )

    def resize_window(self, global_pos):
        """调整窗口大小"""
        geometry = self.geometry()
        new_width = max(global_pos.x() - geometry.x(), 100)  # 最小宽度 100
        new_height = max(global_pos.y() - geometry.y(), 50)  # 最小高度 50
        self.setGeometry(geometry.x(), geometry.y(), new_width, new_height)

    def handle_ctrl_press(self, _):
        """处理全局 Ctrl 按键"""
        self.ctrl_pressed = True
        self.setWindowOpacity(0)

    def handle_ctrl_release(self, _):
        """处理全局 Ctrl 释放"""
        if self.ctrl_pressed:
            self.setWindowOpacity(1)
        self.ctrl_pressed = False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    blocker = LearnAnyLanguageFromVideos()
    blocker.show()
    sys.exit(app.exec_())
