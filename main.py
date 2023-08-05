import tkinter as tk
import time
import csv

class Stopwatch(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Stopwatch Lap Timer")
        self.geometry("300x300")

        self.time_var = tk.StringVar()
        self.time_var.set("00:00:00")

        self.lap_times = []
        self.lap_var = tk.StringVar()
        self.lap_var.set("Question times: ")


        self.create_widgets()

        self.is_running = False
        self.start_time = None

        self.lap_counter = 1


    def create_widgets(self):
        self.timer_label = tk.Label(self, textvariable=self.time_var, font=("Helvetica", 24))
        self.timer_label.pack(pady=20)

        self.start_stop_button = tk.Button(self, text="Start", command=self.start_stop)
        self.start_stop_button.pack(side=tk.LEFT, padx=10)

        self.lap_button = tk.Button(self, text="Lap", command=self.record_lap)
        self.lap_button.pack(side=tk.LEFT, padx=10)

        self.lap_label = tk.Label(self, textvariable=self.lap_var)
        self.lap_label.pack(pady=10)

        self.save_laps_button = tk.Button(self, text="Save", command=self.save_laps)
        self.save_laps_button.pack(side=tk.BOTTOM, pady=10)

        self.paper_name = tk.Text(self, width=20)
        self.paper_name.pack(side=tk.BOTTOM)

    def start_stop(self):
        if not self.is_running:
            self.is_running = True
            self.start_time = time.time()
            self.update_timer()
            self.start_stop_button.config(text="Stop")
            self.lap_button.config(state=tk.NORMAL)
        else:
            self.is_running = False
            self.start_stop_button.config(text="Start")
            self.lap_button.config(state=tk.DISABLED)

    def update_timer(self):
        if self.is_running:
            elapsed_time = time.time() - self.start_time
            time_str = self.format_time(elapsed_time)
            self.time_var.set(time_str)
            self.after(50, self.update_timer)

    def format_time(self, elapsed):
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        milliseconds = int((elapsed % 1) * 1000)
        return f"{minutes:02d}:{seconds:02d}:{milliseconds:03d}"

    def record_lap(self):
        lap_time = self.time_var.get()
        self.lap_times.append([self.lap_counter, lap_time])
        self.update_lap_label()
        self.lap_counter += 1

    def update_lap_label(self):
        laps_text = "Question times: \n" + f"\n ".join([f"{lap[0]}: {lap[1]}" for lap in self.lap_times])
        self.lap_var.set(laps_text)

    def save_laps(self):
        with open("lap_times.csv", "a", newline='') as f:
            writer = csv.writer(f)
            paper = self.paper_name.get("1.0", tk.END)
            writer.writerow([paper])
            for lap in self.lap_times:
                writer.writerow(lap)
            
if __name__ == "__main__":
    app = Stopwatch()
    app.mainloop()