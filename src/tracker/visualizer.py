import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from matplotlib.ticker import FuncFormatter

from tracker import utils
import config.settings as settings

class Visualizer():
    __sample_epsilon = settings.INITIAL_SAMPLE_EPSILON

    # 時間軸目盛り.
    def __custom_sec_mark(self, x, pos):
        return f"{int(x / 1000)} s"

    # グラフを表示して範囲内へのマッピングとダウンサンプリングをする
    def plot(self, time_array : np.array, pos_array : np.array) :
        sampled_points = np.array(utils.downsample(time_array, pos_array, self.__sample_epsilon))
        
        fig, ax = plt.subplots()
        ax.xaxis.set_major_formatter(FuncFormatter(self.__custom_sec_mark))
        ax.set_xlabel("Time")
        ax.set_ylabel("Position")
        ax.set_title("Tracking Data")
        ax.plot(time_array, pos_array, 'r-', label="Original")
        line, = ax.plot(sampled_points[:, 0], sampled_points[:, 1], 'o-', markersize=3, label="Sampled")
        ax.legend()
        plt.subplots_adjust(left=0.1, bottom=0.25)
        ax_sample = plt.axes([0.25, 0.12, 0.65, 0.03])
        sample_slider = Slider(ax_sample, 'Sample Rate', 0, 10, valinit=self.__sample_epsilon)

        # OKボタンの追加
        ax_btn_ok = plt.axes([0.1, 0.02, 0.3, 0.05])
        btn_ok = Button(ax_btn_ok, 'OK')
        ax_btn_cancel = plt.axes([0.6, 0.02, 0.3, 0.05])
        btn_cancel = Button(ax_btn_cancel, 'Cancel')

        # スライダー更新時の動作
        def update(val):
            self.__sample_epsilon = sample_slider.val
            sampled_points = np.array(utils.downsample(time_array, pos_array, self.__sample_epsilon))
            line.set_data(sampled_points[:, 0], sampled_points[:, 1])
            ax.relim()
            fig.canvas.draw_idle()
        sample_slider.on_changed(update)

        self.__ok_flag = False
        # OKボタンが押されたときの動作
        def on_ok_clicked(event):
            self.__ok_flag = True
            plt.close()
        def on_cancel_clicked(event):
            plt.close()
        btn_ok.on_clicked(on_ok_clicked)
        btn_cancel.on_clicked(on_cancel_clicked)

        plt.show()
        if self.__ok_flag :
            sampled_points = np.array(utils.downsample(time_array, pos_array, self.__sample_epsilon))
            return list(sampled_points[:, 0]), list(sampled_points[:, 1])