from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QFrame,
    QProgressBar
)

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
import psutil


class BlasterX(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("BlasterX")
        self.resize(700, 500)

        self.setStyleSheet("""
            QWidget{
                background-color:#0d1117;
            }
        """)

        self.setup_ui()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(1000)

        self.update_stats()

    def get_cpu_temp(self):
        try:
            with open("/sys/class/thermal/thermal_zone0/temp") as f:
                return float(f.read()) / 1000
        except:
            return 0

    def setup_ui(self):

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30,30,30,30)

        card = QFrame()
        card.setStyleSheet("""
            QFrame{
                background:#161b22;
                border:1px solid #30363d;
                border-radius:20px;
            }
        """)

        card_layout = QVBoxLayout()
        card_layout.setSpacing(15)

        self.title = QLabel("BLASTERX")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setFont(QFont("Arial",24,QFont.Weight.Bold))
        self.title.setStyleSheet("color:white;")

        self.subtitle = QLabel("CPU THERMAL MONITOR")
        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle.setStyleSheet("color:#8b949e;")

        self.temp_label = QLabel("--°C")
        self.temp_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.temp_label.setFont(QFont("Arial",56,QFont.Weight.Bold))

        self.status_label = QLabel("LOADING...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setFont(QFont("Arial",14))

        self.temp_bar = QProgressBar()
        self.temp_bar.setRange(0,100)
        self.temp_bar.setTextVisible(False)

        self.temp_bar.setStyleSheet("""
            QProgressBar{
                border:none;
                background:#0d1117;
                height:18px;
                border-radius:9px;
            }

            QProgressBar::chunk{
                background:#00d4ff;
                border-radius:9px;
            }
        """)

        self.cpu_usage = QLabel()
        self.cpu_usage.setStyleSheet("color:white;")

        self.ram_usage = QLabel()
        self.ram_usage.setStyleSheet("color:white;")

        self.max_temp = QLabel("Max Temp: --")
        self.max_temp.setStyleSheet("color:white;")

        card_layout.addWidget(self.title)
        card_layout.addWidget(self.subtitle)
        card_layout.addSpacing(10)

        card_layout.addWidget(self.temp_label)
        card_layout.addWidget(self.status_label)
        card_layout.addWidget(self.temp_bar)

        card_layout.addSpacing(20)

        card_layout.addWidget(self.cpu_usage)
        card_layout.addWidget(self.ram_usage)
        card_layout.addWidget(self.max_temp)

        card.setLayout(card_layout)

        main_layout.addWidget(card)

        self.setLayout(main_layout)

        self.highest_temp = 0

    def update_stats(self):

        temp = self.get_cpu_temp()

        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent

        self.highest_temp = max(self.highest_temp, temp)

        self.temp_label.setText(f"{temp:.1f}°C")
        self.temp_bar.setValue(int(temp))

        self.cpu_usage.setText(f"CPU Usage : {cpu}%")
        self.ram_usage.setText(f"RAM Usage : {ram}%")
        self.max_temp.setText(f"Max Temp : {self.highest_temp:.1f}°C")

        if temp < 60:

            color = "#00ff88"
            status = "● NORMAL"

        elif temp < 80:

            color = "#ffd700"
            status = "● WARM"

        else:

            color = "#ff4d4d"
            status = "● HOT"

        self.temp_label.setStyleSheet(f"""
            color:{color};
        """)

        self.status_label.setStyleSheet(f"""
            color:{color};
        """)

        self.status_label.setText(status)


app = QApplication([])

window = BlasterX()
window.show()

app.exec()
