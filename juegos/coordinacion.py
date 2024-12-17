from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QProgressBar
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont
import random


class GestureRhythmGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Juego de Ritmo con Gestos")
        self.setFixedSize(800, 600)

        self.score = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        self.gesture_sequence = []
        self.current_gesture_index = 0
        self.gesture_mapping = {
            "Left Click": "🖱️",
            "Right Click": "➡️",
            "Double Click": "⏩",
            "Scroll Up": "⬆️",
            "Scroll Down": "⬇️",
        }

        self.init_ui()
        self.generate_sequence()

    def init_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Título
        self.title_label = QLabel("¡Sigue la secuencia de gestos!")
        self.title_label.setFont(QFont("Arial", 20, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)

        # Marcador
        self.score_label = QLabel(f"Puntuación: {self.score}")
        self.score_label.setFont(QFont("Arial", 16))
        self.score_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.score_label)

        # Indicador de gesto actual
        self.gesture_label = QLabel("Preparando...")
        self.gesture_label.setFont(QFont("Arial", 48))
        self.gesture_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.gesture_label)

        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        layout.addWidget(self.progress_bar)

        # Botón para iniciar el juego
        self.start_button = QPushButton("Iniciar Juego")
        self.start_button.clicked.connect(self.start_game)
        layout.addWidget(self.start_button)

    def generate_sequence(self):
        """Genera una secuencia aleatoria de gestos."""
        gestures = list(self.gesture_mapping.keys())
        self.gesture_sequence = [random.choice(gestures) for _ in range(10)]

    def start_game(self):
        """Inicia el juego y el temporizador."""
        self.score = 0
        self.current_gesture_index = 0
        self.progress_bar.setValue(0)
        self.score_label.setText(f"Puntuación: {self.score}")
        self.gesture_label.setText(self.gesture_mapping[self.gesture_sequence[self.current_gesture_index]])
        self.timer.start(2000)  # Cambiar de gesto cada 2 segundos

    def update_game(self):
        """Actualiza el juego cada vez que el temporizador expira."""
        self.current_gesture_index += 1
        if self.current_gesture_index >= len(self.gesture_sequence):
            self.timer.stop()
            self.gesture_label.setText("¡Juego Terminado!")
            self.start_button.setEnabled(True)
            return

        self.gesture_label.setText(self.gesture_mapping[self.gesture_sequence[self.current_gesture_index]])

    def detect_gesture(self, gesture_name):
        """Detecta el gesto realizado por el usuario."""
        if self.current_gesture_index < len(self.gesture_sequence):
            if gesture_name == self.gesture_sequence[self.current_gesture_index]:
                self.score += 10
                self.progress_bar.setValue(int((self.current_gesture_index + 1) / len(self.gesture_sequence) * 100))
                self.score_label.setText(f"Puntuación: {self.score}")

    def mousePressEvent(self, event):
        """Detecta clics del mouse."""
        if event.button() == Qt.LeftButton:
            self.detect_gesture("Left Click")
        elif event.button() == Qt.RightButton:
            self.detect_gesture("Right Click")

    def mouseDoubleClickEvent(self, event):
        """Detecta doble clic."""
        self.detect_gesture("Double Click")

    def wheelEvent(self, event):
        """Detecta movimiento de scroll del mouse."""
        if event.angleDelta().y() > 0:
            self.detect_gesture("Scroll Up")
        else:
            self.detect_gesture("Scroll Down")


if __name__ == "__main__":
    app = QApplication([])
    game = GestureRhythmGame()
    game.show()
    app.exec_()
