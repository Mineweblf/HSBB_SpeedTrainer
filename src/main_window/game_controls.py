from PyQt5.QtWidgets import QLabel, QPushButton, QComboBox

def setup_game_controls(main_window, layout):
    # 模式选择框
    main_window.mode_combo = QComboBox()
    main_window.mode_combo.addItems(["单人", "双人"])
    layout.addWidget(QLabel("选择模式:"))
    layout.addWidget(main_window.mode_combo)

    # 种族选择框
    main_window.race_combo = QComboBox()
    main_window.race_combo.addItems(["亡灵", "机械", "野兽", "野猪人", "鱼人", "元素", "恶魔", "海盗", "纳迦", "龙"])
    layout.addWidget(QLabel("选择种族:"))
    layout.addWidget(main_window.race_combo)

    # 卡池选择框
    main_window.pool_combo = QComboBox()
    main_window.pool_combo.addItems([str(i) for i in range(1, 7)])
    layout.addWidget(QLabel("酒馆等级:"))
    layout.addWidget(main_window.pool_combo)

    # 总游戏时长选择框
    main_window.duration_combo = QComboBox()
    main_window.duration_combo.addItems(["1", "3", "5"])
    layout.addWidget(QLabel("总时长(min):"))
    layout.addWidget(main_window.duration_combo)

    # 难度选择框
    main_window.difficulty_combo = QComboBox()
    main_window.difficulty_combo.addItems(["1.5s", "2s", "2.5s", "3s"])
    layout.addWidget(QLabel("过滤时间标准:"))
    layout.addWidget(main_window.difficulty_combo)

    # 开始游戏按钮
    main_window.start_button = QPushButton("开始游戏")
    main_window.start_button.clicked.connect(main_window.start_game)
    layout.addWidget(main_window.start_button)