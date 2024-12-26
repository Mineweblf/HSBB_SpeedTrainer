import os
import random
from PyQt5.QtWidgets import QLabel, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

def setup_card_display(main_window, layout):
    main_window.cards_layout = layout

def refresh_cards(main_window):
    # 清空当前卡牌布局
    for i in reversed(range(main_window.cards_layout.count())):
        widget_to_remove = main_window.cards_layout.itemAt(i).widget()
        if widget_to_remove is not None:
            main_window.cards_layout.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)

    # 生成新卡牌
    mode = main_window.mode_combo.currentText()
    cards = main_window.game_logic.generate_cards(int(main_window.pool_combo.currentText()), mode)

    for i, (card_type, card_file) in enumerate(cards):
        # 判断卡牌类型并选择正确的文件夹路径
        if card_type == "Spell":
            folder = "Spell"
        elif card_type == "Minions":
            folder = "Minions"
        else:
            print(f"未知卡牌类型: {card_type}")
            continue  # 如果卡牌类型不是 Minions 或 Spell，跳过

        # 拼接卡牌路径
        card_path = os.path.join(os.getcwd(), 'assets', 'cards', folder, card_file)
        
        # 调试：打印拼接后的路径，查看路径是否正确

        # 检查文件是否存在
        if not os.path.exists(card_path):
            print(f"文件不存在: {card_path}")
            continue

        # 加载并显示卡牌图片
        card_label = QLabel()
        pixmap = QPixmap(card_path)
        if pixmap.isNull():
            print(f"无法加载图片: {card_path}")
            continue
        card_label.setPixmap(pixmap.scaled(pixmap.width() // 2, pixmap.height() // 2))  # 缩放图像

        # 存储文件名到QLabel对象
        card_label.setProperty("fileName", card_file)

        # 调试信息
        print(f"Card file name: {card_file}")

        # 添加点击事件
        card_label.mousePressEvent = lambda event, label=card_label: toggle_card_selection(main_window, label)

        main_window.cards_layout.addWidget(card_label, 0, i)

    # 添加间隔和居中
    spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
    main_window.cards_layout.addItem(spacer, 0, len(cards))
    main_window.cards_layout.setAlignment(Qt.AlignCenter)
    print("刷新卡牌")

    # 调试信息
    print(f"卡牌标签数量: {main_window.cards_layout.count()}")

    # 确保卡牌显示区域的高度保持不变
    main_window.cards_widget.setFixedHeight(300)

    # 开始记录玩家“本页停留时间”
    main_window.elapsed_timer.restart()

def toggle_card_selection(main_window, label):
    if label in main_window.selected_cards:
        label.setStyleSheet("")
        main_window.selected_cards.remove(label)
    else:
        label.setStyleSheet("border: 2px solid blue;")
        main_window.selected_cards.add(label)