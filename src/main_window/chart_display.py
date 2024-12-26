import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class ChartCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.fig, self.ax = plt.subplots(1, 3, figsize=(20, 5))  # 修改为3个子图
        super().__init__(self.fig)
        plt.rcParams['font.family'] = 'Microsoft YaHei'  # 设置字体为 Microsoft YaHei
        self.fig.subplots_adjust(bottom=0.25)  # 增加图表底部的边距

    def plot_accuracy(self, data):
        self.ax[0].clear()
        self.ax[0].plot(data)
        self.ax[0].set_title("准确度曲线")
        self.ax[0].set_xlabel("页数")
        self.ax[0].set_ylabel("准确度")
        self.fig.tight_layout()  # 自动调整子图参数
        self.fig.subplots_adjust(bottom=0.25)  # 增加图表底部的边距
        self.draw()

    def plot_final_results(self, game_data, difficulty):
        print("开始生成图表")
        print(f"game_data: {game_data}")
        print(f"difficulty: {difficulty}")

        self.ax[0].clear()
        self.ax[1].clear()
        self.ax[2].clear()  # 新增的子图

        # 准确度曲线和截至平均准确度曲线
        avg_accuracies = [data[5] for data in game_data]
        self.ax[0].plot(avg_accuracies, label="截至平均准确度", color='red')
        self.ax[0].set_title("准确度曲线")
        self.ax[0].set_xlabel("页数")
        self.ax[0].set_ylabel("准确度")
        self.ax[0].legend()

        # 过滤 page_time 小于选择难度的时间的数据
        filtered_data = [data for data in game_data if data[6] < difficulty]
        filtered_avg_accuracies = [data[5] for data in filtered_data]
        self.ax[1].plot(filtered_avg_accuracies, label="截至平均准确度 (过滤)", color='red')
        self.ax[1].set_title("过滤后的准确度曲线")
        self.ax[1].set_xlabel("页数")
        self.ax[1].set_ylabel("准确度")
        self.ax[1].legend()

        # 标准化反应时间图
        normalized_reaction_times = [(data[6] * data[4] / 100) for data in game_data]
        self.ax[2].plot(normalized_reaction_times, label="标准化反应时间", color='blue')
        self.ax[2].set_title("标准化反应时间")
        self.ax[2].set_xlabel("页数")
        self.ax[2].set_ylabel("时间 (秒)")
        self.ax[2].legend()

        self.fig.tight_layout()  # 自动调整子图参数
        self.fig.subplots_adjust(bottom=0.25)  # 增加图表底部的边距
        self.draw()
        print("图表生成完成")

    def clear_charts(self):
        self.ax[0].clear()
        self.ax[1].clear()
        self.ax[2].clear()  # 清空新增的子图
        self.draw()
        print("图表已清空")