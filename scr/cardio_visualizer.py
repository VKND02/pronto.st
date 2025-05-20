import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class CardioVisualizer:
    def __init__(self, signal, time, window_seconds=5, sampling_rate=200,
                 start_time=None, end_time=None):
        self.sampling_rate = sampling_rate
        self.window_seconds = window_seconds

        # 🔒 Sécurité : on aligne les longueurs time/signal
        min_len = min(len(signal), len(time))
        signal = signal[:min_len]
        time = time[:min_len]

        # 🎯 Découpage selon la plage demandée
        if start_time is not None and end_time is not None:
            mask = (time >= start_time) & (time <= end_time)
            self.signal = signal[mask]
            self.time = time[mask]
        else:
            self.signal = signal
            self.time = time

        self.frames = len(self.time)

    def animate(self, save_path="output/cardiogramme_final.gif"):
        """Génère un GIF animé ECG à partir d’un segment temporel contrôlé"""
        window_size = int(self.window_seconds * self.sampling_rate)

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.set_xlim(0, self.window_seconds)
        ax.set_ylim(np.min(self.signal), np.max(self.signal))
        ax.set_xlabel("Temps (s)")
        ax.set_ylabel("Amplitude")
        ax.set_title("Visualisation ECG (GIF animé)")
        ax.grid(True)

        line, = ax.plot([], [], lw=2, color='crimson')

        def init():
            line.set_data([], [])
            return line,

        def update(i):
            start = max(0, i - window_size)
            end = i

            if end <= start:
                return line,

            x = self.time[start:end]
            y = self.signal[start:end]

            min_len = min(len(x), len(y))
            if min_len == 0:
                return line,

            x = x[:min_len] - x[:min_len][0]  # recentrer le temps local
            y = y[:min_len]

            line.set_data(x, y)
            return line,

        ani = animation.FuncAnimation(
            fig, update, init_func=init, frames=self.frames,
            blit=True, interval=20
        )

        import os
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        ani.save(save_path, writer='pillow', fps=25)
        print(f"GIF animé enregistré : {save_path}")
        plt.close()
