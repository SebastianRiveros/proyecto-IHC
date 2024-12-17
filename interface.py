from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QGridLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtCore import Qt
import subprocess
import os


class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rehabilitación de Manos - Menú Principal")

        # Tamaño fijo (similar al juego)
        self.window_width = 800
        self.window_height = 600
        self.setFixedSize(self.window_width, self.window_height)

        # Centrar la ventana en la pantalla
        self.center_window()

        # Fondo gris claro
        self.setStyleSheet("background-color: #F1F1F1;")
        self.init_ui()

    def center_window(self):
        """Centra la ventana en la pantalla."""
        screen_geometry = QApplication.primaryScreen().geometry()
        x = (screen_geometry.width() - self.window_width) // 2
        y = (screen_geometry.height() - self.window_height) // 2
        self.move(x, y)

    def init_ui(self):
        """Inicializa la interfaz de usuario."""
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Título
        title = QLabel("Selecciona un Juego o Controla el Sistema Gestual")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; padding: 10px;")
        layout.addWidget(title)

        # Botones para el control gestual (Iniciar y Detener)
        control_layout = QHBoxLayout()
        self.start_control_button = QPushButton("Iniciar Control Gestual")
        self.start_control_button.setFont(QFont("Arial", 14))
        self.start_control_button.setStyleSheet("""
            background-color: #2980b9;
            color: white;
            border-radius: 10px;
            padding: 10px;
        """)
        self.start_control_button.setFixedWidth(200)
        self.start_control_button.clicked.connect(self.start_hand_control)
        control_layout.addWidget(self.start_control_button)

        self.stop_control_button = QPushButton("Detener Control Gestual")
        self.stop_control_button.setFont(QFont("Arial", 14))
        self.stop_control_button.setStyleSheet("""
            background-color: #c0392b;
            color: white;
            border-radius: 10px;
            padding: 10px;
        """)
        self.stop_control_button.setFixedWidth(200)
        self.stop_control_button.clicked.connect(self.stop_hand_control)
        control_layout.addWidget(self.stop_control_button)

        layout.addLayout(control_layout)

        # Crear un layout de cuadrícula para los botones de juegos
        self.games_layout = QGridLayout()
        layout.addLayout(self.games_layout)

        # Cargar juegos disponibles
        self.load_games()

        # Barra de estado
        self.status_bar = QLabel("Control: Inactivo | Gestos Detectados: Ninguno")
        self.status_bar.setAlignment(Qt.AlignLeft)
        self.status_bar.setStyleSheet("""
            background-color: #34495e;
            color: white;
            padding: 5px;
            font-weight: bold;
        """)
        layout.addWidget(self.status_bar)

    def load_games(self):
        """Carga dinámicamente los juegos disponibles desde la carpeta 'juegos'."""
        games_folder = "juegos"
        if not os.path.exists(games_folder):
            os.makedirs(games_folder)

        row = 0
        col = 0
        for file in os.listdir(games_folder):
            if file.endswith(".py"):
                game_name = file.replace(".py", "")
                image_path = os.path.join(games_folder, "img", f"{game_name}.png")

                # Crear un contenedor para cada juego (imagen + texto)
                game_widget = QWidget()
                game_layout = QVBoxLayout()
                game_widget.setLayout(game_layout)

                # Imagen del juego
                game_button = QPushButton()
                game_button.setFixedSize(120, 120)
                game_button.setStyleSheet("""
                    background-color: #2ecc71;
                    border-radius: 10px;
                """)
                game_button.clicked.connect(lambda _, path=os.path.join(games_folder, file): self.launch_game(path))

                if os.path.exists(image_path):
                    pixmap = QPixmap(image_path).scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    game_button.setIcon(QIcon(pixmap))
                    game_button.setIconSize(pixmap.rect().size())

                game_layout.addWidget(game_button, alignment=Qt.AlignCenter)

                # Nombre del juego
                game_label = QLabel(game_name)
                game_label.setAlignment(Qt.AlignCenter)
                game_label.setFont(QFont("Arial", 10, QFont.Bold))
                game_label.setStyleSheet("color: #34495e; padding: 5px;")
                game_layout.addWidget(game_label)

                # Añadir el contenedor al layout de cuadrícula
                self.games_layout.addWidget(game_widget, row, col)

                col += 1
                if col > 3:  # Máximo 4 juegos por fila
                    col = 0
                    row += 1

    def start_hand_control(self):
        """Inicia el sistema de control gestual en el entorno virtual."""
        try:
            app_path = os.path.join(os.getcwd(), "app.py")
            if not os.path.exists(app_path):
                self.status_bar.setText("Error: app.py no encontrado.")
                return

            # Ejecutar "py app.py" en el entorno virtual
            command = ["py", app_path]
            self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.status_bar.setText("Control: Activo | Gestos Detectados: Esperando...")

        except Exception as e:
            self.status_bar.setText(f"Error al iniciar el control gestual: {e}")

    def stop_hand_control(self):
        """Detiene el sistema de control gestual."""
        if hasattr(self, "process"):
            self.process.terminate()
            self.status_bar.setText("Control: Inactivo | Gestos Detectados: Ninguno")

    def launch_game(self, game_path):
        """Lanza un juego seleccionado."""
        try:
            if not os.path.exists(game_path):
                self.status_bar.setText(f"Error: Archivo {game_path} no encontrado.")
                return

            # Usar "py" para ejecutar el juego
            command = ["py", game_path]
            subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.status_bar.setText(f"Juego {game_path} iniciado.")
        except Exception as e:
            self.status_bar.setText(f"Error al iniciar el juego: {e}")

    def closeEvent(self, event):
        """Sobreescribe el cierre de ventana para detener procesos."""
        self.stop_hand_control()
        event.accept()


if __name__ == "__main__":
    app = QApplication([])
    menu = MainMenu()
    menu.show()
    app.exec_()
