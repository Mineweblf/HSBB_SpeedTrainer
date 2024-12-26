import os
import random
import csv
from PyQt5.QtCore import QTimer, QElapsedTimer

class GameLogic:
    def __init__(self):
        self.races = ["亡灵", "机械", "野兽", "野猪人", "鱼人", "元素", "恶魔", "海盗", "纳迦", "龙"]
        self.tavern_levels = list(range(1, 8))
        self.game_duration = 0
        self.current_races = []
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.time_left = 0
        self.game_data = []
        self.game_id = self.get_last_game_id() + 1  # 获取最后一个对局编号
        self.elapsed_timer = QElapsedTimer()

    def get_last_game_id(self):
        try:
            file_path = os.path.join(os.getcwd(), 'data', 'game_data.csv')
            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # 跳过标题行
                last_row = list(reader)[-1]
                return int(last_row[0])
        except (FileNotFoundError, IndexError, StopIteration):
            return 0

    def start_game(self, selected_race, pool_option, duration, mode):
        self.current_races = self.generate_races(selected_race)
        self.time_left = int(duration) * 60  # 将分钟转换为秒
        self.game_duration = self.time_left
        self.mode = mode
        self.timer.start(1000)  # 每秒更新一次
        print(f"Game started with race: {selected_race}, pool: {pool_option}, duration: {duration} minutes, mode: {mode}")
        # self.auto_refresh_timer.start(2000)  # 每2秒检查一次是否需要自动刷新
        print("游戏开始")
        self.elapsed_timer.start()

    def generate_races(self, selected_race):
        selected_races = [selected_race]
        remaining_races = [race for race in self.races if race != selected_race]
        selected_races.extend(random.sample(remaining_races, 5 - len(selected_races)))

        # 调试信息
        print(f"Generated races: {selected_races}")

        return selected_races

    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            print(f"Time left: {self.time_left} seconds")
        else:
            self.timer.stop()
            print("Game over")

    def save_game_data(self, correct, correct_total, page_accuracy, avg_accuracy, page_time, correct_files):
        page = len(self.game_data) + 1
        print(f"Saving game data - Correct: {correct}")  # 添加打印语句
        self.game_data.append([self.game_id, page, correct, correct_total, page_accuracy, avg_accuracy, page_time])
        file_path = os.path.join(os.getcwd(), 'data', 'game_data.csv')
        with open(file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if file.tell() == 0:  # 检查文件是否为空
                writer.writerow(["Game ID", "Page", "Correct", "Correct Total", "Page Accuracy", "Average Accuracy", "Page Time"])
            writer.writerow([self.game_id, page, correct, correct_total, page_accuracy, avg_accuracy, page_time])

    def save_final_game_data(self):
        file_path = os.path.join(os.getcwd(), 'data', 'game_data.csv')
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Game ID", "Page", "Correct", "Correct Total", "Page Accuracy", "Average Accuracy", "Page Time"])
            for data in self.game_data:
                writer.writerow(data[:7])

    def calculate_average_accuracy(self, current_page_accuracy):
        total_accuracy = sum([data[4] for data in self.game_data if data[0] == self.game_id]) + current_page_accuracy
        return total_accuracy / (len([data for data in self.game_data if data[0] == self.game_id]) + 1)

    def generate_cards(self, tavern_level, mode):
        # 生成卡牌逻辑
        cards = []
        minion_count = {1: 3, 2: 3, 3: 4, 4: 4, 5: 5, 6: 6}.get(tavern_level, 0)
        
        # 添加随从牌
        available_minions = []
        minions_path = os.path.join(os.getcwd(), 'assets', 'cards', 'Minions')
        suffixes = ["1"] if mode == "单人" else ["1", "2"]
        for level in range(1, tavern_level + 1):
            for race in self.current_races:
                for suffix in suffixes:
                    minion_files = [f for f in os.listdir(minions_path) 
                                    if f.startswith(f"{level}_{race}_Minion{suffix}") or f.startswith(f"{level}_全部_Minion{suffix}") or f.startswith(f"{level}_无种族_Minion{suffix}")]
                    available_minions.extend(minion_files)
        
        minion_count = min(minion_count, len(available_minions))  # 避免小兵数量超过可用数量
        cards.extend([("Minions", card) for card in random.sample(available_minions, minion_count)])

        # 添加酒馆法术
        spell_files = []
        spells_path = os.path.join(os.getcwd(), 'assets', 'cards', 'Spell')
        for level in range(1, tavern_level + 1):  # 包括当前等级及更低等级的所有卡
            for race in self.current_races:
                for suffix in suffixes:
                    spell_files.extend([f for f in os.listdir(spells_path) 
                                        if f.startswith(f"{level}_{race}_TavernSpell{suffix}") or f.startswith(f"{level}_全部_TavernSpell{suffix}") or f.startswith(f"{level}_无种族_TavernSpell{suffix}")])
        if spell_files:
            selected_spell = random.choice(spell_files)
            cards.append(("Spell", selected_spell))
        
        return cards

    def get_game_data(self):
        return self.game_data