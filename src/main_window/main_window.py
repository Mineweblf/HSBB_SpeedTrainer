import sys
import os
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QGridLayout, QSpacerItem, QSizePolicy, QProgressBar
from PyQt5.QtCore import QTimer, Qt, QElapsedTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QEvent
from src.game_logic import GameLogic
from src.data_handler import DataHandler
from .game_controls import setup_game_controls
from .card_display import setup_card_display, refresh_cards, toggle_card_selection
from .chart_display import ChartCanvas

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Card Selection Game")
        self.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        self.showMaximized()
        self.setFixedSize(self.size())
        self.setMinimumSize(self.size())
        self.elapsed_timer = QElapsedTimer()
        self.selected_cards = set()

        self.game_logic = GameLogic()
        self.data_handler = DataHandler(os.path.join('..', 'data', 'game_data.csv'))

        # 主窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 主布局
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # 设置区域布局
        settings_layout = QHBoxLayout()
        main_layout.addLayout(settings_layout)

        # 设置游戏控制区域
        setup_game_controls(self, settings_layout)

        # 计时器和准确度显示区域
        status_layout = QHBoxLayout()
        main_layout.addLayout(status_layout)

        # 计时器显示
        self.timer_label = QLabel("剩余时间: 0")
        status_layout.addWidget(self.timer_label)

        # 本局种族显示
        self.current_races_label = QLabel("本局种族: ")
        status_layout.addWidget(self.current_races_label)

        # 准确度显示
        self.accuracy_label = QLabel("准确度: 100.00%")
        status_layout.addWidget(self.accuracy_label)

        # 刷新按钮
        self.refresh_button = QPushButton("刷新")
        self.refresh_button.clicked.connect(self.on_refresh_button_clicked)
        status_layout.addWidget(self.refresh_button)

        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        main_layout.addWidget(self.progress_bar)

        # 卡牌显示区域
        self.cards_layout = QGridLayout()
        self.cards_layout.setSpacing(10)  # 设置图片之间的固定间隔
        main_layout.addLayout(self.cards_layout)

        # 预留图片区域，固定高度
        self.cards_widget = QWidget()
        self.cards_widget.setFixedHeight(755)
        main_layout.addWidget(self.cards_widget)

        # 图表显示区域
        self.chart_canvas = ChartCanvas(self)
        main_layout.addWidget(self.chart_canvas)

        # 定时器
        self.ui_timer = QTimer()
        self.ui_timer.timeout.connect(self.update_timer)

        # 自动刷新定时器
        self.auto_refresh_timer = QTimer()
        self.auto_refresh_timer.timeout.connect(self.on_auto_refresh)

        # 初始化按钮状态
        self.start_button.setEnabled(True)
        self.refresh_button.setEnabled(False)

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange and self.windowState() == Qt.WindowNoState:
            self.showMaximized()
            self.setMinimumSize(self.size())  # 保持最小尺寸不变
        super().changeEvent(event)

    def start_game(self):
        selected_race = self.race_combo.currentText()
        pool_option = self.pool_combo.currentText()
        duration = self.duration_combo.currentText()
        mode = self.mode_combo.currentText()
        self.game_logic.start_game(selected_race, pool_option, duration, mode)
        self.update_timer()  # 手动调用一次 update_timer 以立即更新界面
        self.ui_timer.start(1000)  # 每秒更新一次
        self.auto_refresh_timer.start(10)  # 每0.01秒检查一次是否需要自动刷新
        self.update_current_races()
        refresh_cards(self)
        print("游戏开始")
        self.elapsed_timer.start()

        # 锁定设置区域的所有按键和选择框
        self.start_button.setEnabled(False)
        self.refresh_button.setEnabled(True)
        self.race_combo.setEnabled(False)
        self.pool_combo.setEnabled(False)
        self.duration_combo.setEnabled(False)
        self.mode_combo.setEnabled(False)
        self.difficulty_combo.setEnabled(False)

        # 清空所有图表
        self.chart_canvas.clear_charts()

    def update_timer(self):
        self.timer_label.setText(f"剩余时间: {self.game_logic.time_left}")
        if self.game_logic.time_left <= 0:
            self.ui_timer.stop()
            self.auto_refresh_timer.stop()
            self.end_game()

    def update_current_races(self):
        self.current_races_label.setText(f"本局种族: {', '.join(self.game_logic.current_races)}")

    def on_refresh_button_clicked(self):
        self.calculate_page_accuracy()
        refresh_cards(self)
        self.progress_bar.setValue(0)  # 重置进度条

    def on_auto_refresh(self):
        elapsed_time = self.elapsed_timer.elapsed() / 1000
        difficulty = float(self.difficulty_combo.currentText().replace('s', ''))
        progress = min(100, (elapsed_time / difficulty) * 100)
        self.progress_bar.setValue(int(progress))  # 将 progress 转换为整数
        if progress >= 100:
            self.progress_bar.setStyleSheet("QProgressBar::chunk { background-color: red; }")
        else:
            self.progress_bar.setStyleSheet("QProgressBar::chunk { background-color: green; }")

    def end_game(self):
        # 解锁设置区域的所有按键和选择框
        self.start_button.setEnabled(True)
        self.refresh_button.setEnabled(False)
        self.race_combo.setEnabled(True)
        self.pool_combo.setEnabled(True)
        self.duration_combo.setEnabled(True)
        self.difficulty_combo.setEnabled(True)

        # 统计最后一页（未点击刷新的一页）
        self.calculate_page_accuracy()

        # 统计并保存游戏数据
        self.game_logic.save_final_game_data()

        # 显示最终结果
        self.show_final_results()

    def show_final_results(self):
        game_data = self.game_logic.get_game_data()
        difficulty = float(self.difficulty_combo.currentText().replace('s', ''))
        print("调用 plot_final_results 函数")
        self.chart_canvas.plot_final_results(game_data, difficulty)
        print("图表已刷新")

    def calculate_page_accuracy(self):
        selected_race = self.race_combo.currentText()
        print(f"Selected race: {selected_race}")

        all_cards = [self.cards_layout.itemAt(i).widget().property("fileName") for i in range(self.cards_layout.count()) if self.cards_layout.itemAt(i).widget()]
        print(f"All cards: {all_cards}")

        selected_cards = [label.property("fileName") for label in self.selected_cards]
        print(f"Selected cards: {selected_cards}")

        # 计算全部图片内正确个数和"全部"数
        correct_all = sum(1 for card in all_cards if selected_race in card)
        all_count = sum(1 for card in all_cards if "全部" in card)
        a = correct_all + all_count
        print(f"Correct in all cards: {correct_all}, '全部' in all cards: {all_count}, a: {a}")

        # 计算选择图片内正确个数和"全部"数
        correct_selected = sum(1 for card in selected_cards if selected_race in card)
        selected_all_count = sum(1 for card in selected_cards if "全部" in card)
        r = correct_selected + selected_all_count
        print(f"Correct in selected cards: {correct_selected}, '全部' in selected cards: {selected_all_count}, r: {r}")

        # 选择图片的总数
        c = len(selected_cards)
        print(f"Total selected cards: {c}")

        # 计算准确度
        if a != 0:
            accuracy = (r / a) * 100
        else:
            accuracy = 0 if c - r != 0 else 100
        print(f"Accuracy: {accuracy}")

        # 保存游戏数据
        avg_accuracy = self.game_logic.calculate_average_accuracy(accuracy)
        self.game_logic.save_game_data(correct_selected, correct_all, accuracy, avg_accuracy, self.elapsed_timer.elapsed() / 1000, selected_cards)
        print("Game data saved.")

        # 更新窗口内显示的准确度为平均准确度
        self.accuracy_label.setText(f"准确度: {avg_accuracy:.2f}%")

        # 清空已选择的选项
        for label in self.selected_cards:
            label.setStyleSheet("")
        self.selected_cards.clear()
        print("Selected cards cleared.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())